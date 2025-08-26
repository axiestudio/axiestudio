# AxieStudio Frontend Runner with Swedish Translations
Write-Host "Starting AxieStudio Frontend with Swedish translations..." -ForegroundColor Green
Write-Host ""

# Set the path to your Node.js binary
$NodePath = "C:\Users\mist24lk\Downloads\node-v22.18.0-win-x64\node.exe"

# Check if Node.js exists
if (-not (Test-Path $NodePath)) {
    Write-Host "Error: Node.js not found at $NodePath" -ForegroundColor Red
    Write-Host "Please check the path and try again." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Display Node.js version
Write-Host "Using Node.js from: $NodePath" -ForegroundColor Cyan
& $NodePath --version
Write-Host ""

# Set environment variables for the frontend
$env:VITE_PROXY_TARGET = "https://flow.axiestudio.se"
$env:VITE_PORT = "3000"

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "- Frontend Port: $($env:VITE_PORT)" -ForegroundColor White
Write-Host "- Backend Proxy: $($env:VITE_PROXY_TARGET)" -ForegroundColor White
Write-Host ""

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    & $NodePath npm install
    Write-Host ""
}

Write-Host "Starting development server..." -ForegroundColor Green
Write-Host ""
Write-Host "The app will be available at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the development server
& $NodePath npm run start
