import scrapy
from ..items import MelonItem
from datetime import datetime
from config.models import CollectTargetItem
from django.db.models import Q
from crawler.tasks import crawlinglogger


class MelonSpider(scrapy.Spider):
    name = "melon"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.NoLoginDownloaderMiddleware": 100
        },
    }

    def start_requests(self):
        for target in self.crawl_target:
            artist_name = target['artist_name']
            artist_urls = [target['target_url'], target['target_url_2']]
            target_id = target['id']
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_urls[0], len(artist_urls[0])))
            yield scrapy.Request(url=artist_urls[0], callback=self.parse, encoding="utf-8", meta={"artist": artist_name,
                                                                                                  "next": artist_urls[1],
                                                                                                  "target_id": target_id})

    def parse(self, response):
        artist = response.meta["artist"]
        listener_target = streaming_target = None
        listener_xpath = CollectTargetItem.objects.get(Q(collect_target_id=response.meta["target_id"]) & Q(target_name="listeners")).xpath + "/text()"
        streaming_xpath = CollectTargetItem.objects.get(Q(collect_target_id=response.meta["target_id"]) & Q(target_name="streams")).xpath + "/text()"
        try:
            listener_target = response.xpath(listener_xpath).extract()[2]
        except ValueError:
            crawlinglogger.error(f"[400], {artist}, melon, {listener_xpath}")
            # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.
        
        try:
            streaming_target = response.xpath(streaming_xpath).extract()[2]
        except ValueError:
            crawlinglogger.error(f"[400], {artist}, melon, {streaming_xpath}")

        if listener_target is None:
            crawlinglogger.error(f"[400], {artist}, melon, {listener_xpath}")
            # Xpath가 오류여서 해당 페이지에서 element를 찾을 수 없는 경우입니다.
            # 혹은, Xpath에는 문제가 없으나 해당 페이지의 Element가 없는 경우입니다.
            # 오류일 경우 item을 yield 하지 않아야 합니다.
        elif streaming_target is None:
            crawlinglogger.error(f"[400], {artist}, melon, {streaming_xpath}")
        else:
            listener = listener_target.replace(",", "")
            streaming = streaming_target.replace(",", "")
            url1 = response.url
            yield scrapy.Request(url=response.meta["next"], callback=self.parse_melon, encoding="utf-8",
                                 meta={"artist": artist,
                                       "listeners": listener,
                                       "streams": streaming,
                                       "url1": url1,
                                       "target_id": response.meta["target_id"]})

    def parse_melon(self, response):
        fans_target = None
        fans_xpath = CollectTargetItem.objects.get(Q(collect_target_id=response.meta["target_id"]) & Q(target_name="fans")).xpath + "/text()"
        try:
            fans_target = response.xpath(fans_xpath).get()
        except ValueError:
            pass
            # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.

        if fans_target is None:
            pass
            # Xpath가 오류여서 해당 페이지에서 element를 찾을 수 없는 경우입니다.
            # 혹은, Xpath에는 문제가 없으나 해당 페이지의 Element가 없는 경우입니다.
            # 오류일 경우 item을 yield 하지 않아야 합니다.
        else:
            item = MelonItem()
            item["artist"] = response.meta["artist"]
            item["listeners"] = response.meta["listeners"]
            item["streams"] = response.meta["streams"]
            item["fans"] = fans_target.replace(",", "")
            item["url1"] = response.meta["url1"]
            item["url2"] = response.url
            item["reserved_date"] = datetime.now().date()
            yield item
