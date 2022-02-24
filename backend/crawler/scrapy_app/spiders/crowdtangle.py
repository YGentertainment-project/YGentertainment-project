from urllib import parse

import scrapy
from ..items import CrowdtangleFacebookItem, CrowdtangleInstagramItem
from datetime import datetime
from config.models import CollectTargetItem
from django.db.models import Q

# 정의 : Crowdtangle 크롤링을 담당하는 Spider(Facebook, Instagram에 해당)
# 목적 : 로그인 과정을 수행하는 LoginDownloaderMiddleware 사용, parse 함수에서 DB에 저장된 Locator(Xpath)에 따라 팔로워 수집
# 담당자 : 성균관대학교 김정규, sunrinkingh2160@gmail.com
# 수정일 : 2022-02-23
class CrowdTangleSpider(scrapy.Spider):
    name = "crowdtangle"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.LoginDownloaderMiddleware": 100
        },
    }

    def start_requests(self):
        for target in self.crawl_target:
            artist_name = target['artist_name']
            artist_url = target['target_url']
            target_id = target['id']
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_url, len(artist_url)))
            yield scrapy.Request(url=artist_url, callback=self.parse, encoding="utf-8", meta={"artist": artist_name,
                                                                                              "target_id": target_id})

    def parse(self, response):
        artist = response.meta["artist"]
        url = response.url
        follower_xpath = CollectTargetItem.objects.get(Q(collect_target_id=response.meta["target_id"]) & Q(target_name="followers")).xpath + "/text()"
        follower_num = None
        try:
            follower_num = response.xpath(follower_xpath).get()
        except ValueError:
            self.crawl_logger.error(f"[400], {artist}, {self.name}, {follower_xpath}")
            # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.

        if follower_num is None:
            self.crawl_logger.error(f"[400], {artist}, {self.name}, {url}")
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
                item["reserved_date"] = datetime.now().date()
                yield item
            else:
                item = CrowdtangleInstagramItem()
                item["artist"] = artist
                item["followers"] = int(follower_num.replace(",", ""))
                item["url"] = response.url
                item["reserved_date"] = datetime.now().date()
                yield item
