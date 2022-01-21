
import scrapy
from ..items import MelonItem
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform
from django.db.models import Q


class MelonSpider(scrapy.Spider):
    name = "melon"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.NoLoginDownloaderMiddleware": 100
        },
    }

    def start_requests(self):
        crawl_url = {}
        melon_platform_id = Platform.objects.get(name="melon").id
        CrawlingTarget = CollectTarget.objects.filter(Q(platform_id=melon_platform_id) & Q(target_url__istartswith="https://xn--o39an51b2re.com"))
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
        mainwrapper = '\"main-wrapper\"'
        listener = response.xpath(
            f"//*[@id={mainwrapper}]/div/div[2]/div[2]/div/div/div/ul/li[3]/text()").extract()[2].replace(",", "")
        streaming = response.xpath(
            f"//*[@id={mainwrapper}]/div/div[2]/div[2]/div/div/div/ul/li[4]/text()").extract()[2].replace(",", "")
        url1 = response.url
        yield scrapy.Request(url=response.meta["next"], callback=self.parse_melon, encoding="utf-8",
                             meta={"artist": artist,
                                   "listeners": listener,
                                   "streams": streaming,
                                   "url1": url1})

        item = MelonItem()
        d_like_count = '\"d_like_count\"'
        fans = response.xpath(
            f"//span[@id={d_like_count}]/text()").get().replace(",", "")
        item["artist"] = response.meta["artist"]
        item["listeners"] = response.meta["listeners"]
        item["streams"] = response.meta["streams"]
        item["fans"] = fans
        item["url1"] = response.meta["url1"]
        item["url2"] = response.url
        yield item
