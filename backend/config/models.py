from django.db import models

from dataprocess.models import CollectTarget


class Platform(models.Model):
    name = models.TextField(unique=True)
    url = models.TextField(unique=True)
    description = models.TextField(null=True)

    class Meta:
        db_tabe = "platform"


class CollectTargetItem(models.Model):
    collect_target = models.ForeignKey(CollectTarget, on_delete=models.CASCADE)
    target_name = models.TextField(default="")
    target_type = models.TextField(default="int")
    xpath = models.TextField(default="")
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "collect_target_item"


class Schedule(models.Model):
    collect_target = models.ForeignKey(CollectTarget, on_delete=models.CASCADE)
    schedule_type = models.TextField(default="")
    excute_time = models.TimeField()
    period = models.TextField(default="hour") #hour or daily
    active = models.BooleanField(default=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_tabe = "schedule"


class AuthInfo(models.Model):
    collect_target = models.ForeignKey(CollectTarget, on_delete=models.CASCADE)
    access_type = models.TextField(default="login") #API or login
    user_id = models.TextField(null=True)
    user_pw = models.TextField(null=True)
    api_key = models.TextField(null=True)
    secret_key = models.TextField(null=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auth_info"