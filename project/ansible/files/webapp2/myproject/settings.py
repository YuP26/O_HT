from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'replace-me-in-production')
DEBUG = bool(int(os.getenv('DJANGO_DEBUG', '1')))
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'notes' / 'templates'],
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

WSGI_APPLICATION = 'myproject.wsgi.application'
ASGI_APPLICATION = 'myproject.asgi.application'

DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.mysql",
        "NAME":     "webapp_db",
        "USER":     "webapp",
        "PASSWORD": "secret",
        "HOST":     "192.168.56.30",  # ← адрес master-сервера БД
        "PORT":     "3306",
        "OPTIONS":  {"charset": "utf8mb4"},
        "CONN_MAX_AGE": 60,
    },
    "replica": {
        "ENGINE":   "django.db.backends.mysql",
        "NAME":     "webapp_db",
        "USER":     "webapp",
        "PASSWORD": "secret",
        "HOST":     "192.168.56.31",  # ← адрес slave-сервера
        "PORT":     "3306",
        "OPTIONS":  {"charset": "utf8mb4", "init_command": "SET sql_log_bin=0;"},
        "CONN_MAX_AGE": 60,
    },
}

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

CSRF_TRUSTED_ORIGINS = [
    "https://192.168.56.10",  
    "https://notus.local"
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
