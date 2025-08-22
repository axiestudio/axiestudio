# Simple PowerShell HTTP Server for testing
$port = 8000
$url = "http://localhost:$port/"

Write-Host "🚀 Starting PowerShell HTTP Server on port $port" -ForegroundColor Green
Write-Host "📁 Serving files from: $(Get-Location)" -ForegroundColor Cyan
Write-Host "🎯 Test showcase at: $url" -ForegroundColor Yellow
Write-Host "📊 Store index at: ${url}src/frontend/public/store_components_converted/store_index.json" -ForegroundColor Yellow

# Create HTTP listener
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($url)
$listener.Start()

Write-Host "✅ Server ready! Press Ctrl+C to stop." -ForegroundColor Green

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        # Add CORS headers
        $response.Headers.Add("Access-Control-Allow-Origin", "*")
        $response.Headers.Add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        $response.Headers.Add("Access-Control-Allow-Headers", "Content-Type")
        
        $requestUrl = $request.Url.LocalPath
        Write-Host "📥 Request: $requestUrl" -ForegroundColor Gray
        
        # Handle OPTIONS requests
        if ($request.HttpMethod -eq "OPTIONS") {
            $response.StatusCode = 200
            $response.Close()
            continue
        }
        
        # Determine file path
        $filePath = if ($requestUrl -eq "/") { ".\test_showcase.html" } else { ".$requestUrl" }
        
        if (Test-Path $filePath) {
            $content = Get-Content $filePath -Raw -Encoding UTF8
            $extension = [System.IO.Path]::GetExtension($filePath).ToLower()
            
            # Set content type
            switch ($extension) {
                ".html" { $response.ContentType = "text/html; charset=utf-8" }
                ".js" { $response.ContentType = "text/javascript; charset=utf-8" }
                ".css" { $response.ContentType = "text/css; charset=utf-8" }
                ".json" { $response.ContentType = "application/json; charset=utf-8" }
                default { $response.ContentType = "text/plain; charset=utf-8" }
            }
            
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($content)
            $response.ContentLength64 = $buffer.Length
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
            $response.StatusCode = 200
            Write-Host "✅ Served: $filePath" -ForegroundColor Green
        } else {
            $response.StatusCode = 404
            $errorContent = "<h1>404 Not Found</h1><p>File not found: $requestUrl</p>"
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($errorContent)
            $response.ContentLength64 = $buffer.Length
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
            Write-Host "❌ Not found: $filePath" -ForegroundColor Red
        }
        
        $response.Close()
    }
} catch {
    Write-Host "❌ Server error: $_" -ForegroundColor Red
} finally {
    $listener.Stop()
    Write-Host "🛑 Server stopped." -ForegroundColor Yellow
}
