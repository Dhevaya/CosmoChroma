@echo off
REM CosmoChroma Quick Start Script for Windows

echo.
echo ========================================
echo     CosmoChroma - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from nodejs.org
    pause
    exit /b 1
)

echo ✓ Python and Node.js are installed

REM Start Backend
echo.
echo Starting Backend Server...
echo.
cd cosmochroma-backend

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
if not exist venv\Lib\site-packages\fastapi (
    echo Installing Python dependencies...
    pip install -r requirements.txt
)

REM Start the backend server in a new window
echo Launching backend on http://localhost:8000
start cmd /k "title CosmoChroma Backend && python -m uvicorn main:app --reload --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start Frontend
echo.
echo Starting Frontend Server...
echo.
cd ..\cosmochroma-frontend

REM Install dependencies if node_modules doesn't exist
if not exist node_modules (
    echo Installing Node dependencies...
    call npm install
)

REM Start the frontend server
echo Launching frontend on http://localhost:3000
echo.
start cmd /k "title CosmoChroma Frontend && npm run dev"

REM Open browser
timeout /t 2 /nobreak
echo.
echo ========================================
echo ✓ Both servers are starting!
echo.
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo If windows don't open, check the cmd windows that started
echo ========================================
echo.

pause
