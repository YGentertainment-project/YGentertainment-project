
DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "ygenter",
        'USER': "ygenter",
        'PASSWORD': "ygenter",
        'HOST': "yg-mariadb",
        'PORT': "3306",
    }
}

DEBUG = False

ALLOWED_HOSTS = ["*"]

DATA_DIR = "/data"
