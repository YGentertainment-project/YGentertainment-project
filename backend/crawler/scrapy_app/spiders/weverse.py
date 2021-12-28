import scrapy
from ..items import WeverseItem

class WeverseSpider(scrapy.Spider):
    name = 'weverse'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'crawler.scrapy_app.middlewares.WeverseDownloaderMiddleware': 100
        },
        'ITEM_PIPELINES':{
            'crawler.scrapy_app.pipelines.CrawlerPipeline': 100,
        },
    }
    def start_requests(self):
        artist_url = {
        "(여자)아이들": "",
        "강다니엘": "",
        "뉴이스트": "https://www.weverse.io/nuest/feed",
        "레드벨벳": "",
        "레드벨벳 아이린": "",
        "레드벨벳 슬기": "",
        "레드벨벳 조이": "",
        "레드벨벳 웬디": "",
        "레드벨벳 예리": "",
        "마마무": "",
        "마마무 화사": "",
        "몬스타엑스": "",
        "방탄소년단": "https://www.weverse.io/bts/feed",
        "BLACKPINK": "https://www.weverse.io/blackpink/feed",
        "BLACKPINK 로제": "",
        "BLACKPINK 리사": "",
        "BLACKPINK 제니": "",
        "BLACKPINK 지수": "",
        "BIGBANG": "",
        "BIGBANG 지드래곤": "",
        "샤이니": "",
        "세븐틴": "https://www.weverse.io/seventeen/feed",
        "슈퍼주니어": "",
        "스트레이키즈": "",
        "아스트로": "",
        "아스트로 차은우": "",
        "에스파": "",
        "WINNER": "https://www.weverse.io/winner/feed",
        "크래비티": "",
        "트와이스": "",
        "AB6IX": "",
        "에이티즈": "",
        "엔하이픈": "https://www.weverse.io/enhypen/feed",
        "EXO": "",
        "엑소 백현": "",
        "iKON": "https://www.weverse.io/ikon/feed",
        "ITZY": "",
        "NCT": "",
        "NCT 127": "",
        "NCT DREAM": "",
        "NCT U": "",
        "더보이즈": "",
        "TREASURE": "https://www.weverse.io/treasure/feed",
        "TXT": "https://www.weverse.io/txt/feed",
        "WayV": "",
        "청하": "",
        "선미": "https://www.weverse.io/sunmi/feed",
        "전소미": "",
        "AKMU": "",
        "AKMU 이수현": "",
        "아이유": "",
        "헤이즈": "",
        "소녀시대": "",
        "소녀시대 태연": "",
        "이하이": "",
        "정은지": "",
        "젝스키스": "",
        "백예린": "",
        "볼빨간사춘기": "",
        "현아": "",
        "비투비": "",
        "SF9": "",
        "스테이씨": "https://www.weverse.io/stayc/feed",
        "오마이걸": "",
        "위클리": "https://www.weverse.io/weeekly/feed",
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
        sub = response.xpath('/html/body/div[1]/div/section/aside/div/div[1]/text()').extract()
        # WINNER의 경우, 페이지는 있으나 구독자 수가 공개되어 있지 않으므로 0으로 처리했습니다.
        if not sub:
            sub = 0
        else:
            sub = int(sub[0][:-6].replace(',', ''))
        
        item = WeverseItem()
        item['artist'] = artist
        item['weverses'] = sub
        item['url'] = response.url
        yield item
