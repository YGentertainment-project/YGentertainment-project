import re

import scrapy
from bs4 import BeautifulSoup

from crawlerprojecct.items import VliveItem


class VliveSpider(scrapy.Spider):
    name = 'vlive'
    allowed_domains = ['www.vlive.tv']
    filepath = 'C:/Users/sunri/PycharmProjects/crawlerprojecct/crawlerprojecct/spiders/vlive_urls.txt'
    start_urls = []
    with open(filepath, 'r') as file:
        channels = file.readlines()
    for channel in channels:
        start_urls.append(channel)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        artist = soup.select_one('title').text[:-8]
        s = soup.find('script').get_text()
        regex = r"(\"[\w\s]+\"\:[0-9]+\,)"
        matches = re.finditer(regex, s, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            if not match.group().find('"memberCount":'): member_num = match.group().removeprefix('"memberCount":')
            if not match.group().find('"videoPlayCountOfStar":'): total_view_num = match.group().removeprefix('"videoPlayCountOfStar":')
            if not match.group().find('"videoCountOfStar":'): upload_num = match.group().removeprefix('"videoCountOfStar":')
            if not match.group().find('"videoLikeCountOfStar":'): like_num = match.group().removeprefix('"videoLikeCountOfStar":')

        item = VliveItem()
        item['artist'] = artist
        item['like_num'] = like_num[:-1]
        item['member_num'] = member_num[:-1]
        item['total_view_num'] = total_view_num[:-1]
        item['upload_num'] = upload_num[:-1]
        yield item
