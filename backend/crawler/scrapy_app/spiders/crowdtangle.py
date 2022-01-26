from urllib import parse

import scrapy
from ..items import CrowdtangleFacebookItem, CrowdtangleInstagramItem
from dataprocess.models import CollectTarget
from dataprocess.models import Artist


class CrowdTangleSpider(scrapy.Spider):
    name = "crowdtangle"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.LoginDownloaderMiddleware": 100
        },
    }

    def start_requests(self):
        crawl_url = {}
        CrawlingTarget = CollectTarget.objects.filter(target_url__istartswith="https://apps.crowdtangle.com")
        for row in CrawlingTarget:
            artist_name = Artist.objects.get(id=row.artist_id).name
            artist_url = row.target_url
            crawl_url[artist_url] = artist_name

        for url, artist in crawl_url.items():
            print("artist : {}, url : {}, url_len: {}".format(
                artist, url, len(url)))
            if len(url) > 0:
                yield scrapy.Request(url=url, callback=self.parse, encoding="utf-8", meta={"artist": artist})
            else:
                continue

    def parse(self, response):
        artist = response.meta["artist"]
        follower_num = None
        try:
            follower_num = response.xpath(
                "/html/body/div[3]/div/div/div/div/div[3]/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div/span[1]/text()").get()
        except ValueError:
            pass
            # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.

        if follower_num is None:
            pass
            # Xpath가 오류여서 해당 페이지에서 element를 찾을 수 없는 경우입니다.
            # 혹은, Xpath에는 문제가 없으나 해당 페이지의 Element가 없는 경우입니다.
            # 오류일 경우 item을 yield 하지 않아야 합니다.
        else:
            url = parse.urlparse(response.url)
            target = parse.parse_qs(url.query)["platform"][0]
            if target == "facebook":
                item = CrowdtangleFacebookItem()
                item["artist"] = artist
                item["followers"] = int(follower_num.replace(",", ""))
                item["url"] = response.url
                yield item
            else:
                item = CrowdtangleInstagramItem()
                item["artist"] = artist
                item["followers"] = int(follower_num.replace(",", ""))
                item["url"] = response.url
                yield item
