"""
Django settings for aknova_project project.
"""

from pathlib import Path
import os
import environ

# -----------------------------------------------------------------
# Configuration Django-Environ
# -----------------------------------------------------------------
env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

if os.path.exists(os.path.join(BASE_DIR, '.env')):
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# -----------------------------------------------------------------

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = [
    '.vercel.app',
    '127.0.0.1',
    'localhost',
    'aknova.bj',
    'www.aknova.bj',
]

# -----------------------------------------------------------------
# Applications
# -----------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

# -----------------------------------------------------------------
# Middleware
# -----------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aknova_project.urls'

# -----------------------------------------------------------------
# Templates
# -----------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'aknova_project.wsgi.application'

# -----------------------------------------------------------------
# Database
# -----------------------------------------------------------------

DATABASES = {
    'default': env.db()
}

# -----------------------------------------------------------------
# Password validation
# -----------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------------------------------------------
# Internationalization
# -----------------------------------------------------------------

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------
# Static & Media (DJANGO 5 – PROPRE)
# -----------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = []
if (BASE_DIR / 'static').exists():
    STATICFILES_DIRS.append(BASE_DIR / 'static')
if (BASE_DIR / 'assets').exists():
    STATICFILES_DIRS.append(BASE_DIR / 'assets')

MEDIA_URL = "/media/"

# ⚠️ DJANGO 5 : STORAGES FAIT FOI
STORAGES = {
    "default": {
        "BACKEND": "core.storage_backends.SupabaseStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ❌ NE PLUS UTILISER EN DJANGO 5
# DEFAULT_FILE_STORAGE = ...
# MEDIA_ROOT = ...

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------------------------------------
# Email (SMTP Gmail)
# -----------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('AKNOVA_EMAIL_USER')
EMAIL_HOST_PASSWORD = env('AKNOVA_EMAIL_PASS')
DEFAULT_FROM_EMAIL = f"Aknova Site Web <{env('AKNOVA_EMAIL_USER')}>"
