import scrapy
from ..items import MelonItem
from datetime import datetime
from config.models import CollectTargetItem
from django.db.models import Q


class MelonSpider(scrapy.Spider):
    name = "melon"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.NoLoginDownloaderMiddleware": 100
        },
    }
    melon_platform_id = Platform.objects.get(name="melon").id
    CrawlingTarget = CollectTarget.objects.filter(platform_id=melon_platform_id)

    def start_requests(self):
        for target in self.crawl_target:
            artist_name = target['artist_name']
            artist_urls = [target['target_url'], target['target_url_2']]
            target_id = target['id']
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_urls[0], len(artist_urls[0])))
            yield scrapy.Request(url=artist_urls[0], callback=self.parse, encoding="utf-8", meta={"artist": artist_name,
                                                                                                  "next": artist_urls[1],
                                                                                                  "target_id": target_id})

    def parse(self, response):
        artist = response.meta["artist"]
        listener_xpath = CollectTargetItem.objects.get(Q(collect_target_id=response.meta["target_id"]) & Q(target_name="listeners")).xpath + "/text()"
        streaming_xpath = CollectTargetItem.objects.get(Q(collect_target_id=response.meta["target_id"]) & Q(target_name="streams")).xpath + "/text()"

        listener = response.xpath(listener_xpath).extract()[2].replace(",", "")
        streaming = response.xpath(streaming_xpath).extract()[2].replace(",", "")
        url1 = response.url
        yield scrapy.Request(url=response.meta["next"], callback=self.parse_melon, encoding="utf-8",
                             meta={"artist": artist,
                                   "listeners": listener,
                                   "streams": streaming,
                                   "url1": url1,
                                   "target_id": response.meta["target_id"]})

    def parse_melon(self, response):
        item = MelonItem()
        fans_xpath = CollectTargetItem.objects.get(Q(collect_target_id=response.meta["target_id"]) & Q(target_name="fans")).xpath + "/text()"
        fans = response.xpath(fans_xpath).get().replace(",", "")
        item["artist"] = response.meta["artist"]
        item["listeners"] = response.meta["listeners"]
        item["streams"] = response.meta["streams"]
        item["fans"] = fans
        item["url1"] = response.meta["url1"]
        item["url2"] = response.url
        item["reserved_date"] = datetime.now().date()
        yield item
