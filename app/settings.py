"""
Django settings for hrtt project.
Generated by 'django-admin startproject' using Django 2.0.4.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import mimetypes
import os
from celery import Celery

import environ
from django.contrib.messages import constants as message_constants
from django.contrib.messages import constants as messages

import config

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# App Directory
APP_DIR = "hrtt"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")
IS_LOCAL = env("IS_LOCAL")

CSRF_TRUSTED_ORIGINS = ["https://hrtt.qtsoftwareltd.com:8445","https://172.16.30.49:8445"]
X_FRAME_OPTIONS ='ALLOW-FROM https://hrtt.qtsoftwareltd.com:8445'

if IS_LOCAL:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = [
    "127.0.0.1",
]

CORS_ORIGIN_ALLOW_ALL = True

# SECURE_HSTS_SECONDS = 86400
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = "ALLOWALL"
XS_SHARING_ALLOWED_METHODS = ["POST", "GET", "OPTIONS", "PUT", "DELETE"]

# Celery settings
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Initialize Celery
celery_app = Celery('myproject')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()


# Application definition

INSTALLED_APPS = [
    # apps
    'app',
    'backend',
    'frontend',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    # db app logger
    "django_db_logger",
    # static css and js compressor
    "compressor",
    # google recaptcha
    "captcha",
    # user agent details
    "django_user_agents",
    # datatable
    "django_tables2",
    # debug toolbar
    # 'debug_toolbar',
    # django_archive
    "django_archive",
    # django_tinymce
    "tinymce",
    # cors
    # 'corsheaders',
    # Bootstrap Modals
    "bootstrap_modal_forms",
    # 'background-task',
    "prettyjson",
]

TEMPLATE_PATH_BACKEND = 'backend/'
TEMPLATE_PATH_FRONTEND = 'frontend/'
TEMPLATE_PATH_OFFICE = 'office/'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # other middleware
    "django_user_agents.middleware.UserAgentMiddleware",
    # debug toolbar
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # # cors
    # 'corsheaders.middleware.CorsMiddleware',
    # 'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # app global constants
                "app.context_processors.global_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

APP_DOMAIN_LOCAL = env("APP_DOMAIN_LOCAL")
APP_DOMAIN_PROD = env("APP_DOMAIN_PROD")
LOGO_URL_LOCAL = APP_DOMAIN_LOCAL
LOGO_URL_PROD = APP_DOMAIN_PROD
BACKEND_DOMAIN_LOCAL = APP_DOMAIN_LOCAL+'/backend'
BACKEND_DOMAIN_PROD = APP_DOMAIN_PROD+'/backend'
FRONTEND_DOMAIN_LOCAL = APP_DOMAIN_LOCAL+'/frontend'
FRONTEND_DOMAIN_PROD = APP_DOMAIN_PROD+'/frontend'
OFFICE_DOMAIN_LOCAL = APP_DOMAIN_LOCAL+'/office'
OFFICE_DOMAIN_PROD = APP_DOMAIN_PROD+'/office'
STATIC_LOCAL = APP_DOMAIN_LOCAL+'/static/'
STATIC_PROD = APP_DOMAIN_PROD+'/static/'
# Redirect
LOGIN_URL = "/" + APP_DIR + "/users/signin"
CONTACT_URL = "https://qtsoftwareltd.com"

# Files
APP_FILES_URL = env("APP_FILES_URL")
APP_FILES_URL_LOCAL = env("APP_FILES_URL_LOCAL")
APP_FILES_XAUTH = env("APP_FILES_XAUTH")
# Office
APP_OFFICE_URL = env("APP_OFFICE_URL")
APP_OFFICE_URL_LOCAL = env("APP_OFFICE_URL_LOCAL")
APP_OFFICE_XAUTH = env("APP_OFFICE_XAUTH")

DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_ENGINE"),
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USERNAME"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
        "OPTIONS": {
            "sql_mode": "traditional",
        },
    }
}
DATABASE_NAME = env("DATABASE_NAME")
DATABASE_MONGO = env("DATABASE_MONGO")
# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'db_hrtt',
#             'USER': 'root',
#             'PASSWORD': 'qtm!@#123',
#             'HOST': 'localhost',
#             'PORT': '3306',
#             'OPTIONS': {
#                 'sql_mode': 'traditional',
#             }
#         }
# }
# DATABASE_NAME='db_hrtt'
# DATABASE_MONGO='mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000'

ARCHIVE_DIRECTORY = "backups"
ARCHIVE_FILENAME = "%Y-%m-%d-%H-%M-%S"
ARCHIVE_FORMAT = "bz2"  # gz, bz2
ARCHIVE_EXCLUDE = (
    "contenttypes.ContentType",
    "sessions.Session",
    "auth.Permission",
    "app.Backups",
)

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
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

SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

# Datetime
USE_TZ = True
TIME_IN_SECONDS = True
TIME_ZONE = "UTC"
TIME_DIFFERENCE = -2 * 3600
APP_CONSTANT_DISPLAY_TIME_ZONE = "Africa/Kigali"
APP_CONSTANT_DISPLAY_TIME_ZONE_INFO = ""
APP_CONSTANT_DISPLAY_DATE_FORMAT = "%a, %d %b %Y"
APP_CONSTANT_DISPLAY_TIME_FORMAT = "%H:%M:%S"
APP_CONSTANT_DISPLAY_DATETIME_FORMAT = "%a, %d %b %Y %H:%M:%S"
APP_CONSTANT_DISPLAY_DATETIME_FORMAT_OTHER = "%d %b %Y %H:%M:%S"
APP_CONSTANT_INPUT_DATE_FORMAT = "%Y-%m-%d"
APP_CONSTANT_INPUT_TIME_FORMAT = "%H:%M:%S"
APP_CONSTANT_INPUT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
APP_CONSTANT_DEFAULT_DATETIME = "0001-01-01 00:00:00"
APP_CONSTANT_DEFAULT_DATE = "0001-01-01"
APP_CONSTANT_DEFAULT_TIME = "00:00:00"
APP_CONSTANT_DEFAULT_DATETIME_VALUE = "0001-01-01 00:00:00"
APP_CONSTANT_DEFAULT_DATE_VALUE = "0001-01-01"

USE_I18N = True

USE_L10N = True

MESSAGE_LEVEL = message_constants.DEBUG
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

if IS_LOCAL:
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")
    MEDIA_URL = "/uploads/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "uploads/")
    FILES_URL = "/files/"
    FILES_ROOT = os.path.join(BASE_DIR, "files/")
    ASSETS_URL = "/assets/"
    ASSETS_ROOT = os.path.join(BASE_DIR, "assets/")
else:
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")
    MEDIA_URL = "/uploads/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "uploads/")
    FILES_URL = "/files/"
    FILES_ROOT = os.path.join(BASE_DIR, "files/")
    ASSETS_URL = "/assets/"
    ASSETS_ROOT = os.path.join(BASE_DIR, "assets/")

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # other finders..
    "compressor.finders.CompressorFinder",
)

COMPRESS_ENABLED = True
COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_STORAGE = "compressor.storage.CompressorFileStorage"
COMPRESS_OUTPUT_DIR = "cache"
# COMPRESS_CSS_FILTERS = ["compressor.filters.cssmin.CSSMinFilter"]
# COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]
COMPRESS_CSS_FILTERS = ["compressor.filters.yuglify.YUglifyCSSFilter"]
COMPRESS_JS_FILTERS = ["compressor.filters.yuglify.YUglifyJSFilter"]

# App Constants
# Project related
APP_CONSTANT_COMPANY = "hrtt"
APP_CONSTANT_APP_NAME = "HRTT"
APP_CONSTANT_APP_SHORT_NAME = "HRTT"
APP_CONSTANT_APP_NAME_NO_SPACE = "HRTT"
APP_CONSTANT_APP_PACKAGE_NAME = "hrtt"
APP_CONSTANT_APP_VERSION_CODE = "v1.0.0"
APP_CONSTANT_APP_VERSION_NAME = "v1.0.0"
APP_CONSTANT_APP_VERSION_MOBILE = "v1 (1.0.0)"
APP_CONSTANT_COMPANY_NAME = "QT Software Ltd."
APP_CONSTANT_COMPANY_WEBSITE = "https://qtsoftwareltd.com"
APP_CONSTANT_TECH_SUPPORT_EMAIL_ID = "support@qtsoftwareltd.com"
APP_CONSTANT_ADMIN_SUPPORT_EMAIL_ID = env("EMAIL_HOST_USER")

# Email Settings
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
# EMAIL_USE_SSL = env('EMAIL_USE_SSL')
EMAIL_API = env("EMAIL_API")

# Email Verification
EMAIL_VERIFICATION_SUBJECT = APP_CONSTANT_APP_NAME_NO_SPACE + " : Email Verification"
EMAIL_VERIFICATION_MESSAGE = (
    "Thank you for registration. An email has been sent for verification."
)
EMAIL_VERIFICATION_MESSAGE_SUCCESS = (
    "Your email id has been verified successfully. Please login to continue."
)
EMAIL_VERIFICATION_MESSAGE_WARNING = "Failed to verify your email id!"
EMAIL_VERIFICATION_MESSAGE_ERROR = "Verification Link is not valid!!!"
# Email Reset Password
EMAIL_PASSWORD_RESET_SUBJECT = APP_CONSTANT_APP_NAME_NO_SPACE + " : Reset Password"
EMAIL_PASSWORD_RESET_MESSAGE = (
    "A link has been sent to your registered Email ID to reset your password."
)
# Email Message
EMAIL_NOTIFICATION_SUBJECT = APP_CONSTANT_APP_NAME_NO_SPACE + " : Notification"
EMAIL_NOTIFICATION_MESSAGE = "Message"

# Google Recptcha
RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY")
GOOGLE_RECAPTCHA_SECRET_KEY = RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY")
NOCAPTCHA = env("NOCAPTCHA")
RECAPTCHA_USE_SSL = env("RECAPTCHA_USE_SSL")

# General
ERROR_MESSAGE = "Oops! Something went wrong. Please contact admin for support."
MAX_LOGIN_ATTEMPTS_CAPTCHA = 3

# # cors
# CORS_ORIGIN_WHITELIST = (
#     'localhost:8000',
#     '127.0.0.1:8000'
# )

# External Library Constants
# User Agent
# Cache backend is optional, but recommended to speed up user agent parsing
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
#         "LOCATION": "127.0.0.1:11211",
#     }
# }
# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = "default"

# Backend Sections
BACKEND_SECTION_DASHBOARD = 1
BACKEND_SECTION_USERS = 2
BACKEND_SECTION_PROFILE = 3
BACKEND_SECTION_CHANGE_PASSWORD = 4
BACKEND_SECTION_SETTINGS = 5
BACKEND_SECTION_HELP = 6
BACKEND_SECTION_LOGS = 7
BACKEND_SECTION_FILES = 8
BACKEND_SECTION_NOTIFICATIONS = 9
BACKEND_SECTION_ORGANIZATIONS = 10
# BACKEND_SECTION_DIVISIONS = 11
BACKEND_SECTION_ANALYSIS = 11
BACKEND_SECTION_PROJECTS = 12
BACKEND_SECTION_ACTIVITIES = 13
BACKEND_SECTION_ORGANIZATION = 14
BACKEND_SECTION_LEVELS = 15
BACKEND_SECTION_REPORTERS = 16
BACKEND_SECTION_REPORTS = 17
BACKEND_SECTION_CURRENCY_RATES = 18
BACKEND_SECTION_CONFIGURABLES = 19
BACKEND_SECTION_SYSTEM_REPORTS = 20


# Access Permissions
ACCESS_PERMISSION_USER_CREATE = "user-create"
ACCESS_PERMISSION_USER_UPDATE = "user-update"
ACCESS_PERMISSION_USER_DELETE = "user-delete"
ACCESS_PERMISSION_USER_VIEW = "user-view"
ACCESS_PERMISSION_DASHBOARD_VIEW = "dashboard-view"
ACCESS_PERMISSION_SETTINGS_VIEW = "settings-view"
ACCESS_PERMISSION_LOG_CREATE = "log-create"
ACCESS_PERMISSION_LOG_UPDATE = "log-update"
ACCESS_PERMISSION_LOG_DELETE = "log-delete"
ACCESS_PERMISSION_LOG_VIEW = "log-view"
ACCESS_PERMISSION_FILES_CREATE = "files-create"
ACCESS_PERMISSION_FILES_UPDATE = "files-update"
ACCESS_PERMISSION_FILES_DELETE = "files-delete"
ACCESS_PERMISSION_FILES_VIEW = "files-view"
ACCESS_PERMISSION_FILES_DOWNLOAD = "files-download"
ACCESS_PERMISSION_FILES_OFFICE_VIEW = "files-office-view"
ACCESS_PERMISSION_FILES_OFFICE_EDIT = "files-office-edit"
ACCESS_PERMISSION_FILES_OFFICE_REVIEW = "files-office-review"
ACCESS_PERMISSION_FILES_OFFICE_COMMENT = "files-office-comment"
ACCESS_PERMISSION_FILES_OFFICE_PRINT = "files-office-print"
ACCESS_PERMISSION_FILES_OFFICE_COPY = "files-office-copy"
ACCESS_PERMISSION_ORGANIZATIONS_CREATE = "organizations-create"
ACCESS_PERMISSION_ORGANIZATIONS_UPDATE = "organizations-update"
ACCESS_PERMISSION_ORGANIZATIONS_DELETE = "organizations-delete"
ACCESS_PERMISSION_ORGANIZATIONS_VIEW = "organizations-view"

ACCESS_PERMISSION_PROJECTS_CREATE = "projects-create"
ACCESS_PERMISSION_PROJECTS_UPDATE = "projects-update"
ACCESS_PERMISSION_PROJECTS_DELETE = "projects-delete"
ACCESS_PERMISSION_PROJECTS_VIEW = "projects-view"
ACCESS_PERMISSION_PROJECTS_ASSIGN = "projects-assign"
ACCESS_PERMISSION_ACTIVITIES_CREATE = "activities-create"
ACCESS_PERMISSION_ACTIVITIES_UPDATE = "activities-update"
ACCESS_PERMISSION_ACTIVITIES_DELETE = "activities-delete"
ACCESS_PERMISSION_ACTIVITIES_VIEW = "activities-view"
ACCESS_PERMISSION_ACTIVITIES_SUBMIT = "activities-submit"
ACCESS_PERMISSION_ACTIVITIES_ACCEPT = "activities-accept"
ACCESS_PERMISSION_ACTIVITIES_REJECT = "activities-reject"
ACCESS_PERMISSION_ACTIVITIES_APPROVE = "activities-approve"
ACCESS_PERMISSION_ACTIVITIES_DENY = "activities-deny"


ACCESS_PERMISSION_REPORTS_CREATE = "capital-formation-create"
ACCESS_PERMISSION_REPORTS_UPDATE = "capital-formation-update"
ACCESS_PERMISSION_REPORTS_DELETE = "capital-formation-delete"
ACCESS_PERMISSION_REPORTS_VIEW = "capital-formation-view"
ACCESS_PERMISSION_REPORTS_SUBMIT = "capital-formation-submit"
ACCESS_PERMISSION_REPORTS_ACCEPT = "capital-formation-accept"
ACCESS_PERMISSION_REPORTS_REJECT = "capital-formation-reject"
# ACCESS_PERMISSION_REPORTS_ASSIGN = "capital-formation-assign"
# ACCESS_PERMISSION_REPORTS_REVIEW = "capital-formation-review"
ACCESS_PERMISSION_REPORTS_APPROVE = "capital-formation-approve"
ACCESS_PERMISSION_REPORTS_DENY = "capital-formation-deny"
ACCESS_PERMISSION_LEVELS_CREATE = "levels-create"
ACCESS_PERMISSION_LEVELS_UPDATE = "levels-update"
ACCESS_PERMISSION_LEVELS_DELETE = "levels-delete"
ACCESS_PERMISSION_LEVELS_VIEW = "levels-view"
ACCESS_PERMISSION_COMMENTS_CREATE = "comments-create"
ACCESS_PERMISSION_COMMENTS_UPDATE = "comments-update"
ACCESS_PERMISSION_COMMENTS_DELETE = "comments-delete"
ACCESS_PERMISSION_COMMENTS_VIEW = "comments-view"

ACCESS_PERMISSION_CURRENCY_RATES_CREATE = "currency-rate-create"
ACCESS_PERMISSION_CURRENCY_RATES_VIEW = "currency-rate-view"
ACCESS_PERMISSION_CURRENCY_RATES_UPDATE = "currency-rate-update"
ACCESS_PERMISSION_CURRENCY_RATES_DELETE = "currency-rate-delete"

ACCESS_PERMISSION_SYSTEM_REPORTS_CREATE = "system-reports-create"
ACCESS_PERMISSION_SYSTEM_REPORTS_UPDATE = "system-reports-update"
ACCESS_PERMISSION_SYSTEM_REPORTS_DELETE = "system-reports-delete"
ACCESS_PERMISSION_SYSTEM_REPORTS_VIEW = "system-reports-view"

# Models
MODEL_USERS = "users"
MODEL_USERS_PLURAL_TITLE = "Users"
MODEL_USERS_SINGULAR_TITLE = "User"
MODEL_LOGS = "logs"
MODEL_LOGS_PLURAL_TITLE = "Logs"
MODEL_LOGS_SINGULAR_TITLE = "Log"
MODEL_FILES = "files"
MODEL_FILES_PLURAL_TITLE = "Files"
MODEL_FILES_SINGULAR_TITLE = "File"
MODEL_NOTIFICATIONS = "notifications"
MODEL_NOTIFICATIONS_PLURAL_TITLE = "Notifications"
MODEL_NOTIFICATIONS_SINGULAR_TITLE = "Notification"
MODEL_SMS_LOGS = "logs_sms"
MODEL_SMS_LOGS_PLURAL_TITLE = "SMS Logs"
MODEL_SMS_LOGS_SINGULAR_TITLE = "SMS Log"
MODEL_EMAIL_LOGS = "logs_email"
MODEL_EMAIL_LOGS_PLURAL_TITLE = "Email Logs"
MODEL_EMAIL_LOGS_SINGULAR_TITLE = "Email Log"
MODEL_ORGANIZATIONS = "organizations"
MODEL_ORGANIZATIONS_PLURAL_TITLE = "Organizations"
MODEL_ORGANIZATIONS_SINGULAR_TITLE = "Organization"

MODEL_PROJECTS = "projects"
MODEL_PROJECTS_PLURAL_TITLE = "Projects"
MODEL_PROJECTS_SINGULAR_TITLE = "Project"
MODEL_ACTIVITIES = "Activities"
MODEL_ACTIVITIES_PLURAL_TITLE = "Activities"
MODEL_ACTIVITIES_SINGULAR_TITLE = "Activity"

MODEL_ACTIVITIES_INPUTS = "Activities_Inputs"
MODEL_ACTIVITIES_INPUTS_PLURAL_TITLE = "Activities Inputs"
MODEL_ACTIVITIES_INPUTS_SINGULAR_TITLE = "Activity Input"

MODEL_LEVELS = "levels"
MODEL_LEVELS_PLURAL_TITLE = "Levels"
MODEL_LEVELS_SINGULAR_TITLE = "Level"
MODEL_REPORTS ='Reports'
MODEL_REPORTS_PLURAL_TITLE = 'Reports'
MODEL_REPORTS_SINGULAR_TITLE = 'Report'
MODEL_FUNDINGS = 'Fundings'
MODEL_FUNDINGS_PLURAL_TITLE = 'Fundings'
MODEL_FUNDINGS_SINGULAR_TITLE = 'Funding'
MODEL_COMMENTS = 'Comments'
MODEL_COMMENTS_PLURAL_TITLE = 'Comments'
MODEL_COMMENTS_SINGULAR_TITLE = 'Comment'
MODEL_RATES = "Currencies"
MODEL_RATES_PLURAL_TITLE = "Currency Rates"
MODEL_RATES_SINGULAR_TITLE = "Currency Rate"
MODEL_SYSTEM_REPORTS = "reports"
MODEL_SYSTEM_REPORTS_PLURAL_TITLE = "Reports"
MODEL_SYSTEM_REPORTS_SINGULAR_TITLE = "Report"

MODEL_GDP_POPULATION = "Configurables"
MODEL_GDP_POPULATION_PLURAL_TITLE = "Configurables"
MODEL_GDP_POPULATION_SINGULAR_TITLE = "Configurables"

# Status Colors
STATUS_ACTIVE_COLOR = "#2ECC71"
STATUS_INACTIVE_COLOR = "#ff006f"
STATUS_BLOCKED_COLOR = "#E74C3C"
STATUS_UNVERIFIED_COLOR = "#2980B9"
STATUS_UNAPPROVED_COLOR = "#FFC300"
STATUS_UNDER_REVIEW = "#F29727"

# Image Extensions
MAX_IMAGE_UPLOAD_SIZE = 4 * 1024 * 1024  # 4MB
VALID_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg"]
VALID_IMAGE_MIMES = ("image/png", "image/jpeg")

# File Extensions
MAX_FILE_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
VALID_FILE_EXTENSIONS = [".pdf", ".doc", ".docx", ".xls", ".xlsx"]
VALID_FILE_MIMES = ("image/png", "image/jpeg")

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(asctime)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "db_log": {
            "level": "DEBUG",
            "class": "django_db_logger.db_log_handler.DatabaseLogHandler",
            "formatter": "verbose",
        },
    },
    
    'loggers': {
        'django': {
            'handlers': ['console', 'db_log'],
            'propagate': True,
        },
        'app': {
            'handlers': ['console', 'db_log'],
            'propagate': True,
        },
        'backend': {
            'handlers': ['console', 'db_log'],
            'propagate': True,
        },
        'frontend': {
            'handlers': ['console', 'db_log'],
            'propagate': True,
        },
        'office': {
            'handlers': ['console', 'db_log'],
            'propagate': True,
        },
    }
}


TINYMCE_JS_URL = "https://cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js"
TINYMCE_COMPRESSOR = False
TINYMCE_DEFAULT_CONFIG = {
    "cleanup_on_startup": True,
    "custom_undo_redo_levels": 20,
    "selector": "textarea",
    "theme": "silver",
    "plugins": """
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            """,
    "toolbar1": """
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            """,
    "toolbar2": """
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            """,
    "contextmenu": "formats | link image",
    "menubar": True,
    "statusbar": True,
}

# Template Colors
COLOR_PRIMARY = "#068ECE"
COLOR_PRIMARY_DARK = "#068ECE"
COLOR_PRIMARY_LIGHT = "#068ECE"
COLOR_ACCENT = "#000000"

# office
STORAGE_PATH = "files"
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/html", ".html", True)
mimetypes.add_type("text/javascript", ".js", True)
STATICFILES_DIRS = (os.path.join(config.STORAGE_PATH),)

# from app.models.mailing_server_configurations import MailServerConfig
# try:
#     mailConfig = MailServerConfig.objects.first()
# except (TypeError, ValueError, OverflowError, MailServerConfig.DoesNotExist):
#     pass
