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


class Weverse(models.Model):
    artist = models.CharField(max_length=100, unique=True, primary_key=True)  # 아티스트 이름
    weverses = models.IntegerField()
    recorded_date = models.DateTimeField(auto_now_add=True)  # 업데이트 일
    url = models.TextField(null=True)


class CrowdtangleInstagram(models.Model):
    artist = models.CharField(max_length=100, unique=True, primary_key=True)  # 아티스트 이름
    followers = models.BigIntegerField()
    recorded_date = models.DateTimeField(auto_now_add=True)  # 업데이트 일
    url = models.TextField(null=True)


class CrowdtangleFacebook(models.Model):
    artist = models.CharField(max_length=100, unique=True, primary_key=True)  # 아티스트 이름
    followers = models.BigIntegerField()
    recorded_date = models.DateTimeField(auto_now_add=True)  # 업데이트 일
    url = models.TextField(null=True)


class Vlive(models.Model):
    artist = models.CharField(max_length=100, unique=True, primary_key=True)  # 아티스트 이름
    members = models.IntegerField()
    videos = models.IntegerField()
    likes = models.BigIntegerField()
    plays = models.BigIntegerField()
    recorded_date = models.DateTimeField(auto_now_add=True)
    url = models.TextField(null=True)


class Melon(models.Model):
    artist = models.CharField(max_length=100, unique=True, primary_key=True)  # 아티스트 이름
    listeners = models.BigIntegerField()
    streams = models.BigIntegerField()
    fans = models.IntegerField()
    recorded_date = models.DateTimeField(auto_now_add=True)
    url1 = models.TextField(null=True)
    url2 = models.TextField(null=True)


class Spotify(models.Model):
    artist = models.CharField(max_length=100, unique=True, primary_key=True)  # 아티스트 이름
    monthly_listens = models.BigIntegerField()
    followers = models.BigIntegerField()
    recorded_date = models.DateTimeField(auto_now_add=True)
    url1 = models.TextField(null=True)
    url2 = models.TextField(null=True)
