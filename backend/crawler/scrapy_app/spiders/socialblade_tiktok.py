import scrapy
from ..items import SocialbladeTiktokItem
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform
from datetime import datetime
from config.models import CollectTargetItem
from django.db.models import Q

SOCIALBLADE_DOMAIN = "socialblade.com"
SOCIALBLADE_ROBOT = "https://socialblade.com/robots.txt"


class TiktokSpider(scrapy.Spider):
    name = "tiktok"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.NoLoginDownloaderMiddleware": 100
        },
    }
    tiktok_platform_id = Platform.objects.get(name="tiktok").id
    CrawlingTarget = CollectTarget.objects.filter(platform_id=tiktok_platform_id)

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
            followers_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="followers")).xpath + "/text()"
            likes_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="likes")).xpath + "/text()"
            uploads_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="uploads")).xpath + "/text()"

            artist = response.request.meta["artist"]
            uploads = response.xpath(uploads_xpath).get()
            followers = response.xpath(followers_xpath).get()
            likes = response.xpath(likes_xpath).get()

            item = SocialbladeTiktokItem()
            item["artist"] = artist
            item["uploads"] = 0 if not uploads else uploads.replace(",", "")
            item["followers"] = 0 if not followers else followers.replace(",", "")
            item["likes"] = 0 if not likes else likes.replace(",", "")
            item["url"] = response.url
            item["reserved_date"] = datetime.now().date()
            yield item
