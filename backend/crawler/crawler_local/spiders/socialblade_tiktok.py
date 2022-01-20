import scrapy

from crawlerprojecct.items import TikTokItem


class TiktokSpider(scrapy.Spider):
    name = 'tiktok'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawlerprojecct.middlewares.SocialbladeDownloaderMiddleware': 100,
        }
    }
    def start_requests(self):
        artist_url = {
            "(여자)아이들": "https://socialblade.com/tiktok/user/official_gidle",
            "강다니엘": "https://socialblade.com/tiktok/user/konnect_kangdaniel",
            "뉴이스트": "https://socialblade.com/tiktok/user/nuest_official",
            "레드벨벳": "https://socialblade.com/tiktok/user/redvelvet_smtown",
            "레드벨벳 아이린": "",
            "레드벨벳 슬기": "",
            "레드벨벳 조이": "",
            "레드벨벳 웬디": "",
            "레드벨벳 예리": "",
            "마마무": "https://socialblade.com/tiktok/user/official_mamamoo",
            "마마무 화사": "",
            "몬스타엑스": "https://socialblade.com/tiktok/user/monsta_x_514",
            "방탄소년단": "https://socialblade.com/tiktok/user/bts_official_bighit",
            "BLACKPINK": "https://socialblade.com/tiktok/user/bp_tiktok",
            "BLACKPINK 로제": "https://socialblade.com/tiktok/user/roses_are_rosie",
            "BLACKPINK 리사": "",
            "BLACKPINK 제니": "",
            "BLACKPINK 지수": "",
            "BIGBANG": "",
            "BIGBANG 지드래곤": "",
            "샤이니": "",
            "세븐틴": "https://socialblade.com/tiktok/user/seventeen17_official",
            "슈퍼주니어": "https://socialblade.com/tiktok/user/superjunior_smtown",
            "스트레이키즈": "https://socialblade.com/tiktok/user/jypestraykids",
            "아스트로": "https://socialblade.com/tiktok/user/astro_official",
            "아스트로 차은우": "",
            "에스파": "https://socialblade.com/tiktok/user/aespa_official",
            "WINNER": "https://socialblade.com/tiktok/user/wn_tiktok",
            "크래비티": "https://socialblade.com/tiktok/user/cravityofficial",
            "트와이스": "https://socialblade.com/tiktok/user/twice_tiktok_official",
            "AB6IX": "https://socialblade.com/tiktok/user/ab6ix.official",
            "에이티즈": "https://socialblade.com/tiktok/user/ateez_official_",
            "엔하이픈": "https://socialblade.com/tiktok/user/enhypen",
            "EXO": "",
            "엑소 백현": "",
            "IKON": "https://socialblade.com/tiktok/user/ikon_tiktok",
            "ITZY": "https://socialblade.com/tiktok/user/itzyofficial",
            "NCT": "https://socialblade.com/tiktok/user/official_nct",
            "NCT 127": "",
            "NCT DREAM": "",
            "NCT U": "",
            "더보이즈": "https://socialblade.com/tiktok/user/creker_theboyz",
            "TREASURE": "https://socialblade.com/tiktok/user/yg_treasure_tiktok",
            "TXT": "https://socialblade.com/tiktok/user/txt.bighitent",
            "WayV": "https://socialblade.com/tiktok/user/official_wayv",
            "청하": "https://socialblade.com/tiktok/user/official_chungha",
            "선미": "https://socialblade.com/tiktok/user/official_sunmi",
            "전소미": "https://socialblade.com/tiktok/user/somi_official_",
            "AKMU": "",
            "AKMU 이수현": "https://socialblade.com/tiktok/user/akmu_suhyun",
            "아이유": "",
            "헤이즈": "",
            "소녀시대": "",
            "소녀시대 태연": "",
            "이하이": "",
            "정은지": "",
            "젝스키스": "",
            "백예린": "",
            "볼빨간사춘기": "",
            "현아": "https://socialblade.com/tiktok/user/hyunaofficial",
            "비투비": "https://socialblade.com/tiktok/user/official_btob",
            "SF9": "https://socialblade.com/tiktok/user/sf9official",
            "스테이씨": "https://socialblade.com/tiktok/user/stayc_official",
            "오마이걸": "https://socialblade.com/tiktok/user/wm_ohmygirl",
            "위클리": "https://socialblade.com/tiktok/user/weeekly",
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
        artist = sub = like = upload = None
        artist = response.xpath('//*[@id="YouTubeUserTopInfoBlockTop"]/div[1]/h1/text()').get()
        sub = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[3]/span[2]/text()').get()
        like = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[5]/span[2]/text()').get()
        upload = response.xpath('//*[@id="YouTubeUserTopInfoBlock"]/div[2]/span[2]/text()').get()

        item = TikTokItem()
        item['artist'] = artist
        item['follower_num'] = sub.replace(',', '')
        item['upload_num'] = upload.replace(',', '')
        item['like_num'] = like.replace(',', '')
        yield item
