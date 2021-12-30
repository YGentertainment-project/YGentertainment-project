# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy_djangoitem import DjangoItem
from crawler.models import SocialbladeYoutube, SocialbladeTiktok, SocialbladeTwitter, SocialbladeTwitter2, \
    Weverse, CrowdtangleInstagram, CrowdtangleFacebook, Vlive, Melon, Spotify


class ScrapyAppItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SocialbladeYoutubeItem(DjangoItem):
    django_model = SocialbladeYoutube


class SocialbladeTiktokItem(DjangoItem):
    django_model = SocialbladeTiktok


class SocialbladeTwitterItem(DjangoItem):
    django_model = SocialbladeTwitter


class SocialbladeTwitter2Item(DjangoItem):
    django_model = SocialbladeTwitter2


class WeverseItem(DjangoItem):
    django_model = Weverse


class CrowdtangleInstagramItem(DjangoItem):
    django_model = CrowdtangleInstagram


class CrowdtangleFacebookItem(DjangoItem):
    django_model = CrowdtangleFacebook


class VliveItem(DjangoItem):
    django_model = Vlive


class MelonItem(DjangoItem):
    django_model = Melon


class SpotifyItem(DjangoItem):
    django_model = Spotify
