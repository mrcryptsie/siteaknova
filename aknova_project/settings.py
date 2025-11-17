"""
Django settings for aknova_project project.
...
"""

from pathlib import Path
import os
import environ  # <-- Import de django-environ

# -----------------------------------------------------------------
# Configuration de Django-Environ (pour lire le fichier .env)
# -----------------------------------------------------------------
env = environ.Env(
    # Définir les valeurs par défaut et le type (ex: DEBUG sera un booléen)
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Lecture du fichier .env qui doit être à la racine (BASE_DIR)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
# -----------------------------------------------------------------


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# Lit la SECRET_KEY depuis le fichier .env
SECRET_KEY = env('SECRET_KEY')

# Lit DEBUG depuis le fichier .env (converti en booléen)
DEBUG = env('DEBUG')

# Autorise votre URL de production et le local
ALLOWED_HOSTS = ['.vercel.app', '127.0.0.1']


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
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# --- BLOC DATABASES MIS À JOUR ---
DATABASES = {
    # Lit la variable DATABASE_URL depuis le .env et la configure
    'default': env.db()
}
# --- FIN DU BLOC ---


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i1n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static', # Le dossier où nous copierons vos 'assets'
]
STATIC_ROOT = BASE_DIR / 'staticfiles' # Pour le déploiement

# --- AJOUTEZ CETTE LIGNE ---
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

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