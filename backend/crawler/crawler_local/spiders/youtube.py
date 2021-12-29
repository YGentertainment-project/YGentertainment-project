import re

import scrapy

from crawlerprojecct.items import YoutubeItem

class YoutubeSpider(scrapy.Spider):
    name = 'youtube'
    allowed_domains = ['www.socialblade.com']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawlerprojecct.middlewares.SocialbladeDownloaderMiddleware': 100,
        }
    }
    def start_requests(self):
        filepath = 'youtube_urls.txt'
        with open(filepath, 'r') as file:
            channels = file.readlines()
        for channel in channels:
            if( re.search('socialblade', channel) ):
                yield scrapy.Request(channel, callback=self.socialblade_parse)
            else:
                yield scrapy.Request(channel, callback=self.youtube_parse)

    def socialblade_parse(self, response):
        artist = response.xpath('//*[@id="YouTubeUserTopInfoBlockTop"]/div[1]/h1/text()').get()
        sub = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[3]/span[2]/text()').get()
        views = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[4]/span[2]/text()').get()
        date = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[7]/span[2]/text()').get()
        upload = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[2]/span[2]/text()').get()
        if( sub[-1] == 'M' ): sub = float(sub[:-1])*1000
        elif( sub[-1] == 'K' ): sub = sub[:-1]
        item = YoutubeItem()
        item['artist'] = artist
        item['subscriber_num'] = int(sub)
        item['total_view_num'] = views.replace(',', '')
        item['account_create_dt'] = date
        item['upload_num'] = upload.replace(',', ' ')
        yield item

    def youtube_parse(self, response):
        artist = response.xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/div/div[1]/ytd-channel-name/div/div/yt-formatted-string/text()').extract()[0]
        views = response.xpath('//*[@id="right-column"]/yt-formatted-string[3]/text()').extract()[0]
        item = YoutubeItem()
        item['artist'] = artist
        item['total_view_num'] = views[4:-1].replace(',', '')
        yield item

