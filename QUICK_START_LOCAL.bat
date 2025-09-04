@echo off
echo 🚀 Axie Studio - Complete Local Development Setup
echo ================================================
echo.
echo This will install and run Axie Studio locally with all dependencies...
echo.

REM Set working directory
cd /d "%~dp0"

REM Set comprehensive environment variables (matching production)
set AXIESTUDIO_SECRET_KEY=dev-secret-key-local-testing-12345
set AXIESTUDIO_SUPERUSER=stefan@axiestudio.se
set AXIESTUDIO_SUPERUSER_PASSWORD=STEfanjohn!12
set AXIESTUDIO_AUTO_LOGIN=false
set AXIESTUDIO_NEW_USER_IS_ACTIVE=false
set DATABASE_URL=sqlite:///./axiestudio_local.db
set AXIESTUDIO_HOST=127.0.0.1
set AXIESTUDIO_PORT=7860
set AXIESTUDIO_LOG_LEVEL=DEBUG
set AXIESTUDIO_WORKERS=1
set AXIESTUDIO_CACHE_TYPE=simple
set AXIESTUDIO_CACHE_FOLDER=./cache
set AXIESTUDIO_FRONTEND_PATH=./src/backend/base/axiestudio/frontend
set PORT=7860
set PYTHONPATH=%~dp0src\backend\base;%PYTHONPATH%

echo ✅ Environment variables configured
echo.

echo 📦 Step 1: Installing base package dependencies...
cd src\backend\base
..\..\..\python-portable\python.exe -m pip install --user -e .

echo.
echo 📦 Step 2: Installing main package dependencies...
cd ..\..\..
python-portable\python.exe -m pip install --user -e .

echo.
echo 🔧 Step 3: Verifying installation...
python-portable\python.exe -c "import axiestudio; print('✅ Axie Studio imported successfully')"

echo.
echo 🚀 Step 4: Starting Axie Studio...
echo.
echo ==========================================
echo 🌐 URL: http://localhost:7860
echo 👤 Email: stefan@axiestudio.se
echo 🔑 Password: STEfanjohn!12
echo ==========================================
echo.
echo 📋 Features Available:
echo   ✅ 500+ AI Components
echo   ✅ Drag & Drop Interface
echo   ✅ OpenAI, Anthropic, Google AI
echo   ✅ Vector Databases
echo   ✅ Document Processing
echo   ✅ Authentication System
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server with full logging
python-portable\python.exe -m axiestudio run --host 127.0.0.1 --port 7860 --log-level DEBUG

pause
