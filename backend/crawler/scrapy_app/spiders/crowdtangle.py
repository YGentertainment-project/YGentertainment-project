from urllib import parse

import scrapy
from ..items import CrowdtangleFacebookItem, CrowdtangleInstagramItem
from datetime import datetime
from config.models import CollectTargetItem
from django.db.models import Q


class CrowdTangleSpider(scrapy.Spider):
    name = "crowdtangle"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.LoginDownloaderMiddleware": 100
        },
    }
    facebook_id = Platform.objects.get(name="facebook").id
    instagram_id = Platform.objects.get(name="instagram").id
    CrawlingTarget = CollectTarget.objects.filter(Q(platform_id=facebook_id) | Q(platform_id=instagram_id))

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
        artist = response.meta["artist"]
        follower_xpath = CollectTargetItem.objects.get(
            Q(collect_target_id=response.meta["target_id"]) & Q(target_name="followers")).xpath + "/text()"
        follower_num = response.xpath(follower_xpath).get()
        url = parse.urlparse(response.url)
        target = parse.parse_qs(url.query)["platform"][0]
        if target == "facebook":
            item = CrowdtangleFacebookItem()
            item["artist"] = artist
            item["followers"] = int(follower_num.replace(",", ""))
            item["url"] = response.url
            item["reserved_date"] = datetime.now().date()
            yield item
        else:
            item = CrowdtangleInstagramItem()
            item["artist"] = artist
            item["followers"] = int(follower_num.replace(",", ""))
            item["url"] = response.url
            item["reserved_date"] = datetime.now().date()
            yield item
