@echo off
REM Start RhythmIQ with Real ML Model Integration

echo 🫀 RhythmIQ ECG Analysis System - Full Integration
echo ===================================================

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo 📦 Installing Python API dependencies...
pip install -r api_requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully!
echo.

echo 🐍 Starting Python ML API Service (Port 8083)...
start "Python API" cmd /c "python python_api_service.py"

REM Wait a moment for Python API to start
timeout /t 5 /nobreak >nul

echo 🌐 Testing Python API connection...
curl -s http://localhost:8083/health >nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Python API is running!
) else (
    echo ⚠️  Python API might still be starting...
)

echo.
echo ☕ Starting Java Web Application (Port 8082)...
cd java-webapp
call mvnw.cmd spring-boot:run

echo.
echo 🎉 RhythmIQ is now running with REAL ML MODEL!
echo 🌐 Web Interface: http://localhost:8082
echo 🐍 Python API: http://localhost:8083
echo.
echo Press Ctrl+C to stop both services
pause