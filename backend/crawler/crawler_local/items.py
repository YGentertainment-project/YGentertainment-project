# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YoutubeItem(scrapy.Item):
    artist = scrapy.Field()
    account_create_dt = scrapy.Field()
    subscriber_num = scrapy.Field()
    upload_num = scrapy.Field()
    total_view_num = scrapy.Field()


class VliveItem(scrapy.Item):
    artist = scrapy.Field()
    like_num = scrapy.Field()
    member_num = scrapy.Field()
    upload_num = scrapy.Field()
    total_view_num = scrapy.Field()


class MelonItem(scrapy.Item):
    artist = scrapy.Field()
    listener_num = scrapy.Field()
    streaming_num = scrapy.Field()
    fan_num = scrapy.Field()


class SpotifyItem(scrapy.Item):
    artist = scrapy.Field()
    monthly_listener_num = scrapy.Field()
    follower_num = scrapy.Field()


class TwitterItem(scrapy.Item):
    artist = scrapy.Field()
    account_create_dt = scrapy.Field()
    follower_num = scrapy.Field()
    upload_num = scrapy.Field()


class TikTokItem(scrapy.Item):
    artist = scrapy.Field()
    follower_num = scrapy.Field()
    upload_num = scrapy.Field()
    like_num = scrapy.Field()


class WeverseItem(scrapy.Item):
    artist = scrapy.Field()
    follower_num = scrapy.Field()


class FacebookItem(scrapy.Item):
    artist = scrapy.Field()
    follower_num = scrapy.Field()


class InstagramItem(scrapy.Item):
    artist = scrapy.Field()
    follower_num = scrapy.Field()
