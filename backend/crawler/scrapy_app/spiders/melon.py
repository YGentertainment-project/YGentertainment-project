from urllib import parse

import scrapy
from ..items import MelonItem


class MelonSpider(scrapy.Spider):
    name = 'melon'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.scrapy_app.middlewares.NoLoginDownloaderMiddleware': 100
        },
    }

    def start_requests(self):
        artist_url = {
            "(여자)아이들": "https://xn--o39an51b2re.com/melon/artiststream/2137482",
            "강다니엘": "https://xn--o39an51b2re.com/melon/artiststream/1865969",
            "뉴이스트": "https://xn--o39an51b2re.com/melon/artiststream/640891",
            "레드벨벳": "https://xn--o39an51b2re.com/melon/artiststream/780066",
            "레드벨벳 아이린": "",
            "레드벨벳 슬기": "",
            "레드벨벳 조이": "",
            "레드벨벳 웬디": "",
            "레드벨벳 예리": "",
            "마마무": "https://xn--o39an51b2re.com/melon/artiststream/750053",
            "마마무 화사": "https://xn--o39an51b2re.com/melon/artiststream/756531",
            "몬스타엑스": "https://xn--o39an51b2re.com/melon/artiststream/791216",
            "방탄소년단": "https://xn--o39an51b2re.com/melon/artiststream/672375",
            "BLACKPINK": "https://xn--o39an51b2re.com/melon/artiststream/995169",
            "BLACKPINK 로제": "https://xn--o39an51b2re.com/melon/artiststream/995171",
            "BLACKPINK 리사": "https://xn--o39an51b2re.com/melon/artiststream/995172",
            "BLACKPINK 제니": "https://xn--o39an51b2re.com/melon/artiststream/995173",
            "BLACKPINK 지수": "",
            "BIGBANG": "https://xn--o39an51b2re.com/melon/artiststream/198094",
            "BIGBANG 지드래곤": "https://xn--o39an51b2re.com/melon/artiststream/6984",
            "샤이니": "https://xn--o39an51b2re.com/melon/artiststream/247639",
            "세븐틴": "https://xn--o39an51b2re.com/melon/artiststream/861436",
            "슈퍼주니어": "https://xn--o39an51b2re.com/melon/artiststream/175404",
            "스트레이키즈": "https://xn--o39an51b2re.com/melon/artiststream/2006344",
            "아스트로": "https://xn--o39an51b2re.com/melon/artiststream/945766",
            "아스트로 차은우": "",
            "에스파": "https://xn--o39an51b2re.com/melon/artiststream/2899555",
            "WINNER": "https://xn--o39an51b2re.com/melon/artiststream/775197",
            "크래비티": "https://xn--o39an51b2re.com/melon/artiststream/2863902",
            "트와이스": "https://xn--o39an51b2re.com/melon/artiststream/905701",
            "AB6IX": "https://xn--o39an51b2re.com/melon/artiststream/2640829",
            "에이티즈": "https://xn--o39an51b2re.com/melon/artiststream/2398260",
            "엔하이픈": "https://xn--o39an51b2re.com/melon/artiststream/2899079",
            "EXO": "https://xn--o39an51b2re.com/melon/artiststream/724619",
            "엑소 백현": "https://xn--o39an51b2re.com/melon/artiststream/672859",
            "iKON": "https://xn--o39an51b2re.com/melon/artiststream/895741",
            "ITZY": "https://xn--o39an51b2re.com/melon/artiststream/2622030",
            "NCT": "",
            "NCT 127": "https://xn--o39an51b2re.com/melon/artiststream/991413",
            "NCT DREAM": "https://xn--o39an51b2re.com/melon/artiststream/1066419",
            "NCT U": "https://xn--o39an51b2re.com/melon/artiststream/960278",
            "더보이즈": "https://xn--o39an51b2re.com/melon/artiststream/1816126",
            "TREASURE": "https://xn--o39an51b2re.com/melon/artiststream/2880278",
            "TXT": "https://xn--o39an51b2re.com/melon/artiststream/2632253",
            "WayV": "https://xn--o39an51b2re.com/melon/artiststream/2620698",
            "청하": "https://xn--o39an51b2re.com/melon/artiststream/968265",
            "선미": "https://xn--o39an51b2re.com/melon/artiststream/22938",
            "전소미": "https://xn--o39an51b2re.com/melon/artiststream/968260",
            "AKMU": "https://xn--o39an51b2re.com/melon/artiststream/712452",
            "AKMU 이수현": "https://xn--o39an51b2re.com/melon/artiststream/712454",
            "아이유": "https://xn--o39an51b2re.com/melon/artiststream/261143",
            "헤이즈": "https://xn--o39an51b2re.com/melon/artiststream/751611",
            "소녀시대": "https://xn--o39an51b2re.com/melon/artiststream/228069",
            "소녀시대 태연": "https://xn--o39an51b2re.com/melon/artiststream/236797",
            "이하이": "https://xn--o39an51b2re.com/melon/artiststream/646171",
            "정은지": "https://xn--o39an51b2re.com/melon/artiststream/644871",
            "젝스키스": "https://xn--o39an51b2re.com/melon/artiststream/100052",
            "백예린": "https://xn--o39an51b2re.com/melon/artiststream/698776",
            "볼빨간사춘기": "https://xn--o39an51b2re.com/melon/artiststream/792022",
            "현아": "https://xn--o39an51b2re.com/melon/artiststream/449401",
            "비투비": "https://xn--o39an51b2re.com/melon/artiststream/647971",
            "SF9": "https://xn--o39an51b2re.com/melon/artiststream/1183574",
            "스테이씨": "https://xn--o39an51b2re.com/melon/artiststream/2899290",
            "오마이걸": "https://xn--o39an51b2re.com/melon/artiststream/857994",
            "위클리": "https://xn--o39an51b2re.com/melon/artiststream/2399776",
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
        # listener = response.xpath('//*[@class="list-style-none"]/li[2]/i/text()').extract()[2]
        # streaming = response.xpath('//*[@class="list-style-none"]/li[3]/i/text()').extract()[2]
        listener = response.xpath('//*[@id="main-wrapper"]/div/div[2]/div[2]/div/div/div/ul/li[3]/text()').extract()[2]
        streaming = response.xpath('//*[@id="main-wrapper"]/div/div[2]/div[2]/div/div/div/ul/li[4]/text()').extract()[2]

        item = MelonItem()
        item['artist'] = artist
        item['listeners'] = listener.replace(',', '')
        item['streams'] = streaming.replace(',', '')
        # item['fans'] = -1
        item['url1'] = response.url
        item['url2'] = None
        yield item
