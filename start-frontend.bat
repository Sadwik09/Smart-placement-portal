@echo off
REM Frontend Setup and Start Script
REM Smart Placement Portal

echo ========================================
echo  Smart Placement Portal - Frontend Setup
echo ========================================
echo.

cd frontend

echo [1/4] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed!
    echo Please download and install Node.js from: https://nodejs.org/
    pause
    exit /b 1
)

node --version
npm --version
echo.

echo [2/4] Checking dependencies...
if not exist "node_modules\" (
    echo Installing dependencies... This may take a few minutes.
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo Dependencies already installed.
)
echo.

echo [3/4] Checking environment configuration...
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please update .env with your backend API URL
    echo Current setting: REACT_APP_API_URL=http://localhost:8000/api
    echo.
) else (
    echo .env file exists.
)
echo.

echo [4/4] Starting development server...
echo.
echo ========================================
echo  Frontend will open at: http://localhost:3000
echo  Press Ctrl+C to stop the server
echo ========================================
echo.

call npm start
