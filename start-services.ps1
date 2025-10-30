# RhythmIQ - Start All Services
# Starts Python ML API and Java Web Application

Write-Host "Starting RhythmIQ Services..." -ForegroundColor Cyan

# Stop any existing services first
Write-Host "Checking for existing processes..." -ForegroundColor Gray
$javaProcesses = Get-Process -Name "java" -ErrorAction SilentlyContinue
$pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue

if ($javaProcesses) {
    Write-Host "  Stopping existing Java processes..." -ForegroundColor Yellow
    $javaProcesses | Stop-Process -Force
    Start-Sleep -Seconds 2
}

if ($pythonProcesses) {
    Write-Host "  Stopping existing Python processes..." -ForegroundColor Yellow
    $pythonProcesses | Stop-Process -Force
    Start-Sleep -Seconds 2
}

# Start Python ML API
Write-Host "`n[Python API] Starting on port 8083..." -ForegroundColor Yellow
Start-Process -FilePath "C:/Users/Yash/AppData/Local/Programs/Python/Python313/python.exe" `
              -ArgumentList "rhythmiq_api.py" `
              -WorkingDirectory "E:\Projects\RhythmIQ\11_python_api" `
              -WindowStyle Hidden

Write-Host "  Waiting for Python API to start..." -ForegroundColor Gray
Start-Sleep -Seconds 3

# Verify Python API
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8083/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "  [OK] Python API started successfully" -ForegroundColor Green
    }
} catch {
    Write-Host "  [WARNING] Python API might not be ready yet" -ForegroundColor Yellow
}

# Start Java Web Application
Write-Host "`n[Java Webapp] Starting on port 8082..." -ForegroundColor Yellow
Set-Location "E:\Projects\RhythmIQ\07_java_webapp"
Start-Process -FilePath "java" `
              -ArgumentList "-jar","target\rhythmiq-webapp-1.0.0.jar" `
              -WindowStyle Hidden

Write-Host "  Waiting for webapp to start..." -ForegroundColor Gray
Start-Sleep -Seconds 12

# Verify Java webapp
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8082/" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "  [OK] Java webapp started successfully" -ForegroundColor Green
    }
} catch {
    Write-Host "  [WARNING] Webapp might need more time to start" -ForegroundColor Yellow
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🫀 RhythmIQ Services Started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nAccess Points:" -ForegroundColor Yellow
Write-Host "   🌐 Web Application: http://localhost:8082/" -ForegroundColor White
Write-Host "   🔬 Python ML API: http://localhost:8083/health" -ForegroundColor White

Write-Host "`n📝 Note: No login required - direct access enabled!" -ForegroundColor Cyan
Write-Host "`n🛑 To stop services, run: .\stop-services.ps1" -ForegroundColor Gray

# Open browser
Start-Sleep -Seconds 2
Write-Host "`n🌐 Opening browser..." -ForegroundColor Cyan
Start-Process "http://localhost:8082/"
