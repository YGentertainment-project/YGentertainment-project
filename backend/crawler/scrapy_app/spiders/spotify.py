import json
import scrapy
from bs4 import BeautifulSoup

from ..items import SpotifyItem
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform
from django.db.models import Q
from datetime import datetime


class SpotifySpider(scrapy.Spider):
    name = "spotify"

    def start_requests(self):
        crawl_url = {}
        spotify_platform_id = Platform.objects.get(name="spotify").id
        CrawlingTarget = CollectTarget.objects.filter(Q(platform_id=spotify_platform_id) & Q(target_url__istartswith="https://open.spotify.com"))
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
        artist_id = response.url[32:]
        initial = "initial-state"
        result = soup.select_one(f"script[id={initial}]").text
        json_object = json.loads(result)
        head = "spotify:artist:"
        dummy = json_object["entities"]["items"][head+artist_id]["nodes"]
        for target in dummy:
            if not target:
                continue
            if target["id"] == "artist_biography_row":
                listen = target["custom"]["monthly_listeners_count"]
                follow = target["custom"]["followers"]
        item = SpotifyItem()
        item["artist"] = artist
        item["monthly_listens"] = listen
        item["followers"] = follow
        item["url1"] = response.url
        item["url2"] = None
        item["reserved_date"] = datetime.now().date()
        yield item
