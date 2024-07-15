"""
Django settings for traya_clone project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(&w(jn$3+rco%!rre=*s0d)z0wm+fg4^w$r-def)%ij+8%d9#2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'web_admin',
    'user',
    'mathfilters',
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

ROOT_URLCONF = 'traya_clone.urls'

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

WSGI_APPLICATION = 'traya_clone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')



CC_URL = ' https://test.ccavenue.com'
CC_MERCHANT_ID = '3146555'
CC_ACCESS_CODE = 'AVIR45LA68AD72RIDAE07'
CC_WORKING_KEY = ''
CC_CURRENCY = 'INR'
CC_LANG = 'EN'
CC_BILL_CONTRY = 'India'


AWS_ACCESS_KEY_ID = 'AKIA47CRYTTISDCQ4I43'
AWS_SECRET_ACCESS_KEY = 'ti2dQ0K2VIrRd17dahw0mVx0a061VWLIIeRNC9Dz'
AWS_STORAGE_BUCKET_NAME = 'fidorebucket'
AWS_S3_SIGNATURE_NAME = 's3v4'
AWS_S3_REGION_NAME = 'ap-south-1'  # e.g., us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'



AWS_ACCESS_KEY_ID = 'AKIA47CRYTTISDCQ4I43'
AWS_SECRET_ACCESS_KEY = 'ti2dQ0K2VIrRd17dahw0mVx0a061VWLIIeRNC9Dz'
AWS_STORAGE_BUCKET_NAME = 'fidorebucket'
AWS_S3_SIGNATURE_NAME = 's3v4'
AWS_S3_REGION_NAME = 'ap-south-1'  # e.g., us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
