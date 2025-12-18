# 🚀 Quick Deployment Guide

## Choose Your Deployment Platform

### Option 1: Railway (Recommended - Easiest)

**Why Railway?**
- Free tier available ($5 credit/month)
- Automatic HTTPS
- PostgreSQL included
- GitHub integration
- Zero config deployment

**Steps:**
1. Push code to GitHub (if not already)
2. Go to [railway.app](https://railway.app)
3. Sign up/Login with GitHub
4. Click "New Project" → "Deploy from GitHub repo"
5. Select your repository
6. Railway auto-detects Django and deploys!
7. Add PostgreSQL: "New" → "Database" → "PostgreSQL"
8. Set environment variables (see below)

**Environment Variables to Set:**
```
SECRET_KEY=<generate-random-string>
DEBUG=False
ALLOWED_HOSTS=${{RAILWAY_STATIC_URL}}
DATABASE_URL=${{DATABASE_URL}}
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_VERIFICATION_BASE_URL=https://your-frontend.vercel.app/verify-email
PASSWORD_RESET_BASE_URL=https://your-frontend.vercel.app/password-reset-confirm
SENTRY_DSN=<your-sentry-dsn>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://your-frontend.vercel.app
```

---

### Option 2: Render

**Steps:**
1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Sign up/Login
4. Click "New" → "Web Service"
5. Connect your GitHub repository
6. Render auto-detects `render.yaml`
7. Click "Create Web Service"
8. Add PostgreSQL: "New" → "PostgreSQL"
9. Set environment variables

---

### Option 3: Heroku

**Steps:**
```bash
# Install Heroku CLI
# Windows: Download from heroku.com
# Mac: brew install heroku/brew/heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
cd backend
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
heroku config:set CORS_ALLOWED_ORIGINS="https://your-frontend.vercel.app"

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

---

## Frontend Deployment (Vercel - Recommended)

**Steps:**
1. Go to [vercel.com](https://vercel.com)
2. Sign up/Login with GitHub
3. Click "Add New" → "Project"
4. Import your repository
5. Set root directory to `frontend`
6. Set environment variable:
   ```
   REACT_APP_API_URL=https://your-backend.railway.app/api
   ```
7. Click "Deploy"

**Alternative: Netlify**
1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import from Git"
3. Select repository
4. Build settings:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/build`
5. Set environment variable: `REACT_APP_API_URL`
6. Deploy

---

## Post-Deployment Steps

### 1. Create Superuser
```bash
# Railway
railway run python manage.py createsuperuser

# Render
# Use shell from dashboard

# Heroku
heroku run python manage.py createsuperuser
```

### 2. Download spaCy Model
```bash
# Railway
railway run python -m spacy download en_core_web_sm

# Heroku
heroku run python -m spacy download en_core_web_sm
```

### 3. Test Deployment
- Visit your backend URL: `https://your-app.railway.app/health/`
- Visit your frontend URL: `https://your-app.vercel.app`
- Test login, registration, email verification
- Check Sentry for any errors

### 4. Configure Email (Gmail Example)
1. Enable 2-factor authentication on Gmail
2. Generate App Password: Google Account → Security → App passwords
3. Use app password as `EMAIL_HOST_PASSWORD`

### 5. Set Up Sentry (Error Monitoring)
1. Go to [sentry.io](https://sentry.io)
2. Create new project → Django
3. Copy DSN
4. Set `SENTRY_DSN` environment variable

---

## Quick Command Reference

### Generate SECRET_KEY
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Local Testing Before Deployment
```bash
# Backend
cd backend
python manage.py collectstatic --noinput
python manage.py test
gunicorn placement_portal.wsgi

# Frontend
cd frontend
npm run build
```

---

## Troubleshooting

### Backend Issues
- **Static files not loading**: Run `python manage.py collectstatic`
- **Database errors**: Check DATABASE_URL is set correctly
- **CORS errors**: Add frontend URL to CORS_ALLOWED_ORIGINS
- **500 errors**: Check logs and Sentry

### Frontend Issues
- **API not connecting**: Check REACT_APP_API_URL
- **Build fails**: Run `npm install` and check for errors
- **Blank page**: Check browser console for errors

---

## Cost Estimate

### Free Tier (Suitable for Development/Portfolio)
- **Railway**: $5 credit/month (plenty for small apps)
- **Render**: 750 hours/month free
- **Heroku**: Eco dynos $5/month
- **Vercel**: Free for personal projects
- **Netlify**: Free for personal projects

### Production (Paid)
- **Railway**: ~$10-20/month
- **Render**: ~$7-25/month
- **Heroku**: ~$16-50/month
- **Vercel Pro**: $20/month
- **AWS/DigitalOcean**: ~$10-50/month (more complex)

---

## Recommended Setup

**For Quick Demo/Portfolio:**
- Backend: Railway (free $5 credit)
- Frontend: Vercel (free)
- Database: Railway PostgreSQL (included)
- Total: FREE for first month

**For Production:**
- Backend: Railway/Render ($10/month)
- Frontend: Vercel Pro ($20/month)
- Database: Included or Supabase
- Sentry: Free tier
- Total: ~$30/month

---

## Next Steps After Deployment

1. ✅ Test all features
2. ✅ Set up custom domain (optional)
3. ✅ Configure SSL certificate (auto on Railway/Vercel)
4. ✅ Set up monitoring (Sentry)
5. ✅ Create user documentation
6. ✅ Backup database regularly
7. ✅ Monitor logs and performance

---

Need help? Check the full [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) or the [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)
