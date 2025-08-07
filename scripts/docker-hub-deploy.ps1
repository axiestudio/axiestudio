# Axie Studio Docker Hub Deployment Script (PowerShell)
# This script builds and pushes Axie Studio Docker images to Docker Hub

param(
    [string]$DockerHubUsername = "axiestudio",
    [string]$ImageName = "axiestudio",
    [string]$AccessToken = "",
    [switch]$SkipLogin = $false,
    [switch]$BuildOnly = $false
)

# Get version from pyproject.toml
$Version = (Get-Content "pyproject.toml" | Select-String 'version = "(.+)"').Matches[0].Groups[1].Value
$Platforms = "linux/amd64,linux/arm64"

Write-Host "🚀 AXIE STUDIO DOCKER HUB DEPLOYMENT" -ForegroundColor Blue
Write-Host "====================================" -ForegroundColor Blue
Write-Host "Version: $Version" -ForegroundColor Yellow
Write-Host "Platforms: $Platforms" -ForegroundColor Yellow
Write-Host "Docker Hub: $DockerHubUsername/$ImageName" -ForegroundColor Yellow
Write-Host ""

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

# Login to Docker Hub if access token provided
if (-not $SkipLogin) {
    if ($AccessToken) {
        Write-Host "🔐 Logging into Docker Hub..." -ForegroundColor Blue
        echo $AccessToken | docker login --username $DockerHubUsername --password-stdin
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Failed to login to Docker Hub" -ForegroundColor Red
            exit 1
        }
        Write-Host "✅ Successfully logged into Docker Hub" -ForegroundColor Green
    } else {
        Write-Host "⚠️  No access token provided. Please login manually:" -ForegroundColor Yellow
        Write-Host "   docker login -u $DockerHubUsername" -ForegroundColor Cyan
        Write-Host "   Password: [Use your Docker Hub access token]" -ForegroundColor Cyan
        $continue = Read-Host "Continue? (y/N)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            exit 1
        }
    }
}

# Build frontend first
Write-Host "📦 Building frontend..." -ForegroundColor Blue
Set-Location "src/frontend"
npm ci
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend npm install failed" -ForegroundColor Red
    exit 1
}

npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend build failed" -ForegroundColor Red
    exit 1
}
Set-Location "../.."

# Copy frontend to backend
Write-Host "📋 Copying frontend to backend..." -ForegroundColor Blue
if (Test-Path "src/backend/base/axiestudio/frontend") {
    Remove-Item -Recurse -Force "src/backend/base/axiestudio/frontend"
}
Copy-Item -Recurse "src/frontend/build" "src/backend/base/axiestudio/frontend"

# Create and use buildx builder if it doesn't exist
$builderExists = docker buildx ls | Select-String "axiestudio-builder"
if (-not $builderExists) {
    Write-Host "🔧 Creating buildx builder..." -ForegroundColor Yellow
    docker buildx create --name axiestudio-builder --use
    docker buildx inspect --bootstrap
}

# Build and push main image
Write-Host "🐳 Building and pushing main image..." -ForegroundColor Blue
docker buildx build `
    --platform $Platforms `
    --file docker/build_and_push.Dockerfile `
    --tag "$DockerHubUsername/${ImageName}:$Version" `
    --tag "$DockerHubUsername/${ImageName}:latest" `
    $(if (-not $BuildOnly) { "--push" }) `
    .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Main image build failed" -ForegroundColor Red
    exit 1
}

# Build and push backend-only image
Write-Host "🔧 Building and pushing backend-only image..." -ForegroundColor Blue
docker buildx build `
    --platform $Platforms `
    --file docker/build_and_push_backend.Dockerfile `
    --build-arg AXIESTUDIO_IMAGE="$DockerHubUsername/${ImageName}:$Version" `
    --tag "$DockerHubUsername/${ImageName}-backend:$Version" `
    --tag "$DockerHubUsername/${ImageName}-backend:latest" `
    $(if (-not $BuildOnly) { "--push" }) `
    .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Backend image build failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Successfully deployed to Docker Hub!" -ForegroundColor Green
Write-Host "📦 Images available:" -ForegroundColor Green
Write-Host "   • $DockerHubUsername/${ImageName}:$Version"
Write-Host "   • $DockerHubUsername/${ImageName}:latest"
Write-Host "   • $DockerHubUsername/${ImageName}-backend:$Version"
Write-Host "   • $DockerHubUsername/${ImageName}-backend:latest"
Write-Host ""
Write-Host "🚀 To run the image:" -ForegroundColor Blue
Write-Host "   docker run -p 7860:7860 $DockerHubUsername/${ImageName}:latest"
Write-Host ""
Write-Host "📖 To use with docker-compose:" -ForegroundColor Blue
Write-Host "   docker-compose -f docker-compose.production.yml up"
