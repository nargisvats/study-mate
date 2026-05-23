"""StudyMate Django settings."""
import os
from pathlib import Path

from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-studymate-dev-key-change-in-production")
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "profiles",
    "catalog",
    "scheduling",
    "payments",
    "sessions_live",
    "reviews",
    "notifications",
    "admin_ops",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "studymate.urls"
WSGI_APPLICATION = "studymate.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "studymate.context_processors.site_settings",
            ],
        },
    },
]

# Database configuration - Railway provides DATABASE_URL
if "DATABASE_URL" in os.environ:
    # Railway PostgreSQL
    DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"), conn_max_age=600)}
else:
    USE_MYSQL = os.environ.get("USE_MYSQL", "false").lower() == "true"
    if USE_MYSQL:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": os.environ.get("DB_NAME", "studymate"),
                "USER": os.environ.get("DB_USER", "root"),
                "PASSWORD": os.environ.get("DB_PASSWORD", ""),
                "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
                "PORT": os.environ.get("DB_PORT", "3306"),
                "OPTIONS": {"charset": "utf8mb4"},
            }
        }
    else:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }

AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:post_login_redirect"
LOGOUT_REDIRECT_URL = "home"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# StudyMate platform settings
PAYMENT_PROVIDER = os.environ.get("PAYMENT_PROVIDER", "mock")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
LIVE_PROVIDER = os.environ.get("LIVE_PROVIDER", "jitsi")
DAILY_API_KEY = os.environ.get("DAILY_API_KEY", "")
JITSI_DOMAIN = os.environ.get("JITSI_DOMAIN", "meet.jit.si")
PLATFORM_FEE_PERCENT = int(os.environ.get("PLATFORM_FEE_PERCENT", "10"))
SITE_URL = os.environ.get("SITE_URL", "http://127.0.0.1:8000")

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@studymate.local")

FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# ========================
# PRODUCTION SECURITY SETTINGS
# ========================
# Set SECURE_SSL_REDIRECT to True in production (Railway handles HTTPS)
SECURE_SSL_REDIRECT = not DEBUG and os.environ.get("ENVIRONMENT") == "production"
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
}

# Allow Railway domain and custom domains
if SITE_URL != "http://127.0.0.1:8000":
    CSRF_TRUSTED_ORIGINS = [SITE_URL]

# WhiteNoise static files handling
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
