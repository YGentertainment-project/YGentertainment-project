from time import sleep

import scrapy
from scrapy.utils.python import to_bytes

from crawlerprojecct.items import MelonItem


class MelonSpider(scrapy.Spider):
    name = 'melon'
    allowed_domains = ['xn--o39an51b2re.com/melon/artiststream']
    filepath = 'C:/Users/sunri/PycharmProjects/crawlerprojecct/crawlerprojecct/spiders/melon_urls.txt'
    start_urls = []
    with open(filepath, 'r') as file:
        channels = file.readlines()
    for channel in channels:
        start_urls.append(channel)
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawlerprojecct.middlewares.SocialbladeDownloaderMiddleware': 100,
        }
    }

    def parse(self, response):
        artist = response.xpath('//*[@id="main-wrapper"]/div/div[2]/div[3]/div/div/div/div[2]/div/div[2]/div/table/tbody/tr[1]/td[3]/p[2]/text()').extract()[0]
        listener = response.xpath('//*[@id="main-wrapper"]/div/div[2]/div[2]/div/div/div/ul/li[3]/text()').extract()[2]
        streaming = response.xpath('//*[@id="main-wrapper"]/div/div[2]/div[2]/div/div/div/ul/li[4]/text()').extract()[2]

        item = MelonItem()
        item['artist'] = artist
        item['listener_num'] = listener.replace(',', '')
        item['streaming_num'] = streaming.replace(',', '')
        yield item