# Smart Placement Portal

**AI-Powered Campus Placement Management System**

## 🎯 Project Overview

The Smart Placement Portal automates campus placements using AI-based skill matching and intelligent job recommendations. The system connects students, recruiters, and administrators (TPO) through a unified platform that streamlines the entire placement process.

## 🏗️ Architecture

- **Frontend**: React.js with role-based routing
- **Backend**: Django REST Framework with JWT authentication
- **Database**: PostgreSQL
- **ML Engine**: Python (scikit-learn, NLP)
- **Deployment**: 
  - Frontend: Vercel/Netlify
  - Backend: Render/Railway/AWS
  - Database: Cloud PostgreSQL

## 👥 User Roles

1. **Student**: Profile management, resume upload, job applications, recommendations
2. **Recruiter**: Job posting, candidate search, application management
3. **Admin (TPO)**: User approval, analytics dashboard, system management

## ✨ Core Features

### MVP Features
- ✅ User authentication & role-based access control
- ✅ Resume upload & intelligent parsing
- ✅ AI-powered skill matching
- ✅ Job recommendations for students
- ✅ Candidate recommendations for recruiters
- ✅ Admin dashboard with analytics

### Extended Features
- 📊 Resume scoring system
- 📅 Interview scheduling
- 📧 Email notifications
- 📈 Skill gap analysis
- 📉 Placement analytics (branch-wise, year-wise)

## 🚀 Getting Started

### Prerequisites

```bash
# Required software
- Node.js (v16+)
- Python (v3.8+)
- PostgreSQL (v13+)
```

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

### ML Modules Setup

```bash
cd ml_modules
pip install -r requirements.txt
```

## 📁 Project Structure

```
Smart Placement Portal/
├── backend/              # Django REST API
│   ├── api/             # API endpoints
│   ├── authentication/  # User auth
│   ├── jobs/           # Job management
│   ├── resumes/        # Resume handling
│   └── ml_integration/ # ML model integration
├── frontend/            # React application
│   ├── src/
│   │   ├── components/ # Reusable components
│   │   ├── pages/      # Page components
│   │   ├── services/   # API services
│   │   └── utils/      # Helper functions
├── ml_modules/          # Machine Learning
│   ├── resume_parser/  # PDF parsing & NLP
│   ├── skill_matcher/  # TF-IDF & cosine similarity
│   └── recommender/    # Recommendation engine
└── docs/               # Documentation
    ├── phase1/         # Planning docs
    ├── phase2/         # Design docs
    └── diagrams/       # UML, ER diagrams
```

## 🤖 Machine Learning Components

### 1. Resume Parsing
- PDF text extraction
- NLP-based skill extraction
- Data preprocessing

### 2. Skill Matching
- TF-IDF Vectorization
- Cosine Similarity calculation
- Match score generation

### 3. Recommendation Engine
- Job recommendations for students
- Candidate recommendations for recruiters
- Ranking algorithm

## 📊 Development Roadmap

- **Weeks 1-2**: Planning & Design
- **Weeks 3-4**: Tech setup & Authentication
- **Weeks 5-6**: Resume parsing & Job system
- **Weeks 7-8**: ML models & Recommendations
- **Weeks 9-10**: Admin dashboard & Extended features
- **Weeks 11-12**: Testing & Deployment
- **Week 13**: Documentation & Viva prep

## 🧪 Testing

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

## 📝 API Documentation

API endpoints will be documented using Swagger/OpenAPI.

Access at: `http://localhost:8000/api/docs/`

## 🔒 Security Features

- JWT-based authentication
- Email verification flow
- Password reset with secure tokens
- Password hashing (bcrypt)
- Role-based access control (RBAC)
- CORS configuration
- CSRF protection
- SQL injection prevention (ORM)
- API throttling and rate limiting
- Sentry integration for error monitoring
- Security headers (HSTS, secure cookies)

## 📚 Documentation

- [API Documentation](API_DOCUMENTATION.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [User Guide](USER_GUIDE.md)
- [Production Checklist](PRODUCTION_CHECKLIST.md)
- [Project Structure](PROJECT_STRUCTURE.md)
- [Complete Documentation Index](DOCUMENTATION_INDEX.md)

## 🚀 Production Deployment

See [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) for comprehensive deployment steps.

### Quick Setup
```bash
# Backend
cp .env.example .env
# Fill in environment variables
python manage.py migrate
python manage.py collectstatic

# Frontend
cd frontend
cp .env.example .env
# Set REACT_APP_API_URL
npm run build
```

## 📧 Contact & Support

**Project Type**: Final Year Project / Internship Project

**Tech Stack**: Full Stack + Python + Machine Learning

---

**Last Updated**: December 2024
