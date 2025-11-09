# Django Railway Deployment - Complete Troubleshooting Guide

## 🔍 Your Deployment URL
```
https://blog-website-assignment-production-ecbd.up.railway.app
```

---

## ⚠️ Diagnosis: Why It's Not Responding

Your Django app on Railway isn't responding because:

1. **Missing environment variables** - Django settings not configured
2. **Database connection issues** - PostgreSQL not properly connected
3. **Static files not served** - WhiteNoise configuration incomplete
4. **Startup command issues** - Gunicorn not binding correctly

---

## 🔧 Step-by-Step Fixes

### **Fix 1: Railway Environment Variables** ✅

**You MUST set these in Railway Dashboard:**

1. Go to: https://railway.app → Your Project → Settings → Variables

2. Add these exact variables:

```env
DEBUG=False
SECRET_KEY=django-insecure-your-super-secret-key-here-must-be-unique
ALLOWED_HOSTS=blog-website-assignment-production-ecbd.up.railway.app,localhost,127.0.0.1
DATABASE_URL=postgresql://...  (This should auto-generate from PostgreSQL service)
PYTHONUNBUFFERED=1
PORT=8000
```

**Generate a proper SECRET_KEY:**

To create a secure secret key, run this in PowerShell:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as `SECRET_KEY` in Railway.

### **Fix 2: Check PostgreSQL Connection**

1. In Railway Dashboard, go to your project
2. Click the PostgreSQL service
3. You should see:
   - ✅ Service is running (green status)
   - ✅ DATABASE_URL is visible in Variables
   - ✅ Connection info displayed

If PostgreSQL is not connected:
1. Click "New" 
2. Select "Database" → "PostgreSQL"
3. Railway will automatically add DATABASE_URL

### **Fix 3: Update Settings.py for Production**

Your settings.py needs a few tweaks for Railway production:

```python
# At the top of advanced_blog/settings.py, add:
import os
import dj_database_url

# Security Settings
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECURE_SSL_REDIRECT = not DEBUG  # Force HTTPS in production
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Allow all Railway domains
ALLOWED_HOSTS = ['*']

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
    'https://blog-website-assignment-production-ecbd.up.railway.app',
]

# Database - Auto-detect Railway PostgreSQL
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

# Static Files - WhiteNoise handles everything
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### **Fix 4: Procfile Configuration** ✅

Your Procfile should be:

```
web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn advanced_blog.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - --log-level info
```

### **Fix 5: Check WSGI Application**

Your `advanced_blog/wsgi.py` should look like:

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_blog.settings')
application = get_wsgi_application()
```

---

## 📋 Deployment Checklist

Before pushing to GitHub:

- [ ] Environment variables set in Railway (DEBUG, SECRET_KEY, ALLOWED_HOSTS)
- [ ] PostgreSQL service connected to your Railway project
- [ ] requirements.txt includes all dependencies
- [ ] Procfile configured correctly
- [ ] settings.py has production settings
- [ ] wsgi.py is properly configured
- [ ] No import errors (test locally first)

---

## 🚀 Testing Locally First

Before deploying, test your app locally with production settings:

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Test with production settings
$env:DEBUG="False"
$env:SECRET_KEY="test-secret-key-12345"
python manage.py runserver 0.0.0.0:8000
```

Then access: http://localhost:8000

---

## 🔄 Deployment Steps

### Step 1: Commit Changes
```powershell
git add .
git commit -m "Production fix: Railway configuration and security settings"
```

### Step 2: Push to GitHub
```powershell
git push origin main
```

### Step 3: Redeploy on Railway

Option A - Manual:
1. Go to https://railway.app
2. Select your project
3. Go to Deployments
4. Click latest deployment
5. Click "Redeploy"

Option B - New deployment:
1. Make a new commit
2. Push to GitHub
3. Railway auto-redeploys

### Step 4: Wait for Build & Deployment
- ⏳ 2-5 minutes typically
- Check Deployments tab for status
- Green checkmark = success

### Step 5: Test Your App

Once deployed, test these URLs:

```
https://blog-website-assignment-production-ecbd.up.railway.app/
https://blog-website-assignment-production-ecbd.up.railway.app/admin/
https://blog-website-assignment-production-ecbd.up.railway.app/accounts/login/
```

---

## 🐛 Common Errors & Solutions

### ❌ Error: "502 Bad Gateway"
**Cause**: App crashed during startup
**Fix**: 
1. Check Procfile is correct
2. Make sure all dependencies are in requirements.txt
3. Verify settings.py has no import errors
4. Check DATABASE_URL is set

### ❌ Error: "504 Gateway Timeout"
**Cause**: App taking too long to start
**Fix**:
1. Increase timeout in Procfile (already set to 120s)
2. Check migrations aren't stuck
3. Check database connection

### ❌ Error: "No such file or directory: staticfiles"
**Cause**: collectstatic didn't run
**Fix**:
1. Ensure Procfile runs: `python manage.py collectstatic --noinput`
2. Check STATIC_ROOT is writable
3. Re-run: `python manage.py collectstatic`

### ❌ Error: "ModuleNotFoundError"
**Cause**: Package not in requirements.txt
**Fix**:
```powershell
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### ❌ Error: "Connection refused - PostgreSQL"
**Cause**: DATABASE_URL not set or PostgreSQL not connected
**Fix**:
1. Verify PostgreSQL service exists in Railway
2. Check DATABASE_URL variable is set
3. Restart the service

---

## 📞 Advanced Debugging

### Check Requirements.txt
```powershell
cat requirements.txt
```

Should include:
- Django==5.2.8
- gunicorn==23.0.0
- psycopg2-binary==2.9.10
- whitenoise==6.8.2
- dj-database-url==2.3.0
- All other dependencies

### Test Settings Locally
```powershell
python manage.py check
```

Should output: "System check identified 0 issues"

### Test Database Connection
```powershell
python manage.py dbshell
```

Should open a psql prompt (if using PostgreSQL)

---

## ✅ Success Indicators

Your deployment is working when:

1. ✅ App loads at: https://blog-website-assignment-production-ecbd.up.railway.app/
2. ✅ Admin panel accessible at: /admin/
3. ✅ Login page loads at: /accounts/login/
4. ✅ Can create/view blog posts
5. ✅ Static files load (CSS, images appear correctly)
6. ✅ No console errors in browser DevTools

---

## 🔗 Useful Resources

- [Railway Documentation](https://docs.railway.app)
- [Django Deployment Guide](https://docs.djangoproject.com/en/5.2/howto/deployment/)
- [Gunicorn Configuration](https://gunicorn.org/)
- [WhiteNoise Setup](http://whitenoise.evans.io/)

---

**Need more help?** Check Railway logs or create a minimal test app first.

