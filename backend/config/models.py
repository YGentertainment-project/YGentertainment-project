from django.db import models
from dataprocess.models import CollectTarget


class CollectTargetItem(models.Model):
    collect_target = models.ForeignKey(to=CollectTarget, on_delete=models.CASCADE)
    target_name = models.TextField(default="")
    target_type = models.TextField(default="int")
    xpath = models.TextField(default="", blank=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "collect_target_item"


class Schedule(models.Model):
    collect_target = models.ForeignKey(to=CollectTarget, on_delete=models.CASCADE)
    schedule_type = models.TextField(default="")
    excute_time = models.TimeField()
    period = models.TextField(default="hour") #hour or daily
    active = models.BooleanField(default=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "schedule"


class AuthInfo(models.Model):
    collect_target = models.ForeignKey(to=CollectTarget, on_delete=models.CASCADE)
    access_type = models.TextField(default="login") #API or login
    user_id = models.TextField(null=True)
    user_pw = models.TextField(null=True)
    api_key = models.TextField(null=True)
    secret_key = models.TextField(null=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auth_info"