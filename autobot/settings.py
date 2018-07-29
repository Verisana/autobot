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
    'ad_bot_runner': {
        'task': 'btcbot.tasks.ad_bot_runner',
        'schedule': 5.0},
    'seller_bot_handler': {
        'task': 'btcbot.tasks.seller_bot_handler',
        'schedule': 15.0},
    'daily_routines': {
        'task': 'info_data.tasks.daily_routine_starter',
        'schedule': crontab(minute='00', hour='00')},
    'open_trades_cleaner': {
        'task': 'btcbot.tasks.open_trades_cleaner',
        'schedule': 3600.0},
}

CELERY_TASK_ROUTES = {'btcbot.tasks.ad_bot_runner': {'queue': 'ad_bot_runner'},
                      'btcbot.tasks.sell_ad_bot_execution': {'queue': 'sell_ad_bot_execution'},
                      'btcbot.tasks.buy_ad_bot_execution': {'queue': 'buy_ad_bot_execution'},
                      'btcbot.tasks.seller_bot_handler': {'queue': 'seller_bot_handler'},
                      'btcbot.tasks.open_trades_cleaner': {'queue': 'fast_rare_tasks'},
                      'info_data.tasks.daily_report_handler': {'queue': 'fast_rare_tasks'},
                      'profiles.tasks.qiwi_limit_resetter': {'queue': 'fast_rare_tasks'},
                      'profiles.tasks.qiwi_status_updater': {'queue': 'fast_rare_tasks'},
                      'profiles.tasks.qiwi_profit_fixator': {'queue': 'qiwi_profit_fixator'},
                    }

try:
    from autobot.local_settings import *
except ImportError:
    print('Warning! Local settings are not defined!')
