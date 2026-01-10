"""
Django settings for aknova_project project.
"""

from pathlib import Path
import os
import environ

# -----------------------------------------------------------------
# Configuration de Django-Environ
# -----------------------------------------------------------------
env = environ.Env(
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Lecture du fichier .env (s'il existe)
if os.path.exists(os.path.join(BASE_DIR, '.env')):
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# -----------------------------------------------------------------

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['.vercel.app', '127.0.0.1', 'localhost', 'aknova.bj', "www.aknova.bj"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- INDISPENSABLE POUR LE STYLE
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aknova_project.urls'

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


# Database
DATABASES = {
    'default': env.db()
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]


# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# -----------------------------------------------------------------
# GESTION DES FICHIERS STATIQUES (CSS, JS, IMAGES)
# -----------------------------------------------------------------

STATIC_URL = '/static/'

# Dossier où Django va rassembler tous les fichiers pour Vercel
STATIC_ROOT = BASE_DIR / 'staticfiles'

# On regarde dans 'static' ET 'assets' pour être sûr de ne rien rater
STATICFILES_DIRS = []
if (BASE_DIR / 'static').exists():
    STATICFILES_DIRS.append(BASE_DIR / 'static')
if (BASE_DIR / 'assets').exists():
    STATICFILES_DIRS.append(BASE_DIR / 'assets')

# --- CORRECTION DJANGO 5 ---
# On utilise la nouvelle syntaxe STORAGES au lieu de STATICFILES_STORAGE
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# settings.py

# URL "virtuelle" pour Django (optionnelle, souvent pour admin)
MEDIA_URL = "/media/"

# On ne définit pas de MEDIA_ROOT local
# MEDIA_ROOT = BASE_DIR / 'media'   <-- supprimer ou commenter

# Backend de stockage pour envoyer les fichiers sur Supabase
DEFAULT_FILE_STORAGE = "core.storage_backends.SupabaseStorage"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------------------
# CONFIGURATION EMAIL SMTP (GMAIL)
# -----------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('AKNOVA_EMAIL_USER')
EMAIL_HOST_PASSWORD = env('AKNOVA_EMAIL_PASS')
DEFAULT_FROM_EMAIL = f"Aknova Site Web <{env('AKNOVA_EMAIL_USER')}>"
