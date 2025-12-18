#!/bin/bash
# Setup script for Smart Placement Portal (Unix/Mac)

echo "========================================="
echo "Smart Placement Portal - Setup Script"
echo "========================================="

# Backend Setup
echo ""
echo "Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing backend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp ../.env.example .env
    echo "⚠️  Please edit backend/.env with your configuration!"
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Download spaCy model for NLP
echo "Downloading spaCy language model..."
python -m spacy download en_core_web_sm

echo "✅ Backend setup complete!"

# Frontend Setup
cd ../frontend
echo ""
echo "Setting up frontend..."

# Install dependencies
echo "Installing frontend dependencies..."
npm install

# Copy environment file if not exists
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file from .env.example..."
    cp .env.example .env
    echo "✅ Frontend .env created with default values"
fi

echo "✅ Frontend setup complete!"

cd ..
echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your configuration (SECRET_KEY, database, email, etc.)"
echo "2. Create a superuser: cd backend && python manage.py createsuperuser"
echo "3. Run backend: cd backend && python manage.py runserver"
echo "4. Run frontend: cd frontend && npm start"
echo ""
echo "For production deployment, see PRODUCTION_CHECKLIST.md"
echo "========================================="
