import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-!v2q@wove10@=x1m8#s&da5xi!9+(1q2)dpfy-51_n2_4ozlq9"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

DEFAULT_APP = [
    'usuarios',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

CREATED_APP = [
    'establecimiento',
    'productos',
    'carritocompras',
    'ordenes',
    'pagos',
    'apps.core',
    'apps.administracion',
    'apps.busquedas',
    'apps.feedbacks',
]

THIRD_PARTY_APP = []

INSTALLED_APPS = [*DEFAULT_APP, *CREATED_APP, *THIRD_PARTY_APP]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "es-mx"

TIME_ZONE = "America/Mazatlan"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Directorio donde se recopilarán los archivos estáticos para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Directorios adicionales donde Django buscará archivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Carpeta donde almacenarás tus archivos estáticos
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'usuarios.Usuario'


# Ruta donde se guardarán los archivos multimedia
MEDIA_URL = '/media/'  # URL base para acceder a archivos multimedia
# Directorio en el sistema de archivos donde se guardarán los archivos subidos
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  

# Ajustes de Sesion
SESSION_COOKIE_AGE = 7200  # 2 horas en segundos

#la sesion se cierra cuando se cierra el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True 

# Actualiza la sesión después de cada solicitud
SESSION_SAVE_EVERY_REQUEST = True


# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'juniorrenteria91@gmail.com'  # Replace with your email
EMAIL_HOST_PASSWORD = 'lmnv ucok hiux rfeg'  # Replace with your email password