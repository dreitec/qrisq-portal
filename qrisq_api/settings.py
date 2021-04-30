from pathlib import Path
from datetime import timedelta

import os

from django.urls import reverse_lazy

from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="randomString")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default=["localhost:8000"])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    # Third-party apps
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',

    # Project apps
    'core',
    'user_app',
    'subscriptions',
    'storm',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom Middleware
    'qrisq_api.middleware.JWTTokenMiddleware',
]

ROOT_URLCONF = 'qrisq_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'qrisq_api.wsgi.application'


# Custome User Model
AUTH_USER_MODEL = 'user_app.User'


# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'HEAD',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


# Database
import sys
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': config('DB_NAME', default="qrisq_db"),
            'USER': config('DB_USER', default="postgres"),
            'PASSWORD': config('DB_PASSWORD', default="password"),
            'HOST': config('DB_HOST', default="localhost"),
            'PORT': config('DB_PORT', default=5432),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': config('DB_NAME', default="qrisq_db"),
            'USER': config('DB_USER', default="postgis"),
            'PASSWORD': config('DB_PASSWORD', default="password"),
            'HOST': config('DB_HOST', default="localhost"),
            'PORT': config('DB_PORT', default=5432),
            'OPTIONS': {
                'options': '-c search_path=%s' % config('DB_SCHEMA', default='public')
            }
        },
        'storm': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': config('STORM_DB_NAME', default="qrisq_db"),
            'USER': config('STORM_DB_USER', default="postgis"),
            'PASSWORD': config('STORM_DB_PASSWORD', default="password"),
            'HOST': config('STORM_DB_HOST', default="localhost"),
            'PORT': config('STORM_DB_PORT', default=5432),
            'OPTIONS': {
                'options': '-c search_path=%s' % config('STORM_DB_SCHEMA', default='public')
            }
        }
    }


# Logger
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{asctime} {module} {levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/qrisq.log',
            'when': 'midnight',
            'backupCount': 50,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'core': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'user_app': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'subscriptions': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


# AWS Credentials
AWS_ACCESS_KEY = config('AWS_ACCESS_KEY', "")
AWS_SECRET_KEY = config('AWS_SECRET_KEY', "")
AWS_REGION = config('AWS_REGION', 'us-east-1')
AWS_WKT_BUCKET = config('AWS_WKT_BUCKET', '')
AWS_STORM_BUCKET = config('AWS_STORM_BUCKET', '')
AWS_STORM_MOST_RECENT_FILE = config('AWS_STORM_MOST_RECENT_FILE', '')

# SQS Credentials
AWS_SQS_ACCESS_KEY_ID = config('AWS_SQS_ACCESS_KEY_ID', "")
AWS_SQS_SECRET_ACCESS_KEY = config('AWS_SQS_SECRET_ACCESS_KEY', "")
AWS_SQS_QUEUE_URL = config('AWS_SQS_QUEUE_URL', "")

# Email Settings
# EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
FROM_EMAIL = config('FROM_EMAIL', default='')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = config('EMAIL_PORT', default='')
# EMAIL_USE_TLS = True

#Admin Email
ADMIN_EMAIL = config('ADMIN_EMAIL', default='admin@qrisq.com')


# Domain Name
DOMAIN = config('DOMAIN', 'http://localhost:8000')


# Rest Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}


# Simple JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
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


# drf-yasg Swagger Settings
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'LOGIN_URL': reverse_lazy('login'),
    'LOGOUT_URL': reverse_lazy('logout'),
    'PERSIST_AUTH': True,
    'REFETCH_SCHEMA_WITH_AUTH': True,
    'REFETCH_SCHEMA_ON_LOGOUT': True,
    # default api Info if none is otherwise given; should be an import string to an openapi.Info object
    'DEFAULT_INFO': 'qrisq_api.swagger.swagger_info',
    # default API url if none is otherwise given
    'DEFAULT_API_URL': 'http://127.0.0.1:8000/',
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'in': 'header',
            'name': 'Authorization',
            'type': 'apiKey',
            'description': 'Please pass token as Bearer {{token}}'
        },
    },
    "DEFAULT_PAGINATOR_INSPECTORS": [
        # 'config.inspectors.UnknownPaginatorInspector',
        'drf_yasg.inspectors.DjangoRestResponsePagination',
        'drf_yasg.inspectors.CoreAPICompatInspector',
    ],
    # default inspector classes, see advanced documentation
    'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg.inspectors.SwaggerAutoSchema',
    'DEFAULT_FIELD_INSPECTORS': [
        'drf_yasg.inspectors.CamelCaseJSONFilter',
        'drf_yasg.inspectors.InlineSerializerInspector',
        'drf_yasg.inspectors.RelatedFieldInspector',
        'drf_yasg.inspectors.ChoiceFieldInspector',
        'drf_yasg.inspectors.FileFieldInspector',
        'drf_yasg.inspectors.DictFieldInspector',
        'drf_yasg.inspectors.SimpleFieldInspector',
        'drf_yasg.inspectors.StringDefaultFieldInspector',
    ],
}


# Login Exempts
LOGIN_EXEMPT_PATHS = (
    r'api/auth/login',
    r'api/auth/refresh',
    r'api/auth/reset-password',
    r'api/auth/forgot-password',
    r'api/auth/forgot-email',
    r'api/auth/signup',
    r'api/check-service-area',
    r'api/subscription-plans',
    r'api/swagger$',
    r'api/verify-email',
)


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/api/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Remove appending slash on urls
APPEND_SLASH = False


# Paypal
PAYPAL_TEST = config("PAYPAL_TEST", True)
PAYPAL_CLIENT_ID = config("PAYPAL_CLIENT_ID", "")
PAYPAL_SECRET_KEY = config("PAYPAL_SECRET_KEY", "")


#fluidpay
FLUIDPAY_TEST = config("FLUIDPAY_TEST", True)
FLUID_PAY_API_KEY = config("FLUID_PAY_API_KEY", "")
FLUID_PAY_SANDBOX_URL = config("FLUID_PAY_SANDBOX_URL", "")
FLUID_PAY_PRODUCTION_URL = config("FLUID_PAY_PRODUCTION_URL", "")
FLUID_PAY_PROCESSOR_ID = config("FLUID_PAY_PROCESSOR_ID", "")



