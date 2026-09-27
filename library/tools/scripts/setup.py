#!/usr/bin/env python3
"""Resonance7 first-run setup and workspace doctor.

Idempotent and standard-library only. Safe by default: with no flags it only
reports state; nothing is created, installed, or modified unless a flag asks
for it.

Examples:
  python library/tools/scripts/setup.py                      # report only
  python library/tools/scripts/setup.py --init-dirs          # create runtime folders
  python library/tools/scripts/setup.py --configure-mcp      # .agents/mcp.json + npm install
  python library/tools/scripts/setup.py --install-missing    # opt-in external installs
  python library/tools/scripts/setup.py --all --yes          # everything, non-interactive

External prerequisites are declared in library/tools/setup_requirements.json.
There is no requirements.txt: the Python tools are stdlib-only, and Node
dependencies belong to library/tools/mcp_sqlite_server/package.json.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = REPO_ROOT / "library" / "tools" / "setup_requirements.json"
SETUP_DATABASE = REPO_ROOT / "library" / "tools" / "scripts" / "setup_database.py"

# Runtime folders that are gitignored and therefore absent from a fresh clone.
RUNTIME_DIRS = [
    "library/sessions/current",
    "library/sessions/recent",
    "library/sessions/archived",
    "library/docs/devtools",
    "library/docs/frameworks",
    "library/docs/hardware",
    "library/docs/languages",
    "library/docs/wikis",
    "library/databases/db",
    "library/databases/sources",
    "projects",
    "tests",
]


def line(tag: str, message: str) -> None:
    print(f"[{tag}] {message}")


def ok(message: str) -> None:
    line("ok", message)


def warn(message: str) -> None:
    line("warn", message)


def fail(message: str) -> None:
    line("fail", message)


def info(message: str) -> None:
    line("info", message)


def which(command: str, env=None):
    """Resolve an executable using the supplied environment."""
    return shutil.which(command, path=(env or os.environ).get("PATH"))


def clean_path_entries(value: str) -> list[str]:
    """Return PATH entries without quotes, whitespace, or duplicates."""
    entries = []

    for entry in value.split(os.pathsep):
        entry = entry.strip().strip('"')

        if not entry:
            continue

        if entry not in entries:
            entries.append(entry)

    return entries


def child_environment() -> dict[str, str]:
    """
    Build a clean temporary environment for child processes.

    This does not modify the user's Windows PATH. It only cleans the PATH
    inherited by commands launched from this setup script.
    """
    env = os.environ.copy()
    env["PATH"] = os.pathsep.join(
        clean_path_entries(env.get("PATH", ""))
    )
    return env


def run(cmd, dry_run: bool, quiet: bool = False, env=None) -> int:
    if dry_run:
        info(f"would run: {' '.join(map(str, cmd))}")
        return 0

    try:
        proc = subprocess.run(
            [str(part) for part in cmd],
            capture_output=True,
            text=True,
            env=env or child_environment(),
        )
    except OSError as exc:
        fail(f"{cmd[0]}: {exc}")
        return 1

    if not quiet and proc.stdout.strip():
        print(proc.stdout.strip())

    if not quiet and proc.stderr.strip():
        print(proc.stderr.strip())

    return proc.returncode


def load_manifest():
    if not MANIFEST_PATH.exists():
        warn(f"manifest not found: {MANIFEST_PATH}")
        return []
    try:
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"manifest unreadable: {exc}")
        return []
    return data.get("items", [])


def report_dirs():
    missing = [d for d in RUNTIME_DIRS if not (REPO_ROOT / d).is_dir()]
    if missing:
        warn(f"{len(missing)} runtime dir(s) missing (use --init-dirs): {', '.join(missing)}")
    else:
        ok(f"all {len(RUNTIME_DIRS)} runtime dirs present")
    return missing


def init_dirs(dry_run: bool):
    created = 0
    for rel in RUNTIME_DIRS:
        path = REPO_ROOT / rel
        if path.is_dir():
            continue
        if dry_run:
            info(f"would create: {rel}/")
        else:
            path.mkdir(parents=True, exist_ok=True)
            info(f"created: {rel}/")
        created += 1
    if created == 0:
        ok("runtime dirs already present")
    return created


def check_item(item, env=None):
    check = item.get("check")
    if not check:
        return None
    return which(check[0], env=env) is not None


def report_items(items, env=None):
    missing = []
    for item in items:
        name = item.get("name", "?")
        present = check_item(item, env=env)
        if present is None:
            info(f"{name}: no check defined")
        elif present:
            ok(f"{name}: found")
        else:
            tag = "fail" if item.get("required") else "warn"
            line(tag, f"{name}: not found" + (f" - {item['hint']}" if item.get("hint") else ""))
            missing.append(item)
    return missing


def install_missing(items, dry_run: bool, assume_yes: bool, env=None):
    for item in items:
        install = item.get("install")
        name = item.get("name", "?")
        if not install:
            warn(f"{name}: no install command; install manually" + (f" - {item['hint']}" if item.get("hint") else ""))
            continue
        if dry_run:
            info(f"would install {name}: {' '.join(install)}")
            continue
        proceed = assume_yes
        if not proceed:
            if not sys.stdin.isatty():
                warn(f"{name}: skipping (non-interactive; pass --yes to confirm)")
                continue
            answer = input(f"Install {name} with '{' '.join(install)}'? [y/N] ").strip().lower()
            proceed = answer in ("y", "yes")
        if not proceed:
            warn(f"{name}: skipped")
            continue
        if run(install, dry_run=False, env=env) == 0:
            ok(f"{name}: installed")
        else:
            fail(f"{name}: install command failed")


def report_mcp():
    config = REPO_ROOT / ".agents" / "mcp.json"
    modules = REPO_ROOT / "library" / "tools" / "mcp_sqlite_server" / "node_modules"
    if config.exists():
        ok(".agents/mcp.json present")
    else:
        warn(".agents/mcp.json missing (use --configure-mcp)")
    if modules.is_dir():
        ok("mcp_sqlite_server/node_modules present")
    else:
        warn("mcp_sqlite_server/node_modules missing (use --configure-mcp)")


def configure_mcp(dry_run: bool, env=None) -> int:
    if not SETUP_DATABASE.exists():
        fail(f"setup_database.py not found: {SETUP_DATABASE}")
        return 1

    cmd = [sys.executable, str(SETUP_DATABASE)]

    if dry_run:
        cmd.append("--dry-run")

    return run(cmd, dry_run=False, env=env)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="setup.py",
        description="Resonance7 first-run setup and workspace doctor (stdlib-only, idempotent).",
    )
    parser.add_argument("--init-dirs", action="store_true", help="create missing runtime folders")
    parser.add_argument("--configure-mcp", action="store_true", help="run setup_database.py (writes .agents/mcp.json, npm install)")
    parser.add_argument("--install-missing", action="store_true", help="install missing external prerequisites from the manifest (opt-in)")
    parser.add_argument("--all", action="store_true", help="init dirs, configure MCP, and install missing prerequisites")
    parser.add_argument("--yes", action="store_true", help="do not prompt before running install commands")
    parser.add_argument("--dry-run", action="store_true", help="show what would happen without changing anything")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    env = child_environment()
    do_dirs = args.init_dirs or args.all
    do_mcp = args.configure_mcp or args.all
    do_install = args.install_missing or args.all

    print(f"Resonance7 setup - {REPO_ROOT}")
    print("Report only; pass --init-dirs / --configure-mcp / --install-missing (or --all) to act.")
    print()

    print("Runtime folders")
    report_dirs()

    print("\nMCP / Node dependencies")
    report_mcp()

    print("\nExternal prerequisites")
    items = load_manifest()
    missing = report_items(items, env=env)

    if do_dirs:
        print("\nCreating runtime folders")
        init_dirs(args.dry_run)
    if do_mcp:
        print("\nConfiguring MCP / installing Node dependencies")
        configure_mcp(args.dry_run)
    if do_install and missing:
        print("\nInstalling missing prerequisites")
        install_missing(missing, args.dry_run, args.yes)

    print("\nNext steps")
    print("  - Reload your editor so MCP servers pick up .agents/mcp.json.")
    print("  - Create a session log with: python library/tools/scripts/session_tools.py")
    if not any((do_dirs, do_mcp, do_install)):
        print("  - Run with --all --yes for a full non-interactive setup.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
