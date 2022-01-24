import scrapy
from ..items import WeverseItem
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform
from datetime import datetime


class WeverseSpider(scrapy.Spider):
    name = "weverse"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.LoginDownloaderMiddleware": 100
        },
    }

    def start_requests(self):
        crawl_url = {}
        weverse_platform_id = Platform.objects.get(name="weverse").id
        CrawlingTarget = CollectTarget.objects.filter(platform_id=weverse_platform_id)
        for row in CrawlingTarget:
            artist_name = Artist.objects.get(id=row.artist_id).name
            artist_url = row.target_url
            crawl_url[artist_name] = artist_url

        for artist, url in crawl_url.items():
            print("artist : {}, url : {}, url_len: {}".format(
                artist, url, len(url)))
            if len(url) > 0:
                yield scrapy.Request(url=url, callback=self.parse, encoding="utf-8", meta={"artist": artist})
            else:
                continue

    def parse(self, response):
        artist = response.meta["artist"]
        sub = response.xpath("/html/body/div[1]/div/section/aside/div/div[1]/text()").extract()
        # WINNER의 경우, 페이지는 있으나 구독자 수가 공개되어 있지 않으므로 0으로 처리했습니다.
        item = WeverseItem()
        item["artist"] = artist
        item["weverses"] = 0 if not sub else int(sub[0][:-6].replace(",", ""))
        item["url"] = response.url
        item["reserved_date"] = datetime.now().date()
        yield item
