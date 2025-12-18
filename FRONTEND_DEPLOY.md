# 🚀 Frontend Deployment Guide

## Quick Deploy Options

### 🟢 Option 1: Deploy to Vercel (Recommended)

**Easiest and fastest deployment for React apps**

#### Via Vercel Dashboard (No CLI needed)

1. **Go to [Vercel](https://vercel.com)**
2. Click **"Add New Project"**
3. **Import your GitHub repository:**
   - Connect GitHub account
   - Select `Smart-placement-portal`
   - Select `main` branch
4. **Configure build settings:**
   ```
   Framework Preset: Create React App
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: build
   ```
5. **Add Environment Variables:**
   - Key: `REACT_APP_API_URL`
   - Value: `https://your-backend-url.railway.app/api`
6. Click **"Deploy"**

✅ Your frontend will be live at: `https://your-app.vercel.app`

#### Via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel --prod

# Follow prompts and set REACT_APP_API_URL
```

---

### 🔵 Option 2: Deploy to Netlify

**Great for static sites with built-in CI/CD**

#### Via Netlify Dashboard

1. **Go to [Netlify](https://netlify.com)**
2. Click **"Add new site" → "Import an existing project"**
3. **Connect to GitHub:**
   - Authorize Netlify
   - Select `Smart-placement-portal` repository
4. **Configure build settings:**
   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: frontend/build
   ```
5. **Environment Variables:**
   - Go to Site Settings → Build & Deploy → Environment
   - Add `REACT_APP_API_URL` = `https://your-backend-url.railway.app/api`
6. Click **"Deploy site"**

✅ Your site will be live at: `https://your-app.netlify.app`

#### Via Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Build
cd frontend
npm run build

# Deploy
netlify deploy --prod --dir=build
```

---

### 🟠 Option 3: Deploy to Firebase Hosting

**Google's hosting platform with CDN**

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize (one-time setup)
cd frontend
firebase init hosting

# When prompted:
# - Select: Hosting
# - Public directory: build
# - Single-page app: Yes
# - Automatic builds with GitHub: No (optional)

# Build and deploy
npm run build
firebase deploy --only hosting
```

✅ Your app will be live at: `https://your-app.web.app`

---

### 🟣 Option 4: Deploy to GitHub Pages

**Free hosting for static sites**

#### Step 1: Install gh-pages

```bash
cd frontend
npm install --save-dev gh-pages
```

#### Step 2: Update package.json

Add these lines to `package.json`:

```json
{
  "homepage": "https://Sadwik09.github.io/Smart-placement-portal",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build",
    // ... other scripts
  }
}
```

#### Step 3: Deploy

```bash
npm run deploy
```

✅ Your app will be live at: `https://Sadwik09.github.io/Smart-placement-portal`

**Note:** Enable GitHub Pages in repository settings:
- Go to Settings → Pages
- Source: `gh-pages` branch
- Save

---

## 🔧 Pre-Deployment Checklist

Before deploying, ensure:

### 1. Environment Variables

Update `.env.production` or deployment platform settings:

```env
REACT_APP_API_URL=https://your-backend.railway.app/api
REACT_APP_API_TIMEOUT=15000
```

### 2. Backend CORS Configuration

Update Django `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    'https://your-frontend.vercel.app',
    'https://your-frontend.netlify.app',
    'https://your-frontend.web.app',
    # Add all your frontend URLs
]
```

### 3. Build Test

```bash
cd frontend
npm run build
```

Verify no errors in the build output.

### 4. API Connection Test

```bash
# Test backend is accessible
curl https://your-backend.railway.app/api/

# Should return API response
```

---

## 📱 Deployment Comparison

| Platform | Ease | Speed | Free Tier | Auto Deploy | CDN | Custom Domain |
|----------|------|-------|-----------|-------------|-----|---------------|
| **Vercel** | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | ✅ Unlimited | ✅ Yes | ✅ Yes | ✅ Yes |
| **Netlify** | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | ✅ 100GB/month | ✅ Yes | ✅ Yes | ✅ Yes |
| **Firebase** | ⭐⭐⭐⭐ | ⚡⚡ | ✅ 10GB/month | ⚪ Optional | ✅ Yes | ✅ Yes |
| **GitHub Pages** | ⭐⭐⭐ | ⚡⚡ | ✅ Unlimited | ⚪ Manual | ✅ Yes | ✅ Yes |

**Recommendation:** Use **Vercel** or **Netlify** for easiest deployment with auto-deploy from GitHub.

---

## 🔄 Auto-Deploy Setup

### Vercel Auto-Deploy

✅ **Automatic** - Vercel deploys on every push to `main` branch

### Netlify Auto-Deploy

✅ **Automatic** - Netlify deploys on every push to `main` branch

### GitHub Actions Auto-Deploy

Create `.github/workflows/deploy-frontend.yml`:

```yaml
name: Deploy Frontend

on:
  push:
    branches: [main]
    paths:
      - 'frontend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
          
      - name: Build
        run: |
          cd frontend
          npm run build
        env:
          REACT_APP_API_URL: ${{ secrets.REACT_APP_API_URL }}
          
      - name: Deploy to Vercel
        run: |
          npm install -g vercel
          cd frontend
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

**Setup:**
1. Go to GitHub repository → Settings → Secrets
2. Add `REACT_APP_API_URL` and `VERCEL_TOKEN`

---

## 🌐 Custom Domain Setup

### Vercel

1. Go to Project Settings → Domains
2. Add your domain: `placement.yourdomain.com`
3. Update DNS records (Vercel provides instructions)
4. Wait for SSL certificate (automatic)

### Netlify

1. Go to Site Settings → Domain Management
2. Add custom domain
3. Update DNS:
   ```
   Type: CNAME
   Name: placement
   Value: your-app.netlify.app
   ```
4. SSL enabled automatically

---

## 🐛 Common Deployment Issues

### 1. API CORS Error

**Error:** `CORS policy: No 'Access-Control-Allow-Origin' header`

**Fix:** Update Django backend `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    'https://your-frontend-domain.com',
]
```

### 2. Environment Variables Not Working

**Error:** API calls fail, `undefined` environment variables

**Fix:**
- Ensure variables start with `REACT_APP_`
- Re-deploy after adding environment variables
- Check deployment platform's environment variable settings

### 3. Blank Page After Deploy

**Error:** White screen, no content

**Fix:**
- Check browser console for errors
- Verify `homepage` in `package.json`
- For subdirectories, use: `"homepage": "/subdirectory"`
- Check `BrowserRouter` vs `HashRouter` in React Router

### 4. 404 on Page Refresh

**Error:** Direct URL access returns 404

**Fix:**

**Netlify:** Add `public/_redirects`:
```
/*    /index.html   200
```

**Vercel:** Add `vercel.json`:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

**Firebase:** Already handled by `firebase.json` single-page config

---

## 📊 Post-Deployment Monitoring

### 1. Performance Monitoring

Add to `public/index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-GA-ID');
</script>
```

### 2. Error Tracking (Sentry)

```bash
npm install @sentry/react
```

Update `src/index.js`:
```javascript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "YOUR-SENTRY-DSN",
  environment: "production"
});
```

---

## ✅ Final Checklist

Before going live:

- [ ] Backend deployed and accessible
- [ ] Frontend built successfully (`npm run build`)
- [ ] Environment variables configured
- [ ] CORS settings updated in backend
- [ ] Custom domain configured (if applicable)
- [ ] SSL certificate active (automatic on Vercel/Netlify)
- [ ] Test all user flows (login, job posting, applications)
- [ ] Analytics/monitoring set up
- [ ] Error tracking configured

---

## 🎉 You're Live!

Your Smart Placement Portal frontend is now deployed!

**Next Steps:**
1. Test the live application
2. Share the URL with users
3. Monitor logs and errors
4. Set up staging environment for testing

**Live URLs:**
- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-backend.railway.app`

---

Need help? Check the main [FRONTEND_SETUP.md](FRONTEND_SETUP.md) guide.
