import scrapy
from urllib.parse import urlparse

from ..items import SocialbladeYoutubeItem
from datetime import datetime
from config.models import CollectTargetItem
from django.db.models import Q
from crawler.tasks import crawlinglogger

SOCIALBLADE_DOMAIN = "socialblade.com"
YOUTUBE_DOMAIN = "youtube.com"
SOCIALBLADE_ROBOT = "https://socialblade.com/robots.txt"
YOUTUBE_ROBOT = "https://youtube.com/robots.txt"


class YoutubeSpider(scrapy.Spider):
    name = "youtube"
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
            if urlparse(artist_url).netloc == SOCIALBLADE_DOMAIN:
                yield scrapy.Request(url=artist_url, callback=self.parse_social, encoding="utf-8", meta={"artist": artist_name,
                                                                                                         "target_id": target_id})
            else:
                yield scrapy.Request(url=artist_url, callback=self.parse_youtube, encoding="utf-8", meta={"artist": artist_name,
                                                                                                          "target_id": target_id})

    # 구독자 문자열을 정수형 숫자로 반환
    def parse_subscribers(self, subs_text):
        subs_param = subs_text[-1].strip()
        subs_num = float(subs_text[0:-1].strip())
        result = subs_num
        if subs_param == "M":
            result = int(subs_num * 1000000)  # 1000을 곱해준 정수값을 반환
        elif subs_param == "K":
            result = int(subs_num * 1000)  # 정수값을 반환
        return int(result)

    # "1,334,635,139" 형태의 숫자를 정수형 변수로 반환
    def parse_comma_text(self, view_text):
        result = view_text.replace(",", "")
        return int(result)

    def parse_social(self, response):
        artist = uploads = subscribers = view_text = user_created = None
        if response.request.url == SOCIALBLADE_ROBOT:
            pass
        else:
            artist = response.request.meta["artist"]
            sub_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="subscribers")).xpath + "/text()"
            views_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="views")).xpath + "/text()"
            uploads_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="uploads")).xpath + "/text()"
            user_created_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="user_created")).xpath + "/text()"

            try:
                uploads = response.xpath(uploads_xpath).get()
                subscribers = response.xpath(sub_xpath).get()
                view_text = response.xpath(views_xpath).get()
                user_created = response.xpath(user_created_xpath).get()
            except ValueError:
                crawlinglogger.error(f"[400] {artist} - youtube - {sub_xpath}, {views_xpath}, {uploads_xpath}, {user_created_xpath}")
                # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.

            if uploads is None or view_text is None or subscribers is None or user_created is None:
                crawlinglogger.error(f"[400] {artist} - youtube - {sub_xpath}, {views_xpath}, {uploads_xpath}, {user_created_xpath}")
                # Xpath가 오류여서 해당 페이지에서 element를 찾을 수 없는 경우입니다.
                # 혹은, Xpath에는 문제가 없으나 해당 페이지의 Element가 없는 경우입니다.
                # 오류일 경우 item을 yield 하지 않아야 합니다.
            else:
                subscribers = self.parse_subscribers(subscribers)
                views = self.parse_comma_text(view_text)
                uploads = self.parse_comma_text(uploads)

                item = SocialbladeYoutubeItem()
                item["artist"] = artist
                item["uploads"] = uploads
                item["subscribers"] = subscribers
                item["views"] = views
                item["user_created"] = user_created
                item["reserved_date"] = datetime.now().date()
                # item["platform"] = self.name
                item["url"] = response.url
                yield item

    def parse_youtube(self, response):
        artist = view_text = user_created = None
        if response.request.url == YOUTUBE_ROBOT:
            pass

            views_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="views")).xpath + "/text()"
            user_created_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="user_created")).xpath + "/text()"
            artist = response.request.meta["artist"]
            try:
                view_text = response.xpath(views_xpath).get()
            except ValueError:
                crawlinglogger.error(f"[400] {artist} - youtube - {views_xpath}")
            try:
                user_created = response.xpath(user_created_xpath).get()
            except ValueError:
                crawlinglogger.error(f"[400] {artist} - youtube - {user_created_xpath}")
                # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.

            if view_text is None:
                crawlinglogger.error(f"[400] {artist} - youtube - {views_xpath}")
            elif user_created is None:
                crawlinglogger.error(f"[400] {artist} - youtube - {user_created_xpath}")
                # Xpath가 오류여서 해당 페이지에서 element를 찾을 수 없는 경우입니다.
                # 혹은, Xpath에는 문제가 없으나 해당 페이지의 Element가 없는 경우입니다.
                # 오류일 경우 item을 yield 하지 않아야 합니다.
            else:
                # "조회수 168,048,278회" 형태의 문자열에서 조회수에 해당하는 숫자만 추출
                view_text = view_text[:-5].strip()
                views = self.parse_comma_text(view_text)

                item = SocialbladeYoutubeItem()
                item["artist"] = artist
                item["views"] = views
                item["user_created"] = user_created
                item["url"] = response.url
                item["reserved_date"] = datetime.now().date()
                yield item
