import dj_database_url

import os
from pathlib import Path
from dotenv import load_dotenv


APP_VERIFY_TOKEN = os.getenv("APP_VERIFY_TOKEN", "")

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = [
    "127.0.0.1", "localhost",
    "wh.sistemasfisco.com.br", "mei.sistemasfisco.com.br",
    # Adicionar o domínio do Render
    ".render.com",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts',
    'apps.dashboard',
    'apps.mei',
    'apps.finance',
    'apps.nfe',
    'apps.chat',
    'apps.sales',
    'apps.whatsapp',
    'apps.das_mei',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fiscomei.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'fiscomei.wsgi.application'

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': BASE_DIR / 'db.sqlite3'}
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = os.getenv('TIME_ZONE', 'America/Fortaleza')
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard:index'
LOGOUT_REDIRECT_URL = 'login'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CSRF_TRUSTED_ORIGINS = [
    "https://mei.sistemasfisco.com.br",
    "https://wh.sistemasfisco.com.br",
    "https://smile.sistemasfisco.com.br",
]

ALLOWED_HOSTS = [
    "localhost", "127.0.0.1",
    "mei.sistemasfisco.com.br",
    "wh.sistemasfisco.com.br",
    "smile.sistemasfisco.com.br",
    # Adicionar o domínio do Render
    ".render.com",
]


# Render Postgres via DATABASE_URL
_db_url = os.getenv("DATABASE_URL")
if _db_url:
    DATABASES["default"] = dj_database_url.parse(_db_url, conn_max_age=600, ssl_require=False)

