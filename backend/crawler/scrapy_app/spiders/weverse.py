import scrapy
from ..items import WeverseItem
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform


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
        sub = None
        try:
            sub = response.xpath("/html/body/div[1]/div/section/aside/div/div[1]/text()").get()
        except ValueError:
            pass
            # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.

        if sub is None:
            pass
            # Xpath가 오류여서 해당 페이지에서 element를 찾을 수 없는 경우입니다.
            # 혹은, Xpath에는 문제가 없으나 해당 페이지의 Element가 없는 경우입니다.
            # 오류일 경우 item을 yield 하지 않아야 합니다.
        else:
            item = WeverseItem()
            item["artist"] = artist
            item["weverses"] = int(sub[:-6].replace(",", ""))
            item["url"] = response.url
            yield item
