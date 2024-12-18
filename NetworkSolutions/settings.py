"""
Django settings for NetworkSolutions project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.enviroment.get('SECRET_KEY', default='django-insecure-!@#$%^&*(-_)')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []

RENDER_EXTERNAL_URL = os.environ.get('RENDER_EXTERNAL_URL')
if RENDER_EXTERNAL_URL:
    ALLOWED_HOSTS = append(ALLOWED_HOSTS, RENDER_EXTERNAL_URL)


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'import_export',
    'landing',
    'inventario',
    'facturacion',
]

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",  # Tema oscuro de base
    "navbar": "navbar-dark",  # Estilo de la barra de navegación
    "navbar_fixed": True,  # Navbar fija al hacer scroll
    "sidebar_fixed": True,  # Sidebar fija
    "sidebar": "sidebar-dark-primary",  # Estilo de la barra lateral
    "brand_small_text": False,  # Logo sin texto reducido
    "accent": "orange",  # Color de acento
    "body_small_text": True,  # Texto pequeño en el cuerpo
    "button_classes": {
        "primary": "btn-orange",  # Botones principales personalizados
    },
    "dark_mode_theme": "darkly",  # Tema oscuro específico
    "footer_fixed": False,  # Pie de página no fijo
    "actions_sticky_top": True,  # Acciones (guardar, editar) pegadas arriba
}
JAZZMIN_SETTINGS = {
    "theme": "darkly",  # Puedes usar este tema oscuro como base
    "primary_color": "#f48225",  # Color naranja para destacar (ajusta al tono exacto)
    "secondary_color": "#1c1e2b",  # Fondo oscuro
    "show_ui_builder": False,
    'site_title' : "Network Solutions",
    'site_header' : "Admin",
    'site_brand' : "Network Solutions",
    'site_logo' : "image/logo.jpg",
    'site_favicon' : "image/logo.jpg",
    'welcome_sign' : "Bienvenidos a Ns",
    'copyright' : 'Network Solutions',
    "custom_css": "styles/custom.css",
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",  # Ejemplo de íconos
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhitenoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'NetworkSolutions.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'NetworkSolutions.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'network_solutions',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


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

LANGUAGE_CODE = 'en-es'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
if not DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'login'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'soportens.2024@gmail.com'
EMAIL_HOST_PASSWORD = 'Soportens2024.'

# settings.py
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'