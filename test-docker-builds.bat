@echo off
REM AxieStudio Docker Build Test Script for Windows
REM This script tests all three Docker builds locally

echo 🐳 AxieStudio Docker Build Test Script
echo ======================================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker and try again.
    exit /b 1
)

echo [INFO] Starting Docker build tests...
echo.

REM Test 1: Backend-only build
echo === Test 1: Backend-Only Build ===
echo [INFO] Testing Backend-Only build...
echo [INFO] Dockerfile: docker/backend-only.Dockerfile
echo [INFO] Tag: axiestudio-backend-test

docker build -f docker/backend-only.Dockerfile -t axiestudio-backend-test . --no-cache
if %errorlevel% neq 0 (
    echo [ERROR] Backend-Only build failed!
    goto cleanup
)
echo [SUCCESS] Backend-Only build completed successfully!

REM Test backend container
echo [INFO] Testing Backend-Only container startup...
docker rm -f test-backend >nul 2>&1
docker run -d --name test-backend -p 7860:7860 axiestudio-backend-test
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start backend container
    goto cleanup
)
echo [SUCCESS] Backend container started successfully

REM Wait and check
timeout /t 10 /nobreak >nul
docker ps | findstr test-backend >nul
if %errorlevel% neq 0 (
    echo [ERROR] Backend container stopped unexpectedly
    docker logs test-backend
    goto cleanup
)
echo [SUCCESS] Backend container is running

REM Clean up backend test
docker stop test-backend >nul 2>&1
docker rm test-backend >nul 2>&1
echo [INFO] Backend container cleaned up
echo.

REM Test 2: Frontend-only build
echo === Test 2: Frontend-Only Build ===
echo [INFO] Testing Frontend-Only build...
echo [INFO] Dockerfile: docker/frontend-only.Dockerfile
echo [INFO] Tag: axiestudio-frontend-test

docker build -f docker/frontend-only.Dockerfile -t axiestudio-frontend-test . --no-cache
if %errorlevel% neq 0 (
    echo [ERROR] Frontend-Only build failed!
    goto cleanup
)
echo [SUCCESS] Frontend-Only build completed successfully!

REM Test frontend container
echo [INFO] Testing Frontend-Only container startup...
docker rm -f test-frontend >nul 2>&1
docker run -d --name test-frontend -p 8080:80 axiestudio-frontend-test
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start frontend container
    goto cleanup
)
echo [SUCCESS] Frontend container started successfully

REM Wait and check
timeout /t 10 /nobreak >nul
docker ps | findstr test-frontend >nul
if %errorlevel% neq 0 (
    echo [ERROR] Frontend container stopped unexpectedly
    docker logs test-frontend
    goto cleanup
)
echo [SUCCESS] Frontend container is running

REM Clean up frontend test
docker stop test-frontend >nul 2>&1
docker rm test-frontend >nul 2>&1
echo [INFO] Frontend container cleaned up
echo.

REM Test 3: Fullstack build
echo === Test 3: Fullstack Build ===
echo [INFO] Testing Fullstack build...
echo [INFO] Dockerfile: docker/fullstack.Dockerfile
echo [INFO] Tag: axiestudio-fullstack-test

docker build -f docker/fullstack.Dockerfile -t axiestudio-fullstack-test . --no-cache
if %errorlevel% neq 0 (
    echo [ERROR] Fullstack build failed!
    goto cleanup
)
echo [SUCCESS] Fullstack build completed successfully!

REM Test fullstack container
echo [INFO] Testing Fullstack container startup...
docker rm -f test-fullstack >nul 2>&1
docker run -d --name test-fullstack -p 7861:7860 axiestudio-fullstack-test
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start fullstack container
    goto cleanup
)
echo [SUCCESS] Fullstack container started successfully

REM Wait and check
timeout /t 10 /nobreak >nul
docker ps | findstr test-fullstack >nul
if %errorlevel% neq 0 (
    echo [ERROR] Fullstack container stopped unexpectedly
    docker logs test-fullstack
    goto cleanup
)
echo [SUCCESS] Fullstack container is running

REM Clean up fullstack test
docker stop test-fullstack >nul 2>&1
docker rm test-fullstack >nul 2>&1
echo [INFO] Fullstack container cleaned up
echo.

REM Summary
echo === Build Test Summary ===
echo [SUCCESS] All Docker builds completed!
echo [INFO] Images created:
docker images | findstr "axiestudio.*test"

:cleanup
echo [INFO] Cleaning up test images...
docker rmi axiestudio-backend-test axiestudio-frontend-test axiestudio-fullstack-test >nul 2>&1

echo [SUCCESS] 🎉 All tests completed successfully!
pause
