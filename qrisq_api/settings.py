from pathlib import Path
from datetime import timedelta

import os

from django.urls import reverse_lazy

from decouple import config, Csv


import os

import boto3


if "QRISQ_ENV" in os.environ and os.environ["QRISQ_ENV"].lower() in ["dev", "staging", "prod"]:
    def get_resources_from(ssm_details):
        results = ssm_details['Parameters']
        resources = [result for result in results]
        next_token = ssm_details.get('NextToken', None)
        return resources, next_token

    client = boto3.client('ssm')
    param_prefix = "/copilot/apps/{}/secrets/".format(os.environ["QRISQ_ENV"].lower())
    next_token = ' '
    resources = []
    while next_token is not None:
        ssm_details = client.describe_parameters(MaxResults=50,
                                                 ParameterFilters=[{
                                                     "Key": "Name",
                                                     "Option": "BeginsWith",
                                                     "Values": [param_prefix]
                                                 }],
                                                 NextToken=next_token)
        current_batch, next_token = get_resources_from(ssm_details)
        resources += current_batch

    for param in resources:
        param_name = param["Name"]
        response = client.get_parameter(Name=param_name,WithDecryption=True)
        param_value = response["Parameter"]["Value"]
        env_var_name = param_name[param_name.rindex("/")+1:].upper()
        print("Set {} from SSM {}".format(env_var_name, param_name))
        os.environ[env_var_name] = param_value
else:
    print("Not reading data from parameter store.")



# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="randomString")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default=["localhost",])


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
    'storages',
    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',

    # Project apps
    'core',
    'user_app',
    'subscriptions',
    'storm',
    'billing',
    'settings',
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
# CORS_ALLOWED_ORIGINS = config('CORS_HOSTS', cast=Csv(), default=['http://localhost',])
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
CORS_ALLOW_CREDENTIALS = True


# Database
import sys
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
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
            'ENGINE': 'django.db.backends.postgresql',
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
            'ENGINE': 'django.db.backends.postgresql',
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

# I don't even know why we are using log file on a server when Cloudwatch exists, but I'm leaving this in to preserve the old implementation.
qrisq_log = "logs/qrisq.log"
os.makedirs("logs", exist_ok=True)
log_file = Path(qrisq_log)
log_file.touch(exist_ok=True)

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
}


# AWS Credentials
AWS_ACCESS_KEY = config('AWS_ACCESS_KEY', "")
AWS_SECRET_KEY = config('AWS_SECRET_KEY', "")
AWS_REGION = config('AWS_REGION', 'us-east-1')
AWS_WKT_BUCKET = config('AWS_WKT_BUCKET', '')
AWS_STORM_BUCKET = config('AWS_STORM_BUCKET', '')
AWS_STORM_MOST_RECENT_FILE = config('AWS_STORM_MOST_RECENT_FILE', '')

# AWS Credentials
# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY', "")
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_KEY', "")
# AWS_STORAGE_BUCKET_NAME = config('AWS_WKT_BUCKET', "")
# AWS_S3_SIGNATURE_VERSION = 's3v4'
# AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_FILE_OVERWRITE = False
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_DEFAULT_ACL = None
# AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' 

# SQS Credentials
AWS_SQS_ACCESS_KEY_ID = config('AWS_SQS_ACCESS_KEY_ID', "")
AWS_SQS_SECRET_ACCESS_KEY = config('AWS_SQS_SECRET_ACCESS_KEY', "")
AWS_SQS_QUEUE_URL = config('AWS_SQS_QUEUE_URL', "")

# Email Settings
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
FROM_EMAIL = config('FROM_EMAIL', default='')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = config('EMAIL_PORT', default='')
EMAIL_USE_TLS = True

#Admin Email
ADMIN_EMAIL = config('ADMIN_EMAIL', default='admin@qrisq.com')


# Domain Name
DOMAIN = config('DOMAIN', 'http://localhost:8000')
FRONTEND_DOMAIN = config('FRONTEND_DOMAIN', 'http://localhost:4200')


# Rest Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'qrisq_api.pagination.CustomPagination',
    'PAGE_SIZE': 25
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
    'DEFAULT_API_URL': 'http://127.0.0.1:8000',
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
    r'api/subscription-plans-discount',
    r'api/swagger$',
    r'api/verify-recaptcha_v3',
    r'api/verify-email',
    r'api/health-check',
    r'api/zip/*',
    r'api/static/*',
    r'api/send-message',
    r'api/storm-data',
    r'api/surge-data',
    r'api/wind-data',
    r'api/webhook-paypal',
    r'api/webhook-fluidpay'
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

MEDIA_URL = '/api/zip/'
MEDIA_ROOT = os.path.join(BASE_DIR, "zip")

# Remove appending slash on urls
APPEND_SLASH = False

# Google Recaptcha V3
RECAPTCHA_SECRET_KEY = config("RECAPTCHA_SECRET_KEY", "")

# Paypal
PAYPAL_TEST = config("PAYPAL_TEST", True)
PAYPAL_CLIENT_ID = config("PAYPAL_CLIENT_ID", "")
PAYPAL_SECRET_KEY = config("PAYPAL_SECRET_KEY", "")
PAYPAL_RETURN_URL = config("PAYPAL_RETURN_URL", "")
PAYPAL_WEBHOOK_ID = config("PAYPAL_WEBHOOK_ID", "")


#fluidpay
FLUIDPAY_TEST = config("FLUIDPAY_TEST", "False")
FLUID_PAY_API_KEY = config("FLUID_PAY_API_KEY", "")
FLUID_PAY_SANDBOX_URL = config("FLUID_PAY_SANDBOX_URL", "")
FLUID_PAY_PRODUCTION_URL = config("FLUID_PAY_PRODUCTION_URL", "")
FLUID_PAY_PROCESSOR_ID = config("FLUID_PAY_PROCESSOR_ID", "")
FLUID_PAY_WEBHOOK_SIGNATURE = config("FLUID_PAY_WEBHOOK_SIGNATURE", "")