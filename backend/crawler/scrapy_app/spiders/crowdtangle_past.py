from urllib import parse

import scrapy
from ..items import CrowdtangleFacebookItem, CrowdtangleInstagramItem
from datetime import datetime


# 정의 : Crowdtangle 크롤링을 담당하는 Spider(Facebook, Instagram에 해당), Crowdtangle에서 30일을 기준으로 과거 데이터를 수집
# 목적 : 로그인 과정을 수행하는 LoginDownloaderMiddleware 사용, parse 함수에서 DB에 저장된 Locator(Xpath)에 따라 팔로워 수집
#       일부 누락된 데이터를 얻기 위한 Spot성 Spider, 따로 스케줄링을 걸어두지 않음.
# 담당자 : 성균관대학교 김정규, sunrinkingh2160@gmail.com
# 수정일 : 2022-02-23
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
