#!/bin/bash

# CosmoChroma Quick Start Script for macOS/Linux

echo ""
echo "========================================"
echo "     CosmoChroma - Quick Start"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from python.org"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js 18+ from nodejs.org"
    exit 1
fi

echo "✓ Python and Node.js are installed"

# Start Backend
echo ""
echo "Starting Backend Server..."
echo ""
cd cosmochroma-backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
if ! python -c "import fastapi" &> /dev/null; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Start the backend server in background
echo "Launching backend on http://localhost:8000"
python -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start Frontend
echo ""
echo "Starting Frontend Server..."
echo ""
cd ../cosmochroma-frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
fi

# Start the frontend server
echo "Launching frontend on http://localhost:3000"
npm run dev &
FRONTEND_PID=$!

# Open browser (macOS only)
if [ "$(uname)" = "Darwin" ]; then
    sleep 2
    open http://localhost:3000
fi

echo ""
echo "========================================"
echo "✓ Both servers are starting!"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "========================================"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
