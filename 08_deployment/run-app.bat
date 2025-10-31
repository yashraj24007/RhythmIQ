@echo off
echo 🫀 RhythmIQ ECG Analysis System
echo ==================================

REM Find Java installation
for /f "tokens=2*" %%i in ('java -XshowSettings:properties -version 2^>^&1 ^| find "java.home"') do set JAVA_HOME=%%j
echo JAVA_HOME set to: %JAVA_HOME%

REM Navigate to webapp directory
cd "%~dp0java-webapp"
if not exist "mvnw.cmd" (
    echo Error: Maven wrapper not found!
    echo Current directory: %CD%
    dir
    pause
    exit /b 1
)

echo 📦 Starting RhythmIQ Web Application...
echo.
echo 🌐 Application will be available at: http://localhost:8081
echo 📊 Model Accuracy: 99.1%
echo.
echo Press Ctrl+C to stop the application
echo.

mvnw.cmd spring-boot:run

pause