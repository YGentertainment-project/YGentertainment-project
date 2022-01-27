import scrapy
from ..items import SocialbladeTwitterItem
from datetime import datetime
from config.models import CollectTargetItem
from django.db.models import Q


SOCIALBLADE_DOMAIN = "socialblade.com"
SOCIALBLADE_ROBOT = "https://socialblade.com/robots.txt"


class TwitterSpider(scrapy.Spider):
    name = "twitter"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.NoLoginDownloaderMiddleware": 100
        },
    }
    twitter_platform_id = Platform.objects.get(name="twitter").id
    CrawlingTarget = CollectTarget.objects.filter(platform_id=twitter_platform_id)

    def start_requests(self):
        for target in self.crawl_target:
            artist_name = target['artist_name']
            artist_url = target['target_url']
            target_id = target['id']
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_url, len(artist_url)))
            yield scrapy.Request(url=artist_url, callback=self.parse, encoding="utf-8", meta={"artist": artist_name,
                                                                                              "target_id": target_id})

    def parse(self, response):
        if response.request.url == SOCIALBLADE_ROBOT:
            pass
        else:
            followers_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="followers")).xpath + "/text()"
            twits_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="twits")).xpath + "/text()"
            user_created_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="user_created")).xpath + "/text()"

            artist = response.request.meta["artist"]
            followers = response.xpath(followers_xpath).extract()[0]
            twits = response.xpath(twits_xpath).extract()[0]
            user_created = response.xpath(user_created_xpath).extract()[0]

            item = SocialbladeTwitterItem()
            item["artist"] = artist
            item["followers"] = followers.replace(",", "")
            item["twits"] = twits.replace(",", "")
            item["user_created"] = user_created
            item["url"] = response.url
            item["reserved_date"] = datetime.now().date()
            yield item
