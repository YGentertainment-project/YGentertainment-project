from utils.shortcuts import get_env

DATABASES = {
    #DATABASES adapting required
}

REDIS_CONF = {
    #REDIS CONFIGURATION required
    "host": get_env("REDIS_HOST", "yg-redis"),
    "port": get_env("REDIS_PORT", "6379")
}

DEBUG = False

ALLOWED_HOSTS = ['*']

DATA_DIR = "/data"
