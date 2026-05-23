# Railway Deployment Troubleshooting

## "Application failed to respond" Error

This error typically means the Django app is crashing on startup. Follow these steps:

## Step 1: Check Railway Logs

### Via Railway CLI:
```bash
railway logs -f
```

### Via Railway Dashboard:
1. Go to https://railway.app/dashboard
2. Select your project
3. Click **Logs** tab
4. Look for error messages in red

**Common errors:**
- `ModuleNotFoundError` - Missing dependencies
- `psycopg2` error - Database not connected
- `DisallowedHost` - ALLOWED_HOSTS misconfigured
- `OperationalError` - Database migration failed

---

## Step 2: Verify Environment Variables are Set

In Railway Dashboard:
1. Go to Project > **Variables** tab
2. Verify these REQUIRED variables exist:

```
SECRET_KEY = (should have a value)
DEBUG = False
ALLOWED_HOSTS = your-app-name.railway.app
DATABASE_URL = (should be set automatically if PostgreSQL is added)
```

If `DATABASE_URL` is missing:
- Go to **Service > Add**
- Select **PostgreSQL**
- Confirm it's linked to your project
- Railway will auto-set DATABASE_URL

---

## Step 3: Set ALLOWED_HOSTS Correctly

The most common issue is ALLOWED_HOSTS. Set it to your Railway domain:

```
ALLOWED_HOSTS=your-app-name.railway.app
```

Or if you want to accept multiple domains:
```
ALLOWED_HOSTS=your-app-name.railway.app,your-domain.com
```

---

## Step 4: Verify Database is Connected

Run these commands via Railway:

```bash
# Check environment variables
railway variables

# Test database connection
railway run python manage.py dbshell

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser
```

---

## Step 5: Force Redeploy

After making changes:

```bash
# Push changes to GitHub
git add .
git commit -m "Fix deployment issues"
git push origin main

# Or manually redeploy
railway trigger
```

---

## Common Fixes

### Fix 1: Enable DEBUG to See Errors (Temporary)

Set in Railway Variables:
```
DEBUG = True
```

This will show detailed error messages. **Remember to set back to False after debugging!**

### Fix 2: Collect Static Files

```bash
railway run python manage.py collectstatic --noinput
```

### Fix 3: Check Python/Django Versions

```bash
railway run python --version
railway run python -m django --version
```

### Fix 4: Test Basic Functionality

```bash
railway run python manage.py check
```

This runs Django's system check framework.

---

## Quick Checklist

- [ ] PostgreSQL database is added to project
- [ ] DATABASE_URL is visible in Variables
- [ ] ALLOWED_HOSTS set to your Railway domain
- [ ] SECRET_KEY is set to a secure value
- [ ] DEBUG = False in production
- [ ] Procfile exists and is correct
- [ ] runtime.txt specifies Python version
- [ ] requirements.txt has all dependencies
- [ ] Migrations have been run
- [ ] Static files collected (handled by Procfile)

---

## Need More Help?

1. **Check detailed logs:**
   ```bash
   railway logs --pageSize 100
   ```

2. **SSH into the running container:**
   ```bash
   railway shell
   ```

3. **Check Railway docs:**
   https://docs.railway.app/reference/cli-commands

4. **Check Django error page:**
   If DEBUG=True, visit your app URL and look for detailed error messages

---

## If Still Stuck

Share the error from:
- `railway logs` output
- Variables configuration
- Recent git commits

This will help identify the exact issue!
