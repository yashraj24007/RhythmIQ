@echo off
REM RhythmIQ Java Web Application - Build and Run Script for Windows

echo 🫀 RhythmIQ ECG Analysis System
echo ==================================

REM Change to webapp directory
cd java-webapp

echo 📦 Building application...
call mvnw.cmd clean package -DskipTests

if %ERRORLEVEL% EQU 0 (
    echo ✅ Build successful!
    echo.
    echo 🚀 Starting RhythmIQ Web Application...
    echo 🌐 Application will be available at: http://localhost:8080
    echo.
    
    REM Run the application
    call mvnw.cmd spring-boot:run
) else (
    echo ❌ Build failed!
    pause
    exit /b 1
)