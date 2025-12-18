#!/bin/bash
echo "========================================"
echo "Smart Placement Portal - Pre-Deployment Check"
echo "========================================"
echo ""

cd backend

echo "[1/6] Installing production dependencies..."
pip install gunicorn whitenoise dj-database-url sentry-sdk

echo ""
echo "[2/6] Running tests..."
python manage.py test

if [ $? -ne 0 ]; then
    echo "ERROR: Tests failed! Fix issues before deploying."
    exit 1
fi

echo ""
echo "[3/6] Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "[4/6] Checking for migrations..."
python manage.py makemigrations --check --dry-run

echo ""
echo "[5/6] Building frontend..."
cd ../frontend
npm install
npm run build

if [ $? -ne 0 ]; then
    echo "ERROR: Frontend build failed!"
    exit 1
fi

cd ..

echo ""
echo "[6/6] Pre-deployment checks complete!"
echo ""
echo "========================================"
echo "Ready to Deploy!"
echo "========================================"
echo ""
echo "Next Steps:"
echo "1. Push code to GitHub"
echo "2. Choose deployment platform (Railway, Render, or Heroku)"
echo "3. Follow QUICK_DEPLOY.md for platform-specific steps"
echo "4. Set environment variables on the platform"
echo "5. Deploy!"
echo ""
echo "See QUICK_DEPLOY.md for detailed instructions."
echo "========================================"
