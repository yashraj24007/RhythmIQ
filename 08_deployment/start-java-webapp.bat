@echo off
cd /d "E:\Projects\RhythmIQ\06_java_webapp"
echo Starting RhythmIQ Java Webapp...
echo Python API should be running on http://localhost:8083
echo Java Webapp will start on http://localhost:8082

:start
echo [%TIME%] Starting Java Webapp...
java -jar target/rhythmiq-webapp-1.0.0.jar --server.port=8082 --logging.level.com.rhythmiq=DEBUG
echo [%TIME%] Java Webapp stopped with exit code %ERRORLEVEL%
if %ERRORLEVEL% neq 0 (
    echo Error occurred, restarting in 5 seconds...
    timeout /t 5 /nobreak >nul
    goto start
)
pause