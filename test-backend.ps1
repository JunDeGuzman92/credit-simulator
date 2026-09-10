# Test backend connection
# Run this after starting the backend server

Write-Host "Testing backend connection..." -ForegroundColor Green

try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get
    Write-Host "✅ Backend is running!" -ForegroundColor Green
    Write-Host "Status: $($response.status)" -ForegroundColor Cyan
    Write-Host "Model loaded: $($response.model_loaded)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Backend connection failed" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure the backend is running:" -ForegroundColor Yellow
    Write-Host '  & "C:\Users\junbu\Documents\credit-simulator\.venv\Scripts\python.exe" -m uvicorn backend.api:app --reload --host 127.0.0.1 --port 8000' -ForegroundColor Gray
}

Write-Host ""
Write-Host "Testing prediction endpoint..." -ForegroundColor Green

$sampleData = @{
    checking_status = "0-to-200"
    duration_months = 24
    credit_history = "existing-paid"
    purpose = "radio-tv"
    credit_amount = 3500.0
    savings = "100-to-500"
    employment = "1-to-4"
    installment_rate = 2
    personal_status = "male-single"
    other_debtors = "none"
    residence_years = 3
    property = "real-estate"
    age = 32
    other_installment_plans = "none"
    housing = "own"
    existing_credits = 1
    job = "skilled-employee"
    dependents = 1
    telephone = "yes"
    foreign_worker = "yes"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" -Method Post -Body $sampleData -ContentType "application/json"
    Write-Host "✅ Prediction successful!" -ForegroundColor Green
    Write-Host "Prediction: $($response.prediction)" -ForegroundColor Cyan
    Write-Host "Simulated Score: $($response.simulated_credit_score)" -ForegroundColor Cyan
    Write-Host "Good Credit %: $($response.probabilities.good_credit)%" -ForegroundColor Cyan
    Write-Host "High Risk %: $($response.probabilities.bad_credit)%" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Prediction failed" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Response: $($_.ErrorDetails.Message)" -ForegroundColor Red
}