"""
Django settings for my_app project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^y1p205fuz*!*rh=x5@eo-&o5^musb0zbw7e396ji@y7nx!la%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'lawyer_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'lawyer_app.middleware.NoCacheMiddleware',
]

ROOT_URLCONF = 'my_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

SUPABASE_DB_NAME = os.getenv('SUPABASE_DB_NAME')
SUPABASE_USER = os.getenv('SUPABASE_USER')
SUPABASE_PASSWORD = os.getenv('SUPABASE_PASSWORD')
SUPABASE_HOST = os.getenv('SUPABASE_HOST')
SUPABASE_PORT = os.getenv('SUPABASE_PORT')

# print("Database Name:", SUPABASE_DB_NAME)
# print("User:", SUPABASE_USER)
# print("Password:", SUPABASE_PASSWORD)
# print("Host:", SUPABASE_HOST)
# print("Port:", SUPABASE_PORT)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': SUPABASE_DB_NAME,  # New database name
        'USER': SUPABASE_USER,  # Supabase user
        'PASSWORD': SUPABASE_PASSWORD,  # Supabase password
        'HOST': SUPABASE_HOST,  # Supabase host
        'PORT': SUPABASE_PORT,  # Supabase port
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = r'lawyer_app.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_TEMPLATE_PACK = 'bootstrap4'


#SESSION_COOKIE_AGE = 60*60



GMAIL_PORT=os.getenv('GMAIL_PORT')
GMAIL_HOST=os.getenv('GMAIL_HOST')
GMAIL_USE_TLS=os.getenv('GMAIL_USE_TLS',True)
GMAIL_HOST_USER=os.getenv('GMAIL_HOST_USER')
GMAIL_HOST_PASSWORD=os.getenv('GMAIL_HOST_PASSWORD')
GMAIL_FROM_EMAIL=os.getenv('GMAIL_FROM_EMAIL')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = GMAIL_HOST
EMAIL_PORT = GMAIL_PORT
EMAIL_USE_TLS = GMAIL_USE_TLS
EMAIL_HOST_USER = GMAIL_HOST_USER
EMAIL_HOST_PASSWORD = GMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = GMAIL_FROM_EMAIL

SITE_URL=os.getenv('SITE_URL','http://localhost:8000')