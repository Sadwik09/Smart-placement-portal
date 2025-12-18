# Tech Stack Setup Guide

## Prerequisites

Ensure you have the following installed:
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 16+**: [Download Node.js](https://nodejs.org/)
- **PostgreSQL 13+** (Optional, using SQLite for development): [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git**: [Download Git](https://git-scm.com/downloads/)

## Phase 3: Complete Setup Instructions

### Step 1: Clone/Navigate to Project

```bash
cd "d:\Projects\Smart Placement Portal"
```

### Step 2: Backend Setup (Django)

```bash
# Navigate to backend
cd backend

# Activate virtual environment
venv\Scripts\activate  # Windows

# Install all dependencies
pip install -r requirements.txt

# Download spaCy model for NLP
python -m spacy download en_core_web_sm

# Create .env file
copy .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Backend will run at: `http://localhost:8000`

### Step 3: Frontend Setup (React)

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Install additional packages
npm install axios react-router-dom @mui/material @emotion/react @emotion/styled

# Start development server
npm start
```

Frontend will run at: `http://localhost:3000`

### Step 4: ML Modules Setup

```bash
# Open new terminal
cd ml_modules

# Install ML dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Step 5: Verify Setup

1. **Backend**: Visit `http://localhost:8000/admin` and login with superuser credentials
2. **Frontend**: Visit `http://localhost:3000` - you should see the React app
3. **API**: Visit `http://localhost:8000/api/auth/` - should show available endpoints

## Database Setup (PostgreSQL - Optional)

If you want to use PostgreSQL instead of SQLite:

1. **Create Database**:
```sql
CREATE DATABASE placement_db;
CREATE USER placement_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE placement_db TO placement_user;
```

2. **Update settings.py**:
Uncomment the PostgreSQL configuration and comment out SQLite.

3. **Install psycopg2**:
```bash
pip install psycopg2-binary
```

4. **Run migrations again**:
```bash
python manage.py migrate
```

## Development Workflow

### Running All Services

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

**Backend Tests**:
```bash
cd backend
python manage.py test
```

**Frontend Tests**:
```bash
cd frontend
npm test
```

## Next Steps (Phase 4 onwards)

- ✅ Phase 1-2: Planning & Design (Completed)
- ✅ Phase 3: Tech Stack Setup (Completed)
- 🔄 Phase 4: Authentication & User Management
  - Implement registration flow
  - Add role-based dashboards
  - Create profile pages
- 🔜 Phase 5: Resume Upload & Parsing
- 🔜 Phase 6: Job Posting & Application System
- 🔜 Phase 7-8: ML Implementation
- 🔜 Phase 9-10: Admin Dashboard & Extended Features
- 🔜 Phase 11-12: Testing & Deployment
- 🔜 Phase 13: Documentation & Viva Prep

## Troubleshooting

### Common Issues

**1. Django import errors**:
```bash
pip install --upgrade django djangorestframework
```

**2. React build errors**:
```bash
rm -rf node_modules package-lock.json
npm install
```

**3. spaCy model not found**:
```bash
python -m spacy download en_core_web_sm
```

**4. Port already in use**:
- Backend: Use `python manage.py runserver 8001`
- Frontend: Set `PORT=3001` in environment

## Useful Commands

### Django Commands
```bash
python manage.py makemigrations  # Create migrations
python manage.py migrate         # Apply migrations
python manage.py createsuperuser # Create admin
python manage.py shell           # Django shell
python manage.py collectstatic   # Collect static files
```

### Git Commands
```bash
git init
git add .
git commit -m "Initial project setup"
git branch -M main
```

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [Material-UI](https://mui.com/)
- [scikit-learn](https://scikit-learn.org/)

---

**Setup completed!** 🎉

You now have a fully configured development environment for the Smart Placement Portal.
