# 용도 : Celery app의 기본 설정을 설정하는 파일
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19

import os
from celery import Celery
from utils.shortcuts import get_env

# Django 프로젝트의 기본세팅 가져오기
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yg.settings")
production_env = get_env("YG_ENV", "dev") == "production" # 환경 변수가 production인지 development인지 확인

# Broker인 Rabbitmq와의 연결을 설정하는 부분
if production_env: # production 환경인 경우
    app = Celery("crawler", backend="rpc://", broker="amqp://guest:guest@yg-rabbitmq:5672/") # yg-rabbitmq 컨테이너와 연결
else: # development 환경인 경우
    app = Celery("crawler", backend="rpc://", broker="amqp://guest:guest@localhost:5672/") # local에서 실행된 rabbitmq와 연결

app.config_from_object("django.conf:settings", namespace="CELERY") # django 세팅과 Celery세팅 연동
app.autodiscover_tasks() # tasks.py에서 정의된 task를


# celery app의 각종 설정들 세팅
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_track_started=True,
    timezone="Asia/Seoul",
    enable_utc=False,
    beat_scheduler='django_celery_beat.schedulers:DatabaseScheduler',
    worker_redirect_stdouts_level='INFO',
)