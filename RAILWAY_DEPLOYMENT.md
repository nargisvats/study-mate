# Railway Deployment Guide for StudyMate

This guide will help you deploy the StudyMate Django application to Railway.

## Prerequisites

- A Railway account (sign up at https://railway.app)
- Git installed and configured
- The project committed to a Git repository

## Step 1: Prepare Your Project

All necessary configuration files have been created:

- ✅ `Procfile` - Defines how Railway runs your app
- ✅ `runtime.txt` - Specifies Python 3.11.9
- ✅ `requirements.txt` - Updated with production dependencies (gunicorn, whitenoise, dj-database-url)
- ✅ `studymate/settings.py` - Updated for production

## Step 2: Set Up a Git Repository

If you haven't already, initialize and commit your project:

```bash
git init
git add .
git commit -m "Initial commit - Ready for Railway deployment"
git remote add origin https://github.com/YOUR_USERNAME/studymate.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Railway

### Option A: Railway CLI (Recommended)

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Create a new project:**
   ```bash
   railway init
   ```
   - Choose a project name
   - Select "Empty Project"

4. **Add a PostgreSQL database:**
   ```bash
   railway add
   ```
   - Select "PostgreSQL"

5. **Deploy your project:**
   ```bash
   railway up
   ```

### Option B: Railway Dashboard (Web UI)

1. Go to https://railway.app/dashboard
2. Click **New Project**
3. Select **Deploy from GitHub**
4. Authorize Railway with your GitHub account
5. Select your `studymate` repository
6. Railway will auto-detect the `Procfile` and deploy

## Step 4: Configure Environment Variables

After deployment, set these environment variables in Railway:

### Required Variables:

```env
SECRET_KEY=your-very-secret-key-generate-a-new-one
DEBUG=False
ALLOWED_HOSTS=your-railway-url.railway.app

# Database is auto-configured via DATABASE_URL
# You only need to add if using MySQL instead:
# USE_MYSQL=true
# DB_NAME=studymate
# DB_USER=root
# DB_PASSWORD=your-password
# DB_HOST=your-mysql-host
# DB_PORT=3306

# Payment Settings
PAYMENT_PROVIDER=mock  # or "stripe" for production
STRIPE_SECRET_KEY=sk_live_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Live Session Provider
LIVE_PROVIDER=jitsi  # or "daily" for Daily.co
DAILY_API_KEY=your_daily_api_key_if_using_daily
JITSI_DOMAIN=meet.jit.si

# Platform Settings
PLATFORM_FEE_PERCENT=10
SITE_URL=https://your-railway-url.railway.app

# Email Settings (Optional but recommended)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password  # Use app-specific password for Gmail
DEFAULT_FROM_EMAIL=noreply@studymate.app

# File Upload
FILE_UPLOAD_MAX_MEMORY_SIZE=10485760
```

## Step 5: Run Database Migrations

After deployment, you need to run migrations on the deployed database:

### Using Railway CLI:
```bash
railway run python manage.py migrate
railway run python manage.py seed_subjects
railway run python manage.py seed_demo
```

### Using Railway Dashboard:
1. Go to your project in Railway
2. Open the **Terminal** tab
3. Run:
   ```bash
   python manage.py migrate
   python manage.py seed_subjects
   python manage.py seed_demo
   ```

## Step 6: Create a Superuser (Optional)

To access Django admin:

```bash
railway run python manage.py createsuperuser
```

Then access admin at: `https://your-railway-url.railway.app/admin/`

## Step 7: Set Up Logs & Monitoring

In Railway Dashboard:
- **Logs tab:** View real-time logs
- **Metrics tab:** Monitor CPU, RAM, and request latency
- **Monitoring:** Set up alerts for failures

## Troubleshooting

### "ModuleNotFoundError" on Deploy

**Issue:** Missing dependencies
**Solution:** Make sure `requirements.txt` is up-to-date:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### "DisallowedHost" Error

**Issue:** ALLOWED_HOSTS misconfiguration
**Solution:** Set `ALLOWED_HOSTS` to your Railway domain:
```
ALLOWED_HOSTS=your-app-name.railway.app,*.railway.app
```

### "Static files not loading"

**Solution:** Railway automatically collects static files via the Procfile, which runs:
```bash
python manage.py migrate && gunicorn studymate.wsgi
```

If needed, manually collect:
```bash
railway run python manage.py collectstatic --noinput
```

### Database Connection Issues

**Solution:** Verify DATABASE_URL is set:
```bash
railway variables
```

If missing, add PostgreSQL:
```bash
railway add postgresql
```

## Redeploy After Code Changes

Simply push to your main branch:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Railway will auto-detect changes and redeploy.

## Production Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Generate a secure `SECRET_KEY`
- [ ] Configure ALLOWED_HOSTS for your domain
- [ ] Set up email configuration
- [ ] Configure payment provider (Stripe)
- [ ] Set SITE_URL to your production domain
- [ ] Enable HTTPS (Railway does this automatically)
- [ ] Back up your database regularly
- [ ] Monitor logs for errors
- [ ] Set up error tracking (optional: Sentry)

## Next Steps

1. **Custom Domain:** In Railway > Project > Domains > Add Custom Domain
2. **Environment-Specific Settings:** Create separate `.env` files for staging/production
3. **CI/CD Improvements:** Set up automated testing before deploy
4. **Database Backups:** Enable Railway's backup feature

---

For more help, visit Railway docs: https://docs.railway.app
