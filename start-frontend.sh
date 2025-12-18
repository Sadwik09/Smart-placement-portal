#!/bin/bash
# Frontend Setup and Start Script
# Smart Placement Portal

echo "========================================"
echo " Smart Placement Portal - Frontend Setup"
echo "========================================"
echo ""

cd frontend

echo "[1/4] Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed!"
    echo "Please download and install Node.js from: https://nodejs.org/"
    exit 1
fi

node --version
npm --version
echo ""

echo "[2/4] Checking dependencies..."
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies... This may take a few minutes."
    npm install
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
else
    echo "Dependencies already installed."
fi
echo ""

echo "[3/4] Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please update .env with your backend API URL"
    echo "Current setting: REACT_APP_API_URL=http://localhost:8000/api"
    echo ""
else
    echo ".env file exists."
fi
echo ""

echo "[4/4] Starting development server..."
echo ""
echo "========================================"
echo " Frontend will open at: http://localhost:3000"
echo " Press Ctrl+C to stop the server"
echo "========================================"
echo ""

npm start
