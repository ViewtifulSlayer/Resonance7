#!/usr/bin/env python3
"""
Write `.cursor/mcp.json` and run `npm install` for the Resonance7 SQLite MCP server.

Resolves the workspace root from this file's location, picks a single Node
executable (prefer a full install over the first on PATH), and uses that same
Node's npm in `library/tools/mcp_sqlite_server` so native modules (better-sqlite3)
match the runtime.

Environment:
    NODE_EXE   If set, use this path as the Node executable (overridden by --node).

Usage:
    python library/tools/setup_mcp_sqlite.py
    python library/tools/setup_mcp_sqlite.py --dry-run
    python library/tools/setup_mcp_sqlite.py --node "C:\\Program Files\\nodejs\\node.exe"
    python library/tools/setup_mcp_sqlite.py --workspace "E:\\Resonance7"
    python library/tools/setup_mcp_sqlite.py --skip-audit-fix
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

__version__ = "1.0.0"

# Minimum major Node version (must stay aligned with mcp_sqlite_server/package.json engines)
MIN_NODE_MAJOR = 18

# Template committed at library/templates/configuration_templates/mcp.json.example
TEMPLATE_REF = "library/templates/configuration_templates/mcp.json.example"


def _err(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)


def _info(msg: str) -> None:
    print(msg)


def _warn(msg: str) -> None:
    print(f"WARNING: {msg}", file=sys.stderr)


def _node_install_instructions() -> str:
    return (
        "Node.js was not found or could not be used. Install Node 18 or newer, then run this script again.\n"
        "  LTS (recommended): https://nodejs.org/en/download\n"
        "  Windows (winget):  winget install OpenJS.NodeJS.LTS\n"
        "After installing, open a new terminal (or restart Cursor) so PATH updates.\n"
        "If Node is already installed, set NODE_EXE to the full path to node.exe, or pass --node."
    )


def find_workspace_root(explicit: Optional[Path] = None) -> Path:
    if explicit is not None:
        root = explicit.resolve()
        if not (root / "library" / "tools" / "mcp_sqlite_server").is_dir():
            raise SystemExit(
                f"Not a Resonance7 workspace: missing library/tools/mcp_sqlite_server under {root}"
            )
        return root
    # This file: library/tools/setup_mcp_sqlite.py
    here = Path(__file__).resolve()
    root = here.parents[2]  # tools -> library -> workspace
    if not (root / "library" / "tools" / "mcp_sqlite_server").is_dir():
        raise SystemExit(
            f"Could not resolve workspace root from {here}. Use --workspace <path to Resonance7 root>."
        )
    return root


def _read_mcp_engines_majors(server_pkg: Path) -> int:
    """Return minimum required Node major from package.json engines (best-effort)."""
    if not server_pkg.is_file():
        return MIN_NODE_MAJOR
    try:
        data: dict[str, Any] = json.loads(server_pkg.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return MIN_NODE_MAJOR
    eng = data.get("engines") or {}
    spec = str(eng.get("node", "")).strip()
    m = re.search(r"(\d+)", spec)
    if m:
        return int(m.group(1))
    return MIN_NODE_MAJOR


def _parse_node_v_version(text: str) -> Optional[tuple[int, ...]]:
    t = text.strip()
    if t.startswith("v"):
        t = t[1:].split()[0] if t[1:].split() else ""
    if not t:
        return None
    parts: list[int] = []
    for p in t.split(".")[:3]:
        try:
            parts.append(int(p))
        except ValueError:
            break
    if not parts:
        return None
    return tuple(parts)


def _get_node_version_tuple(node: Path) -> Optional[tuple[int, ...]]:
    try:
        out = subprocess.run(
            [str(node), "--version"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except OSError:
        return None
    if out.returncode != 0 or not (out.stdout or out.stderr):
        return None
    line = (out.stdout or out.stderr or "").strip().splitlines()[0]
    return _parse_node_v_version(line)


def _windows_program_files_nodes() -> list[Path]:
    out: list[Path] = []
    for part in (
        os.environ.get("ProgramFiles", r"C:\Program Files"),
        os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
    ):
        n = Path(part) / "nodejs" / "node.exe"
        if n.is_file():
            out.append(n)
    return out


def resolve_node_exe(
    arg_node: Optional[str], required_major: int
) -> Path:
    """Pick one node.exe. Prefer env/--node, then a full Windows install, then PATH."""
    candidates: list[Path] = []

    if arg_node:
        p = Path(arg_node).expanduser().resolve()
        if p.is_file():
            candidates.append(p)
        else:
            raise SystemExit(f"--node does not point to a file: {p}")

    env = os.environ.get("NODE_EXE", "").strip()
    if not candidates and env:
        p = Path(env).expanduser().resolve()
        if p.is_file():
            candidates.append(p)
        else:
            raise SystemExit(f"NODE_EXE is set but is not a file: {p}")

    if not candidates and os.name == "nt":
        candidates.extend(_windows_program_files_nodes())

    if not candidates:
        w = shutil.which("node")
        if w:
            candidates.append(Path(w).resolve())

    if not candidates:
        _err(_node_install_instructions())
        raise SystemExit(1)

    chosen = candidates[0]
    if len(candidates) > 1 and os.name == "nt" and not arg_node and not env:
        wpf = [c for c in candidates if "Program Files" in str(c) and "nodejs" in str(c).lower()]
        if wpf:
            chosen = wpf[0]
        _info(
            f"Note: multiple Node executables are available. Using: {chosen}\n"
            f"      Set NODE_EXE or use --node to pick a different one."
        )

    ver = _get_node_version_tuple(chosen)
    if not ver or ver[0] < required_major:
        vtext = "unknown version" if not ver else ".".join(str(x) for x in ver)
        _err(
            f"Node {required_major}+ required (per package.json engines). "
            f"Found: {chosen} ({vtext})"
        )
        _err(_node_install_instructions())
        raise SystemExit(1)

    return chosen


def resolve_npm_path(node: Path) -> Path:
    """Use npm that ships next to the chosen node when possible."""
    d = node.parent
    if os.name == "nt":
        for name in ("npm.cmd", "npm.exe"):
            p = d / name
            if p.is_file():
                return p
    else:
        p = d / "npm"
        if p.is_file():
            return p
    w = shutil.which("npm")
    if w:
        return Path(w).resolve()
    _err("Could not find npm next to the Node you selected, and 'npm' is not on PATH.")
    _err(_node_install_instructions())
    raise SystemExit(1)


def build_mcp_config(workspace: Path, node: Path) -> dict[str, Any]:
    server_js = (
        workspace
        / "library"
        / "tools"
        / "mcp_sqlite_server"
        / "src"
        / "server.js"
    ).resolve()
    default_db = (
        workspace
        / "library"
        / "resources"
        / "databases"
        / "db"
        / "session_logs.db"
    ).resolve()

    return {
        "mcpServers": {
            "Resonance7-sqlite": {
                "command": str(node),
                "args": [str(server_js)],
                "env": {"DEFAULT_DB_PATH": str(default_db)},
            }
        }
    }


def run_npm_install(npm: Path, cwd: Path) -> None:
    _info(f"Running npm install in {cwd} ...")
    r = subprocess.run(
        [str(npm), "install"],
        cwd=str(cwd),
        shell=False,
    )
    if r.returncode != 0:
        raise SystemExit(f"npm install failed with exit code {r.returncode}")


def run_npm_audit_fix(npm: Path, cwd: Path) -> None:
    """Apply compatible security fixes (npm audit fix). Non-zero exit is warning only."""
    _info(f"Running npm audit fix in {cwd} ...")
    r = subprocess.run(
        [str(npm), "audit", "fix"],
        cwd=str(cwd),
        shell=False,
    )
    if r.returncode != 0:
        _warn(
            f"npm audit fix exited with code {r.returncode}. "
            "Run `npm audit` in that folder to review any remaining items."
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Configure Cursor MCP for the Resonance7 SQLite server and install npm dependencies.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_node_install_instructions(),
    )
    parser.add_argument(
        "--workspace",
        type=str,
        default=None,
        help="Resonance7 root (folder that contains library/). Default: infer from this script location.",
    )
    parser.add_argument(
        "--node",
        type=str,
        default=None,
        help="Full path to node.exe (or node on macOS/Linux). Overrides NODE_EXE.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print paths and JSON only; do not write .cursor/mcp.json or run npm install/audit fix.",
    )
    parser.add_argument(
        "--skip-audit-fix",
        action="store_true",
        help="After npm install, skip `npm audit fix` (not recommended).",
    )
    args = parser.parse_args()

    ws_path = (
        Path(args.workspace).resolve()
        if args.workspace
        else None
    )
    root = find_workspace_root(ws_path)
    server_pkg = root / "library" / "tools" / "mcp_sqlite_server" / "package.json"
    required_major = _read_mcp_engines_majors(server_pkg)

    node = resolve_node_exe(args.node, required_major=required_major)
    npm = resolve_npm_path(node)

    mcp_dir = root / "library" / "tools" / "mcp_sqlite_server"
    out_file = root / ".cursor" / "mcp.json"
    cfg = build_mcp_config(root, node)

    _info(f"Workspace:     {root}")
    _info(f"Node:          {node}")
    v = _get_node_version_tuple(node)
    if v is not None:
        ver_s = "v" + ".".join(str(n) for n in v)
        _info(f"Node version:  {ver_s}")
    _info(f"npm:           {npm}")
    _info(f"MCP config:    {out_file}")
    _info(f"Template ref:  {root / TEMPLATE_REF}")
    if args.dry_run:
        _info("--- would write mcp.json ---")
        print(json.dumps(cfg, indent=2))
        _info("--- dry run: skipped writing file and npm install ---")
        return

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    _info(f"Wrote {out_file}")
    run_npm_install(npm, mcp_dir)
    if not args.skip_audit_fix:
        run_npm_audit_fix(npm, mcp_dir)
    else:
        _info("Skipped npm audit fix (--skip-audit-fix).")
    _info("Done. Reload the Cursor window so MCP servers pick up the new config.")


if __name__ == "__main__":
    main()
