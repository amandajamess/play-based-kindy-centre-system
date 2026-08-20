"""
Django settings for myproject project.

Originally generated using Django 4.1.4.
Updated for local development + Render deployment.
"""

import os
from pathlib import Path

import dj_database_url


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SECURITY SETTINGS
# =========================================================

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'temporary-local-development-key-change-this-later'
)

# True locally by default.
# On Render we will set DEBUG=False.
DEBUG = os.environ.get(
    'DEBUG',
    'True'
).lower() == 'true'


# Local hosts
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

# Render automatically provides this hostname.
RENDER_EXTERNAL_HOSTNAME = os.environ.get(
    'RENDER_EXTERNAL_HOSTNAME'
)

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Optional additional hosts from environment variable
EXTRA_ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    ''
)

if EXTRA_ALLOWED_HOSTS:
    ALLOWED_HOSTS.extend(
        [
            host.strip()
            for host in EXTRA_ALLOWED_HOSTS.split(',')
            if host.strip()
        ]
    )


# =========================================================
# CSRF TRUSTED ORIGINS
# =========================================================

CSRF_TRUSTED_ORIGINS = []

if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(
        f'https://{RENDER_EXTERNAL_HOSTNAME}'
    )


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project applications
    'app',
    'additem',
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise must come immediately after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =========================================================
# URL CONFIGURATION
# =========================================================

ROOT_URLCONF = 'myproject.urls'


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates',
        ],

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


# =========================================================
# WSGI
# =========================================================

WSGI_APPLICATION = 'myproject.wsgi.application'


# =========================================================
# DATABASE
# =========================================================

# LOCAL DEVELOPMENT
# If DATABASE_URL does not exist, Django continues using SQLite.

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:

    # ONLINE / RENDER PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

else:

    # LOCAL SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',

        'OPTIONS': {
            'min_length': 8,
        },
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


# WhiteNoise static file storage
STORAGES = {
    'default': {
        'BACKEND':
        'django.core.files.storage.FileSystemStorage',
    },

    'staticfiles': {
        'BACKEND':
        'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}


# =========================================================
# MEDIA FILES
# =========================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================================================
# LOGIN / LOGOUT
# =========================================================

LOGIN_URL = '/login/'

LOGOUT_REDIRECT_URL = '/'

LOGIN_REDIRECT_URL = '/'


# =========================================================
# EMAIL CONFIGURATION
# =========================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True


EMAIL_HOST_USER = os.environ.get(
    'EMAIL_HOST_USER',
    ''
)

EMAIL_HOST_PASSWORD = os.environ.get(
    'EMAIL_HOST_PASSWORD',
    ''
)

DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL',
    EMAIL_HOST_USER
)


# =========================================================
# PRODUCTION SECURITY
# =========================================================

# These settings activate only when DEBUG=False.

if not DEBUG:

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_PROXY_SSL_HEADER = (
        'HTTP_X_FORWARDED_PROTO',
        'https'
    )