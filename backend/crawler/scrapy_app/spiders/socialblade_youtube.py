import scrapy
from urllib.parse import urlparse

from ..items import SocialbladeYoutubeItem
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform

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
        crawl_url = {}
        youtube_platform_id = Platform.objects.get(name="youtube").id
        CrawlingTarget = CollectTarget.objects.filter(platform_id=youtube_platform_id)
        for row in CrawlingTarget:
            artist_name = Artist.objects.get(id=row.artist_id).name
            artist_url = row.target_url
            crawl_url[artist_name] = artist_url

        for artist, url in crawl_url.items():
            print("artist : {}, url : {}, url_len: {}".format(
                artist, url, len(url)))
            if len(url) > 0:
                if urlparse(url).netloc == SOCIALBLADE_DOMAIN:
                    yield scrapy.Request(url=url, callback=self.parse_social, encoding="utf-8", meta={"artist": artist})
                else:
                    yield scrapy.Request(url=url, callback=self.parse_youtube, encoding="utf-8", meta={"artist": artist})
            else:
                continue

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
            youtubeusertopinfoblock = '\"YouTubeUserTopInfoBlock\"'

            try:
                uploads = response.xpath(
                    f"//*[@id={youtubeusertopinfoblock}]/div[2]/span[2]/text()").get()
                subscribers = response.xpath(
                    f"//*[@id={youtubeusertopinfoblock}]/div[3]/span[2]/text()").get()
                view_text = response.xpath(
                    f"//*[@id={youtubeusertopinfoblock}]/div[4]/span[2]/text()").get()
                user_created = response.xpath(
                    f"//*[@id={youtubeusertopinfoblock}]/div[7]/span[2]/text()").get()
            except ValueError:
                pass
                # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.

            if uploads is None or view_text is None or subscribers is None or user_created is None:
                pass
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
                # item["platform"] = self.name
                item["url"] = response.url
                yield item

    def parse_youtube(self, response):
        artist = view_text = user_created = None
        if response.request.url == YOUTUBE_ROBOT:
            pass
        else:
            artist = response.request.meta["artist"]
            rightcolumn = '\"right-column\"'

            try:
                view_text = response.xpath(
                    f"//*[@id={rightcolumn}]/yt-formatted-string[3]/text()").get()
                user_created = response.xpath(
                    f"//*[@id={rightcolumn}]/yt-formatted-string[2]/span[2]/text()").get()
            except ValueError:
                pass
                # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.

            if view_text is None or user_created is None:
                pass
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
                yield item
