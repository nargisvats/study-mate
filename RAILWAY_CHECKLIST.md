# Railway Deployment Quick Checklist

Complete this checklist before deploying to Railway.

## Pre-Deployment ✅

- [ ] Update all code and commit to git
- [ ] Test locally with `python manage.py runserver`
- [ ] Run migrations locally: `python manage.py migrate`
- [ ] Update requirements.txt: `pip freeze > requirements.txt`

## Code Preparation ✅

- [ ] `Procfile` exists and is correct
- [ ] `runtime.txt` exists with Python version
- [ ] `requirements.txt` includes gunicorn, dj-database-url, whitenoise
- [ ] `.gitignore` includes `.env`, `db.sqlite3`, `.venv/`
- [ ] `studymate/settings.py` has Railway database configuration

## Environment Variables ✅

Before deploying, gather these values (you'll set them in Railway):

```
SECRET_KEY = ___________________________
ALLOWED_HOSTS = your-app.railway.app
DEBUG = False

STRIPE_SECRET_KEY = sk_live_________________
STRIPE_PUBLISHABLE_KEY = pk_live_________________
STRIPE_WEBHOOK_SECRET = whsec_________________

LIVE_PROVIDER = jitsi (or "daily")
DAILY_API_KEY = _________________ (if using Daily.co)

SITE_URL = https://your-app.railway.app

EMAIL_HOST = smtp.gmail.com
EMAIL_HOST_USER = your-email@gmail.com
EMAIL_HOST_PASSWORD = your-app-password

PAYMENT_PROVIDER = mock (or "stripe" for production)
PLATFORM_FEE_PERCENT = 10
```

## Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### 2. Deploy via Railway Dashboard
- Visit https://railway.app/dashboard
- Click "New Project"
- Select "Deploy from GitHub"
- Choose your `studymate` repository
- Click "Deploy"

### 3. Add Database
- In Railway project, click "Add"
- Select "PostgreSQL"
- Link it to your project
- Railway will automatically set `DATABASE_URL`

### 4. Set Environment Variables
In Railway Project Settings:
- Go to **Variables** tab
- Add all variables from the Environment Variables section above
- Click "Save"

### 5. Deploy the App
- Railway will auto-deploy when you push to GitHub
- Or click the deploy button manually

### 6. Run Migrations
```bash
railway run python manage.py migrate
railway run python manage.py seed_subjects
railway run python manage.py seed_demo
```

### 7. Create Superuser (Optional)
```bash
railway run python manage.py createsuperuser
```

### 8. Verify Deployment
- Check Railway Logs for errors
- Visit your Railway URL
- Try logging in with demo accounts
- Check `/admin/` with your superuser account

## Post-Deployment ✅

- [ ] Test all features in production
- [ ] Set up custom domain (if needed)
- [ ] Configure email notifications
- [ ] Set up error monitoring (Sentry)
- [ ] Configure backups for database
- [ ] Test payment processing (with Stripe test keys first)

## Troubleshooting

### "Application error" or "502 Bad Gateway"
- Check logs: Railway > Project > Logs tab
- Ensure `DEBUG=False` is set
- Verify all required environment variables are set
- Run: `railway run python manage.py check`

### Static files not loading
- Run: `railway run python manage.py collectstatic --noinput`
- Verify `STATICFILES_STORAGE` is set correctly in settings.py

### Database connection error
- Verify PostgreSQL is added to project
- Check `DATABASE_URL` is set in variables
- Ensure migrations are run

### Email not sending
- Check `EMAIL_HOST` and credentials
- For Gmail: Use app-specific password (not regular password)
- Enable "Less secure app access" or use app passwords
- Test locally first with console backend

## Useful Commands

```bash
# View logs in real-time
railway logs -f

# SSH into running instance
railway shell

# Run Django commands
railway run python manage.py shell
railway run python manage.py createsuperuser
railway run python manage.py migrate --plan

# View environment variables
railway variables

# Deploy manually
railway up

# Pull production database for local testing (CAREFUL!)
# This copies production DB to local - use only for debugging
railway run python manage.py dumpdata > production_backup.json
```

## Production Checklist

- [ ] `DEBUG=False` in production
- [ ] `SECRET_KEY` is unique and random
- [ ] `ALLOWED_HOSTS` includes your domain
- [ ] Database is PostgreSQL (not SQLite)
- [ ] Email is configured and tested
- [ ] Stripe keys are production keys (not test keys)
- [ ] HTTPS is enabled (Railway default)
- [ ] All sensitive data in environment variables (not in code)
- [ ] Backups are configured
- [ ] Error monitoring is set up

## Need Help?

- Railway Docs: https://docs.railway.app
- Django Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
- StudyMate README: See RAILWAY_DEPLOYMENT.md for detailed guide

---

Once deployment is complete, share your Railway URL and enjoy StudyMate in production! 🚀
