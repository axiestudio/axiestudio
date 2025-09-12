# AxieStudio LFX to AXX Rebranding Script
# This script systematically replaces all LFX/Langflow references with AXX/AxieStudio

Write-Host "🚀 Starting LFX to AXX Rebranding Process..." -ForegroundColor Green

$rootPath = "C:\Users\mist24lk\Downloads\aaa\axiestudio\lfx\src\axx"
$totalFiles = 0
$processedFiles = 0

# Get all Python files recursively
$pythonFiles = Get-ChildItem -Path $rootPath -Recurse -Include "*.py" | Where-Object { $_.FullName -notlike "*__pycache__*" }
$totalFiles = $pythonFiles.Count

Write-Host "📁 Found $totalFiles Python files to process" -ForegroundColor Yellow

foreach ($file in $pythonFiles) {
    $processedFiles++
    $relativePath = $file.FullName.Replace($rootPath, "").TrimStart('\')
    Write-Progress -Activity "Rebranding Files" -Status "Processing: $relativePath" -PercentComplete (($processedFiles / $totalFiles) * 100)
    
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
        $content = $content -replace 'langflow', 'axiestudio'
        $content = $content -replace 'LFX', 'AXX'
        $content = $content -replace 'lfx', 'axx'
        
        # Replace specific patterns
        $content = $content -replace 'lfx\.components', 'axx.components'
        $content = $content -replace 'lfx\.base', 'axx.base'
        $content = $content -replace 'lfx\.custom', 'axx.custom'
        $content = $content -replace 'lfx\.graph', 'axx.graph'
        $content = $content -replace 'lfx\.schema', 'axx.schema'
        $content = $content -replace 'lfx\.utils', 'axx.utils'
        $content = $content -replace 'lfx\.services', 'axx.services'
        $content = $content -replace 'lfx\.template', 'axx.template'
        $content = $content -replace 'lfx\.field_typing', 'axx.field_typing'
        $content = $content -replace 'lfx\.inputs', 'axx.inputs'
        $content = $content -replace 'lfx\.io', 'axx.io'
        $content = $content -replace 'lfx\.log', 'axx.log'
        $content = $content -replace 'lfx\.memory', 'axx.memory'
        $content = $content -replace 'lfx\.processing', 'axx.processing'
        $content = $content -replace 'lfx\.serialization', 'axx.serialization'
        $content = $content -replace 'lfx\.load', 'axx.load'
        $content = $content -replace 'lfx\.helpers', 'axx.helpers'
        $content = $content -replace 'lfx\.interface', 'axx.interface'
        $content = $content -replace 'lfx\.events', 'axx.events'
        $content = $content -replace 'lfx\.exceptions', 'axx.exceptions'
        $content = $content -replace 'lfx\.cli', 'axx.cli'
        $content = $content -replace 'lfx\.type_extraction', 'axx.type_extraction'
        
        # Only write if content changed
        if ($content -ne $originalContent) {
            Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
            Write-Host "✅ Updated: $relativePath" -ForegroundColor Green
        }
        
    } catch {
        Write-Host "❌ Error processing $($file.FullName): $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "🎉 Rebranding completed! Processed $processedFiles files." -ForegroundColor Green
Write-Host "📋 Summary:" -ForegroundColor Cyan
Write-Host "   - Total files processed: $processedFiles" -ForegroundColor White
Write-Host "   - All 'lfx' imports changed to 'axx'" -ForegroundColor White
Write-Host "   - All 'LANGFLOW_' env vars changed to 'AXIESTUDIO_'" -ForegroundColor White
Write-Host "   - All documentation updated" -ForegroundColor White
