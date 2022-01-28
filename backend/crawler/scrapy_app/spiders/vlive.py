import json

import scrapy
from bs4 import BeautifulSoup

from ..items import VliveItem
from datetime import datetime


class VliveSpider(scrapy.Spider):
    name = "vlive"

    def start_requests(self):
        for target in self.crawl_target:
            artist_name = target['artist_name']
            artist_url = target['target_url']
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_url, len(artist_url)))
            yield scrapy.Request(url=artist_url, callback=self.parse, encoding="utf-8", meta={"artist": artist_name})

    def parse(self, response):
        artist = response.meta["artist"]
        soup = BeautifulSoup(response.text, "html.parser")
        script_target = soup.select_one("script")
        script = script_target.text
        json_object = json.loads(script[27:-308])
        members = json_object["channel"]["channel"]["memberCount"]
        videoplay = json_object["channel"]["channel"]["videoPlayCountOfStar"]
        videocount = json_object["channel"]["channel"]["videoCountOfStar"]
        videolike = json_object["channel"]["channel"]["videoLikeCountOfStar"]

        item = VliveItem()
        item["artist"] = artist
        item["likes"] = videolike
        item["members"] = members
        item["plays"] = videoplay
        item["videos"] = videocount
        item["url"] = response.url
        item["reserved_date"] = datetime.now().date()
        yield item
