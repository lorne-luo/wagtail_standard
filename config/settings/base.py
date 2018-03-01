"""
Django settings project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from __future__ import absolute_import, unicode_literals

import os
import environ

root = environ.Path(__file__) - 3  # (wagtail-standard/config/settings/base.py - 3 = wagtail-standard/)

# Load operating system environment variables and then prepare to use them
env = environ.Env()
env_file = root('.env')
if os.path.exists(env_file):
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined as environment variables.
    print('[environ] Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('[environ] The .env file has been loaded. See base.py for more information')

BASE_DIR = root()

# AUTH & USER
AUTH_USER_MODEL = 'users.user'

# APP CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps

INSTALLED_APPS = [
    # DJANGO_APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # WAGTAIL_APPS
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.settings',
    'wagtail.contrib.table_block',

    # THIRD_PARTY_APPS
    'modelcluster',
    'taggit',
    'rest_framework',

    # LOCAL_APPS
    'apps.home',
    'apps.search',
    'apps.users',
    'apps.custom_settings',
]


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
]


# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('templates'),
        ],
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


# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# Uses django-environ to accept uri format
# See: https://django-environ.readthedocs.io/en/latest/#supported-types

DATABASES = {
    'default': env.db('DATABASE_URL', default='mysql://test:test@localhost:3306/db_name_example')
}

DATABASES['default']['OPTIONS'] = {
    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug

DEBUG = env.bool('DEBUG', False)


# URL Configuration
# ------------------------------------------------------------------------------

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins

ADMINS = env.list('ADMINS', default=['dev@luotao.net'])


# INTERNATIONALIZATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

# AUSTRALIA DATE FORMAT
DATE_FORMAT = "d M Y"

SHORT_DATE_FORMAT = "d M Y"

DATETIME_FORMAT = "h:i A, d M Y"

SHORT_DATETIME_FORMAT = "h:i A"

# STATIC FILES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    root('static'),
]

STATIC_ROOT = root('staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = root('media')
MEDIA_URL = '/media/'


# WAGTAIL SETTINGS
# ------------------------------------------------------------------------------

WAGTAIL_SITE_NAME = "mysite"
WAGTAIL_USER_EDIT_FORM = 'apps.users.forms.CustomUserEditForm'
WAGTAIL_USER_CREATION_FORM = 'apps.users.forms.CustomUserCreationForm'
WAGTAIL_USER_CUSTOM_FIELDS = []

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = env('BASE_URL', default='http://example.com')


# PROJECT SETTINGS
# ------------------------------------------------------------------------------

# All your project settings go here
