@echo off
REM Load environment variables from .env file for Windows

echo Loading environment variables from .env...

if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and update with your Supabase credentials
    exit /b 1
)

for /f "tokens=1,2 delims==" %%a in (.env) do (
    set "line=%%a"
    REM Skip comments and empty lines
    if not "!line:~0,1!"=="#" if not "%%a"=="" (
        set "%%a=%%b"
        echo Set %%a
    )
)

echo Environment variables loaded successfully!
