import scrapy
from ..items import WeverseItem
from config.models import CollectTargetItem
from datetime import datetime
from django.db.models import Q
from crawler.tasks import crawlinglogger


class WeverseSpider(scrapy.Spider):
    name = "weverse"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.LoginDownloaderMiddleware": 100
        },
    }

    def start_requests(self):
        for target in self.crawl_target:
            artist_name = target['artist_name']
            artist_url = target['target_url']
            target_id = target['id']
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_url, len(artist_url)))
            yield scrapy.Request(url=artist_url, callback=self.parse, encoding="utf-8", meta={"artist": artist_name,
                                                                                              "target_id": target_id, "url": artist_url})

    def parse(self, response):
        artist = response.meta["artist"]
        url = response.meta["url"]
        sub_xpath = CollectTargetItem.objects.get(Q(collect_target_id=response.meta["target_id"]) & Q(target_name="weverses")).xpath + "/text()"
        sub = None
        try:
            sub = response.xpath(sub_xpath).get()
        except ValueError:
            crawlinglogger.error(f"[400], {artist}, weverse, {url}")
            # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.

        if sub is None:
            crawlinglogger.error(f"[400], {artist}, weverse, {url}")
            # Xpath가 오류여서 해당 페이지에서 element를 찾을 수 없는 경우입니다.
            # 혹은, Xpath에는 문제가 없으나 해당 페이지의 Element가 없는 경우입니다.
            # 오류일 경우 item을 yield 하지 않아야 합니다.
        else:
            item = WeverseItem()
            item["artist"] = artist
            item["weverses"] = int(sub[:-6].replace(",", ""))
            item["url"] = response.url
            item["reserved_date"] = datetime.now().date()
            yield item
