import json
from django.db import models
from django.utils import timezone


class SocialbladeYoutube(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    uploads = models.IntegerField(null=True)  # 업로드 개수
    subscribers = models.IntegerField(null=True)  # 구독자수
    views = models.BigIntegerField(null=True)  # 조회수
    user_created = models.TextField(null=True)  # 계정 생성일
    recorded_date = models.DateTimeField(auto_now_add=True)
    url = models.TextField(null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique youtube record"
            ),
        ]


class SocialbladeTiktok(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    followers = models.IntegerField()
    uploads = models.IntegerField()
    likes = models.BigIntegerField()
    recorded_date = models.DateTimeField(auto_now_add=True)
    url = models.TextField(null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique tiktok record"
            ),
        ]


class SocialbladeTwitter(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    followers = models.IntegerField()
    twits = models.IntegerField()
    user_created = models.TextField()
    recorded_date = models.DateTimeField(auto_now_add=True)
    url = models.TextField(null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique twitter record"
            ),
        ]


class SocialbladeTwitter2(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    followers = models.IntegerField()
    twits = models.IntegerField()
    user_created = models.TextField()
    recorded_date = models.DateTimeField(auto_now_add=True)
    url = models.TextField(null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique twitter2 record"
            ),
        ]


class Weverse(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    weverses = models.IntegerField()
    recorded_date = models.DateTimeField(auto_now_add=True)
    url = models.TextField(null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique weverse record"
            ),
        ]


class CrowdtangleInstagram(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    followers = models.BigIntegerField()
    recorded_date = models.DateTimeField(auto_now_add=True)
    url = models.TextField(null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique instagram record"
            ),
        ]


class CrowdtangleFacebook(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    followers = models.BigIntegerField()
    recorded_date = models.DateTimeField(auto_now_add=True)
    url = models.TextField(null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique facebook record"
            ),
        ]


class Vlive(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    members = models.IntegerField()
    videos = models.IntegerField()
    likes = models.BigIntegerField()
    plays = models.BigIntegerField()
    recorded_date = models.DateTimeField(auto_now_add=True)
    url = models.TextField(null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique vlive record"
            ),
        ]


class Melon(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    listeners = models.BigIntegerField()
    streams = models.BigIntegerField()
    fans = models.IntegerField(null=True)
    recorded_date = models.DateTimeField(auto_now_add=True)
    url1 = models.TextField(null=True)
    url2 = models.TextField(null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique melon record"
            ),
        ]


class Spotify(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    monthly_listens = models.BigIntegerField()
    followers = models.BigIntegerField()
    recorded_date = models.DateTimeField(auto_now_add=True)
    url1 = models.TextField(null=True)
    url2 = models.TextField(null=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique spotify record"
            ),
        ]
