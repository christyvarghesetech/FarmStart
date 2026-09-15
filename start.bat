@echo off
title FarmStart - New Farmer Copilot
echo ===================================================
echo   Starting FarmStart (FastAPI + ML + Groq Copilot)
echo ===================================================
cd /d "%~dp0"
python run_app.py
pause
