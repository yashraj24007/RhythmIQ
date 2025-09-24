@echo off
echo RhythmIQ ECG Analysis System - Java Web Application
echo ====================================================

cd java-webapp

echo Checking for Maven installation...
where mvn >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Maven found! Building and running application...
    mvn clean spring-boot:run
) else (
    echo.
    echo Maven not found in PATH. 
    echo Please install Maven or use an IDE to run the application.
    echo.
    echo Manual steps:
    echo 1. Install Maven from https://maven.apache.org/
    echo 2. Add Maven to your PATH
    echo 3. Run: mvn clean spring-boot:run
    echo.
    echo Alternative - Use IDE:
    echo 1. Open java-webapp folder in IntelliJ IDEA or VS Code
    echo 2. Import as Maven project
    echo 3. Run RhythmIQApplication.java
    echo.
    echo The application will be available at: http://localhost:8080
    pause
)