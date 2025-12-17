# PowerShell setup script for Windows

Write-Host "🍌 Setting up Nano Banana TA Tool..." -ForegroundColor Cyan

# Backend setup
Write-Host "📦 Installing backend dependencies..." -ForegroundColor Yellow
Set-Location backend

# Create virtual environment
python -m venv venv
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create .env if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  Please edit backend/.env and add your GOOGLE_API_KEY" -ForegroundColor Red
}

Set-Location ..

# Frontend setup
Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
Set-Location frontend
npm install

Set-Location ..

Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Cyan
Write-Host "1. Backend: cd backend && python main.py"
Write-Host "2. Frontend: cd frontend && npm run dev"
Write-Host ""
Write-Host "Don't forget to add your GOOGLE_API_KEY to backend/.env" -ForegroundColor Yellow

