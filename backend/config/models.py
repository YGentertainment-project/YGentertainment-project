from django.db import models
from dataprocess.models import CollectTarget

class CollectTargetItem(models.Model):
    collect_target = models.ForeignKey(to=CollectTarget, on_delete=models.CASCADE)
    target_name = models.TextField(default="") # 조사항목 이름
    target_type = models.TextField(default="int") # 조사항목 type
    xpath = models.TextField(default="", blank=True) # 조사항목 xpath
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "collect_target_item"

class Schedule(models.Model):
    collect_target = models.ForeignKey(to=CollectTarget, on_delete=models.CASCADE)
    schedule_type = models.TextField(default="hour")  # hour or daily
    execute_time = models.TimeField(null=True) # 크롤링 시작 시간
    period = models.TimeField(null=True) # 주기(시간 단위)
    active = models.BooleanField(default=True) # 활성화 여부
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "schedule"

class AuthInfo(models.Model):
    collect_target = models.ForeignKey(to=CollectTarget, on_delete=models.CASCADE)
    access_type = models.TextField(default="login") # API or login
    user_id = models.TextField(null=True)
    user_pw = models.TextField(null=True)
    api_key = models.TextField(null=True)
    secret_key = models.TextField(null=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auth_info"
