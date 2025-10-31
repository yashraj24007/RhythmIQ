@echo off
cd /d "E:\Projects\RhythmIQ\06_java_webapp"
echo Starting RhythmIQ Java Webapp...
echo Working directory: %CD%
dir target\rhythmiq-webapp-1.0.0.jar
java -jar target\rhythmiq-webapp-1.0.0.jar
pause