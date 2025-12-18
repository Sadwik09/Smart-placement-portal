@echo off
REM Setup script for Smart Placement Portal (Windows)

echo =========================================
echo Smart Placement Portal - Setup Script
echo =========================================

REM Backend Setup
echo.
echo Setting up backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing backend dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Copy environment file if not exists
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy ..\\.env.example .env
    echo WARNING: Please edit backend\.env with your configuration!
)

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Download spaCy model for NLP
echo Downloading spaCy language model...
python -m spacy download en_core_web_sm

echo Backend setup complete!

REM Frontend Setup
cd ..\frontend
echo.
echo Setting up frontend...

REM Install dependencies
echo Installing frontend dependencies...
call npm install

REM Copy environment file if not exists
if not exist ".env" (
    echo Creating frontend .env file from .env.example...
    copy .env.example .env
    echo Frontend .env created with default values
)

echo Frontend setup complete!

cd ..
echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo Next steps:
echo 1. Edit backend\.env with your configuration (SECRET_KEY, database, email, etc.)
echo 2. Create a superuser: cd backend ^&^& python manage.py createsuperuser
echo 3. Run backend: cd backend ^&^& python manage.py runserver
echo 4. Run frontend: cd frontend ^&^& npm start
echo.
echo For production deployment, see PRODUCTION_CHECKLIST.md
echo =========================================
pause
