import scrapy
from ..items import SocialbladeTwitter2Item
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform
from datetime import datetime
from config.models import CollectTargetItem
from django.db.models import Q

SOCIALBLADE_DOMAIN = "socialblade.com"
SOCIALBLADE_ROBOT = "https://socialblade.com/robots.txt"


class Twitter2Spider(scrapy.Spider):
    name = "twitter2"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.NoLoginDownloaderMiddleware": 100
        },
    }
    twitter2_platform_id = Platform.objects.get(name="twitter2").id
    CrawlingTarget = CollectTarget.objects.filter(platform_id=twitter2_platform_id)

    def start_requests(self):
        for row in self.CrawlingTarget:
            artist_name = Artist.objects.get(id=row.artist_id).name
            artist_url = row.target_url
            target_id = row.id
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_url, len(artist_url)))
            yield scrapy.Request(url=artist_url, callback=self.parse, encoding="utf-8", meta={"artist": artist_name,
                                                                                              "target_id": target_id})

    def parse(self, response):
        if response.request.url == SOCIALBLADE_ROBOT:
            pass
        else:
            artist = response.request.meta["artist"]
            followers_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="followers")).xpath + "/text()"
            twits_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="twits")).xpath + "/text()"
            user_created_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="user_created")).xpath + "/text()"
            try:
                followers = response.xpath(followers_xpath).get()
                twits = response.xpath(twits_xpath).get()
                user_created = response.xpath(user_created_xpath).get()
            except ValueError:
                pass
                # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.
            if twits is None or followers is None or user_created is None:
                pass
                # Xpath가 오류여서 해당 페이지에서 element를 찾을 수 없는 경우입니다.
                # 혹은, Xpath에는 문제가 없으나 해당 페이지의 Element가 없는 경우입니다.
                # 오류일 경우 item을 yield 하지 않아야 합니다.
            else:
                item = SocialbladeTwitter2Item()
                item["artist"] = artist
                item["followers"] = followers.replace(",", "")
                item["twits"] = twits.replace(",", "")
                item["user_created"] = user_created
                item["url"] = response.url
                item["reserved_date"] = datetime.now().date()
                yield item
