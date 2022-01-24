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

    def start_requests(self):
        crawl_url = {}
        vlive_platform_id = Platform.objects.get(name="vlive").id
        CrawlingTarget = CollectTarget.objects.filter(platform_id=vlive_platform_id)
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
        soup = BeautifulSoup(response.text, "html.parser")
        script = soup.find("script").get_text()
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
