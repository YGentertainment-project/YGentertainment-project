import scrapy
from urllib.parse import urlparse
from ..items import SocialbladeTwitterItem
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform

SOCIALBLADE_DOMAIN = "socialblade.com"
SOCIALBLADE_ROBOT = "https://socialblade.com/robots.txt"


class TwitterSpider(scrapy.Spider):
    name = 'twitter'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.scrapy_app.middlewares.NoLoginDownloaderMiddleware': 100
        },
    }

    def start_requests(self):
        crawl_url = {}
        twitter_platform_id = Platform.objects.get(name='twitter').id
        CrawlingTarget = CollectTarget.objects.filter(platform_id=twitter_platform_id)
        for row in CrawlingTarget:
            artist_name = Artist.objects.get(id=row.artist_id).name
            artist_url = row.target_url
            crawl_url[artist_name] = artist_url
        for artist, url in crawl_url.items():
            print("artist : {}, url : {}, url_len: {}".format(
                artist, url, len(url)))
            if len(url) > 0:
                yield scrapy.Request(url=url, callback=self.parse, encoding='utf-8', meta={'artist': artist})
            else:
                continue

    def parse(self, response):
        domain = urlparse(response.url).netloc
        artist = followers = twits = user_created = None

        if domain == SOCIALBLADE_DOMAIN:
            if response.request.url == SOCIALBLADE_ROBOT:
                pass
            else:
                artist = response.request.meta['artist']
                followers = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[2]/span[2]/text()').extract()[0]
                twits = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[5]/span[2]/text()').extract()[0]
                user_created = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[6]/span[2]/text()').extract()[0]

        if response.request.url == SOCIALBLADE_ROBOT:
            pass
        else:
            item = SocialbladeTwitterItem()
            item["artist"] = artist
            item["followers"] = followers.replace(',', '')
            item["twits"] = twits.replace(',', '')
            item["user_created"] = user_created
            item["url"] = response.url
            yield item
