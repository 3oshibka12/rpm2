import os
from pathlib import Path

# Базовые пути
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-test-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'core',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cinema_conf.urls'
WSGI_APPLICATION = 'cinema_conf.wsgi.application'

# ТЕ САМЫЕ ШАБЛОНЫ ДЛЯ АДМИНКИ (Решение твоей ошибки)
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

# Настройки подключения к PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'cinema_db'),
        'USER': os.environ.get('DB_USER', 'cinema_user'),
        'PASSWORD': os.environ.get('DB_PASS', 'cinema_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'cinema_db'),
        'USER': os.environ.get('DB_USER', 'cinema_user'),
        'PASSWORD': os.environ.get('DB_PASS', 'cinema_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    },
    'replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'cinema_db'),
        'USER': os.environ.get('DB_USER', 'cinema_user'),
        'PASSWORD': os.environ.get('DB_PASS', 'cinema_password'),
        'HOST': os.environ.get('DB_REPLICA_HOST', 'localhost'),
        'PORT': os.environ.get('DB_REPLICA_PORT', '5434'),
    }
}

DATABASES['shard_0'] = {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'cinema_db', 'USER': 'cinema_user', 'PASSWORD': 'cinema_password', 'HOST': 'shard_0', 'PORT': '5432'}
DATABASES['shard_1'] = {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'cinema_db', 'USER': 'cinema_user', 'PASSWORD': 'cinema_password', 'HOST': 'shard_1', 'PORT': '5432'}
DATABASES['shard_2'] = {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'cinema_db', 'USER': 'cinema_user', 'PASSWORD': 'cinema_password', 'HOST': 'shard_2', 'PORT': '5432'}
DATABASES['shard_3'] = {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'cinema_db', 'USER': 'cinema_user', 'PASSWORD': 'cinema_password', 'HOST': 'shard_3', 'PORT': '5432'}

# Настройки Django REST Framework и Swagger
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Статические файлы (чтобы Swagger был красивым)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Прочие системные настройки
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ = True


# DATABASE_ROUTERS = ['core.routers.ReplicaRouter']