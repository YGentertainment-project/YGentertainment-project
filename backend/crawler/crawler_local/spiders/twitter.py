import scrapy

from crawlerprojecct.items import TwitterItem


class TwitterSpider(scrapy.Spider):
    name = 'twitter'
    allowed_domains = ['www.socialblade.com']
    filepath = 'C:/Users/sunri/PycharmProjects/crawlerprojecct/crawlerprojecct/spiders/twitter_urls.txt'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawlerprojecct.middlewares.SocialbladeDownloaderMiddleware': 100,
        }
    }
    start_urls = []
    with open(filepath, 'r') as file:
        channels = file.readlines()
    for channel in channels:
        start_urls.append(channel)

    def parse(self, response):
        artist = response.xpath('//*[@id="YouTubeUserTopInfoBlockTop"]/div[1]/h2/text()').extract()[0]
        sub = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[2]/span[2]/text()').extract()[0]
        date = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[6]/span[2]/text()').extract()[0]
        upload = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[5]/span[2]/text()').extract()[0]

        item = TwitterItem()
        item['artist'] = artist
        item['account_create_dt'] = date
        item['follower_num'] = sub.replace(',', '')
        item['upload_num'] = upload.replace(',', '')
        yield item
