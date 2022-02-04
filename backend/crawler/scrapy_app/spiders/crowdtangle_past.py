from urllib import parse

import scrapy
from ..items import CrowdtangleFacebookItem, CrowdtangleInstagramItem
from datetime import datetime


class CrowdTangleSpider(scrapy.Spider):
    name = "crowdtangle-past"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.LoginDownloaderMiddleware": 100
        },
    }

    def start_requests(self):
        for target in self.crawl_target:
            artist_name = target["artist_name"]
            artist_url = target["target_url"].replace("3months", "1month")
            target_id = target["id"]
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_url, len(artist_url)))
            yield scrapy.Request(url=artist_url, callback=self.parse, encoding="utf-8", meta={"artist": artist_name,
                                                                                              "target_id": target_id,
                                                                                              "target_url": target["target_url"]})

    def parse_date(self, string):
        date_object = datetime.strptime(string, "%b %d, %Y")
        return date_object.date()

    def parse(self, response):
        artist = response.meta["artist"]
        reserved_xpath = "//g[@class='bar-graph']/text[1]/title" + "/text()"
        follower_xpath = "//g[@class='bar-graph']/text[2]/title" + "/text()"
        follower_num = response.xpath(follower_xpath).extract()
        reserved_date = response.xpath(reserved_xpath).extract()
        url = parse.urlparse(response.url)
        target = parse.parse_qs(url.query)["platform"][0]
        for i in range(0, 30+1):
            if target == "facebook":
                item = CrowdtangleFacebookItem()
                item["artist"] = artist
                item["followers"] = int(follower_num[i].replace(",", ""))
                item["url"] = response.meta["target_url"]
                item["reserved_date"] = self.parse_date(reserved_date[i])
                yield item
            else:
                item = CrowdtangleInstagramItem()
                item["artist"] = artist
                item["followers"] = int(follower_num[i].replace(",", ""))
                item["url"] = response.meta["target_url"]
                item["reserved_date"] = self.parse_date(reserved_date[i])
                yield item
