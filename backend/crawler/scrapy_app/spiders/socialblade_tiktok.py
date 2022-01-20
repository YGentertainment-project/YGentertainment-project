import scrapy
from urllib.parse import urlparse
from ..items import SocialbladeTiktokItem
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform

SOCIALBLADE_DOMAIN = "socialblade.com"
SOCIALBLADE_ROBOT = "https://socialblade.com/robots.txt"


class TiktokSpider(scrapy.Spider):
    name = "tiktok"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.NoLoginDownloaderMiddleware": 100
        },
    }

    def start_requests(self):
        crawl_url = {}
        tiktok_platform_id = Platform.objects.get(name="tiktok").id
        CrawlingTarget = CollectTarget.objects.filter(platform_id=tiktok_platform_id)
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
        domain = urlparse(response.url).netloc
        artist = uploads = followers = likes = None

        if domain == SOCIALBLADE_DOMAIN:
            if response.request.url == SOCIALBLADE_ROBOT:
                pass
            else:
                artist = response.request.meta["artist"]
                youtubeusertopinfoblock = "YouTubeUserTopInfoBlock"
                uploads = response.xpath(f"//*[@id={youtubeusertopinfoblock}]/div[2]/span[2]/text()").get()
                followers = response.xpath(f"//*[@id={youtubeusertopinfoblock}]/div[3]/span[2]/text()").get()
                likes = response.xpath(f"//*[@id={youtubeusertopinfoblock}]/div[5]/span[2]/text()").get()
        if response.request.url == SOCIALBLADE_ROBOT:
            pass
        else:
            item = SocialbladeTiktokItem()
            item["artist"] = artist
            item["uploads"] = 0 if not uploads else uploads.replace(",", "")
            item["followers"] = 0 if not followers else followers.replace(",", "")
            item["likes"] = 0 if not likes else likes.replace(",", "")
            item["url"] = response.url
            yield item
