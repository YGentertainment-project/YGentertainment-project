import json
from json import JSONDecodeError

import scrapy
from bs4 import BeautifulSoup

from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError

from ..items import VliveItem
from datetime import datetime
from crawler.tasks import crawlinglogger


class VliveSpider(scrapy.Spider):
    name = "vlive"

    def start_requests(self):
        for target in self.crawl_target:
            artist_name = target['artist_name']
            artist_url = target['target_url']
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_url, len(artist_url)))
            yield scrapy.Request(url=artist_url, callback=self.parse, encoding="utf-8", meta={"artist": artist_name, "url": artist_url},
                                 errback=self.errback)

    def parse(self, response):
        artist = response.meta["artist"]
        url = response.meta["url"]
        soup = BeautifulSoup(response.text, "html.parser")
        script_target = soup.select_one("script")
        if script_target is None:
            crawlinglogger.error(f"[400], {artist}, vlive, {url}")
            # Script Tag 안의 내용이 바뀌어 element를 찾을 수 없는 경우입니다.
            # 혹은, selector의 문법에 문제가 발생한 경우입니다. selector의 형식을 확인 해주세요.
            # 오류일 경우, 더 이상 진행할 수 없습니다.
        else:
            script = script_target.text
            try:
                json_object = json.loads(script[27:-308])
                members = json_object["channel"]["channel"]["memberCount"]
                videoplay = json_object["channel"]["channel"]["videoPlayCountOfStar"]
                videocount = json_object["channel"]["channel"]["videoCountOfStar"]
                videolike = json_object["channel"]["channel"]["videoLikeCountOfStar"]
            except KeyError:
                crawlinglogger.error(f"[400], {artist}, vlive, {url}")
                # 크롤링 해야할 JSON 부분의 형식이 바뀌어 element를 찾지 못하는 경우입니다.
                # 오류일 경우 item을 yield 하지 않아야 합니다.
            except JSONDecodeError:
                crawlinglogger.error(f"[400] {artist}, vlive, {url}")
                # 해당 페이지의 Element가 없는 경우입니다.
                # 오류일 경우 item을 yield 하지 않아야 합니다.
            else:
                item = VliveItem()
                item["artist"] = artist
                item["likes"] = videolike
                item["members"] = members
                item["plays"] = videoplay
                item["videos"] = videocount
                item["url"] = response.url
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
