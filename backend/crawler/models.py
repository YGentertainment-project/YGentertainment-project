from django.db import models
from django.utils.timezone import now


class SocialbladeYoutube(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    uploads = models.IntegerField(null=True)  # 업로드 개수
    subscribers = models.IntegerField(null=True)  # 구독자수
    views = models.BigIntegerField(null=True)  # 조회수
    user_created = models.TextField(null=True)  # 계정 생성일
    recorded_date = models.DateTimeField(auto_now_add=True)
    reserved_date = models.DateField(default=now)
    updated_at = models.DateField(null=True)
    url = models.TextField(null=True)

    class Meta:
        # db_table = 'youtube'
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique youtube record"
            ),
        ]


class SocialbladeTiktok(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    followers = models.IntegerField(null=True)
    uploads = models.IntegerField(null=True)
    likes = models.BigIntegerField(null=True)
    recorded_date = models.DateTimeField(auto_now_add=True)
    reserved_date = models.DateField(default=now)
    updated_at = models.DateField(null=True)
    url = models.TextField(null=True)

    class Meta:
        # db_table = 'tiktok'
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique tiktok record"
            ),
        ]

        
class SocialbladeTwitter(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    followers = models.IntegerField(null=True)
    twits = models.IntegerField(null=True)
    user_created = models.TextField(null=True)
    recorded_date = models.DateTimeField(auto_now_add=True)
    reserved_date = models.DateField(default=now)
    updated_at = models.DateField(null=True)
    url = models.TextField(null=True)

    class Meta:
        # db_table = 'twitter'
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique twitter record"
            ),
        ]


class SocialbladeTwitter2(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    followers = models.IntegerField(null=True)
    twits = models.IntegerField(null=True)
    user_created = models.TextField(null=True)
    recorded_date = models.DateTimeField(auto_now_add=True)
    reserved_date = models.DateField(default=now)
    updated_at = models.DateField(null=True)
    url = models.TextField(null=True)

    class Meta:
        # db_table = 'twitter2'
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique twitter2 record"
            ),
        ]


class Weverse(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    weverses = models.IntegerField(null=True)
    recorded_date = models.DateTimeField(auto_now_add=True)
    reserved_date = models.DateField(default=now)
    updated_at = models.DateField(null=True)
    url = models.TextField(null=True)

    class Meta:
        # db_table = 'weverse'
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique weverse record"
            ),
        ]


class CrowdtangleInstagram(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    followers = models.BigIntegerField(null=True)
    recorded_date = models.DateTimeField(auto_now_add=True)
    reserved_date = models.DateField(default=now)
    updated_at = models.DateField(null=True)
    url = models.TextField(null=True)

    class Meta:
        # db_table = 'instagram'
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique instagram record"
            ),
        ]


class CrowdtangleFacebook(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    followers = models.BigIntegerField(null=True)
    recorded_date = models.DateTimeField(auto_now_add=True)
    reserved_date = models.DateField(default=now)
    updated_at = models.DateField(null=True)
    url = models.TextField(null=True)

    class Meta:
        # db_table = 'facebook'
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique facebook record"
            ),
        ]


class Vlive(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    members = models.IntegerField(null=True)
    videos = models.IntegerField(null=True)
    likes = models.BigIntegerField(null=True)
    plays = models.BigIntegerField(null=True)
    recorded_date = models.DateTimeField(auto_now_add=True)
    reserved_date = models.DateField(default=now)
    updated_at = models.DateField(null=True)
    url = models.TextField(null=True)

    class Meta:
        # db_table = 'vlive'
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique vlive record"
            ),
        ]


class Melon(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    listeners = models.BigIntegerField(null=True)
    streams = models.BigIntegerField(null=True)
    fans = models.IntegerField(null=True)
    recorded_date = models.DateTimeField(auto_now_add=True)
    reserved_date = models.DateField(default=now)
    updated_at = models.DateField(null=True)
    url1 = models.TextField(null=True)
    url2 = models.TextField(null=True)

    class Meta:
        # db_table = 'melon'
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique melon record"
            ),
        ]


class Spotify(models.Model):
    artist = models.CharField(max_length=100)  # 아티스트 이름
    monthly_listens = models.BigIntegerField(null=True)
    followers = models.BigIntegerField(null=True)
    recorded_date = models.DateTimeField(auto_now_add=True)
    reserved_date = models.DateField(default=now)
    updated_at = models.DateField(null=True)
    url1 = models.TextField(null=True)
    url2 = models.TextField(null=True)

    class Meta:
        # db_table = 'spotify'
        constraints = [
            models.UniqueConstraint(
                fields=["artist", "recorded_date"],
                name="unique spotify record"
            ),
        ]
