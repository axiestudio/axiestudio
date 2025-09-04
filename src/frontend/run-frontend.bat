@echo off
echo Starting AxieStudio Frontend with Swedish translations...
echo.

REM Set the path to your Node.js binary
set NODE_PATH=C:\Users\mist24lk\Downloads\node-v22.18.0-win-x64\node-v22.18.0-win-x64\node.exe
set NPM_PATH=C:\Users\mist24lk\Downloads\node-v22.18.0-win-x64\node-v22.18.0-win-x64\node_modules\npm\bin\npm-cli.js

REM Check if Node.js exists
if not exist "%NODE_PATH%" (
    echo Error: Node.js not found at %NODE_PATH%
    echo Please check the path and try again.
    pause
    exit /b 1
)

REM Display Node.js version
echo Using Node.js from: %NODE_PATH%
"%NODE_PATH%" --version
echo.

REM Set environment variables for the frontend
set VITE_PROXY_TARGET=https://flow.axiestudio.se
set VITE_PORT=3000

echo Configuration:
echo - Frontend Port: %VITE_PORT%
echo - Backend Proxy: %VITE_PROXY_TARGET%
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    "%NODE_PATH%" "%NPM_PATH%" install
    echo.
)

echo Starting development server...
echo.
echo The app will be available at: http://localhost:3000
echo Press Ctrl+C to stop the server
echo.

REM Start the development server
"%NODE_PATH%" "%NPM_PATH%" run start

pause
