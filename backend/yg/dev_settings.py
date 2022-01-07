# coding=utf-8
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': 1398,
        'NAME': "ygenter",
        'USER': "root",
        'PASSWORD': "ygenter",
    }
}

DEBUG = True

ALLOWED_HOSTS = ['*']

DATA_DIR = f"{BASE_DIR}/data"
