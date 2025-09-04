@echo off
REM AxieStudio Tauri Development Script for Windows
REM This script helps with local Tauri development and testing

setlocal enabledelayedexpansion

REM Check if we're in the right directory
if not exist "src-tauri\tauri.conf.json" (
    echo [ERROR] Please run this script from the axiestudio directory
    exit /b 1
)

REM Function to check prerequisites
:check_prerequisites
echo [INFO] Checking prerequisites...

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js first.
    exit /b 1
)

REM Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed. Please install npm first.
    exit /b 1
)

REM Check Rust
rustc --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Rust is not installed. Please install Rust first.
    echo [INFO] Visit: https://rustup.rs/
    exit /b 1
)

REM Check Tauri CLI
tauri --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Tauri CLI is not installed. Installing...
    npm install -g @tauri-apps/cli
)

echo [SUCCESS] All prerequisites are installed!
goto :eof

REM Function to install dependencies
:install_dependencies
echo [INFO] Installing dependencies...

REM Install frontend dependencies
echo [INFO] Installing frontend dependencies...
cd src\frontend
if exist "package-lock.json" (
    npm ci
) else (
    npm install
)
cd ..\..

echo [SUCCESS] Dependencies installed!
goto :eof

REM Function to create placeholder icons
:create_placeholder_icons
echo [INFO] Creating placeholder icons...

if not exist "src-tauri\icons" mkdir src-tauri\icons

REM Create empty placeholder files
echo. > src-tauri\icons\32x32.png
echo. > src-tauri\icons\128x128.png
echo. > src-tauri\icons\128x128@2x.png
echo. > src-tauri\icons\icon.ico
echo. > src-tauri\icons\icon.icns

echo [WARNING] Created empty placeholder icons
echo [INFO] Please replace with actual icons before building for production
goto :eof

REM Function to run development server
:run_dev
echo [INFO] Starting Tauri development server...
echo [INFO] This will start both the frontend dev server and Tauri app

REM Build frontend first
echo [INFO] Building frontend...
cd src\frontend
npm run build
cd ..\..

REM Start Tauri dev
tauri dev
goto :eof

REM Function to build the application
:build_app
echo [INFO] Building Tauri application...

REM Build frontend
echo [INFO] Building frontend...
cd src\frontend
npm run build
cd ..\..

REM Build Tauri app
echo [INFO] Building Tauri app (this may take a while)...
tauri build

echo [SUCCESS] Build completed! Check src-tauri\target\release\bundle\ for output files
goto :eof

REM Function to run tests
:run_tests
echo [INFO] Running tests...

REM Frontend tests
echo [INFO] Running frontend tests...
cd src\frontend
npm run test 2>nul
if errorlevel 1 (
    echo [WARNING] Frontend tests failed or not configured
) else (
    echo [SUCCESS] Frontend tests passed!
)
cd ..\..

REM Rust tests
echo [INFO] Running Rust tests...
cd src-tauri
cargo test
if errorlevel 1 (
    echo [WARNING] Rust tests failed
) else (
    echo [SUCCESS] Rust tests passed!
)
cd ..
goto :eof

REM Function to clean build artifacts
:clean
echo [INFO] Cleaning build artifacts...

REM Clean frontend
if exist "src\frontend\build" rmdir /s /q src\frontend\build
if exist "src\frontend\node_modules\.cache" rmdir /s /q src\frontend\node_modules\.cache

REM Clean Rust
cd src-tauri
cargo clean
cd ..

echo [SUCCESS] Cleaned build artifacts!
goto :eof

REM Main script logic
if "%1"=="check" (
    call :check_prerequisites
) else if "%1"=="install" (
    call :check_prerequisites
    call :install_dependencies
    call :create_placeholder_icons
) else if "%1"=="dev" (
    call :check_prerequisites
    call :run_dev
) else if "%1"=="build" (
    call :check_prerequisites
    call :build_app
) else if "%1"=="test" (
    call :check_prerequisites
    call :run_tests
) else if "%1"=="clean" (
    call :clean
) else if "%1"=="setup" (
    call :check_prerequisites
    call :install_dependencies
    call :create_placeholder_icons
    echo [SUCCESS] Setup complete! Run 'scripts\dev-tauri.bat dev' to start development
) else (
    echo AxieStudio Tauri Development Script for Windows
    echo.
    echo Usage: %0 [command]
    echo.
    echo Commands:
    echo   setup   - Complete setup (check, install, icons)
    echo   check   - Check prerequisites
    echo   install - Install dependencies
    echo   dev     - Start development server
    echo   build   - Build the application
    echo   test    - Run tests
    echo   clean   - Clean build artifacts
    echo   help    - Show this help message
    echo.
    echo Examples:
    echo   %0 setup   # First time setup
    echo   %0 dev     # Start development
    echo   %0 build   # Build for production
)
