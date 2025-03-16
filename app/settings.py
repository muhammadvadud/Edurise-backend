import os
import os.path
from pathlib import Path
from .conf import *  # noqa
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEFAULT_DOMAIN = "https://edurise.uz"

SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ["*", "edurise.uz"]

CSRF_TRUSTED_ORIGINS = [
    "https://edurise.uz",
]

# Application definition

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    "django.contrib.admin",  # required
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "crispy_bootstrap5",
    "rest_framework",
    "crispy_forms",
    "dashboard",
    "students",
    "teachers",
    "rooms",
    "groups",
    "courses",
    "accounts",
    "education",
    "payments",
    "settings",
    "adm",
    "registration",
    "certificate",
    "api",
    "Employee",
    "fast_certificate",
    "salary",
]

CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "web/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "helpers.context.user_context",
            ],
            "libraries": {"helpers": "helpers.helpers"},
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
# Database sozlamalari
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'edurisedb',  # PostgreSQL bazasi nomi
        'USER': 'edurise_user',  # PostgreSQL foydalanuvchi nomi
        'PASSWORD': 'edurise_password',  # PostgreSQL paroli
        'HOST': 'db',  # Docker Compose dagi db servisi nomi
        'PORT': '5432',  # PostgreSQL standart porti
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "uz"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_URL = "static/"

# STATIC_ROOT = BASE_DIR / "web/static"

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "web/static"),
]

STATIC_ROOT = BASE_DIR.joinpath("staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# my settings

AUTH_USER_MODEL = "accounts.Users"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR.joinpath("web/media")
CRISPY_TEMPLATE_PACK = "bootstrap5"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

DATE_INPUT_FORMATS = [
    "%d.%m.%Y",  # 01.06.2023
]

TIME_INPUT_FORMATS = [
    "%H:%M",
]

# AUTHENTICATION_BACKENDS = ["accounts.verify.PhoneBackend"]
