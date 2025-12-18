#!/bin/bash
# Railway Deployment Script

echo "========================================"
echo "Deploying to Railway"
echo "========================================"
echo ""

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "[1/5] Logging into Railway..."
railway login

# Link or create project
echo "[2/5] Linking to Railway project..."
railway link

# Add PostgreSQL if not exists
echo "[3/5] Ensure PostgreSQL is added to your project via Railway dashboard"
echo "Press any key once PostgreSQL is added..."
read -n 1

# Set environment variables
echo "[4/5] Setting environment variables..."
railway variables set SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS='${{RAILWAY_STATIC_URL}}'
railway variables set CORS_ALLOWED_ORIGINS='https://your-frontend.vercel.app'
railway variables set SECURE_SSL_REDIRECT=True
railway variables set SESSION_COOKIE_SECURE=True
railway variables set CSRF_COOKIE_SECURE=True

# Deploy
echo "[5/5] Deploying..."
railway up

echo ""
echo "========================================"
echo "Deployment Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Get your backend URL from Railway dashboard"
echo "2. Deploy frontend to Vercel with REACT_APP_API_URL=<backend-url>/api"
echo "3. Update CORS_ALLOWED_ORIGINS with frontend URL"
echo "4. Run: railway run python manage.py createsuperuser"
echo "5. Test your deployment!"
echo "========================================"
