@echo off
echo 🧪 Axie Studio - Simple Local Test
echo ==================================
echo.
echo Attempting to run Axie Studio with minimal setup...
echo.

REM Set minimal environment
set PYTHONPATH=%~dp0src\backend\base
set AXIESTUDIO_SECRET_KEY=test-key
set AXIESTUDIO_SUPERUSER=stefan@axiestudio.se
set AXIESTUDIO_SUPERUSER_PASSWORD=STEfanjohn!12
set AXIESTUDIO_AUTO_LOGIN=false
set DATABASE_URL=sqlite:///./test.db
set AXIESTUDIO_HOST=127.0.0.1
set AXIESTUDIO_PORT=7860

echo 📦 Installing minimal dependencies...
python-portable\python.exe -m pip install --user fastapi uvicorn sqlalchemy pydantic loguru typer

echo.
echo 🚀 Attempting to start Axie Studio...
echo.
echo If this works, open: http://localhost:7860
echo Login: stefan@axiestudio.se / STEfanjohn!12
echo.

cd src\backend\base
..\..\..\python-portable\python.exe -c "
import sys
sys.path.insert(0, '.')
try:
    from axiestudio.__main__ import main
    print('✅ Successfully imported Axie Studio')
    main()
except ImportError as e:
    print('❌ Import failed:', e)
    print('📋 You may need to use the online options instead')
except Exception as e:
    print('❌ Error:', e)
    print('📋 Try the GitHub Codespaces option for guaranteed success')
"

echo.
echo 📋 If this didn't work, use the online options:
echo    - GitHub Codespaces (recommended)
echo    - GitPod
echo    - Railway
echo.
echo See RUN_ONLINE_DEMO.md for instructions
echo.

pause
