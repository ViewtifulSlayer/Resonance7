@echo off
REM Resonance 7 Session Tools - Quick Launcher
REM This batch file runs the session management tool
REM Located in library/tools/ and accessible via library/ symlink in projects

cd /d "%~dp0"
python session_tools.py %*

