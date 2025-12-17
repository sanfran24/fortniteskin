# PowerShell script to build and zip frontend for Namecheap upload
# Run this from the project root directory

Write-Host "🚀 Building frontend for production..." -ForegroundColor Green

# Check if backend URL is set
$backendUrl = $env:VITE_API_URL
if (-not $backendUrl) {
    Write-Host "⚠️  VITE_API_URL not set. Using default Render URL..." -ForegroundColor Yellow
    $env:VITE_API_URL = "https://nano-banana-ta-backend.onrender.com"
}

Write-Host "📦 Backend URL: $env:VITE_API_URL" -ForegroundColor Cyan

# Navigate to frontend directory
Set-Location frontend

# Install dependencies if needed
if (-not (Test-Path "node_modules")) {
    Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Build the frontend
Write-Host "🔨 Building production bundle..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    Set-Location ..
    exit 1
}

# Go back to root
Set-Location ..

# Check if dist folder exists
if (-not (Test-Path "frontend/dist")) {
    Write-Host "❌ Build output not found!" -ForegroundColor Red
    exit 1
}

# Create zip file
$zipPath = "frontend-build.zip"
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
    Write-Host "🗑️  Removed existing zip file" -ForegroundColor Yellow
}

Write-Host "📦 Creating zip file..." -ForegroundColor Yellow
Compress-Archive -Path frontend\dist\* -DestinationPath $zipPath -Force

if (Test-Path $zipPath) {
    $zipSize = (Get-Item $zipPath).Length / 1MB
    Write-Host "✅ Build complete!" -ForegroundColor Green
    Write-Host "📁 Zip file created: $zipPath ($([math]::Round($zipSize, 2)) MB)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📤 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Upload $zipPath to Namecheap cPanel File Manager" -ForegroundColor White
    Write-Host "   2. Extract it in public_html folder" -ForegroundColor White
    Write-Host "   3. Make sure index.html is in public_html root" -ForegroundColor White
    Write-Host "   4. Update backend CORS to allow your domain" -ForegroundColor White
} else {
    Write-Host "❌ Failed to create zip file!" -ForegroundColor Red
    exit 1
}

