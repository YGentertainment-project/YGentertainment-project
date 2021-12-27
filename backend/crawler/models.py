import json
from django.db import models
from django.utils import timezone


class SocialbladeYoutube(models.Model):
    artist = models.CharField(max_length=100, unique=True, primary_key=True)  # 아티스트 이름
    uploads = models.IntegerField()  # 업로드 개수
    subscribers = models.IntegerField()  # 구독자수
    views = models.BigIntegerField()  # 조회수
    user_created = models.TextField()  # 계정 생성일
    # platform = models.TextField(null=True)  # socialblade 내 어떤 플랫폼인지 표시
    recorded_date = models.DateTimeField(auto_now_add=True)  # 업데이트 일
    url = models.TextField(null=True)


class SocialbladeTiktok(models.Model):
    artist = models.CharField(max_length=100, unique=True, primary_key=True)  # 아티스트 이름
    followers = models.IntegerField()
    uploads = models.IntegerField()
    likes = models.BigIntegerField()
    # platform = models.TextField(null=True)
    recorded_date = models.DateTimeField(auto_now_add=True)  # 업데이트 일
    url = models.TextField(null=True)


class SocialbladeTwitter(models.Model):
    artist = models.CharField(max_length=100, unique=True, primary_key=True)  # 아티스트 이름
    followers = models.IntegerField()
    twits = models.IntegerField()
    user_created = models.TextField()
    recorded_date = models.DateTimeField(auto_now_add=True)  # 업데이트 일
    url = models.TextField(null=True)


class SocialbladeTwitter2(models.Model):
    artist = models.CharField(max_length=100, unique=True, primary_key=True)  # 아티스트 이름
    followers = models.IntegerField()
    twits = models.IntegerField()
    user_created = models.TextField()
    recorded_date = models.DateTimeField(auto_now_add=True)  # 업데이트 일
    url = models.TextField(null=True)
