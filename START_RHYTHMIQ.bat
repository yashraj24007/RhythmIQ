@echo off
REM ===========================================
REM  RhythmIQ - One-Click Startup
REM ===========================================

echo.
echo ========================================
echo   🫀 Starting RhythmIQ Services
echo ========================================
echo.

REM Run PowerShell script to start both services
powershell -ExecutionPolicy Bypass -File "%~dp008_deployment\start-services.ps1"

echo.
echo Press any key to exit...
pause >nul
