import json
import scrapy
from bs4 import BeautifulSoup
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError

from ..items import SpotifyItem
from datetime import datetime
from ..middlewares import crawlinglogger


class SpotifySpider(scrapy.Spider):
    name = "spotify"

    def start_requests(self):
        for target in self.crawl_target:
            artist_name = target['artist_name']
            artist_url = [target['target_url'], target['target_url_2']]
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_url, len(artist_url)))
            yield scrapy.Request(url=artist_url, callback=self.parse, encoding="utf-8", meta={"artist": artist_name, "url": artist_url},
                                 errback=self.errback)

    def parse(self, response):
        artist = response.meta["artist"]
        url = response.meta["url"]
        soup = BeautifulSoup(response.text, "html.parser")
        artist_id = response.url[32:]
        initial = "initial-state"
        result_target = soup.select_one(f"script[id={initial}]")
        if result_target is None:
            crawlinglogger.error(f"[400] {artist} - spotify - {url}")
            # Script Tag 안의 내용이 바뀌어 element를 찾을 수 없는 경우입니다.
            # 혹은, selector의 문법에 문제가 발생한 경우입니다. selector의 형식을 확인 해주세요.
            # 오류일 경우, 더 이상 진행할 수 없습니다.
        else:
            result = result_target.text
            json_object = json.loads(result)
            try:
                head = "spotify:artist:"
                dummy = json_object["entities"]["items"][head + artist_id]["nodes"]
                for target in dummy:
                    if not target:
                        continue
                    if target["id"] == "artist_biography_row":
                        listen = target["custom"]["monthly_listeners_count"]
                        follow = target["custom"]["followers"]
            except KeyError:
                crawlinglogger.error(f"[400] {artist} - spotify - {url}")
                # 크롤링 해야할 JSON 부분의 형식이 바뀌어 element를 찾지 못하는 경우입니다.
                # 오류일 경우 item을 yield 하지 않아야 합니다.
            item = SpotifyItem()
            item["artist"] = artist
            item["monthly_listens"] = listen
            item["followers"] = follow
            item["url1"] = response.url
            item["url2"] = None
            item["reserved_date"] = datetime.now().date()
            yield item

    def errback(self, failure):
        if failure.check(HttpError):
            status = failure.value.response.status
            artist = failure.request.meta["artist"]
            url = failure.request.url
            if status == 404:
                crawlinglogger.error(f"[400] {artist} - spotify - {url}")
            elif status == 403:
                crawlinglogger.error(f"[402] {artist} - spotify - {url}")
        elif failure.check(DNSLookupError):
            artist = failure.request.meta["artist"]
            url = failure.request.url
            crawlinglogger.error(f"[400] {artist} - spotify - {url}")
