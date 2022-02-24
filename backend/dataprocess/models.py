from django.db import models

class Platform(models.Model):
    name = models.TextField(unique=True) # 플랫폼 이름
    url = models.TextField() # 플랫폼 대표 url(크롤링과 무관)
    description = models.TextField(null=True, blank=True, default="") # 플랫폼 설명
    active = models.BooleanField(default=True) # 활성화 여부

    class Meta:
        db_table = "platform"

# 현재 사용 x
class ArtistProfile(models.Model):
    # More requirements is needed
    age = models.TextField(null=True)
    height = models.TextField(null=True)
    weight = models.TextField(null=True)

    class Meta:
        db_table = "artist_profile"


class Artist(models.Model):
    name = models.TextField(unique=True, max_length=100) # 아티스트 이름
    level = models.TextField(max_length=10, default="S") # 등급
    gender = models.TextField(max_length=10, default="M") # 성별
    member_num = models.IntegerField(default=1) # 멤버수
    member_nationality = models.TextField(max_length=100, default="", blank=True) # 국적
    agency = models.TextField(null=True, default="", blank=True) # 소속사
    image = models.ImageField(null=True) # 사진
    profile = models.OneToOneField(ArtistProfile, on_delete=models.CASCADE, null=True)
    debut_date = models.DateField(null=True) #데뷔일자
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "artist"


class CollectTarget(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)  # if Artist is deleted, all of his/her data is removed
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    target_url = models.TextField(default="") # 크롤링 url1
    target_url_2 = models.TextField(default="") # 크롤링 url2
    channel = models.TextField(null=True)
    channel_name = models.TextField(null=True)
    sibling = models.BooleanField(default=False)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "collect_target"


class CollectData(models.Model):
    collect_target = models.ForeignKey(CollectTarget, on_delete=models.CASCADE)
    collect_items = models.JSONField(default=dict) # 수집데이터

    class Meta:
        db_table = "collect_data"
