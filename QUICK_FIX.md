# 🎯 RAILWAY DEPLOYMENT - 3 STEP FIX

## Your Live URL (Update soon!)
```
https://blog-website-assignment-production-ecbd.up.railway.app
```

---

## 🔴 STEP 1: Set Environment Variables (5 minutes)

### Go to Railway Dashboard:
https://railway.app

### Click Your Project:
- Project name: `blog-website-assignment`

### Go to Settings:
- Click **Settings** tab (or gear icon)
- Click **Variables**

### Add These 3 Variables:

```
1. DEBUG = False
2. PYTHONUNBUFFERED = 1
3. SECRET_KEY = [GENERATE BELOW]
```

### Generate SECRET_KEY:
Open PowerShell and run:
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output (long random string) and paste as SECRET_KEY value.

**Example:**
```
DEBUG = False
PYTHONUNBUFFERED = 1
SECRET_KEY = django-insecure-s_)9z#!@9k)_7@^&z$^@s_)9z#!@9k)_7@^&z$^@
```

### Click "Save" or "Update"

✅ Step 1 Complete!

---

## 🟡 STEP 2: Verify PostgreSQL (2 minutes)

### Still in Railway Dashboard:

### Check Your Services:
Look for these cards in your project:

```
✅ blog-website-assignment (App service)
✅ PostgreSQL (Database service)
```

### If PostgreSQL is MISSING:
1. Click **"New"** button
2. Click **"Database"**
3. Select **"PostgreSQL"**
4. Railway will auto-create DATABASE_URL

✅ Step 2 Complete!

---

## 🟢 STEP 3: Trigger Redeploy (2-5 minutes)

### In Railway Dashboard:

### Option A: Manual Redeploy (Recommended)
1. Click **"Deployments"** tab
2. Find the latest deployment
3. Click **"..."** (three dots menu)
4. Click **"Redeploy"**
5. Watch the build progress

### Option B: Auto Redeploy (Push code)
```powershell
# In your PowerShell
git add .
git commit -m "Trigger redeploy"
git push origin main
```

### Railway will auto-redeploy when code is pushed ✅

---

## ⏳ WAIT FOR DEPLOYMENT

Look for:
- 🔵 Blue circle = Building
- 🟢 Green checkmark = Deployed successfully
- 🔴 Red X = Deployment failed

**Usually takes 2-5 minutes**

---

## ✅ TEST YOUR SITE

Once you see green checkmark, visit:

### Main Site:
```
https://blog-website-assignment-production-ecbd.up.railway.app
```

### Admin Panel:
```
https://blog-website-assignment-production-ecbd.up.railway.app/admin
```

### Login:
```
https://blog-website-assignment-production-ecbd.up.railway.app/accounts/login
```

---

## 🎉 SUCCESS INDICATORS

✅ Homepage loads with blog posts  
✅ CSS/images display correctly  
✅ Admin panel accessible  
✅ Can login/register  
✅ No 502/504 errors  
✅ No timeout messages  

---

## ❌ STILL NOT WORKING?

### Check Railway Logs:
1. Go to Deployments tab
2. Click latest deployment
3. Click "Logs"
4. Look for error messages

### Most Common Issues:

| Error | Fix |
|-------|-----|
| "ModuleNotFoundError" | Check requirements.txt has all packages |
| "Connection refused" | Verify DATABASE_URL is set |
| "Secret key not set" | Add SECRET_KEY variable to Railway |
| "Timeout" | Already fixed in code |

---

## 📝 SUMMARY

| What | Status |
|------|--------|
| Code pushed | ✅ Done |
| Procfile updated | ✅ Done |
| Settings fixed | ✅ Done |
| Environment vars | ⏳ **YOU DO THIS** |
| PostgreSQL check | ⏳ **YOU DO THIS** |
| Redeploy | ⏳ **YOU DO THIS** |
| Test site | ⏳ **YOU DO THIS** |

---

**🚀 After these 3 steps, your site will be live!**

Need help? Check Railway logs or reach out!

