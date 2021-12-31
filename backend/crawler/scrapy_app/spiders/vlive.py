import scrapy
from bs4 import BeautifulSoup
import re
from ..items import VliveItem


class VliveSpider(scrapy.Spider):
    name = 'vlive'
    # custom_settings = {
    # }

    def start_requests(self):
        artist_url = {
            "(여자)아이들": "https://www.vlive.tv/channel/CE2621",
            "강다니엘": "https://www.vlive.tv/channel/B019E3",
            "뉴이스트": "https://www.vlive.tv/channel/F59133",
            "레드벨벳": "https://www.vlive.tv/channel/DCF447",
            "레드벨벳 아이린": "",
            "레드벨벳 슬기": "",
            "레드벨벳 조이": "",
            "레드벨벳 웬디": "",
            "레드벨벳 예리": "",
            "마마무": "https://www.vlive.tv/channel/FCD4B",
            "마마무 화사": "",
            "몬스타엑스": "https://www.vlive.tv/channel/FE123",
            "방탄소년단": "https://www.vlive.tv/channel/FE619",
            "BLACKPINK": "https://www.vlive.tv/channel/F001E5",
            "BLACKPINK 로제": "",
            "BLACKPINK 리사": "",
            "BLACKPINK 제니": "",
            "BLACKPINK 지수": "",
            "BIGBANG": "https://www.vlive.tv/channel/F13F",
            "BIGBANG 지드래곤": "",
            "샤이니": "https://www.vlive.tv/channel/96DD0B",
            "세븐틴": "https://www.vlive.tv/channel/F99B3",
            "슈퍼주니어": "",
            "스트레이키즈": "https://www.vlive.tv/channel/D7A4F1",
            "아스트로": "https://www.vlive.tv/channel/F6F107",
            "아스트로 차은우": "",
            "에스파": "https://www.vlive.tv/channel/97CCED",
            "WINNER": "https://www.vlive.tv/channel/FDC2D",
            "크래비티": "https://www.vlive.tv/channel/A34B7D",
            "트와이스": "https://www.vlive.tv/channel/EDBF",
            "AB6IX": "https://www.vlive.tv/channel/B5D92B",
            "에이티즈": "https://www.vlive.tv/channel/C057DB",
            "엔하이픈": "https://www.vlive.tv/channel/9A0CA5",
            "EXO": "https://www.vlive.tv/channel/F94BD",
            "엑소 백현": "",
            "iKON": "https://www.vlive.tv/channel/FD241",
            "ITZY": "https://www.vlive.tv/channel/BAE889",
            "NCT": "https://www.vlive.tv/channel/F3C16D",
            "NCT 127": "",
            "NCT DREAM": "",
            "NCT U": "",
            "더보이즈": "https://www.vlive.tv/channel/DE341F",
            "TREASURE": "https://www.vlive.tv/channel/B978B7",
            "TXT": "https://www.vlive.tv/channel/BA18A3",
            "WayV": "https://www.vlive.tv/channel/A01BE3/board/6610",
            "청하": "https://www.vlive.tv/channel/E3437D",
            "선미": "https://www.vlive.tv/channel/DA6499",
            "전소미": "https://www.vlive.tv/channel/B4595B",
            "AKMU": "https://www.vlive.tv/channel/F36179",
            "AKMU 이수현": "",
            "아이유": "https://www.vlive.tv/channel/FA895",
            "헤이즈": "https://www.vlive.tv/channel/CF85F5",
            "소녀시대": "",
            "소녀시대 태연": "",
            "이하이": "https://www.vlive.tv/channel/F57137",
            "정은지": "",
            "젝스키스": "https://www.vlive.tv/channel/EFA1F1",
            "백예린": "",
            "볼빨간사춘기": "https://www.vlive.tv/channel/9F3BFF",
            "현아": "https://www.vlive.tv/channel/96ED09",
            "비투비": "https://www.vlive.tv/channel/FD737",
            "SF9": "https://www.vlive.tv/channel/ED7237",
            "스테이씨": "https://www.vlive.tv/channel/968D15",
            "오마이걸": "https://www.vlive.tv/channel/F51143",
            "위클리": "https://www.vlive.tv/channel/A0ABD1",
            "HYBE LABELS": "",
            "SM ENTERTAINMENT": "",
            "JYP ENTERTAINMENT": "",
        }
        for artist, url in artist_url.items():
            print("artist : {}, url : {}, url_len: {}".format(
                artist, url, len(url)))
            if len(url) > 0:
                yield scrapy.Request(url=url, callback=self.parse, encoding='utf-8', meta={'artist': artist})
            else:
                continue

    def parse(self, response):
        artist = response.meta['artist']
        soup = BeautifulSoup(response.text, 'html.parser')
        s = soup.find('script').get_text()
        regex = r"(\"[\w\s]+\"\:[0-9]+\,)"
        matches = re.finditer(regex, s, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            if not match.group().find('"memberCount":'): member_num = match.group()[14:]
            if not match.group().find('"videoPlayCountOfStar":'): total_view_num = match.group()[23:]
            if not match.group().find('"videoCountOfStar":'): upload_num = match.group()[19:]
            if not match.group().find('"videoLikeCountOfStar":'): like_num = match.group()[23:]

        item = VliveItem()
        item['artist'] = artist
        item['likes'] = like_num[:-1]
        item['members'] = member_num[:-1]
        item['plays'] = total_view_num[:-1]
        item['videos'] = upload_num[:-1]
        item['url'] = response.url
        yield item