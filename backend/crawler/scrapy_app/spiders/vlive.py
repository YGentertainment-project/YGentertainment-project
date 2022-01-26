import json

import scrapy
from bs4 import BeautifulSoup

from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform
from ..items import VliveItem
from datetime import datetime


class VliveSpider(scrapy.Spider):
    name = "vlive"
    vlive_platform_id = Platform.objects.get(name="vlive").id
    CrawlingTarget = CollectTarget.objects.filter(platform_id=vlive_platform_id)

    def start_requests(self):
        for row in self.CrawlingTarget:
            artist_name = Artist.objects.get(id=row.artist_id).name
            artist_url = row.target_url
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_url, len(artist_url)))
            yield scrapy.Request(url=artist_url, callback=self.parse, encoding="utf-8", meta={"artist": artist_name})

    def parse(self, response):
        artist = response.meta["artist"]
        soup = BeautifulSoup(response.text, "html.parser")
        script_target = soup.select_one("script")
        if script_target is None:
            pass
            # Script Tag 안의 내용이 바뀌어 element를 찾을 수 없는 경우입니다.
            # 혹은, selector의 문법에 문제가 발생한 경우입니다. selector의 형식을 확인 해주세요.
            # 오류일 경우, 더 이상 진행할 수 없습니다.
        else:
            script = script_target.text
            json_object = json.loads(script[27:-308])
            try:
                members = json_object["channel"]["channel"]["memberCount"]
                videoplay = json_object["channel"]["channel"]["videoPlayCountOfStar"]
                videocount = json_object["channel"]["channel"]["videoCountOfStar"]
                videolike = json_object["channel"]["channel"]["videoLikeCountOfStar"]
            except KeyError:
                pass
                # 크롤링 해야할 JSON 부분의 형식이 바뀌어 element를 찾지 못하는 경우입니다.
                # 오류일 경우 item을 yield 하지 않아야 합니다.
            item = VliveItem()
            item["artist"] = artist
            item["likes"] = videolike
            item["members"] = members
            item["plays"] = videoplay
            item["videos"] = videocount
            item["url"] = response.url
            item["reserved_date"] = datetime.now().date()
            yield item

