# Simple LFX to AXX Rebranding Script
Write-Host "Starting LFX to AXX Rebranding Process..." -ForegroundColor Green

$rootPath = "C:\Users\mist24lk\Downloads\aaa\axiestudio\lfx\src\axx"
$processedFiles = 0

# Get all Python files recursively
$pythonFiles = Get-ChildItem -Path $rootPath -Recurse -Include "*.py"
$totalFiles = $pythonFiles.Count

Write-Host "Found $totalFiles Python files to process" -ForegroundColor Yellow

foreach ($file in $pythonFiles) {
    $processedFiles++
    $relativePath = $file.FullName.Replace($rootPath, "").TrimStart('\')
    
    if ($processedFiles % 50 -eq 0) {
        Write-Host "Processing file $processedFiles of $totalFiles..." -ForegroundColor Cyan
    }
    
    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        $originalContent = $content
        
        # Replace import statements
        $content = $content -replace 'from lfx\.', 'from axx.'
        $content = $content -replace 'import lfx\.', 'import axx.'
        $content = $content -replace 'from lfx ', 'from axx '
        $content = $content -replace 'import lfx ', 'import axx '
        
        # Replace environment variables
        $content = $content -replace 'LANGFLOW_', 'AXIESTUDIO_'
        $content = $content -replace '"langflow"', '"axiestudio"'
        $content = $content -replace "'langflow'", "'axiestudio'"
        
        # Replace documentation strings
        $content = $content -replace 'Langflow', 'AxieStudio'
        $content = $content -replace 'LFX', 'AXX'
        
        # Only write if content changed
        if ($content -ne $originalContent) {
            Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
        }
        
    } catch {
        Write-Host "❌ Error processing $($file.FullName): $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "Rebranding completed! Processed $processedFiles files." -ForegroundColor Green
