# 🎨 Frontend Setup Guide - Smart Placement Portal

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Project Structure](#project-structure)
7. [API Integration](#api-integration)
8. [Environment Variables](#environment-variables)
9. [Build & Deploy](#build--deploy)
10. [Troubleshooting](#troubleshooting)

---

## ⚡ Quick Start

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
copy .env.example .env

# Start development server
npm start
```

The app will open at **http://localhost:3000**

---

## 📦 Prerequisites

Before starting, ensure you have:

- ✅ **Node.js** (v14 or higher) - [Download](https://nodejs.org/)
- ✅ **npm** (comes with Node.js) or **yarn**
- ✅ **Backend API running** on http://localhost:8000

Check your Node.js version:
```bash
node --version
npm --version
```

---

## 🔧 Installation

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

This will install:
- **React 19.2.3** - UI framework
- **React Router 7.10.1** - Navigation
- **React Scripts 5.0.1** - Build tools
- All testing libraries

### Step 2: Verify Installation

```bash
npm list react
npm list react-router-dom
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file in the `frontend/` directory:

```bash
# Copy the example file
copy .env.example .env
```

Edit `.env` with your settings:

```env
# Backend API URL
REACT_APP_API_URL=http://localhost:8000/api

# API timeout (milliseconds)
REACT_APP_API_TIMEOUT=10000

# Optional: Production API URL
# REACT_APP_API_URL=https://your-backend.railway.app/api
```

### Configuration Options

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `REACT_APP_API_URL` | Backend API base URL | `http://localhost:8000/api` | ✅ Yes |
| `REACT_APP_API_TIMEOUT` | Request timeout in ms | `10000` | ⚪ Optional |

---

## 🚀 Running the Application

### Development Mode

```bash
npm start
```

- Opens browser at **http://localhost:3000**
- Hot reload enabled (auto-refresh on file changes)
- Shows lint errors in console

### Production Build

```bash
npm run build
```

Creates optimized build in `build/` folder:
- Minified JavaScript
- Optimized assets
- Production-ready code

### Testing

```bash
# Run all tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run specific test file
npm test -- App.test.js
```

---

## 📁 Project Structure

```
frontend/
├── public/              # Static files
│   ├── index.html       # HTML template
│   ├── favicon.ico      # App icon
│   └── manifest.json    # PWA config
│
├── src/
│   ├── components/      # Reusable components
│   │   ├── Navbar.js           # Navigation bar
│   │   ├── Navbar.css
│   │   └── ProtectedRoute.js   # Auth guard
│   │
│   ├── pages/           # Page components
│   │   ├── Home.js              # Landing page
│   │   ├── Login.js             # Login page
│   │   ├── Register.js          # Registration
│   │   ├── Dashboard.js         # Student dashboard
│   │   ├── RecruiterDashboard.js # Recruiter dashboard
│   │   ├── AdminDashboard.js    # Admin dashboard
│   │   ├── JobList.js           # Browse jobs
│   │   ├── JobDetail.js         # Job details
│   │   ├── JobPost.js           # Post new job
│   │   ├── ResumeUpload.js      # Upload resume
│   │   ├── Recommendations.js   # ML recommendations
│   │   ├── Interviews.js        # Interview schedule
│   │   ├── ScheduleInterview.js # Schedule interview
│   │   ├── Notifications.js     # Notifications
│   │   ├── VerifyEmail.js       # Email verification
│   │   ├── PasswordResetRequest.js
│   │   └── PasswordResetConfirm.js
│   │
│   ├── services/        # API integration
│   │   └── api.js       # Axios configuration & API calls
│   │
│   ├── context/         # React Context (if using)
│   ├── utils/           # Helper functions
│   ├── App.js           # Main app component
│   ├── App.css          # Global styles
│   └── index.js         # Entry point
│
├── .env.example         # Environment template
├── .env                 # Your environment variables (gitignored)
├── package.json         # Dependencies & scripts
└── README.md            # Project documentation
```

---

## 🔌 API Integration

### API Service (`src/services/api.js`)

The frontend communicates with the backend via Axios HTTP client.

**Key Features:**
- Automatic JWT token handling
- Request/response interceptors
- Error handling
- Token refresh logic

**Example Usage:**

```javascript
import api from '../services/api';

// Login
const response = await api.post('/auth/login/', {
  email: 'user@example.com',
  password: 'password123'
});

// Get jobs
const jobs = await api.get('/jobs/');

// Upload resume
const formData = new FormData();
formData.append('file', file);
await api.post('/resumes/upload/', formData);
```

### Available API Endpoints

#### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/verify-email/<token>/` - Verify email
- `POST /api/auth/password-reset/` - Request password reset
- `POST /api/auth/password-reset-confirm/` - Confirm password reset

#### Jobs
- `GET /api/jobs/` - List all jobs
- `GET /api/jobs/<id>/` - Get job details
- `POST /api/jobs/` - Create job (recruiter only)
- `PUT /api/jobs/<id>/` - Update job
- `DELETE /api/jobs/<id>/` - Delete job
- `POST /api/jobs/<id>/apply/` - Apply to job

#### Resumes
- `POST /api/resumes/upload/` - Upload resume
- `GET /api/resumes/` - Get user's resumes
- `GET /api/resumes/<id>/` - Get resume details
- `DELETE /api/resumes/<id>/` - Delete resume

#### Recommendations
- `GET /api/recommendations/` - Get ML-based job recommendations

#### Interviews
- `GET /api/interviews/` - Get user's interviews
- `POST /api/interviews/` - Schedule interview
- `PUT /api/interviews/<id>/` - Update interview
- `DELETE /api/interviews/<id>/` - Cancel interview

#### Notifications
- `GET /api/notifications/` - Get notifications
- `PUT /api/notifications/<id>/read/` - Mark as read
- `DELETE /api/notifications/<id>/` - Delete notification

---

## 🌍 Environment Variables

### Development (.env.development)

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_API_TIMEOUT=10000
```

### Production (.env.production)

```env
REACT_APP_API_URL=https://your-backend.railway.app/api
REACT_APP_API_TIMEOUT=15000
```

---

## 🏗️ Build & Deploy

### Build for Production

```bash
npm run build
```

Output: `build/` directory with optimized production build

### Deploy to Vercel

1. **Install Vercel CLI:**
```bash
npm install -g vercel
```

2. **Login to Vercel:**
```bash
vercel login
```

3. **Deploy:**
```bash
cd frontend
vercel --prod
```

4. **Set Environment Variables in Vercel Dashboard:**
   - Go to Project Settings → Environment Variables
   - Add `REACT_APP_API_URL` with your backend URL

### Deploy to Netlify

1. **Install Netlify CLI:**
```bash
npm install -g netlify-cli
```

2. **Build the app:**
```bash
npm run build
```

3. **Deploy:**
```bash
netlify deploy --prod --dir=build
```

4. **Set Environment Variables:**
   - Go to Site Settings → Build & Deploy → Environment
   - Add `REACT_APP_API_URL`

### Deploy to Firebase

1. **Install Firebase CLI:**
```bash
npm install -g firebase-tools
```

2. **Login:**
```bash
firebase login
```

3. **Initialize Firebase:**
```bash
firebase init hosting
```

4. **Build and Deploy:**
```bash
npm run build
firebase deploy
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. **Module Not Found Error**

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 2. **API Connection Failed**

**Check:**
- ✅ Backend is running on http://localhost:8000
- ✅ `.env` file exists with correct `REACT_APP_API_URL`
- ✅ CORS is enabled in Django backend

**Test Backend:**
```bash
curl http://localhost:8000/api/
```

#### 3. **Port 3000 Already in Use**

```bash
# Kill process on port 3000 (Windows)
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use different port
PORT=3001 npm start
```

#### 4. **React Router Not Working After Deploy**

Add `_redirects` file in `public/` folder:
```
/*    /index.html   200
```

#### 5. **Environment Variables Not Loading**

- ✅ Restart development server after changing `.env`
- ✅ Variable names must start with `REACT_APP_`
- ✅ Use `process.env.REACT_APP_API_URL` in code

#### 6. **JWT Token Expires**

The API service automatically refreshes tokens. If issues persist:
```javascript
// Clear localStorage and login again
localStorage.clear();
window.location.href = '/login';
```

---

## 🎯 Development Workflow

### 1. **Start Backend First**

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python manage.py runserver
```

### 2. **Start Frontend**

```bash
cd frontend
npm start
```

### 3. **Development Flow**

1. Edit files in `src/`
2. Save → Auto-refresh in browser
3. Check console for errors
4. Test API calls in DevTools Network tab

### 4. **Before Committing**

```bash
# Run tests
npm test

# Check for lint errors
npm run build
```

---

## 📚 Additional Resources

- **React Documentation:** https://react.dev/
- **React Router:** https://reactrouter.com/
- **Create React App:** https://create-react-app.dev/
- **Axios:** https://axios-http.com/

---

## 🔑 Key Commands Cheat Sheet

```bash
# Install dependencies
npm install

# Start dev server
npm start

# Build for production
npm run build

# Run tests
npm test

# Update dependencies
npm update

# Check for security issues
npm audit

# Fix security issues
npm audit fix
```

---

## ✅ Checklist Before Going Live

- [ ] Backend API is deployed and accessible
- [ ] Environment variables configured in `.env`
- [ ] `REACT_APP_API_URL` points to production backend
- [ ] Build succeeds without errors (`npm run build`)
- [ ] All tests pass (`npm test`)
- [ ] CORS configured in backend for frontend domain
- [ ] SSL/HTTPS enabled (if production)
- [ ] Error tracking configured (Sentry)
- [ ] Analytics set up (Google Analytics)

---

## 🤝 Support

If you encounter issues:

1. Check this guide's **Troubleshooting** section
2. Review browser console for errors
3. Check Network tab in DevTools for API errors
4. Verify backend is running and accessible

---

**Happy Coding! 🚀**
