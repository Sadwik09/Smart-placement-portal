# 🚀 Quick Start Guide

## Initial Setup (One-Time)

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Create .env file
copy .env.example .env

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Enter email, username, password when prompted

# Run server
python manage.py runserver
```

✅ Backend ready at: `http://localhost:8000`

### 2. Frontend Setup

```bash
# Open NEW terminal
cd frontend

# Install dependencies
npm install

# Install additional packages
npm install axios react-router-dom @mui/material @emotion/react @emotion/styled

# Create .env file
copy .env.example .env

# Start development server
npm start
```

✅ Frontend ready at: `http://localhost:3000`

### 3. ML Setup

```bash
# Open NEW terminal
cd ml_modules

# Install ML dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

✅ ML modules ready!

## Daily Development Workflow

### Start Development Environment

**Terminal 1 - Backend**:
```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm start
```

### Testing

**Test Backend**:
```bash
cd backend
python manage.py test
```

**Test Frontend**:
```bash
cd frontend
npm test
```

### Create New Django App

```bash
cd backend
python manage.py startapp app_name
```

Then add `'app_name'` to `INSTALLED_APPS` in `settings.py`

### Create New Migration

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

## Common Commands

### Django Commands
```bash
python manage.py runserver           # Start server
python manage.py makemigrations      # Create migrations
python manage.py migrate             # Apply migrations
python manage.py createsuperuser     # Create admin
python manage.py shell               # Django shell
python manage.py test                # Run tests
```

### npm Commands
```bash
npm start          # Start dev server
npm test           # Run tests
npm run build      # Build for production
npm install <pkg>  # Install package
```

### Git Commands
```bash
git status                          # Check status
git add .                          # Stage all changes
git commit -m "message"            # Commit changes
git push origin main               # Push to remote
```

## Testing the Setup

### 1. Test Backend API
- Visit: `http://localhost:8000/admin`
- Login with superuser credentials
- Navigate to Users section

### 2. Test Frontend
- Visit: `http://localhost:3000`
- Check if React app loads

### 3. Test Authentication API

**Register User**:
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "email": "student1@example.com",
    "password": "TestPass123",
    "password2": "TestPass123",
    "role": "student"
  }'
```

**Login User** (after admin approval):
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student1@example.com",
    "password": "TestPass123"
  }'
```

## Troubleshooting

### Django Errors

**Port already in use**:
```bash
python manage.py runserver 8001
```

**Migration errors**:
```bash
python manage.py migrate --run-syncdb
```

**Module not found**:
```bash
pip install -r requirements.txt
```

### React Errors

**Port already in use**:
Set `PORT=3001` in `.env` file

**Build errors**:
```bash
rm -rf node_modules package-lock.json
npm install
```

### ML Errors

**spaCy model not found**:
```bash
python -m spacy download en_core_web_sm
```

**Import errors**:
```bash
pip install -r requirements.txt
```

## Next Steps

1. ✅ Complete Phase 4: User Management
2. ✅ Build login/registration UI
3. ✅ Create role-based dashboards
4. ✅ Implement profile pages
5. ✅ Move to Phase 5: Resume System

## Need Help?

- Check `PROJECT_STATUS.md` for current progress
- Review `docs/` folder for detailed documentation
- Check app-specific README files
- Review Django/React official docs

---

**Happy Coding! 🎉**
