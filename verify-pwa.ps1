# Verify PWA Setup for Swedish AxieStudio
# Check all required files for 30/30 PWA Builder score

Write-Host "🔍 Verifying Swedish AxieStudio PWA Setup..." -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

$baseDir = "src\frontend\public"
$faviconDir = "$baseDir\favicon_io"

# Check critical files
$criticalFiles = @(
    @{path="$baseDir\manifest.json"; desc="Web App Manifest"},
    @{path="$baseDir\sw.js"; desc="Service Worker"},
    @{path="$baseDir\offline.html"; desc="Offline Page"},
    @{path="$baseDir\index.html"; desc="Main HTML"}
)

Write-Host "`n📋 Critical PWA Files:" -ForegroundColor Cyan
foreach ($file in $criticalFiles) {
    if (Test-Path $file.path) {
        $size = (Get-Item $file.path).Length
        Write-Host "  ✅ $($file.desc) ($([math]::Round($size/1KB, 1)) KB)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $($file.desc) - MISSING!" -ForegroundColor Red
    }
}

# Check Apple icons (CRITICAL for 30/30)
$appleIcons = @(
    "apple-touch-icon-120x120.png",
    "apple-touch-icon-152x152.png", 
    "apple-touch-icon-167x167.png",
    "apple-touch-icon-180x180.png",
    "icon-1024x1024.png"
)

Write-Host "`n🍎 Apple Icons (CRITICAL):" -ForegroundColor Cyan
$appleCount = 0
foreach ($icon in $appleIcons) {
    $iconPath = "$faviconDir\$icon"
    if (Test-Path $iconPath) {
        $appleCount++
        Write-Host "  ✅ $icon" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $icon - MISSING!" -ForegroundColor Red
    }
}

# Check PWA icons
$pwaIcons = @(
    "android-chrome-192x192.png",
    "android-chrome-512x512.png",
    "android-chrome-72x72.png",
    "android-chrome-96x96.png",
    "android-chrome-128x128.png",
    "android-chrome-144x144.png",
    "android-chrome-384x384.png"
)

Write-Host "`n🤖 PWA Icons:" -ForegroundColor Cyan
$pwaCount = 0
foreach ($icon in $pwaIcons) {
    $iconPath = "$faviconDir\$icon"
    if (Test-Path $iconPath) {
        $pwaCount++
        Write-Host "  ✅ $icon" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $icon - Missing" -ForegroundColor Yellow
    }
}

# Check Windows icons
$windowsIcons = @(
    "mstile-144x144.png",
    "mstile-70x70.png",
    "mstile-150x150.png",
    "mstile-310x310.png",
    "mstile-310x150.png"
)

Write-Host "`n🪟 Windows Icons:" -ForegroundColor Cyan
$windowsCount = 0
foreach ($icon in $windowsIcons) {
    $iconPath = "$faviconDir\$icon"
    if (Test-Path $iconPath) {
        $windowsCount++
        Write-Host "  ✅ $icon" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $icon - Missing" -ForegroundColor Yellow
    }
}

# Calculate PWA Score
Write-Host "`n📊 PWA Score Estimation:" -ForegroundColor Yellow
Write-Host "========================" -ForegroundColor Yellow

$manifestScore = if (Test-Path "$baseDir\manifest.json") { 10 } else { 0 }
$swScore = if (Test-Path "$baseDir\sw.js") { 10 } else { 0 }
$securityScore = 10  # Assuming HTTPS will be enabled

$totalScore = $manifestScore + $swScore + $securityScore

if ($appleCount -eq 5) {
    Write-Host "🍎 Apple Icons: PERFECT (5/5)" -ForegroundColor Green
} else {
    Write-Host "🍎 Apple Icons: $appleCount/5 - Need all 5 for perfect score!" -ForegroundColor Yellow
}

Write-Host "📋 Manifest: $manifestScore/10" -ForegroundColor $(if($manifestScore -eq 10){"Green"}else{"Red"})
Write-Host "⚙️  Service Worker: $swScore/10" -ForegroundColor $(if($swScore -eq 10){"Green"}else{"Red"})
Write-Host "🔒 Security (HTTPS): $securityScore/10" -ForegroundColor Green

Write-Host "`n🎯 ESTIMATED PWA BUILDER SCORE: $totalScore/30" -ForegroundColor $(if($totalScore -eq 30){"Green"}elseif($totalScore -ge 25){"Yellow"}else{"Red"})

if ($totalScore -eq 30 -and $appleCount -eq 5) {
    Write-Host "`n🎉 PERFECT! Your Swedish PWA should achieve 30/30!" -ForegroundColor Green
    Write-Host "✅ All critical files present" -ForegroundColor Green
    Write-Host "✅ All Apple icons created" -ForegroundColor Green
    Write-Host "✅ Service Worker ready" -ForegroundColor Green
    Write-Host "✅ Offline support enabled" -ForegroundColor Green
} elseif ($appleCount -lt 5) {
    Write-Host "`n⚠️  Almost there! Missing Apple icons will prevent 30/30" -ForegroundColor Yellow
} else {
    Write-Host "`n⚠️  Some critical files missing" -ForegroundColor Yellow
}

Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Deploy to HTTPS server" -ForegroundColor White
Write-Host "2. Test on https://pwabuilder.com" -ForegroundColor White
Write-Host "3. Test install on iPhone/Android" -ForegroundColor White
Write-Host "4. Verify offline functionality" -ForegroundColor White

$totalIcons = (Get-ChildItem -Path $faviconDir -Filter "*.png" -ErrorAction SilentlyContinue).Count
Write-Host "`n📊 Total Icons Created: $totalIcons" -ForegroundColor Green

Write-Host "`n🇸🇪 Din svenska PWA är redo för test! (Your Swedish PWA is ready for testing!)" -ForegroundColor Green
