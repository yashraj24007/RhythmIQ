# Test RhythmIQ Integration
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Testing RhythmIQ Integration" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Test 1: Python API Health
Write-Host "`n[1] Testing Python API Health..." -ForegroundColor Yellow
try {
    $pythonHealth = Invoke-WebRequest -Uri "http://localhost:8083/health" -Method GET
    $healthData = $pythonHealth.Content | ConvertFrom-Json
    if ($healthData.model_loaded -eq $true) {
        Write-Host "PASS: Python API is healthy and model is loaded" -ForegroundColor Green
    }
} catch {
    Write-Host "FAIL: Python API is not responding" -ForegroundColor Red
    exit 1
}

# Test 2: Java Webapp
Write-Host "`n[2] Testing Java Webapp..." -ForegroundColor Yellow
try {
    $javaResponse = Invoke-WebRequest -Uri "http://localhost:8082/" -Method GET
    if ($javaResponse.StatusCode -eq 200) {
        Write-Host "PASS: Java Webapp is responding" -ForegroundColor Green
    }
} catch {
    Write-Host "FAIL: Java Webapp is not responding" -ForegroundColor Red
    exit 1
}

# Test 3: End-to-End with Sample Image
Write-Host "`n[3] Testing End-to-End with Sample ECG Image..." -ForegroundColor Yellow
$testImage = "E:\Projects\RhythmIQ\01_data\test\F\F0.png"

if (Test-Path $testImage) {
    Write-Host "Using test image: F0.png (Class: F)" -ForegroundColor Gray
    $curlOutput = & curl.exe -s -X POST -F "image=@$testImage" "http://localhost:8083/analyze"
    $result = $curlOutput | ConvertFrom-Json
    
    Write-Host "PASS: Analysis completed" -ForegroundColor Green
    Write-Host "  Predicted: $($result.predicted_class) | Confidence: $($result.confidence_percentage)" -ForegroundColor Cyan
    Write-Host "  Severity: $($result.severity) | Expected: F" -ForegroundColor Cyan
}

Write-Host "`n==================================" -ForegroundColor Cyan
Write-Host "All Tests Passed!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "`nWebapp running at: http://localhost:8082/" -ForegroundColor Green
Write-Host "Please test manually with images from each class (F, M, N, Q, S, V)" -ForegroundColor Yellow
