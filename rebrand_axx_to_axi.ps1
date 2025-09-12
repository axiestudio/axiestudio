# AXX to AXI Rebranding Script
Write-Host "Starting AXX to AXI Rebranding Process..." -ForegroundColor Green

$rootPath = "C:\Users\mist24lk\Downloads\aaa\axiestudio\axx"
$processedFiles = 0

# Get all files recursively (Python, TOML, Markdown, Makefile, etc.)
$allFiles = Get-ChildItem -Path $rootPath -Recurse -Include "*.py", "*.toml", "*.md", "Makefile", "*.txt", "*.yml", "*.yaml"
$totalFiles = $allFiles.Count

Write-Host "Found $totalFiles files to process" -ForegroundColor Yellow

foreach ($file in $allFiles) {
    $processedFiles++
    
    if ($processedFiles % 25 -eq 0) {
        Write-Host "Processing file $processedFiles of $totalFiles..." -ForegroundColor Cyan
    }
    
    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        $originalContent = $content
        
        # Replace import statements and module references
        $content = $content -replace 'from axx\.', 'from axi.'
        $content = $content -replace 'import axx\.', 'import axi.'
        $content = $content -replace 'from axx ', 'from axi '
        $content = $content -replace 'import axx ', 'import axi '
        $content = $content -replace '"axx"', '"axi"'
        $content = $content -replace "'axx'", "'axi'"
        
        # Replace CLI command references
        $content = $content -replace 'axx --', 'axi --'
        $content = $content -replace 'axx serve', 'axi serve'
        $content = $content -replace 'axx run', 'axi run'
        $content = $content -replace 'AXX serve', 'AXI serve'
        $content = $content -replace 'AXX --', 'AXI --'
        
        # Replace project names and descriptions
        $content = $content -replace 'AXX', 'AXI'
        $content = $content -replace 'axx', 'axi'
        $content = $content -replace 'AxieStudio Executor', 'AxieStudio Executor'  # Keep this the same
        
        # Replace package names in pyproject.toml
        $content = $content -replace 'name = "axx"', 'name = "axi"'
        $content = $content -replace '\[project\.scripts\]\s*axx', '[project.scripts]`naxi'
        
        # Replace directory references
        $content = $content -replace 'src/axx/', 'src/axi/'
        $content = $content -replace 'src\\axx\\', 'src\axi\'
        
        # Only write if content changed
        if ($content -ne $originalContent) {
            Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
        }
        
    } catch {
        Write-Host "Error processing $($file.FullName): $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "Rebranding completed! Processed $processedFiles files." -ForegroundColor Green
Write-Host "Next step: Rename directory from 'axx' to 'axi'" -ForegroundColor Yellow
