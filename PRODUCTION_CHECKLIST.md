# Production Deployment Checklist

## Backend Configuration

### Environment Variables
1. Copy `.env.example` to `.env` and fill in all required values:
   - `SECRET_KEY`: Generate a strong secret key
   - `DEBUG=False` for production
   - `ALLOWED_HOSTS`: Add your domain
   - `DATABASE_URL`: PostgreSQL connection string (recommended for production)
   - `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: SMTP credentials
   - `SENTRY_DSN`: For error monitoring
   - `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`
   - `CSRF_TRUSTED_ORIGINS`: Add your frontend domain

### Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Static Files
```bash
# Collect static files
python manage.py collectstatic --no-input
```

### Testing
```bash
# Run tests before deploying
python manage.py test
```

## Frontend Configuration

### Environment Variables
1. Copy `frontend/.env.example` to `frontend/.env` and set:
   - `REACT_APP_API_URL`: Your production backend API URL

### Build
```bash
cd frontend
npm install
npm run build
```

## Security Checklist
- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` set
- [ ] `ALLOWED_HOSTS` configured
- [ ] SSL/TLS enabled (`SECURE_SSL_REDIRECT=True`)
- [ ] Secure cookies enabled
- [ ] CORS origins restricted to your domain
- [ ] CSRF trusted origins set
- [ ] Database credentials secured
- [ ] Email credentials secured
- [ ] Sentry DSN configured for monitoring

## Email Verification & Password Reset
- Ensure `EMAIL_VERIFICATION_BASE_URL` and `PASSWORD_RESET_BASE_URL` point to your production frontend URLs
- Configure SMTP settings for real email delivery
- Test email flows in staging before production

## CI/CD
- GitHub Actions workflow is configured in `.github/workflows/ci.yml`
- Runs backend tests and frontend build on push/PR
- Add deployment steps after build passes

## Monitoring & Error Tracking
- Sentry is integrated for error tracking
- Set `SENTRY_DSN` in backend environment
- Check Sentry dashboard for errors post-deployment

## Performance & Scaling
- Enable DRF throttling and pagination (already configured)
- Consider using Redis for caching and session storage
- Use a production WSGI server (Gunicorn recommended)
- Serve frontend static files via CDN or Nginx

## Post-Deployment
- [ ] Test all authentication flows (register, verify, login, password reset)
- [ ] Test job posting, application, interview scheduling
- [ ] Test ML recommendations and resume scoring
- [ ] Test notifications and real-time features
- [ ] Monitor Sentry for errors
- [ ] Review server logs and metrics
