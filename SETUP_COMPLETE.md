# Quick Setup Guide - Railway Superuser

## What I've Done:

✅ Created automatic superuser creation command
✅ Superuser will have 'admin' role in Profile
✅ Command runs automatically on every deployment
✅ Updates existing superuser role if needed

## Next Steps - IMPORTANT:

### 1. Set Environment Variables on Railway (RECOMMENDED)

Go to your Railway dashboard:
1. Open your project at https://railway.app/
2. Click on your service
3. Go to "Variables" tab
4. Click "New Variable" and add these:

```
DJANGO_SUPERUSER_USERNAME = youradmin
DJANGO_SUPERUSER_EMAIL = youremail@example.com
DJANGO_SUPERUSER_PASSWORD = YourSecurePassword123!
```

**Or use the defaults** (less secure):

If you don't add environment variables, these defaults will be used:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123`

### 2. Deploy to Railway

```bash
git add .
git commit -m "Add automatic superuser creation with admin role"
git push
```

### 3. Wait for Deployment

Railway will automatically:
- Run migrations
- **Create superuser with admin role** ✨
- Collect static files
- Start the server

### 4. Login

Visit your site:
```
https://web-production-c529.up.railway.app/accounts/login/
```

Or admin panel directly:
```
https://web-production-c529.up.railway.app/admin/
```

Login with the credentials you set (or defaults).

## What You'll Have:

✅ **Superuser Status** - Full Django superuser privileges
✅ **Admin Role** - Profile.role = 'admin'
✅ **is_staff = True** - Can access Django admin
✅ **is_superuser = True** - All permissions
✅ **is_admin property = True** - Based on profile role

## Verify Your Role:

After logging in, you can verify your role:

1. Go to `/admin/accounts/profile/`
2. Find your profile
3. Role should show "Admin"

Or check in Python shell (Railway):
```python
from django.contrib.auth.models import User
user = User.objects.get(username='admin')
print(user.is_superuser)  # True
print(user.is_staff)      # True
print(user.profile.role)  # 'admin'
print(user.profile.is_admin)  # True
```

## Features You'll Have Access To:

- ✅ Create/Edit/Delete all posts
- ✅ Manage all users
- ✅ Approve/Disapprove comments
- ✅ Manage categories and tags
- ✅ Access Django Admin panel
- ✅ All administrative functions

## Security Note:

⚠️ If using default credentials (`admin/admin123`), **CHANGE THEM IMMEDIATELY** after first login!

Change password via:
1. Admin panel: `/admin/auth/user/` → Click your user → Change password
2. Or via Railway shell: `railway run python manage.py changepassword admin`

---

**Ready to deploy!** Just commit and push the changes. 🚀
