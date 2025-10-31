@echo off
REM 🔍 Pre-commit Security Check Script for Windows

echo 🔒 RhythmIQ Security Check - Scanning for sensitive files...
echo ================================================================

echo 🔍 Checking what would be committed:
git status --porcelain

echo.
echo ⚠️  SECURITY WARNINGS:
echo - Make sure NO API keys or passwords are in files
echo - Make sure NO .joblib or .pkl model files are included  
echo - Make sure NO ECG images or datasets are included
echo - Make sure NO personal configuration files are included

echo.
echo 📁 Current staged files:
git diff --cached --name-only

echo.
echo 📊 Repository size:
dir .git /s /-c | find "bytes"

echo.
echo 🔐 SECURITY CHECKLIST:
echo [ ] No secrets or API keys in code
echo [ ] No trained models (.joblib, .pkl files)
echo [ ] No ECG images or datasets  
echo [ ] No personal configuration files
echo [ ] Only source code and documentation
echo [ ] Reviewed all changes with 'git diff --cached'

echo.
echo ✅ If checklist is complete, run 'git commit'
echo ❌ Otherwise, use 'git reset' to unstage files

pause