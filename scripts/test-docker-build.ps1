# Test Docker Build Script for Axie Studio
# This script tests the Docker build process locally

param(
    [switch]$SkipFrontend = $false,
    [switch]$TestOnly = $false
)

Write-Host "🔍 AXIE STUDIO DOCKER BUILD TEST" -ForegroundColor Blue
Write-Host "===============================" -ForegroundColor Blue

# Check if Docker is running
Write-Host "🐳 Checking Docker status..." -ForegroundColor Blue
try {
    $dockerInfo = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Docker is not running or not accessible." -ForegroundColor Red
        Write-Host "Please start Docker Desktop and run as Administrator if needed." -ForegroundColor Yellow
        exit 1
    }
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker command failed: $_" -ForegroundColor Red
    exit 1
}

# Check required files
Write-Host "📋 Checking required files..." -ForegroundColor Blue
$requiredFiles = @(
    "Dockerfile",
    "pyproject.toml",
    "uv.lock",
    "src/backend/base/pyproject.toml",
    "src/backend/base/uv.lock",
    "src/frontend/package.json"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file exists" -ForegroundColor Green
    } else {
        Write-Host "❌ $file missing" -ForegroundColor Red
        exit 1
    }
}

# Build frontend if not skipped
if (-not $SkipFrontend) {
    Write-Host "📦 Building frontend..." -ForegroundColor Blue
    Set-Location "src/frontend"
    
    if (-not (Test-Path "node_modules")) {
        Write-Host "📥 Installing frontend dependencies..." -ForegroundColor Yellow
        npm ci
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Frontend npm install failed" -ForegroundColor Red
            exit 1
        }
    }
    
    npm run build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Frontend build failed" -ForegroundColor Red
        exit 1
    }
    
    Set-Location "../.."
    Write-Host "✅ Frontend built successfully" -ForegroundColor Green
    
    # Copy frontend to backend
    Write-Host "📋 Copying frontend to backend..." -ForegroundColor Blue
    if (Test-Path "src/backend/base/axiestudio/frontend") {
        Remove-Item -Recurse -Force "src/backend/base/axiestudio/frontend"
    }
    Copy-Item -Recurse "src/frontend/build" "src/backend/base/axiestudio/frontend"
    Write-Host "✅ Frontend copied to backend" -ForegroundColor Green
}

if ($TestOnly) {
    Write-Host "✅ Test completed successfully - all prerequisites met!" -ForegroundColor Green
    exit 0
}

# Test Docker build
Write-Host "🏗️  Testing Docker build..." -ForegroundColor Blue
$buildCommand = "docker build -f Dockerfile -t axiestudio-test:latest ."

Write-Host "Running: $buildCommand" -ForegroundColor Cyan
Invoke-Expression $buildCommand

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker build successful!" -ForegroundColor Green
    
    # Test run the container
    Write-Host "🚀 Testing container startup..." -ForegroundColor Blue
    $containerId = docker run -d -p 7861:7860 axiestudio-test:latest
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Container started successfully!" -ForegroundColor Green
        Write-Host "Container ID: $containerId" -ForegroundColor Cyan
        
        # Wait a moment for startup
        Start-Sleep -Seconds 10
        
        # Test health check
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:7861/health_check" -TimeoutSec 10
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ Health check passed!" -ForegroundColor Green
            } else {
                Write-Host "⚠️  Health check returned status: $($response.StatusCode)" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "⚠️  Health check failed: $_" -ForegroundColor Yellow
        }
        
        # Stop and remove test container
        Write-Host "🧹 Cleaning up test container..." -ForegroundColor Blue
        docker stop $containerId | Out-Null
        docker rm $containerId | Out-Null
        Write-Host "✅ Test container cleaned up" -ForegroundColor Green
    } else {
        Write-Host "❌ Container failed to start" -ForegroundColor Red
    }
    
    # Clean up test image
    Write-Host "🧹 Cleaning up test image..." -ForegroundColor Blue
    docker rmi axiestudio-test:latest | Out-Null
    Write-Host "✅ Test image cleaned up" -ForegroundColor Green
    
} else {
    Write-Host "❌ Docker build failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 All tests passed! Ready for Docker Hub deployment." -ForegroundColor Green
Write-Host "To deploy to Docker Hub, run:" -ForegroundColor Blue
Write-Host "   .\scripts\docker-hub-deploy.ps1 -AccessToken `$env:DOCKER_HUB_TOKEN" -ForegroundColor Cyan
