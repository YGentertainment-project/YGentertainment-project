import scrapy
from ..items import SocialbladeTiktokItem
from datetime import datetime
from config.models import CollectTargetItem
from django.db.models import Q
from crawler.tasks import crawlinglogger

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
            artist = response.request.meta["artist"]
            followers_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="followers")).xpath + "/text()"
            likes_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="likes")).xpath + "/text()"
            uploads_xpath = CollectTargetItem.objects.get(
                Q(collect_target_id=response.meta["target_id"]) & Q(target_name="uploads")).xpath + "/text()"
            try:
                uploads = response.xpath(uploads_xpath).get()
            except ValueError:
                crawlinglogger.error(f"[400], {artist}, tictok, {uploads_xpath}")
            try:
                followers = response.xpath(followers_xpath).get()
            except ValueError:
                crawlinglogger.error(f"[400], {artist}, tictok, {followers_xpath}")
            try:    
                likes = response.xpath(likes_xpath).get()
            except ValueError:
                crawlinglogger.error(f"[400], {artist}, tictok, {likes_xpath}")
                # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.
            
            if uploads is None:
                crawlinglogger.error(f"[400], {artist}, tictok, {uploads_xpath}")
            elif followers is None:
                crawlinglogger.error(f"[400], {artist}, tictok, {followers_xpath}")
            elif likes is None:
                crawlinglogger.error(f"[400], {artist}, tictok, {likes_xpath}")
                # Xpath가 오류여서 해당 페이지에서 element를 찾을 수 없는 경우입니다.
                # 혹은, Xpath에는 문제가 없으나 해당 페이지의 Element가 없는 경우입니다.
                # 오류일 경우 item을 yield 하지 않아야 합니다.
            else:
                item = SocialbladeTiktokItem()
                item["artist"] = artist
                item["uploads"] = uploads.replace(",", "")
                item["followers"] = followers.replace(",", "")
                item["likes"] = likes.replace(",", "")
                item["url"] = response.url
                item["reserved_date"] = datetime.now().date()
                yield item
