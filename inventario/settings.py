"""
Django settings for inventario project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9_(xj75j=+_m17++ogqpvw9@cm!3gdpcmvytki-*yofn7@$e_z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Host permitidos para acceder desde otra computadora en la misma red
# Si se necesita permitir a todos (solo produccion) ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['192.168.1.28', 'localhost', '*']


# Application definition

INSTALLED_APPS = [
    # Apps del sistema
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps personalizadas
    'productos',
    'usuarios',
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

ROOT_URLCONF = 'inventario.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Esto le dice a Django que busque plantillas en la carpeta "templates" en la raíz
        'APP_DIRS': True, # Esto le dice a Django que busque en las carpetas "templates" de cada aplicación
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

WSGI_APPLICATION = 'inventario.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# Se configuraran los datos para que utilicemos nuestra base de datos postgresql

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_inventario_elconet',
        'USER': 'user_inventario_elconet',
        'PASSWORD': 'axel',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Sistema de autenticacion para que no sea case sensitive
AUTHENTICATION_BACKENDS = [
    'usuarios.auth_backend.CaseInsensitiveUsernameBackend',  # tu backend personalizado
    'django.contrib.auth.backends.ModelBackend',  # opcional, por si querés mantener el original como fallback
]


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Guatemala'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / 'staticfiles'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Informacion para la utilizacion de TELEGRAM
TELEGRAM_BOT_TOKEN = "7512055988:AAF3pQ7kAlxf63O_9PsUQITqfmwzqYgEgiw"
TELEGRAM_CHAT_ID = -4985420036

# URLs que manejaran el movimiento de nuestra pagina
# Gestionar las URL de autenticación
LOGIN_URL = "/usuarios/login/"
LOGIN_REDIRECT_URL = "/productos/"
LOGOUT_REDIRECT_URL = "/usuarios/login/"

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis como broker
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE  # Usa la misma zona horaria de Django
