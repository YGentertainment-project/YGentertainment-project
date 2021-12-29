import scrapy
from urllib.parse import urlparse
from ..items import SocialbladeTwitter2Item

SOCIALBLADE_DOMAIN = "socialblade.com"
SOCIALBLADE_ROBOT = "https://socialblade.com/robots.txt"

class Twitter2Spider(scrapy.Spider):
    name = 'twitter2'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'crawler.scrapy_app.middlewares.SocialbladeDownloaderMiddleware': 100
        },
        'ITEM_PIPELINES':{
            'crawler.scrapy_app.pipelines.CrawlerPipeline': 100,
        },
    }

    def start_requests(self):
        artist_url = {
            "(여자)아이들": "",
            "강다니엘": "",
            "뉴이스트": "",
            "레드벨벳": "",
            "레드벨벳 아이린": "",
            "레드벨벳 슬기": "",
            "레드벨벳 조이": "",
            "레드벨벳 웬디": "",
            "레드벨벳 예리": "",
            "마마무": "",
            "마마무 화사": "",
            "몬스타엑스": "",
            "방탄소년단": "https://socialblade.com/twitter/user/bts_bighit",
            "BLACKPINK": "https://socialblade.com/twitter/user/blackpink",
            "BLACKPINK 로제": "",
            "BLACKPINK 리사": "",
            "BLACKPINK 제니": "",
            "BLACKPINK 지수": "",
            "BIGBANG": "",
            "BIGBANG 지드래곤": "",
            "샤이니": "",
            "세븐틴": "",
            "슈퍼주니어": "",
            "스트레이키즈": "",
            "아스트로": "https://socialblade.com/twitter/user/ASTRO_Staff",
            "아스트로 차은우": "",
            "에스파": "",
            "WINNER": "https://socialblade.com/twitter/user/yg_winnercity",
            "크래비티": "https://socialblade.com/twitter/user/cravitystarship",
            "트와이스": "",
            "AB6IX": "https://socialblade.com/twitter/user/AB6IX",
            "에이티즈": "",
            "엔하이픈": "https://socialblade.com/twitter/user/ENHYPEN",
            "EXO": "",
            "엑소 백현": "",
            "iKON": "",
            "ITZY": "",
            "NCT": "",
            "NCT 127": "",
            "NCT DREAM": "",
            "NCT U": "",
            "더보이즈": "https://socialblade.com/twitter/user/ist_theboyz",
            "TREASURE": "https://socialblade.com/twitter/user/ygtreasuremaker",
            "TXT": "https://socialblade.com/twitter/user/TXT_bighit",
            "WayV": "",
            "청하": "",
            "선미": "https://socialblade.com/twitter/user/official_sunmi_",
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
            "스테이씨": "",
            "오마이걸": "",
            "위클리": "",
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
        domain = urlparse(response.url).netloc
        artist = followers = twits = user_created = None

        if domain == SOCIALBLADE_DOMAIN:
            if response.request.url == SOCIALBLADE_ROBOT:
                pass
            else:
                artist = response.request.meta['artist']
                followers = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[2]/span[2]/text()').get()
                twits = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[5]/span[2]/text()').get()
                user_created = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[6]/span[2]/text()').get()

        if response.request.url == SOCIALBLADE_ROBOT:
            pass
        else:
            item = SocialbladeTwitter2Item()
            item["artist"] = artist
            item["followers"] = followers.replace(',', '')
            item["twits"] = twits.replace(',', '')
            item["user_created"] = user_created
            item["url"] = response.url
            yield item
