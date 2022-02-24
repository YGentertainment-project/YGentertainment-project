import scrapy
from ..items import SocialbladeTwitter2Item
from datetime import datetime
from config.models import CollectTargetItem
from django.db.models import Q

SOCIALBLADE_DOMAIN = "socialblade.com"
SOCIALBLADE_ROBOT = "https://socialblade.com/robots.txt"

# 정의 : Socialblade 크롤링을 담당하는 Spider(Twitter2에 해당)
# 목적 : 로그인 과정은 없으나 Selenium은 활용하는 NoLoginDownloaderMiddleware 사용, parse 함수에서 DB에 저장된 Locator(Xpath)에 따라 팔로워 수집
# 담당자 : 성균관대학교 김정규, sunrinkingh2160@gmail.com
# 수정일 : 2022-02-23
class Twitter2Spider(scrapy.Spider):
    name = "twitter2"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.NoLoginDownloaderMiddleware": 100
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
        if response.request.url == SOCIALBLADE_ROBOT:
            pass
        else:
            url = response.url
            artist = response.request.meta["artist"]
            followers_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="followers")).xpath + "/text()"
            twits_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="twits")).xpath + "/text()"
            user_created_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="user_created")).xpath + "/text()"
            try:
                followers = response.xpath(followers_xpath).get()
            except ValueError:
                self.crawl_logger.error(f"[400], {artist}, {self.name}, {followers_xpath}")
            try:
                twits = response.xpath(twits_xpath).get()
            except ValueError:
                self.crawl_logger.error(f"[400], {artist}, {self.name}, {twits_xpath}")
            try:
                user_created = response.xpath(user_created_xpath).get()
            except ValueError:
                self.crawl_logger.error(f"[400], {artist}, {self.name}, {user_created_xpath}")
                # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.
            
            if twits is None or followers is None or user_created is None:
                self.crawl_logger.error(f"[400], {artist}, {self.name}, {url}")
                # Xpath가 오류여서 해당 페이지에서 element를 찾을 수 없는 경우입니다.
                # 혹은, Xpath에는 문제가 없으나 해당 페이지의 Element가 없는 경우입니다.
                # 오류일 경우 item을 yield 하지 않아야 합니다.
            else:
                item = SocialbladeTwitter2Item()
                item["artist"] = artist
                item["followers"] = followers.replace(",", "")
                item["twits"] = twits.replace(",", "")
                item["user_created"] = user_created
                item["url"] = response.url
                item["reserved_date"] = datetime.now().date()
                yield item
