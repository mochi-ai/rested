import os
import sys
import logging

if 'test' in sys.argv: logging.disable(logging.CRITICAL)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'q)ksawpkl_=$&mx*!hn3ip$-oz3n0195n23uy5k1l+k9glj$yr'
DEBUG = True
ALLOWED_HOSTS = ['testserver']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test',
    }
}
INSTALLED_APPS = [
    'example',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rested.middleware.TokenAuthenticationMiddleware',
    'rested.middleware.RestMiddleware',
]
AUTH_USER_MODEL = 'example.User'
CSRF_FAILURE_VIEW = 'rested.patterns.handler_csrf'
ROOT_URLCONF = 'example.urls'
WSGI_APPLICATION = 'example.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
