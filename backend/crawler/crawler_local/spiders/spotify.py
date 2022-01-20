import scrapy

from crawlerprojecct.items import SpotifyItem


class SpotifySpider(scrapy.Spider):
    name = 'spotify'
    allowed_domains = ['open.spotify.com']
    filepath = 'C:/Users/sunri/PycharmProjects/crawlerprojecct/crawlerprojecct/spiders/spotify_urls.txt'
    start_urls = []
    with open(filepath, 'r') as file:
        channels = file.readlines()
    for channel in channels:
        start_urls.append(channel)

    def parse(self, response):
        artist = response.xpath('//*[@class="view-header"]/text()').extract()[0]
        sub = response.xpath('//*[@class="insights__column__number"]/text()').extract()[0]
        item = SpotifyItem()
        item['artist'] = artist
        item['monthly_listener_num'] = sub
        yield item
