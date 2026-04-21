"""
Release helper — bumps the version, pushes, and opens a PR into main.
Merging the PR triggers release.yml which builds, publishes to PyPI, and
creates a GitHub release.

Usage:
    python publish.py           # auto-increment patch  (0.2.99 -> 0.2.100)
    python publish.py 1.2.3     # pin to a specific version

Requires the GitHub CLI (gh) to be installed and authenticated.
"""

import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Version helpers
# ---------------------------------------------------------------------------


def _parse(ver: str) -> tuple[int, int, int]:
    parts = ver.strip().strip('"').split(".")
    if len(parts) != 3:
        raise ValueError(f"expected MAJOR.MINOR.PATCH, got {ver!r}")
    return tuple(int(p) for p in parts)


def _fmt(v: tuple[int, int, int]) -> str:
    return f"{v[0]}.{v[1]}.{v[2]}"


def _bump_patch(v: tuple[int, int, int]) -> tuple[int, int, int]:
    return (v[0], v[1], v[2] + 1)


def _update_version(path: Path, pattern: str, new_ver: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated = re.sub(
        pattern,
        lambda m: f"{m.group(1)}{new_ver}{m.group(3)}",
        text,
        flags=re.MULTILINE,
    )
    path.write_text(updated, encoding="utf-8")


def bump_version(
    pyproject: Path,
    module: Path,
    new_version: tuple[int, int, int] | None = None,
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    pyproject_text = pyproject.read_text(encoding="utf-8")
    m = re.search(
        r'^version\s*=\s*"([0-9]+\.[0-9]+\.[0-9]+)"', pyproject_text, re.MULTILINE
    )
    if not m:
        raise RuntimeError("Could not find version in pyproject.toml")
    old = _parse(m.group(1))
    new = _bump_patch(old) if new_version is None else new_version

    _update_version(
        pyproject, r'(^version\s*=\s*")([0-9]+\.[0-9]+\.[0-9]+)(")', _fmt(new)
    )
    _update_version(
        module, r'(^__version__\s*=\s*")([0-9]+\.[0-9]+\.[0-9]+)(")', _fmt(new)
    )
    return old, new


# ---------------------------------------------------------------------------
# Shell helpers
# ---------------------------------------------------------------------------


def _run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f"error: '{' '.join(cmd)}' exited {result.returncode}", file=sys.stderr)
        sys.exit(result.returncode)


def _capture(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"error: '{' '.join(cmd)}' exited {result.returncode}", file=sys.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()


def _gh_installed() -> bool:
    try:
        result = subprocess.run(["gh", "--version"], capture_output=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    project_root = Path(__file__).parent
    pyproject = project_root / "pyproject.toml"
    module = project_root / "bruhanimate" / "__init__.py"

    new_ver = None
    if len(sys.argv) == 2:
        try:
            new_ver = _parse(sys.argv[1])
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            sys.exit(1)

    # Bump version
    old, new = bump_version(pyproject, module, new_ver)
    ver_str = _fmt(new)
    print(f"version: {_fmt(old)} → {ver_str}")

    # Commit and push current branch
    branch = _capture(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    _run(["git", "add", "pyproject.toml", "bruhanimate/__init__.py"])
    _run(["git", "commit", "-m", f"version bump {ver_str}"])
    _run(["git", "push", "--set-upstream", "origin", branch])

    # Open PR into main via gh CLI
    if not _gh_installed():
        print(
            "\ngh CLI not found — open a PR manually and merge into main to trigger the release."
        )
        return

    print("\nOpening PR into main...")
    _run(
        [
            "gh",
            "pr",
            "create",
            "--base",
            "main",
            "--head",
            branch,
            "--title",
            f"release v{ver_str}",
            "--body",
            f"Bumps version to `{ver_str}`.\n\nMerging this PR will trigger the release workflow: PyPI publish + GitHub release.",
        ]
    )

    print(
        f"\nPR opened. Merge it into main and GitHub Actions will publish v{ver_str}."
    )


if __name__ == "__main__":
    main()
