# Required Railway Environment Variables

Add these environment variables in your Railway dashboard:

## Essential Variables:

```
DEBUG=False
SECRET_KEY=your-secret-key-here-generate-a-new-one
ALLOWED_HOSTS=.railway.app,.up.railway.app
```

## Database (Auto-configured by Railway):
```
DATABASE_URL=postgresql://... (automatically set by Railway if you add PostgreSQL)
```

## Superuser Credentials:
```
DJANGO_SUPERUSER_USERNAME=your_admin_username
DJANGO_SUPERUSER_EMAIL=your_email@example.com
DJANGO_SUPERUSER_PASSWORD=your_secure_password
```

## Optional but Recommended:
```
DJANGO_SETTINGS_MODULE=advanced_blog.settings
PORT=8000
```

---

## Current Issue Fix:

If your website crashed when trying to login, it's likely due to:
1. Missing profile for the user
2. Signal errors
3. Database not migrated properly

I've now added:
- ✅ Better error handling in profile signals
- ✅ Improved superuser creation command with error catching
- ✅ Logging configuration
- ✅ Safe profile creation with `get_or_create`

## Next Steps:

1. Commit and push these fixes:
   ```
   git add .
   git commit -m "Fix profile creation and add error handling"
   git push
   ```

2. Wait for Railway to redeploy

3. Check Railway logs for any errors

4. Try logging in again

5. If still having issues, you may need to run migrations manually via Railway shell:
   ```
   railway run python manage.py migrate
   railway run python manage.py create_superuser_auto
   ```
