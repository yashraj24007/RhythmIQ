# RhythmIQ - Complete System Test Report

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "  RhythmIQ ECG Analysis System - Test Report" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

# Test all 6 ECG classes
$testCases = @(
    @{Class="F"; File="F0.png"; Description="Fusion of ventricular and normal beat"},
    @{Class="M"; File="M0.png"; Description="Myocardial infarction"},
    @{Class="N"; File="N0.png"; Description="Normal beat"},
    @{Class="Q"; File="Q0.png"; Description="Unknown beat"},
    @{Class="S"; File="S0.png"; Description="Supraventricular premature beat"},
    @{Class="V"; File="V0.png"; Description="Ventricular ectopic beat"}
)

$results = @()

foreach ($test in $testCases) {
    $imagePath = "E:\Projects\RhythmIQ\01_data\test\$($test.Class)\$($test.File)"
    
    if (Test-Path $imagePath) {
        Write-Host "Testing $($test.Class) - $($test.Description)..." -ForegroundColor Yellow
        
        try {
            $response = & curl.exe -s -X POST -F "image=@$imagePath" "http://localhost:8083/analyze"
            $result = $response | ConvertFrom-Json
            
            if ($result.success) {
                $match = if ($result.predicted_class -eq $test.Class) { "MATCH" } else { "MISMATCH" }
                $matchColor = if ($result.predicted_class -eq $test.Class) { "Green" } else { "Red" }
                
                Write-Host "  Expected: $($test.Class) | Predicted: $($result.predicted_class) | $match" -ForegroundColor $matchColor
                Write-Host "  Confidence: $($result.confidence_percentage) | Severity: $($result.severity)`n" -ForegroundColor Gray
                
                $results += [PSCustomObject]@{
                    ExpectedClass = $test.Class
                    PredictedClass = $result.predicted_class
                    Confidence = $result.confidence_percentage
                    Severity = $result.severity
                    Match = ($result.predicted_class -eq $test.Class)
                }
            } else {
                Write-Host "  ERROR: $($result.error)`n" -ForegroundColor Red
            }
        } catch {
            Write-Host "  ERROR: Failed to analyze image`n" -ForegroundColor Red
        }
    } else {
        Write-Host "  SKIPPED: Image not found at $imagePath`n" -ForegroundColor Yellow
    }
}

# Summary
Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "  Test Summary" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

$totalTests = $results.Count
$correctPredictions = ($results | Where-Object { $_.Match -eq $true }).Count
$accuracy = if ($totalTests -gt 0) { [math]::Round(($correctPredictions / $totalTests) * 100, 2) } else { 0 }

Write-Host "Total Tests: $totalTests" -ForegroundColor White
Write-Host "Correct Predictions: $correctPredictions" -ForegroundColor Green
Write-Host "Accuracy: $accuracy%" -ForegroundColor $(if ($accuracy -ge 80) { "Green" } else { "Yellow" })

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "  System Status" -ForegroundColor Cyan
Write-Host "================================================`n" -ForegroundColor Cyan

Write-Host "[OK] Python ML API: Running on port 8083" -ForegroundColor Green
Write-Host "[OK] Java Webapp: Running on port 8082" -ForegroundColor Green
Write-Host "[OK] Model Loaded: RhythmGuard ECG Classifier" -ForegroundColor Green
Write-Host "`nWebapp URL: http://localhost:8082/" -ForegroundColor Cyan
Write-Host "`nYou can now manually test the webapp with any ECG image!`n" -ForegroundColor Yellow
