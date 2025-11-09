# 🚂 Railway Deployment Fix - Complete Guide

## 🔴 Issue: ERR_CONNECTION_TIMED_OUT

Your deployment is timing out. Follow these steps to fix it:

---

## ✅ Step 1: Environment Variables Setup

Go to your Railway Dashboard → Project Settings → Variables and set these:

```env
DEBUG=False
SECRET_KEY=your-very-secret-key-here-change-this
ALLOWED_HOSTS=*
DATABASE_URL=postgresql://... (already set by Railway automatically)
```

**Generate a new SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## ✅ Step 2: Verify Settings.py Configuration

These settings have been updated in your `advanced_blog/settings.py`:

- ✓ `ALLOWED_HOSTS = ['*']` - Allows all domains
- ✓ `CSRF_TRUSTED_ORIGINS` - Includes your Railway domain
- ✓ Database URL handling - Works with PostgreSQL
- ✓ Static files with WhiteNoise - Properly configured

---

## ✅ Step 3: Check Procfile and railway.json

Your files have been updated with proper timeout settings:

**Procfile:**
```
web: gunicorn advanced_blog.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60 --access-logfile - --error-logfile -
```

**railway.json:**
```json
{
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn advanced_blog.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60 --access-logfile - --error-logfile -"
  }
}
```

---

## ✅ Step 4: Push Changes to GitHub

```powershell
git add .
git commit -m "Fix Railway deployment - timeout and config issues"
git push origin main
```

---

## ✅ Step 5: Redeploy on Railway

1. Go to Railway Dashboard
2. Click your project: `blog-website-assignment`
3. Go to "Deployments" tab
4. Click the latest deployment
5. Click "Redeploy" button

Or manually trigger:
```bash
railway deploy
```

---

## ✅ Step 6: Monitor Deployment Logs

In Railway Dashboard:
1. Click your project
2. Go to "Deployments" 
3. Click the latest deployment
4. Check "Logs" tab

Look for:
- ✓ "System check identified 0 issues"
- ✓ "Starting development server"
- ✓ No error messages

---

## 🔧 Common Issues & Fixes

### ❌ Issue: "Connection timed out" still appearing

**Fix:**
1. Increase PORT timeout in railway.json (already done - 60s)
2. Check if database connection is working:
   ```bash
   railway run python manage.py dbshell
   ```
3. Restart the deployment

### ❌ Issue: "Static files not loading"

**Fix:**
```bash
railway run python manage.py collectstatic --noinput
```

### ❌ Issue: "Module not found"

**Fix:**
1. Verify requirements.txt is updated:
   ```bash
   pip freeze > requirements.txt
   ```
2. Push changes and redeploy

### ❌ Issue: "Database connection error"

**Fix:**
1. Go to Railway Dashboard
2. Verify PostgreSQL service is connected
3. Check DATABASE_URL environment variable is set
4. Redeploy

---

## 📝 Deployment Checklist

- [ ] Set `DEBUG=False` in Railway variables
- [ ] Set unique `SECRET_KEY` in Railway variables
- [ ] DATABASE_URL is set (PostgreSQL connected)
- [ ] Pushed code to GitHub main branch
- [ ] Deployment started
- [ ] Logs show no errors
- [ ] Website loads at: https://blog-website-assignment-production.up.railway.app
- [ ] Admin panel works: https://blog-website-assignment-production.up.railway.app/admin
- [ ] Can login/register
- [ ] Can create blog posts

---

## 🔍 Test Your Deployment

After deployment is complete:

```bash
# SSH into Railway app and test
railway shell

# Check database
python manage.py dbshell

# Create test superuser
python manage.py createsuperuser

# Check static files
python manage.py collectstatic --noinput
```

---

## 🚀 Your Live URL

```
https://blog-website-assignment-production.up.railway.app
```

---

## 📞 Still Having Issues?

### Check Railway Logs
```bash
railway logs -f  # Follow logs in real-time
```

### Check Specific Service
```bash
railway status
```

### View Environment Variables
```bash
railway variables
```

### Restart Service
```bash
railway down
railway up
```

---

## 📚 Useful Resources

- [Railway Documentation](https://docs.railway.app)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Gunicorn Configuration](https://gunicorn.org/#docs)

---

**Last Updated:** November 9, 2025

