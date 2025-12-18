# 🚀 Deployment Guide - Smart Placement Portal

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Backend Deployment (Django)](#backend-deployment)
3. [Frontend Deployment (React)](#frontend-deployment)
4. [Database Setup](#database-setup)
5. [Environment Configuration](#environment-configuration)
6. [Production Checklist](#production-checklist)

---

## Prerequisites

- Python 3.10+
- Node.js 16+
- PostgreSQL 14+
- Git
- Domain name (optional)
- Server (VPS/Cloud: AWS, DigitalOcean, Heroku, etc.)

---

## Backend Deployment (Django)

### Option 1: Heroku Deployment

1. **Install Heroku CLI**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
heroku login
```

2. **Create Heroku App**
```bash
cd backend
heroku create smart-placement-api
```

3. **Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:mini
```

4. **Configure Environment Variables**
```bash
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="smart-placement-api.herokuapp.com"
heroku config:set CORS_ALLOWED_ORIGINS="https://your-frontend-domain.com"
```

5. **Create Procfile**
```bash
# backend/Procfile
web: gunicorn placement_portal.wsgi --log-file -
release: python manage.py migrate
```

6. **Create runtime.txt**
```bash
# backend/runtime.txt
python-3.11.0
```

7. **Update requirements.txt**
```bash
pip install gunicorn psycopg2-binary whitenoise
pip freeze > requirements.txt
```

8. **Update settings.py for production**
```python
# backend/placement_portal/settings.py

import dj_database_url

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://localhost/placement_db',
        conn_max_age=600
    )
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
```

9. **Deploy**
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

10. **Run migrations**
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Option 2: DigitalOcean/AWS Deployment

1. **Setup Ubuntu Server**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql
```

2. **Clone Repository**
```bash
git clone https://github.com/yourusername/smart-placement-portal.git
cd smart-placement-portal/backend
```

3. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

4. **Configure PostgreSQL**
```bash
sudo -u postgres psql
CREATE DATABASE placement_db;
CREATE USER placement_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE placement_db TO placement_user;
\q
```

5. **Environment Variables**
```bash
# Create .env file
nano .env
```
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://placement_user:your_password@localhost/placement_db
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

6. **Run Migrations**
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

7. **Configure Gunicorn**
```bash
# /etc/systemd/system/gunicorn.service
[Unit]
Description=Gunicorn daemon for Smart Placement Portal
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/smart-placement-portal/backend
ExecStart=/home/ubuntu/smart-placement-portal/backend/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/ubuntu/smart-placement-portal/backend/gunicorn.sock \
          placement_portal.wsgi:application

[Install]
WantedBy=multi-user.target
```

8. **Configure Nginx**
```nginx
# /etc/nginx/sites-available/smart-placement
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/smart-placement-portal/backend;
    }
    
    location /media/ {
        root /home/ubuntu/smart-placement-portal/backend;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/smart-placement-portal/backend/gunicorn.sock;
    }
}
```

9. **Enable and Start Services**
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo ln -s /etc/nginx/sites-available/smart-placement /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

10. **Setup SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

## Frontend Deployment (React)

### Option 1: Vercel (Recommended for React)

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Configure Environment Variables**
```bash
# frontend/.env.production
REACT_APP_API_URL=https://your-backend-domain.com/api
```

3. **Deploy**
```bash
cd frontend
vercel
```

4. **Set Environment Variables in Vercel Dashboard**
- Go to your project settings on Vercel
- Add `REACT_APP_API_URL` environment variable

### Option 2: Netlify

1. **Build the project**
```bash
cd frontend
npm run build
```

2. **Create `_redirects` file**
```bash
# frontend/public/_redirects
/*  /index.html  200
```

3. **Deploy via Netlify CLI**
```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Option 3: Nginx Static Hosting

1. **Build the project**
```bash
cd frontend
npm run build
```

2. **Copy build files to server**
```bash
scp -r build/* user@server:/var/www/smart-placement-portal/
```

3. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name frontend-domain.com;
    root /var/www/smart-placement-portal;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

---

## Database Setup

### PostgreSQL Production Configuration

1. **Create Database Backup Strategy**
```bash
# Create backup script
#!/bin/bash
pg_dump placement_db > backup_$(date +%Y%m%d).sql
```

2. **Schedule Automated Backups**
```bash
crontab -e
# Add daily backup at 2 AM
0 2 * * * /path/to/backup-script.sh
```

3. **Connection Pooling (Optional)**
```bash
pip install psycopg2-pool
```

---

## Environment Configuration

### Backend .env (Production)
```env
SECRET_KEY=generate-with-python-secrets
DEBUG=False
ALLOWED_HOSTS=api.yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/db
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 for Media Files (Optional)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1
```

### Frontend .env.production
```env
REACT_APP_API_URL=https://api.yourdomain.com/api
REACT_APP_ENV=production
```

---

## Production Checklist

### Backend ✅
- [ ] `DEBUG = False` in settings.py
- [ ] Strong `SECRET_KEY` configured
- [ ] PostgreSQL database configured
- [ ] Static files collected and served
- [ ] Media files storage configured (S3/CloudFront)
- [ ] HTTPS enforced
- [ ] CORS properly configured
- [ ] Environment variables secured
- [ ] Database backups automated
- [ ] Gunicorn/uWSGI configured
- [ ] Nginx configured as reverse proxy
- [ ] SSL certificate installed
- [ ] Error logging configured (Sentry)
- [ ] Admin interface secured
- [ ] Rate limiting implemented

### Frontend ✅
- [ ] Production build created
- [ ] API URL configured
- [ ] Environment variables set
- [ ] CDN configured (optional)
- [ ] Assets optimized
- [ ] HTTPS enforced
- [ ] Analytics configured (Google Analytics)
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring
- [ ] SEO optimized

### ML Modules ✅
- [ ] All required packages installed
- [ ] spaCy model downloaded (`python -m spacy download en_core_web_sm`)
- [ ] PDF parsing libraries installed
- [ ] ML modules path configured correctly

### Security ✅
- [ ] HTTPS enforced on all domains
- [ ] Security headers configured
- [ ] CSRF protection enabled
- [ ] XSS protection enabled
- [ ] SQL injection protection (ORM used)
- [ ] User authentication secure
- [ ] File upload validation
- [ ] Rate limiting on APIs
- [ ] Regular security audits

### Monitoring ✅
- [ ] Application monitoring (New Relic/Datadog)
- [ ] Error tracking (Sentry)
- [ ] Server monitoring (UptimeRobot)
- [ ] Database monitoring
- [ ] Log aggregation (ELK/Papertrail)

---

## Post-Deployment

### 1. Create Admin User
```bash
python manage.py createsuperuser
```

### 2. Load Initial Data (Optional)
```bash
python manage.py loaddata fixtures/initial_data.json
```

### 3. Test All Features
- User registration
- Login/Logout
- Job posting
- Resume upload
- ML recommendations
- Interview scheduling

### 4. Monitor Logs
```bash
tail -f /var/log/nginx/error.log
tail -f /var/log/gunicorn/error.log
```

---

## Troubleshooting

### Common Issues

**1. Static files not loading**
```bash
python manage.py collectstatic --clear
```

**2. Database connection errors**
- Check DATABASE_URL in environment
- Verify PostgreSQL is running
- Check firewall rules

**3. CORS errors**
- Verify CORS_ALLOWED_ORIGINS in settings
- Check frontend API URL configuration

**4. 502 Bad Gateway**
- Check Gunicorn is running: `sudo systemctl status gunicorn`
- Check Nginx configuration: `sudo nginx -t`

---

## Scaling Considerations

### When to Scale:
- High traffic (>1000 concurrent users)
- Slow response times
- Database bottlenecks

### Scaling Options:
1. **Horizontal Scaling**: Add more servers behind load balancer
2. **Database**: Read replicas, connection pooling
3. **Caching**: Redis/Memcached for sessions and queries
4. **CDN**: CloudFlare/CloudFront for static assets
5. **Queue System**: Celery for async tasks

---

**🎉 Congratulations! Your Smart Placement Portal is now deployed!**

For support, contact: support@smartplacement.com
