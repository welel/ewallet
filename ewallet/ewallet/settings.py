import os
from pathlib import Path

from dotenv import load_dotenv

if not os.environ.get("DOCKER_MODE", False):
    load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent

SECRET_KEY = os.environ.get('SECRET_KEY', "")

DEBUG = True if os.environ.get('DEBUG') in (1, "1") else False

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(" ")

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    
    'rest_framework',

	'money.apps.MoneyConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ewallet.urls'


WSGI_APPLICATION = 'ewallet.wsgi.application'
if os.environ.get('DB_ENGINE', False):
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
            "NAME": os.environ.get("DB_NAME", "ewallet"),
            "USER": os.environ.get("DB_USER", "ewallet"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "ewallet"),
            "HOST": os.environ.get("DB_HOST", ""),
            "PORT": os.environ.get("DB_PORT", ""),
            "TEST": {
                "NAME": "ewallet_test",
                "MIGRATE": False,
            },
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.environ.get('TZ', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'UNAUTHENTICATED_USER': None,
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
