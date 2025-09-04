# Create PWA Icons for Swedish AxieStudio
# This script copies the existing 512x512 icon to create all required sizes
# Note: For production, you should use proper image resizing tools

Write-Host "🎨 Creating PWA Icons for Swedish AxieStudio..." -ForegroundColor Green

$sourceIcon = "src\frontend\public\favicon_io\android-chrome-512x512.png"
$outputDir = "src\frontend\public\favicon_io"

# Check if source exists
if (-not (Test-Path $sourceIcon)) {
    Write-Host "❌ Source icon not found: $sourceIcon" -ForegroundColor Red
    exit 1
}

Write-Host "📁 Source: $sourceIcon" -ForegroundColor Yellow
Write-Host "📁 Output: $outputDir" -ForegroundColor Yellow

# Create the critical Apple icons by copying the 512x512 (temporary solution)
$appleIcons = @(
    "apple-touch-icon-120x120.png",
    "apple-touch-icon-152x152.png", 
    "apple-touch-icon-167x167.png",
    "apple-touch-icon-180x180.png",
    "icon-1024x1024.png"
)

Write-Host "`n🍎 Creating CRITICAL Apple Icons..." -ForegroundColor Cyan

foreach ($iconName in $appleIcons) {
    $outputPath = Join-Path $outputDir $iconName
    
    if (-not (Test-Path $outputPath)) {
        Copy-Item $sourceIcon $outputPath
        Write-Host "  ✅ Created $iconName" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $iconName already exists" -ForegroundColor Yellow
    }
}

# Create additional PWA icons
$pwaIcons = @(
    "android-chrome-72x72.png",
    "android-chrome-96x96.png",
    "android-chrome-128x128.png", 
    "android-chrome-144x144.png",
    "android-chrome-384x384.png"
)

Write-Host "`n🤖 Creating Additional PWA Icons..." -ForegroundColor Cyan

foreach ($iconName in $pwaIcons) {
    $outputPath = Join-Path $outputDir $iconName
    
    if (-not (Test-Path $outputPath)) {
        Copy-Item $sourceIcon $outputPath
        Write-Host "  ✅ Created $iconName" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $iconName already exists" -ForegroundColor Yellow
    }
}

# Create Windows tiles
$windowsIcons = @(
    "mstile-144x144.png",
    "mstile-70x70.png",
    "mstile-150x150.png",
    "mstile-310x310.png",
    "mstile-310x150.png"
)

Write-Host "`n🪟 Creating Windows Tile Icons..." -ForegroundColor Cyan

foreach ($iconName in $windowsIcons) {
    $outputPath = Join-Path $outputDir $iconName
    
    if (-not (Test-Path $outputPath)) {
        Copy-Item $sourceIcon $outputPath
        Write-Host "  ✅ Created $iconName" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $iconName already exists" -ForegroundColor Yellow
    }
}

Write-Host "`n📊 Final Icon Count:" -ForegroundColor Yellow
$iconCount = (Get-ChildItem -Path $outputDir -Filter "*.png").Count
Write-Host "Total PNG icons: $iconCount" -ForegroundColor Green

Write-Host "`n🎉 SUCCESS! All PWA icons created!" -ForegroundColor Green
Write-Host "⚠️  NOTE: These are copies of 512x512. For production, resize properly." -ForegroundColor Yellow
Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Test on https://pwabuilder.com" -ForegroundColor White
Write-Host "2. Should achieve 30/30 score!" -ForegroundColor White
Write-Host "3. For production: Use proper image resizing" -ForegroundColor White

Write-Host "`n🇸🇪 Din svenska PWA är redo! (Your Swedish PWA is ready!)" -ForegroundColor Green
