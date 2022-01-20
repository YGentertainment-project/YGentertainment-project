import scrapy

from crawlerprojecct.items import WeverseItem


class WeverseSpider(scrapy.Spider):
    name = 'weverse'
    filepath = 'C:/Users/sunri/PycharmProjects/crawlerprojecct/crawlerprojecct/spiders/weverse_urls.txt'
    start_urls = []
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawlerprojecct.middlewares.WeverseDownloaderMiddleware': 100,
        }
    }

    with open(filepath, 'r') as file:
        channels = file.readlines()
    for channel in channels:
        start_urls.append(channel)

    def parse(self, response):
        artist = response.css('#root > div > section > aside > div > a > div > p::text').extract()[0]
        sub = response.xpath('//*[@id="root"]/div/section/aside/div/div[1]/text()').extract()
        if not sub: sub = ""
        else: sub = sub[0]
        item = WeverseItem()
        item['artist'] = artist
        item['follower_num'] = sub
        yield item
