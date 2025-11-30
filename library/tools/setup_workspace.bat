@echo off
REM Resonance 7 Workspace Setup - Quick Launcher
REM This batch file runs the workspace setup tool
REM Located in library/tools/ and accessible via library/ symlink in projects

cd /d "%~dp0"
python setup_workspace.py %*

