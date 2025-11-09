# Superuser Setup for Railway Deployment

## Automatic Superuser Creation

The application will automatically create a superuser on deployment using the management command `create_superuser_auto`.

## Setting Up Credentials on Railway

### Step 1: Go to Railway Dashboard
1. Visit https://railway.app/
2. Go to your project
3. Click on your service (Blog App)

### Step 2: Add Environment Variables
Click on the **Variables** tab and add these three variables:

```
DJANGO_SUPERUSER_USERNAME=your_admin_username
DJANGO_SUPERUSER_EMAIL=your_email@example.com
DJANGO_SUPERUSER_PASSWORD=your_secure_password
```

**Example:**
```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@blogapp.com
DJANGO_SUPERUSER_PASSWORD=SecurePass123!
```

### Step 3: Redeploy
After adding the variables, Railway will automatically redeploy your application.

### Step 4: Login
Once deployed, you can login at:
```
https://web-production-c529.up.railway.app/admin/
```

**Or** login from the main site at:
```
https://web-production-c529.up.railway.app/accounts/login/
```

## Default Credentials (If No Environment Variables Set)

If you don't set environment variables, the default credentials will be:
- **Username:** admin
- **Email:** admin@example.com
- **Password:** admin123

⚠️ **Security Warning:** Change these default credentials immediately in production!

## Verifying Superuser Creation

Check the deployment logs on Railway to see the message:
```
Superuser "admin" created successfully!
```

Or if it already exists:
```
Superuser "admin" already exists.
```

## User Roles

When you login with the superuser account:
- ✅ You will have **admin/superuser** status
- ✅ Full access to Django Admin panel at `/admin/`
- ✅ Can create, edit, and delete all posts, categories, tags, and comments
- ✅ Can manage all users
- ✅ Staff status enabled automatically

## Accessing Admin Features

Once logged in as superuser:

1. **Django Admin Panel:**
   - Go to `/admin/` URL
   - Full administrative interface

2. **Frontend Admin Actions:**
   - Create posts at `/post/create/`
   - Edit/delete your own posts
   - Manage comments

## Troubleshooting

### Superuser not created?
Check Railway logs for error messages.

### Can't login?
1. Verify environment variables are set correctly
2. Check deployment logs
3. Try default credentials if no env vars set

### Want to change password?
Use Railway shell:
```bash
railway run python manage.py changepassword admin
```

Or create a new superuser:
```bash
railway run python manage.py createsuperuser
```
