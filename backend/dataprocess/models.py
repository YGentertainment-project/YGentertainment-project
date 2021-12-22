
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django.db import models
from django.db.models import JSONField
from django.db.models.fields import NullBooleanField
from django.db.utils import DEFAULT_DB_ALIAS

#from config.models import Platform


class ArtistProfile(models.Model):
    # More requirements is needed
    age = models.TextField(null=True)
    height = models.TextField(null=True)
    weight = models.TextField(null=True)


class Artist(AbstractBaseUser):
    name = models.TextField(unique=True)
    agency = models.TextField(null=True)
    image = models.ImageField(null=True)
    profile = models.OneToOneField(ArtistProfile, on_delete=models.CASCADE)
    debut_date = models.DateField(null=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "artist"


class CollectTarget(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE) # if Artist is deleted, all of his/her data is removed
    platform = models.ForeignKey('config.Platform', on_delete=models.CASCADE)
    target_url = models.TextField(null=False)
    channel = models.TextField(null=True)
    channel_name = models.TextField(null=True)
    sibling = models.BooleanField(default=False)
    create_dt = models.DateTimeField(auto_now_add=True)
    update_dt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "collect_target"


class CollectData(models.Model):
    collect_target = models.ForeignKey(CollectTarget, on_delete=models.CASCADE)
    collect_item = models.JSONField(default=dict)

    class Meta:
        db_table = "collect_data"