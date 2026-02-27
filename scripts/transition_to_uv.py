#!/usr/bin/env python3
"""Migrate pyproject.toml from Poetry to uv, then self-clean."""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def remove_section(content: str, section_name: str) -> str:
    """Remove a TOML section header and its key-value lines."""
    lines = content.splitlines(keepends=True)
    result: list[str] = []
    skipping = False
    header = f"[{section_name}]"
    for line in lines:
        if line.strip() == header:
            skipping = True
            continue
        if skipping and line.strip().startswith("["):
            skipping = False
        if not skipping:
            result.append(line)
    return "".join(result)


def update_build_system(content: str) -> str:
    """Replace poetry-core build system with hatchling."""
    content = re.sub(
        r'requires\s*=\s*\["poetry-core[^"]*"\]',
        'requires = ["hatchling"]',
        content,
    )
    content = re.sub(
        r'build-backend\s*=\s*"poetry\.core\.masonry\.api"',
        'build-backend = "hatchling.build"',
        content,
    )
    return content


def extract_poetry_packages(content: str) -> list[str]:
    """Extract package paths from the [tool.poetry] packages key."""
    packages: list[str] = []
    in_poetry = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped == "[tool.poetry]":
            in_poetry = True
        elif in_poetry and stripped.startswith("["):
            break
        elif in_poetry and "packages" in stripped:
            for m in re.finditer(
                r'\{\s*include\s*=\s*"([^"]+)"(?:,\s*from\s*=\s*"([^"]+)")?\s*\}',
                stripped,
            ):
                name, from_dir = m.group(1), m.group(2)
                packages.append(f"{from_dir}/{name}" if from_dir else name)
    return packages


def insert_hatch_section(content: str, packages: list[str]) -> str:
    """Insert [tool.hatch.build.targets.wheel] after the [build-system] block."""
    if "[tool.hatch.build.targets.wheel]" in content:
        return content
    packages_str = ", ".join(f'"{p}"' for p in packages)
    hatch_block = (
        f"[tool.hatch.build.targets.wheel]\n"
        f"packages = [{packages_str}]\n"
    )
    lines = content.splitlines(keepends=True)
    result: list[str] = []
    in_build_system = False
    inserted = False
    for line in lines:
        if line.strip() == "[build-system]":
            in_build_system = True
        elif in_build_system and line.strip().startswith("[") and not inserted:
            result.append(hatch_block + "\n")
            in_build_system = False
            inserted = True
        result.append(line)
    if in_build_system and not inserted:
        result.append("\n" + hatch_block)
    return "".join(result)


def add_poethepoet_to_dev(content: str) -> str:
    """Add poethepoet to the [dependency-groups] dev list."""
    if "poethepoet" in content:
        return content
    match = re.search(r"dev\s*=\s*\[(.*?)\]", content, flags=re.DOTALL)
    if not match:
        return content
    items = re.findall(r'"[^"]+"', match.group(1))
    all_items = ['"poethepoet>=0.34.0"'] + items
    new_list = "[\n" + "".join(f"    {item},\n" for item in all_items) + "]"
    return content[: match.start()] + f"dev = {new_list}" + content[match.end() :]


def remove_script_key(content: str, key: str) -> str:
    """Remove a single key-value line from [project.scripts]."""
    lines = content.splitlines(keepends=True)
    result: list[str] = []
    in_scripts = False
    for line in lines:
        if line.strip() == "[project.scripts]":
            in_scripts = True
        elif in_scripts and line.strip().startswith("["):
            in_scripts = False
        if in_scripts and line.strip().startswith(f"{key}"):
            continue
        result.append(line)
    return "".join(result)


def delete_if_exists(path: Path) -> None:
    if path.exists():
        path.unlink()
        print(f"Deleted {path.name}")


def main() -> None:
    pyproject = ROOT / "pyproject.toml"
    if not pyproject.exists():
        print(f"Error: {pyproject} not found", file=sys.stderr)
        sys.exit(1)

    content = pyproject.read_text(encoding="utf-8")

    packages = extract_poetry_packages(content)

    content = remove_section(content, "tool.poetry.requires-plugins")
    content = update_build_system(content)
    if packages:
        content = insert_hatch_section(content, packages)
    content = remove_section(content, "tool.poetry")
    content = add_poethepoet_to_dev(content)
    content = remove_script_key(content, "transition-to-uv")

    pyproject.write_text(content, encoding="utf-8")
    print("pyproject.toml migrated to uv.")

    delete_if_exists(ROOT / "poetry.lock")
    delete_if_exists(ROOT / "poetry.toml")

    print("Running uv sync...")
    subprocess.run(["uv", "sync"], check=True, cwd=ROOT)

    Path(__file__).unlink()
    print("Done.")


if __name__ == "__main__":
    main()
