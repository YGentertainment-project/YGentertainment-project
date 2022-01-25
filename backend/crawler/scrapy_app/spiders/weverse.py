import scrapy
from ..items import WeverseItem
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform
from config.models import CollectTargetItem
from datetime import datetime
from django.db.models import Q


class WeverseSpider(scrapy.Spider):
    name = "weverse"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "crawler.scrapy_app.middlewares.LoginDownloaderMiddleware": 100
        },
    }
    weverse_platform_id = Platform.objects.get(name="weverse").id
    crawlingtarget = CollectTarget.objects.filter(platform_id=weverse_platform_id)

    def start_requests(self):
        for row in self.crawlingtarget:
            artist_name = Artist.objects.get(id=row.artist_id).name
            artist_url = row.target_url
            target_id = row.id
            print("artist : {}, url : {}, url_len: {}".format(
                artist_name, artist_url, len(artist_url)))
            yield scrapy.Request(url=artist_url, callback=self.parse, encoding="utf-8", meta={"artist": artist_name,
                                                                                              "target_id": target_id})

    def parse(self, response):
        artist = response.meta["artist"]
        sub_xpath = CollectTargetItem.objects.get(Q(collect_target_id=response.meta["target_id"]) & Q(target_name="weverses")).xpath + "/text()"
        sub = response.xpath(sub_xpath).extract()
        # WINNER의 경우, 페이지는 있으나 구독자 수가 공개되어 있지 않으므로 0으로 처리했습니다.
        item = WeverseItem()
        item["artist"] = artist
        item["weverses"] = 0 if not sub else int(sub[0][:-6].replace(",", ""))
        item["url"] = response.url
        item["reserved_date"] = datetime.now().date()
        yield item
