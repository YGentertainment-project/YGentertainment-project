import scrapy
from ..items import MelonItem
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform


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
        CrawlingTarget = CollectTarget.objects.filter(platform_id=melon_platform_id)
        for row in CrawlingTarget:
            artist_name = Artist.objects.get(id=row.artist_id).name
            artist_urls = [row.target_url, row.target_url_2]
            crawl_url[artist_name] = artist_urls

        for artist, urls in crawl_url.items():
            print("artist : {}, url : {}, url_len: {}".format(
                artist, urls[0], len(urls[0])))
            yield scrapy.Request(url=urls[0], callback=self.parse, encoding="utf-8", meta={"artist": artist,
                                                                                           "next": urls[1]})

    def parse(self, response):
        artist = response.meta["artist"]
        mainwrapper = '\"main-wrapper\"'
        listener_target = streaming_target = None
        try:
            listener_target = response.xpath(
                f"//*[@id={mainwrapper}]/div/div[2]/div[2]/div/div/div/ul/li[3]/text()").extract()[2]
            streaming_target = response.xpath(
                f"//*[@id={mainwrapper}]/div/div[2]/div[2]/div/div/div/ul/li[4]/text()").extract()[2]
        except ValueError:
            pass
            # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.

        if listener_target is None or streaming_target is None:
            pass
            # Xpath가 오류여서 해당 페이지에서 element를 찾을 수 없는 경우입니다.
            # 혹은, Xpath에는 문제가 없으나 해당 페이지의 Element가 없는 경우입니다.
            # 오류일 경우 item을 yield 하지 않아야 합니다.
        else:
            listener = listener_target.replace(",", "")
            streaming = streaming_target.replace(",", "")
            url1 = response.url
            yield scrapy.Request(url=response.meta["next"], callback=self.parse_melon, encoding="utf-8",
                                 meta={"artist": artist,
                                       "listeners": listener,
                                       "streams": streaming,
                                       "url1": url1})

    def parse_melon(self, response):
        fans_target = None
        d_like_count = '\"d_like_count\"'
        try:
            fans_target = response.xpath(f"//span[@id={d_like_count}]/text()").get()
        except ValueError:
            pass
            # Xpath Error라고 나올 경우, 잘못된 Xpath 형식으로 생긴 문제입니다.

        if fans_target is None:
            pass
            # Xpath가 오류여서 해당 페이지에서 element를 찾을 수 없는 경우입니다.
            # 혹은, Xpath에는 문제가 없으나 해당 페이지의 Element가 없는 경우입니다.
            # 오류일 경우 item을 yield 하지 않아야 합니다.
        else:
            item = MelonItem()
            fans = fans_target.replace(",", "")
            item["artist"] = response.meta["artist"]
            item["listeners"] = response.meta["listeners"]
            item["streams"] = response.meta["streams"]
            item["fans"] = fans
            item["url1"] = response.meta["url1"]
            item["url2"] = response.url
            yield item
