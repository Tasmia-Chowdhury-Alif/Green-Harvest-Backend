from pathlib import Path
import dj_database_url
import environ
from datetime import timedelta
import cloudinary


env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS") 
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT",]


AUTH_USER_MODEL = 'users.User'

# Application definition

INSTALLED_APPS = [
    #External package 
    "corsheaders",
    "whitenoise.runserver_nostatic",
    "mptt", # for MPTTModelAdmin
    'django_filters',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # External Packages
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "djoser",
    'drf_spectacular',
    'drf_spectacular_sidecar',

    # Internal Apps
    'users.apps.UsersConfig',
    'products.apps.ProductsConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'green_harvest_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'green_harvest_backend.wsgi.app'


# Database configuration
DATABASE_ENGINE = env.str("DATABASE_ENGINE", default="sqlite").lower()

if DATABASE_ENGINE == "postgresql":
    DATABASES = {
        "default": dj_database_url.parse(
            env("DATABASE_URL", default="")
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static',]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' 

# Cloudinary Configuration 
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

cloudinary.config(
    cloud_name=env("CLOUDINARY_CLOUD_NAME"),
    api_key=env("CLOUDINARY_API_KEY"),
    api_secret=env("CLOUDINARY_API_SECRET"),
    secure=True  # Use HTTPS for uploads/delivery
)


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}


DJOSER = {
    'LOGIN_FIELD': 'email',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,

    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',

    'EMAIL_FRONTEND_PROTOCOL': env('FRONTEND_PROTOCOL', default='https'),
    'EMAIL_FRONTEND_DOMAIN': env('FRONTEND_DOMAIN', default='https://eco-bazar-seven.vercel.app'),
    'EMAIL_FRONTEND_SITE_NAME': 'Green Harvest',


    'SERIALIZERS': {
        'user_create': 'djoser.serializers.UserCreateSerializer',  # Default for registration
        'user': 'users.serializers.UserProfileSerializer',  # For general user endpoints
        'current_user': 'users.serializers.UserProfileSerializer',  # Specifically for /users/me/
    },
    'PERMISSIONS': {
        'user_create': ['rest_framework.permissions.AllowAny'],
    },
    'HIDE_USERS': False,
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'Green Harvest Backend',
    'DESCRIPTION': 'A Django REST Framework-based e-commerce backend for a grocery store, featuring user authentication, product management, cart, wishlist, orders, and multiple payment gateways (SSLCOMMERZ and Stripe).',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    "COMPONENT_SPLIT_REQUEST": True,
    # OTHER SETTINGS
    "COMPONENT_SPLIT_REQUEST": True,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
        'defaultModelsExpandDepth': 2,
        'defaultModelExpandDepth': 2,
        'displayRequestDuration': True,
        # 'docExpansion': 'none',
    },
    'REDOC_UI_SETTINGS': {
        # 'expandResponses': '200,201',
        'pathInMiddle': True,
        'requiredPropsFirst': True,
        'showExtensions': True,
    },
    'TAGS': [
        {
            'name': 'auth',
            'description': 'Endpoints for user authentication, registration, and management (powered by Djoser and JWT).'
        },
        {
            'name': 'products',
            'description': 'Endpoints for products, categories, and related operations.'
        },
    ],
    'TAGS_SORTER': 'alpha',
    'OPERATIONS_SORTER': 'method',
    'ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE': False,
    'SORT_OPERATIONS': True,
    'SORT_OPERATION_PARAMETERS': True,
    'CAMELIZE_NAMES': False,
    'SECURITY': [],
    'POSTPROCESSING_HOOKS': [
        'drf_spectacular.hooks.postprocess_schema_enums',
        'green_harvest_backend.hooks.custom_tag_generator',  # Custom hook for tag assignment
    ],
    'ENABLE_DJANGO_DEPLOY_CHECK': True,
}


