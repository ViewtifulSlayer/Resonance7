@echo off
REM Resonance 7 Session Tools - Quick Launcher
REM This batch file runs the session management tool

cd /d "%~dp0"
python tools\session_tools.py %*

