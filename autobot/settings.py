import os
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '^1)5vh#kddfkvf(06xuf!a=3h&(d)15+t!+7r#18xn!a@%=@m+'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'info_data.apps.InfoDataConfig',
    'btcbot.apps.BtcbotConfig',
    'profiles.apps.ProfilesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'autobot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/'),
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

WSGI_APPLICATION = 'autobot.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_HOST = '127.0.0.1'

EMAIL_PORT = '1025'

AUTH_USER_MODEL = 'profiles.Profile'

ADMINS = [('admin', 'admin@example.com')]

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')

INTERNAL_IPS = ['127.0.0.1']

LOGIN_REDIRECT_URL = '/'

CELERY_TIMEZONE = 'Asia/Yekaterinburg'

CELERY_RESULT_BACKEND = 'rpc://'

CELERY_BEAT_SCHEDULE = {
    'ads_update_runner': {
        'task': 'info_data.tasks.ads_update_runner',
        'schedule': 10.0},
}

CELERY_TASK_ROUTES = {'info_data.tasks.ads_update_runner': {'queue': 'ads_update_runner'},
                      'info_data.tasks.ads_updater': {'queue': 'ads_updater'},
                    }

try:
    from autobot.local_settings import *
except ImportError:
    print('Warning! Local settings are not defined!')
