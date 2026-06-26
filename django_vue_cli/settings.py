from pathlib import Path
import sys
import os
from datetime import timedelta

# lib文件夹中手动导入的第三方库
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(1, os.path.join(os.getcwd(), 'lib'))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-u5_r=pekio0@zt!y(kgbufuosb9mddu8*qeejkzj@=7uyvb392')

DEBUG = False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_NAME = "django_vue_cli_csrftoken"
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8080"
]

INSTALLED_APPS = [
    "corsheaders",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "applications.task",
    "applications.user",
    "applications.music",
    "applications.subsonic",
    # "django_extensions",

]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "component.drf.middleware.AppExceptionMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_vue_cli.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "static", "dist")],
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

WSGI_APPLICATION = 'django_vue_cli.wsgi.application'
TIME_ZONE = "Asia/Shanghai"
LANGUAGE_CODE = "zh-hans"

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

USE_I18N = True

USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]  # noqa

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "component.drf.generics.exception_handler",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "component.drf.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 10,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ),
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "NON_FIELD_ERRORS_KEY": "params_error",
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('JWT',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}
BASE_URL = "https://music.163.com/"
REVERSE_PROXY_TYPE = "nginx"
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
SUBSONIC_DEFAULT_TRANSCODING_FORMAT = "mp3"
SITE_LOGIN = os.getenv("SITE_LOGIN", "true")
try:
    from local_settings import *  # noqa
except ImportError:
    pass
