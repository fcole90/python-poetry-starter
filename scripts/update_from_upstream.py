"""CLI tool to squash-merge upstream template repo changes."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Sequence

__UPSTREAM_URL__ = "https://github.com/fcole90/python-poetry-starter.git"
__TARGET_BRANCH__ = "main"
__REMOTE_NAME__ = "upstream"


def run_git(
    args: Sequence[str], check: bool = True, raise_on_error: bool = False
) -> str:
    """Execute git command and return stdout."""
    cmd = f"git {' '.join(args)}"
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, check=False
    )
    if check and result.returncode != 0:
        error_msg = (
            result.stderr.strip() or result.stdout.strip() or "(no error message)"
        )
        print(f"Git command failed with exit code {result.returncode}", file=sys.stderr)
        print(f"Error: {error_msg}", file=sys.stderr)
        if raise_on_error:
            raise subprocess.CalledProcessError(
                result.returncode, cmd, result.stdout, result.stderr
            )
    return result.stdout.strip()


def get_recent_upstream_changes(upstream_ref: str) -> list[str]:
    """Get recent commits from upstream for commit message."""
    try:
        log = run_git(["log", f"{upstream_ref}~10..{upstream_ref}", "--oneline"])
        return log.splitlines()[:8]
    except subprocess.CalledProcessError:
        return ["(Could not fetch changelog)"]


def main() -> None:
    """CLI entrypoint: update repo from upstream template."""
    # Setup remote
    remotes = run_git(["remote"]).splitlines()
    if __REMOTE_NAME__ not in remotes:
        print(f"Adding {__REMOTE_NAME__} remote...")
        run_git(["remote", "add", __REMOTE_NAME__, __UPSTREAM_URL__])
    else:
        print(f"No need to add {__REMOTE_NAME__} remote, it already exists.")

    print(f"Fetching latest from {__REMOTE_NAME__}...")
    run_git(["fetch", __REMOTE_NAME__])
    print("Fetch complete.")

    # If there are staged changes in the index, exit early to avoid
    # accidentally squashing or merging on top of an in-progress change.
    staged_files = run_git(["diff", "--cached", "--name-only"]).strip()
    if staged_files:
        print(
            "There are staged changes in the index. Please commit or stash them before running this script.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Check if update needed
    upstream_ref = f"{__REMOTE_NAME__}/{__TARGET_BRANCH__}"
    try:
        upstream_hash = run_git(["rev-parse", upstream_ref])
        local_hash = run_git(["rev-parse", "HEAD"])
        if upstream_hash == local_hash:
            print("✅ Upstream up to date.")
            return
    except subprocess.CalledProcessError:
        pass

    # Switch to target branch
    run_git(["checkout", __TARGET_BRANCH__])

    # Squash merge workflow
    temp_branch = f"update-upstream-{datetime.now().strftime('%Y%m%d-%H%M')}"
    print(f"Creating temp branch: {temp_branch}")

    run_git(["checkout", "-b", temp_branch])

    # Generate commit message
    changes = get_recent_upstream_changes(upstream_ref)
    commit_msg = f"""Merge upstream changes ({datetime.now().strftime('%Y-%m-%d')})

Recent upstream commits:
{chr(10).join(f'• {line}' for line in changes)}"""

    # Interactive commit
    msg_file = Path(".git/COMMIT_TEMPLATE")
    msg_file.write_text(commit_msg)

    run_git(["merge", upstream_ref, "--squash"])

    # Check for merge conflicts
    if run_git(["status", "--porcelain"]).strip():
        print("⚠️  Merge conflicts detected!")
        print("Resolve conflicts manually:")
        print("1. Edit conflicted files")
        print("2. git add <files>")
        print(
            f"3. Run {' '.join(['git', 'commit', '--edit', '--template', str(msg_file)])} to commit"
        )
        sys.exit(1)

    run_git(["add", "-A"])

    print("Committing... (edit if needed, save & exit)")
    # Use the prepared commit message file as the starting message and open
    # the editor so users (e.g., VS Code) see the content instead of an
    # empty message buffer.
    try:
        run_git(["commit", "--edit", "--template", str(msg_file)])
    except subprocess.CalledProcessError:
        sys.exit(1)
    finally:
        # Clean up the temporary template file
        msg_file.unlink(missing_ok=True)

    # Complete merge
    run_git(["checkout", __TARGET_BRANCH__])
    run_git(["merge", temp_branch])
    run_git(["push", "origin", __TARGET_BRANCH__])
    run_git(["branch", "-D", temp_branch])

    print("✅ Update complete!")
