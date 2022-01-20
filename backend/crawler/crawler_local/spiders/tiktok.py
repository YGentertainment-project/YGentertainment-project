import scrapy

from crawlerprojecct.items import TikTokItem


class TiktokSpider(scrapy.Spider):
    name = 'tiktok'
    allowed_domains = ['www.socialblade.com']
    filepath = 'C:/Users/sunri/PycharmProjects/crawlerprojecct/crawlerprojecct/spiders/tiktok_urls.txt'
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
        artist = response.xpath('//*[@id="YouTubeUserTopInfoBlockTop"]/div[1]/h1/text()').extract()[0]
        sub = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[3]/span[2]/text()').extract()[0]
        like = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[5]/span[2]/text()').extract()[0]
        upload = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[2]/span[2]/text()').extract()[0]

        item = TikTokItem()
        item['artist'] = artist
        item['follower_num'] = sub.replace(',', '')
        item['upload_num'] = upload.replace(',', '')
        item['like_num'] = like.replace(',', '')
        yield item
