import os
from datetime import timedelta
import rest_framework
from Bookstore.cred import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = credentials["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!

AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by G-mail
    'allauth.account.auth_backends.AuthenticationBackend',

]

# Application definition
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # REST Framework apps
    'rest_framework',
    'rest_framework.authtoken',   # app For Token based(Not JSON web tokens) authentication.

    # My apps
    'cuser',
    'books',
    'api',
    'post',

    # Third party apps
    'crispy_forms',
    'storages',

    # social all auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # social all auth providers
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
}

REST_FRAMEWORK = {

    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework.authentication.BasicAuthentication',     # Authenticating user using username, password.
    #     'rest_framework.authentication.SessionAuthentication',
    #     'rest_framework.authentication.TokenAuthentication',     # Authenticating user using token(Not JSON web token).
    # ],

    'DEFAULT_AUTHENTICATION_CLASSES' : [
        'rest_framework_simplejwt.authentication.JWTAuthentication',   # Authenticating user using JSON web token.
    ],

    'DEFAULT_PERMISSION_CLASSES' : [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],

}

# JWT customizing settings.
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'books', 'templates')],
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


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# SMTP Configurations to send mail
EMAIL_BACKEND = credentials['EMAIL_BACKEND']
EMAIL_HOST = credentials['EMAIL_HOST']
EMAIL_PORT = credentials['EMAIL_PORT']
EMAIL_HOST_USER = credentials['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = credentials['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = credentials['EMAIL_USE_TLS']
EMAIL_USE_SSL = credentials['EMAIL_USE_SSL']


# Celery settings
CELERY_BROKER_URL = credentials['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = credentials['CELERY_RESULT_BACKEND']
CELERY_ACCEPT_CONTENT = credentials['CELERY_ACCEPT_CONTENT']
CELERY_TASK_SERIALIZER = credentials['CELERY_TASK_SERIALIZER']
CELERY_RESULT_SERIALIZER = credentials['CELERY_RESULT_SERIALIZER']
CELERY_TIMEZONE = credentials['CELERY_TIMEZONE']


# AWS S3 Service settings
AWS_ACCESS_KEY_ID = credentials['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = credentials['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = credentials['AWS_STORAGE_BUCKET_NAME']

DEFAULT_FILE_STORAGE = credentials['DEFAULT_FILE_STORAGE']
AWS_DEFAULT_ACL = credentials['AWS_DEFAULT_ACL']          # ACL means Access Control List. by default inherits the bucket permissions.
AWS_S3_FILE_OVERWRITE = credentials['AWS_S3_FILE_OVERWRITE']    # By default files with the same name will overwrite each other. True by default.
AWS_S3_REGION_NAME = credentials['AWS_S3_REGION_NAME'] # change to your region

# STATICFILES_STORAGE = credentials['STATICFILES_STORAGE']        # To serve static file like css, js from AWS S3.


# For social all auth
SITE_ID = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL =True

ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = 'user-signin-path'
SOCIALACCOUNT_AUTO_SIGNUP = True 

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# This setting will tell us from where to start url lookups.
ROOT_URLCONF = 'Bookstore.urls'

# This setting will specify which user model should use for authentication
AUTH_USER_MODEL = 'cuser.User'

# Login settings
LOGIN_URL = 'user-signin-path'
LOGOUT_URL = 'user-signout-path'
LOGIN_REDIRECT_URL = 'set-user-password'

# Web server gateway interface application
WSGI_APPLICATION = 'Bookstore.wsgi.application'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'books', 'static')

# Files uploads like images, files using ImageField, FileField in the forms
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'books', 'static', 'images')


# Crispy forms pack
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# SameSite Cookie
# SESSION_COOKIE_SAMESITE = None
# CSRF_COOKIE_SAMESITE = None
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SESSION_SAVE_EVERY_REQUEST = True