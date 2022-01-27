import json
import scrapy
from bs4 import BeautifulSoup

from ..items import SpotifyItem
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform
from django.db.models import Q
from datetime import datetime
from ..middlewares import crawlinglogger


class SpotifySpider(scrapy.Spider):
    name = "spotify"
    spotify_platform_id = Platform.objects.get(name="spotify").id
    CrawlingTarget = CollectTarget.objects.filter(platform_id=spotify_platform_id)

    def start_requests(self):
        for row in self.CrawlingTarget:
            artist_name = Artist.objects.get(id=row.artist_id).name
            artist_url = row.target_url
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_url, len(artist_url)))
            yield scrapy.Request(url=artist_url, callback=self.parse, encoding="utf-8", meta={"artist": artist_name, "url": artist_url})

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
