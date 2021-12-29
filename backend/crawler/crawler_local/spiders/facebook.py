import scrapy
from bs4 import BeautifulSoup

from crawlerprojecct.items import FacebookItem


class FacebookSpider(scrapy.Spider):
    name = 'facebook'
    filepath = 'C:/Users/sunri/PycharmProjects/crawlerprojecct/crawlerprojecct/spiders/facebook_urls.txt'
    start_urls = []
    with open(filepath, 'r') as file:
        channels = file.readlines()
    for channel in channels:
        start_urls.append(channel)

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES' : {
            'crawlerprojecct.middlewares.CrowdtangleDownloaderMiddleware': 100
        }
    }

    def parse(self, response):
        artist = response.xpath('//span[@class="omni-select-value-label"]/text()').extract()[0]
        follower_num = response.xpath('//span[@class="ct-tooltip right arrow-middle"]/text()').extract()[0]
        item = FacebookItem()
        item['artist'] = artist
        item['follower_num'] = follower_num
        yield item

