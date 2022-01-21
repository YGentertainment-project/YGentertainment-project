from django.db import models


class Platform(models.Model):
    name = models.TextField(unique=True)
    url = models.TextField()
    description = models.TextField(null=True, blank=True, default="")
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "platform"


class ArtistProfile(models.Model):
    # More requirements is needed
    age = models.TextField(null=True)
    height = models.TextField(null=True)
    weight = models.TextField(null=True)

    class Meta:
        db_table = "artist_profile"


class Artist(models.Model):
    name = models.TextField(unique=True, max_length=100)
    level = models.TextField(max_length=10, default="S")
    gender = models.TextField(max_length=10, default="M")
    member_num = models.IntegerField(default=1)
    member_nationality = models.TextField(max_length=100, default="", blank=True)
    agency = models.TextField(null=True, default="", blank=True)
    image = models.ImageField(null=True)
    profile = models.OneToOneField(ArtistProfile, on_delete=models.CASCADE, null=True)
    debut_date = models.DateField(null=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "artist"


class CollectTarget(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)  # if Artist is deleted, all of his/her data is removed
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    target_url = models.TextField(default="")
    target_url_2 = models.TextField(default="")
    channel = models.TextField(null=True)
    channel_name = models.TextField(null=True)
    sibling = models.BooleanField(default=False)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "collect_target"


class CollectData(models.Model):
    collect_target = models.ForeignKey(CollectTarget, on_delete=models.CASCADE)
    collect_items = models.JSONField(default=dict)

    class Meta:
        db_table = "collect_data"
