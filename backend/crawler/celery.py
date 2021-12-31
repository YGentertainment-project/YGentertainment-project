import os
from celery import Celery
from celery.schedules import crontab
from yg import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yg.settings')
app = Celery('crawler', backend='rpc://', broker='amqp://guest:guest@localhost:5672/')

# settigs.py에서 celery setting을 CELERY_로 시작하게 한다.
app.config_from_object('django.conf:settings', 'CELERY')
app.autodiscover_tasks(lambda : settings.LOCAL_APPS)

app.conf.beat_schedule = {
    # 'crawl-vlive-every-5minutes' : {
    #     'task': 'crawling',
    #     'schedule': crontab(minute='*/3'),
    #     'args': ['vlive'],
    # }
}