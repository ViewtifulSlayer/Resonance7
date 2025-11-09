@echo off
REM Resonance 7 Workspace Setup - Quick Launcher
REM This batch file runs the workspace setup tool

cd /d "%~dp0"
python tools\setup_workspace.py %*

