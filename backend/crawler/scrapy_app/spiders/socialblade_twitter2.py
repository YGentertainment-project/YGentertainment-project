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
            'crawler.scrapy_app.pipelines.SocialbladeTwitter2Pipeline': 100,
        },
    }

    def start_requests(self):
        artist_url = {
            "(여자)아이들": "https://socialblade.com/twitter/user/g_i_dle",
            "강다니엘": "https://socialblade.com/twitter/user/konnect_danielk",
            "뉴이스트": "https://socialblade.com/twitter/user/nuestnews",
            "레드벨벳": "https://socialblade.com/twitter/user/rvsmtown",
            "레드벨벳 아이린": "",
            "레드벨벳 슬기": "",
            "레드벨벳 조이": "",
            "레드벨벳 웬디": "",
            "레드벨벳 예리": "",
            "마마무": "https://socialblade.com/twitter/user/RBW_Mamamoo",
            "마마무 화사": "",
            "몬스타엑스": "https://socialblade.com/twitter/user/officialmonstax",
            "방탄소년단": "https://socialblade.com/twitter/user/bts_twt",
            "BLACKPINK": "https://socialblade.com/twitter/user/ygofficialblink",
            "BLACKPINK 로제": "",
            "BLACKPINK 리사": "",
            "BLACKPINK 제니": "",
            "BLACKPINK 지수": "",
            "BIGBANG": "https://socialblade.com/twitter/user/yg_globalvip",
            "BIGBANG 지드래곤": "https://socialblade.com/twitter/user/ibgdrgn",
            "샤이니": "https://socialblade.com/twitter/user/shinee",
            "세븐틴": "https://socialblade.com/twitter/user/pledis_17",
            "슈퍼주니어": "https://socialblade.com/twitter/user/Sjofficial",
            "스트레이키즈": "https://socialblade.com/twitter/user/stray_kids",
            "아스트로": "https://socialblade.com/twitter/user/offclastro",
            "아스트로 차은우": "",
            "에스파": "https://socialblade.com/twitter/user/aespa_official",
            "WINNER": "https://socialblade.com/twitter/user/yginnercircle",
            "크래비티": "https://socialblade.com/twitter/user/cravity_twt",
            "트와이스": "https://socialblade.com/twitter/user/jypetwice",
            "AB6IX": "https://socialblade.com/twitter/user/ab6ix_members",
            "에이티즈": "https://socialblade.com/twitter/user/ateezofficial",
            "엔하이픈": "https://socialblade.com/twitter/user/enhypen_members",
            "EXO": "https://socialblade.com/twitter/user/weareoneexo",
            "엑소 백현": "https://socialblade.com/twitter/user/b_hundred_hyun",
            "iKON": "https://socialblade.com/twitter/user/yg_ikonic",
            "ITZY": "https://socialblade.com/twitter/user/itzyofficial",
            "NCT": "https://socialblade.com/twitter/user/nctsmtown",
            "NCT 127": "https://socialblade.com/twitter/user/nctsmtown_127",
            "NCT DREAM": "https://socialblade.com/twitter/user/nctsmtown_dream",
            "NCT U": "",
            "더보이즈": "https://socialblade.com/twitter/user/we_the_boyz",
            "TREASURE": "https://socialblade.com/twitter/user/treasuremembers",
            "TXT": "https://socialblade.com/twitter/user/txt_members",
            "WayV": "https://socialblade.com/twitter/user/wayv_official",
            "청하": "https://socialblade.com/twitter/user/chungha_mnhent",
            "선미": "https://socialblade.com/twitter/user/miyaohyeah",
            "전소미": "https://socialblade.com/twitter/user/somi_official_",
            "AKMU": "https://socialblade.com/twitter/user/official_akmu",
            "AKMU 이수현": "",
            "아이유": "https://socialblade.com/twitter/user/_iuofficial",
            "헤이즈": "https://socialblade.com/twitter/user/heize_official",
            "소녀시대": "https://socialblade.com/twitter/user/GirlsGeneration",
            "소녀시대 태연": "",
            "이하이": "https://socialblade.com/twitter/user/leehi_hi",
            "정은지": "https://socialblade.com/twitter/user/Apinkjej",
            "젝스키스": "",
            "백예린": "",
            "볼빨간사춘기": "https://socialblade.com/twitter/user/bol4_official",
            "현아": "",
            "비투비": "https://socialblade.com/twitter/user/OFFICIALBTOB",
            "SF9": "https://socialblade.com/twitter/user/SF9official",
            "스테이씨": "https://socialblade.com/twitter/user/STAYC_official",
            "오마이걸": "https://socialblade.com/twitter/user/wm_ohmygirl",
            "위클리": "https://socialblade.com/twitter/user/_weeekly",
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
