from urllib import parse

import scrapy
from ..items import MelonItem
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform
from django.db.models import Q

class MelonSpider(scrapy.Spider):
    name = 'melon'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.scrapy_app.middlewares.NoLoginDownloaderMiddleware': 100
        },
    }

    def start_requests(self):
        crawl_url = {}
        melon_platform_id = Platform.objects.get(name='melon').id
        CrawlingTarget = CollectTarget.objects.filter(Q(platform_id=melon_platform_id)&Q(target_url__istartswith="https://xn--o39an51b2re.com"))
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
        artist = response.meta['artist']
        # listener = response.xpath('//*[@class="list-style-none"]/li[2]/i/text()').extract()[2]
        # streaming = response.xpath('//*[@class="list-style-none"]/li[3]/i/text()').extract()[2]
        listener = response.xpath('//*[@id="main-wrapper"]/div/div[2]/div[2]/div/div/div/ul/li[3]/text()').extract()[2]
        streaming = response.xpath('//*[@id="main-wrapper"]/div/div[2]/div[2]/div/div/div/ul/li[4]/text()').extract()[2]

        item = MelonItem()
        item['artist'] = artist
        item['listeners'] = listener.replace(',', '')
        item['streams'] = streaming.replace(',', '')
        item['fans'] = -1
        item['url1'] = response.url
        item['url2'] = None
        yield item
