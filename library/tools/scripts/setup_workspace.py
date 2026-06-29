#!/usr/bin/env python3
"""
Resonance7 workspace bootstrap and external project pairing.

Creates runtime directories under the foundation repo (sessions, docs scaffolding,
projects/, tests/, etc.) and can write multi-root *.code-workspace files that
pair this repo with an external project folder.

Idempotent: safe to run multiple times; only creates missing directories.

Usage:
    python library/tools/scripts/setup_workspace.py
    python library/tools/scripts/setup_workspace.py --dry-run
    python library/tools/scripts/setup_workspace.py --interactive
    python library/tools/scripts/setup_workspace.py --pair my-app --project-path "D:\\dev\\my-app"
    python library/tools/scripts/setup_workspace.py --show
    python library/tools/scripts/setup_workspace.py --workspace "<root>"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

__version__ = "1.0.0"

# ---------------------------------------------------------------------------
# Runtime layout (relative to workspace root). Created on first run if missing.
# ---------------------------------------------------------------------------
RUNTIME_DIRECTORIES: tuple[str, ...] = (
    "library/databases/schemas",  # e.g. session_logs.sql
    "library/databases/scripts",  # e.g. ingest_session_logs.py
    "library/databases/sources",
    "library/docs/devtools",
    "library/docs/frameworks",
    "library/docs/hardware",
    "library/docs/languages",
    "library/docs/wikis",
    "library/sessions/archived",
    "library/sessions/current",
    "library/sessions/recent",
    "projects",  # holds local *.code-workspace pairing files (gitignored)
    "tests",
)

# Safe workspace file names: letters, digits, hyphen, underscore.
_PAIR_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")

# Tracked in Git; removed locally after first successful bootstrap (do not commit deletion).
SETUP_SENTINEL_REL = "library/.workspace_setup_required"


# ---------------------------------------------------------------------------
# Small result types for readable summaries
# ---------------------------------------------------------------------------
@dataclass
class BootstrapResult:
    """Tracks which runtime dirs were created vs already present."""

    created: list[str] = field(default_factory=list)
    existing: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Logging helpers (match setup_database.py style)
# ---------------------------------------------------------------------------
def _err(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)


def _info(msg: str) -> None:
    print(msg)


def _warn(msg: str) -> None:
    print(f"WARNING: {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Workspace root detection
# ---------------------------------------------------------------------------
def find_workspace_root(explicit: Path | None = None) -> Path:
    """
    Resolve the Resonance7 foundation repo root.

    Default: infer from this file's location (library/tools/scripts/ -> root).
    Explicit --workspace must contain library/agent_foundation.json.
    """
    if explicit is not None:
        root = explicit.resolve()
    else:
        root = Path(__file__).resolve().parents[3]

    marker = root / "library" / "agent_foundation.json"
    if not marker.is_file():
        _err(f"Not a Resonance7 workspace (missing {marker})")
        raise SystemExit(1)
    return root


# ---------------------------------------------------------------------------
# Directory bootstrap
# ---------------------------------------------------------------------------
def bootstrap_directories(root: Path, dry_run: bool = False) -> BootstrapResult:
    """
    Create any missing RUNTIME_DIRECTORIES under root.

    Never deletes or modifies existing paths; mkdir parents as needed.
    """
    result = BootstrapResult()

    for rel in RUNTIME_DIRECTORIES:
        target = root / rel
        if target.exists():
            result.existing.append(rel)
            continue
        if dry_run:
            result.created.append(rel)
            continue
        target.mkdir(parents=True, exist_ok=True)
        result.created.append(rel)

    return result


def print_bootstrap_summary(root: Path, result: BootstrapResult, dry_run: bool) -> None:
    """Human-readable bootstrap report."""
    prefix = "Would create" if dry_run else "Created"
    _info(f"Workspace: {root}")
    if result.created:
        for rel in result.created:
            _info(f"  {prefix}: {rel}")
    if result.existing:
        for rel in result.existing:
            _info(f"  Exists:  {rel}")
    _info(
        f"Done. {len(result.created)} {'would be ' if dry_run else ''}created, "
        f"{len(result.existing)} already present."
    )


# ---------------------------------------------------------------------------
# First-run sentinel (library/.workspace_setup_required)
# ---------------------------------------------------------------------------
def setup_sentinel_path(root: Path) -> Path:
    """Path to the tracked marker that signals bootstrap has not run on this clone."""
    return root / SETUP_SENTINEL_REL


def clear_setup_sentinel(root: Path, dry_run: bool = False) -> bool:
    """
    Remove the first-run marker after successful setup.

    Fresh clones ship with this file; deleting it locally is expected.
    Upstream keeps it tracked so the next clone still gets the marker.
    """
    path = setup_sentinel_path(root)
    if not path.is_file():
        return False
    if dry_run:
        _info(f"Would remove first-run marker: {path}")
        return True
    path.unlink()
    _info(f"Removed first-run marker: {path}")
    return True


# ---------------------------------------------------------------------------
# External project pairing (*.code-workspace)
# ---------------------------------------------------------------------------
def validate_pair_name(name: str) -> str:
    """Reject names that are unsafe as filenames or confusing as paths."""
    name = name.strip()
    if not name:
        raise SystemExit("Pair name is required.")
    if not _PAIR_NAME_RE.match(name):
        raise SystemExit(
            "Invalid pair name. Use letters, digits, hyphen, or underscore "
            "(must start with a letter or digit)."
        )
    return name


def resolve_project_path(raw: str) -> Path:
    """
    Resolve and validate the external project directory.

    v1: directory must already exist; we do not scaffold project trees here.
    """
    path = Path(raw.strip()).expanduser().resolve()
    if not path.is_dir():
        _err(f"Project path is not an existing directory: {path}")
        raise SystemExit(1)
    return path


def build_code_workspace(root: Path, name: str, project_path: Path) -> dict:
    """
    Build multi-root workspace JSON (Cursor and VS Code compatible).

    File lives at projects/<name>.code-workspace; '..' points at foundation root.
    """
    return {
        "folders": [
            {"path": "..", "name": "Resonance7"},
            {"path": str(project_path), "name": name},
        ],
        "settings": {},
    }


def workspace_file_path(root: Path, name: str) -> Path:
    """Standard location for pairing files."""
    return root / "projects" / f"{name}.code-workspace"


def write_code_workspace(
    root: Path,
    name: str,
    project_path: Path,
    *,
    dry_run: bool = False,
    force: bool = False,
) -> Path:
    """
    Write projects/<name>.code-workspace after ensuring projects/ exists.

    Prompts are handled by callers; this function enforces overwrite policy.
    """
    name = validate_pair_name(name)
    project_path = resolve_project_path(str(project_path))

    # Bootstrap ensures projects/ exists before we write into it.
    bootstrap_directories(root, dry_run=dry_run)

    out_path = workspace_file_path(root, name)
    if out_path.exists() and not force:
        _err(f"Workspace file already exists: {out_path}")
        _err("Use --force to overwrite, or pick a different name.")
        raise SystemExit(1)

    cfg = build_code_workspace(root, name, project_path)

    if dry_run:
        _info(f"Would write: {out_path}")
        _info(json.dumps(cfg, indent=2))
        return out_path

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    _info(f"Wrote {out_path}")
    _info(f"  Resonance7 root: {root}")
    _info(f"  Project folder:  {project_path}")
    _info("Open this .code-workspace file in Cursor or VS Code for a multi-root workspace.")
    # Pairing runs bootstrap first; clear first-run marker when not previewing.
    clear_setup_sentinel(root, dry_run=dry_run)
    return out_path


def pair_project_workflow(
    root: Path,
    name: str | None,
    project_path: str | None,
    *,
    dry_run: bool = False,
    force: bool = False,
    interactive: bool = False,
) -> int:
    """
    Pairing entry point: CLI flags or interactive prompts.

    Returns exit code 0 on success, 1 on cancel/error.
    """
    if interactive or not name or not project_path:
        if not interactive:
            _err("Both --pair and --project-path are required (or use --interactive).")
            return 1
        _info("")
        _info("Pair external project with Resonance7 foundation")
        _info("-" * 48)
        if not name:
            name = input("Workspace name (e.g. my-app): ").strip()
        if not project_path:
            project_path = input("Absolute path to existing project folder: ").strip()
        if not name or not project_path:
            _err("Name and project path are required.")
            return 1
        out_path = workspace_file_path(root, validate_pair_name(name))
        if out_path.exists() and not force:
            answer = input(f"{out_path} exists. Overwrite? [y/N]: ").strip().lower()
            if answer not in ("y", "yes"):
                _info("Cancelled.")
                return 1
            force = True

    assert name is not None and project_path is not None
    write_code_workspace(root, name, Path(project_path), dry_run=dry_run, force=force)
    return 0


# ---------------------------------------------------------------------------
# Workspace status (replaces old project_tools "show structure")
# ---------------------------------------------------------------------------
def show_workspace_status(root: Path) -> None:
    """Print foundation paths and any pairing files under projects/."""
    _info("=" * 64)
    _info("  WORKSPACE STATUS")
    _info("=" * 64)
    _info(f"Foundation root: {root}")
    _info("")

    _info("Runtime directories:")
    for rel in RUNTIME_DIRECTORIES:
        target = root / rel
        mark = "ok" if target.is_dir() else "missing"
        _info(f"  [{mark}] {rel}")
    _info("")

    sentinel = setup_sentinel_path(root)
    if sentinel.is_file():
        _info("First-run marker: present (run bootstrap to remove)")
    else:
        _info("First-run marker: absent (bootstrap completed on this clone)")
    _info("")

    projects_dir = root / "projects"
    if projects_dir.is_dir():
        files = sorted(projects_dir.glob("*.code-workspace"))
        if files:
            _info("Pairing files (projects/):")
            for f in files:
                _info(f"  {f.name}")
        else:
            _info("Pairing files: (none yet)")
    else:
        _info("Pairing files: projects/ not created yet")


# ---------------------------------------------------------------------------
# Interactive menu (--interactive)
# ---------------------------------------------------------------------------
def show_menu() -> int:
    """Simple numbered menu; returns 1-4 or raises SystemExit on bad input."""
    _info("")
    _info("-" * 48)
    _info("  WORKSPACE SETUP")
    _info("-" * 48)
    _info("1. Bootstrap runtime directories")
    _info("2. Pair external project (.code-workspace)")
    _info("3. Show workspace status")
    _info("4. Exit")
    _info("")
    while True:
        choice = input("Choice [1-4]: ").strip()
        if choice in ("1", "2", "3", "4"):
            return int(choice)
        _info("Invalid choice. Enter 1, 2, 3, or 4.")


def run_interactive_menu(root: Path, dry_run: bool) -> int:
    """Loop until user exits; each action is idempotent where applicable."""
    while True:
        choice = show_menu()
        if choice == 1:
            result = bootstrap_directories(root, dry_run=dry_run)
            print_bootstrap_summary(root, result, dry_run)
            clear_setup_sentinel(root, dry_run=dry_run)
        elif choice == 2:
            code = pair_project_workflow(
                root, None, None, dry_run=dry_run, interactive=True
            )
            if code != 0:
                return code
        elif choice == 3:
            show_workspace_status(root)
        elif choice == 4:
            _info("Goodbye.")
            return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Bootstrap Resonance7 runtime directories and pair external projects "
            "via projects/*.code-workspace files."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
      Bootstrap missing runtime directories (default after clone).

  %(prog)s --dry-run
      Preview bootstrap without creating directories.

  %(prog)s --interactive
      Menu: bootstrap, pair project, show status.

  %(prog)s --pair my-app --project-path "D:\\dev\\my-app"
      Write projects/my-app.code-workspace for multi-root editing.

  %(prog)s --show
      Print directory and pairing status only.
        """,
    )
    parser.add_argument(
        "--workspace",
        type=str,
        default=None,
        help="Resonance7 root (contains library/). Default: infer from script location.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing directories or workspace files.",
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Interactive menu (bootstrap, pair, status).",
    )
    parser.add_argument(
        "--pair",
        type=str,
        default=None,
        metavar="NAME",
        help="Pairing name for projects/NAME.code-workspace (requires --project-path).",
    )
    parser.add_argument(
        "--project-path",
        type=str,
        default=None,
        metavar="PATH",
        help="Absolute or relative path to an existing external project directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing projects/NAME.code-workspace file.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show workspace status only (no bootstrap).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    ws_path = Path(args.workspace).resolve() if args.workspace else None
    root = find_workspace_root(ws_path)

    # Status-only mode: no side effects.
    if args.show:
        show_workspace_status(root)
        return 0

    # Direct pairing via flags (non-interactive).
    if args.pair or args.project_path:
        if not args.pair or not args.project_path:
            _err("Both --pair and --project-path are required together.")
            return 1
        return pair_project_workflow(
            root,
            args.pair,
            args.project_path,
            dry_run=args.dry_run,
            force=args.force,
            interactive=False,
        )

    # Interactive menu (optional bootstrap actions inside menu).
    if args.interactive:
        return run_interactive_menu(root, dry_run=args.dry_run)

    # Default: bootstrap only (README install step 2).
    result = bootstrap_directories(root, dry_run=args.dry_run)
    print_bootstrap_summary(root, result, dry_run=args.dry_run)
    clear_setup_sentinel(root, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
