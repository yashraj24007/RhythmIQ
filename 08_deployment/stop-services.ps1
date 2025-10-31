# RhythmIQ - Stop All Services
# Stops all running Java and Python processes for clean restart

Write-Host "🛑 Stopping RhythmIQ Services..." -ForegroundColor Yellow

# Stop Java processes
$javaProcesses = Get-Process -Name "java" -ErrorAction SilentlyContinue
if ($javaProcesses) {
    Write-Host "  ⏹ Stopping $($javaProcesses.Count) Java process(es)..." -ForegroundColor Cyan
    $javaProcesses | Stop-Process -Force
    Start-Sleep -Seconds 2
    Write-Host "  ✅ Java processes stopped" -ForegroundColor Green
} else {
    Write-Host "  ℹ No Java processes running" -ForegroundColor Gray
}

# Stop Python processes
$pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "  ⏹ Stopping $($pythonProcesses.Count) Python process(es)..." -ForegroundColor Cyan
    $pythonProcesses | Stop-Process -Force
    Start-Sleep -Seconds 2
    Write-Host "  ✅ Python processes stopped" -ForegroundColor Green
} else {
    Write-Host "  ℹ No Python processes running" -ForegroundColor Gray
}

Write-Host "`n✅ All services stopped successfully!" -ForegroundColor Green
Write-Host "   You can now run start-services.ps1 to restart" -ForegroundColor Gray
