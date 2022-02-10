import json
import scrapy
from bs4 import BeautifulSoup
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError

from ..items import SpotifyItem
from datetime import datetime
from crawler.tasks import crawlinglogger


class SpotifySpider(scrapy.Spider):
    name = "spotify"

    def start_requests(self):
        for target in self.crawl_target:
            artist_name = target['artist_name']
            artist_url = target['target_url']
            artist_url_2 = target['target_url_2']
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_url, len(artist_url)))
            yield scrapy.Request(url=artist_url, callback=self.parse, encoding="utf-8", meta={"artist": artist_name,
                                                                                              "url": artist_url,
                                                                                              "url2": artist_url_2},
                                 errback=self.errback)

    def parse(self, response):
        artist = response.meta["artist"]
        url = response.meta["url"]
        listen = follow = None
        try:
            listen = response.xpath("//*[contains(@class,'DrwCs')]/text()").get()
            follow = response.xpath("//*[contains(@class,'jxvBiz')]/text()").get()
        except ValueError:
            crawlinglogger.error(f"[400], {artist}, spotify, {url}")
            # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.
        if listen is None or follow is None:
            crawlinglogger.error(f"[400] {artist}, spotify, {url}")
            # Xpath가 오류여서 해당 페이지에서 element를 찾을 수 없는 경우입니다.
            # 혹은, Xpath에는 문제가 없으나 해당 페이지의 Element가 없는 경우입니다.
            # 오류일 경우 item을 yield 하지 않아야 합니다.
        else:
            item = SpotifyItem()
            item["artist"] = artist
            item["monthly_listens"] = listen[:-18].replace(",","")
            item["followers"] = follow.replace(",","")
            item["url1"] = response.url
            item["url2"] = response.meta["url2"]
            item["reserved_date"] = datetime.now().date()
            yield item

    def errback(self, failure):
        if failure.check(HttpError):
            status = failure.value.response.status
            artist = failure.request.meta["artist"]
            url = failure.request.url
            if status == 404:
                crawlinglogger.error(f"[400], {artist}, spotify, {url}")
            elif status == 403:
                crawlinglogger.error(f"[402], {artist}, spotify, {url}")
        elif failure.check(DNSLookupError):
            artist = failure.request.meta["artist"]
            url = failure.request.url
            crawlinglogger.error(f"[400], {artist}, spotify, {url}")
