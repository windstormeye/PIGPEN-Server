"""
Django settings for masquerade project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#1i(0ib4%%7&ce5q7r^*vujik=40t1^o)9t5(^1sdpqv$sh7$='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 定时任务插件
    'django_crontab',
    'user',
    'blog',
    'comment',
    'read_statistics',
    'like_statistics',
    'pet',
    'virtual_pet',
    'relationship',
    'avatar',
    'pet_drink',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.tokenCheckMiddleware',
]

ROOT_URLCONF = 'masquerade.urls'

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

WSGI_APPLICATION = 'masquerade.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pigpen_db',
        'USER': 'pigpen',
        'PASSWORD': 'pigpen_2018',
        'HOST': '',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
    }
}

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

# django-crontab 定时任务配置
CRONJOBS = [
    # 早上 8：00
    ('0 08 * * *', 'pet.tasks.updatePannageTask'),
    # 早上 8：00
    ('0 08 * * *', 'pet_drink.tasks.update8HourWaterMarks'),
    # 下午 16：00
    ('0 16 * * *', 'pet_drink.tasks.update16HourWaterMarks'),
    # 晚上 24：00
    ('0 24 * * *', 'pet_drink.tasks.update24HourWaterMarks'),
    # 晚上 24：00
    ('0 24 * * *', 'pet_drink.tasks.updateDayWaterMarks'),
]

# set admin email, and remember set DEBUG = False
ADMINS = (
    ('pjhubs', '877302410@qq.com'),
)

# not null url, but show not found(404), send email
SEND_BROKEN_LINK_EMAILS = True

# set sender
SERVER_EMAIL = '877302410@qq.com'
DEFAULT_FROM_EMAIL = '877302410@qq.com'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# set email prefix
EMAIL_SUBJECT_PREFIX = '[masquerade] '

# smtp email sever
EMAIL_HOST = 'smtp.qq.com'

# smtp email sever account
EMAIL_HOST_USER = '877302410@qq.com'

# smtp email sever password
EMAIL_HOST_PASSWORD = 'drtumapmedrobbci'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%('
                      'levelname)s]- %(message)s'}
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        # Null处理器，所有高于（包括）debug的消息会被传到/dev/null
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },

        'info_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, "log", 'log.log'),
        },
        # 发送邮件通知管理员
        # AdminEmail处理器，所有高于（包括）而error的消息会被发送给站点管理员，使用的是special格式器
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            # must DEBUG = False
            'filters': ['require_debug_false'],
            'include_html': True,
        },
        # must `mkdir log` and `touch log.log` in log dir
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "log", 'log.log'),
            # 文件大小
            'maxBytes': 1024 * 1024 * 5,
            # 备份份数
            'backupCount': 5,
            'formatter': 'standard',
        },
        # 输出到控制台
        # 流处理器，所有的高于（包括）debug的消息会被传到stderr，使用的是standard格式器
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    # 定义了三个记录器
    'loggers': {
        # 使用null处理器，所有高于（包括）info的消息会被发往null处理器，向父层次传递信息
        'info_logger': {
            'handlers': ['console', 'info_file'],
            'level': 'DEBUG',
            # extends superClass('propagate': True) will show custom log message
            'propagate': False
        },
        # 所有高于（包括）error的消息会被发往mail_admins处理器，消息不向父层次发送
        'django.request': {
            'handlers': ['debug', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # 对于不在 ALLOWED_HOSTS 中的请求不发送报错邮件
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 自定义参数
EACH_PAGE_BLOGS_NUMBER = 10

# 七牛
QINIU_ACCESS_KEY = 'HUFE4cvWpUrohdU7w1HU-Lb82jOvI58er5DlPSDs'
QINIU_SECRET_KEY = '6bRiKrD-P37HJUIbT3KWEKNRuZd_Zr_XQCecW7QR'

# 狗品种
DOG_BREED_DIR = BASE_DIR + '/pet/dog_breed.txt'
# 猫品种
CAT_BREED_DIR = BASE_DIR + '/pet/cat_breed.txt'

# 融云
RC_APP_KEY = 'kj7swf8ok3sq2'
RC_APP_SECRET = 'DughOAL5cS9c1'