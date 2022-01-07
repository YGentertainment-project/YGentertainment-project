import scrapy
from urllib.parse import urlparse
from ..items import SocialbladeYoutubeItem

SOCIALBLADE_DOMAIN = "socialblade.com"
YOUTUBE_DOMAIN = "youtube.com"
SOCIALBLADE_ROBOT = "https://socialblade.com/robots.txt"
YOUTUBE_ROBOT = "https://youtube.com/robots.txt"

class YoutubeSpider(scrapy.Spider):
    name = 'youtube'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.scrapy_app.middlewares.NoLoginDownloaderMiddleware': 100
        },
    }

    def start_requests(self):
        artist_url = {
            "(여자)아이들": "https://socialblade.com/youtube/channel/UCritGVo7pLJLUS8wEu32vow",
            "강다니엘": "https://socialblade.com/youtube/channel/UCHGJwrjlY6rmZJInxRmiztA",
            "뉴이스트": "https://socialblade.com/youtube/user/pledisnuest",
            "레드벨벳": "https://socialblade.com/youtube/channel/UCk9GmdlDTBfgGRb7vXeRMoQ",
            "레드벨벳 아이린": "",
            "레드벨벳 슬기": "",
            "레드벨벳 조이": "",
            "레드벨벳 웬디": "",
            "레드벨벳 예리": "",
            "마마무": "https://socialblade.com/youtube/user/wamamamoo",
            "마마무 화사": "",
            "몬스타엑스": "https://socialblade.com/youtube/channel/UCZvCP6sWj75MwpUP4LVtpNw",
            "방탄소년단": "https://socialblade.com/youtube/user/bangtantv",
            "BLACKPINK": "https://socialblade.com/youtube/channel/UCOmHUn--16B90oW2L6FRR3A",
            "BLACKPINK 로제": "https://socialblade.com/youtube/channel/UCBo1hnzxV9rz3WVsv__Rn1g",
            "BLACKPINK 리사": "https://socialblade.com/youtube/channel/UC35HKvKYPkri4Grd5KXl3wQ",
            "BLACKPINK 제니": "https://socialblade.com/youtube/channel/UCNYi_zGmR519r5gYdOKLTjQ",
            "BLACKPINK 지수": "",
            "BIGBANG": "https://socialblade.com/youtube/user/bigbang",
            "BIGBANG 지드래곤": "https://socialblade.com/youtube/user/officialgdragon",
            "샤이니": "https://socialblade.com/youtube/user/shinee",
            "세븐틴": "https://socialblade.com/youtube/user/pledis17",
            "슈퍼주니어": "https://socialblade.com/youtube/user/superjunior",
            "스트레이키즈": "https://socialblade.com/youtube/user/superjunior",
            "아스트로": "https://socialblade.com/youtube/channel/UCZqY2yIsAM9wh3vvMwKd27g",
            "아스트로 차은우": "",
            "에스파": "https://socialblade.com/youtube/channel/UC9GtSLeksfK4yuJ_g1lgQbg",
            "WINNER": "https://socialblade.com/youtube/user/officialygwinner",
            "크래비티": "https://socialblade.com/youtube/channel/UCRm-0JVuUFh5HV7NGG7qXlQ",
            "트와이스": "https://socialblade.com/youtube/channel/UCzgxx_DM2Dcb9Y1spb9mUJA",
            "AB6IX": "https://socialblade.com/youtube/channel/UCwytna6i1rFCt13a3Qvuk-A",
            "에이티즈": "https://socialblade.com/youtube/channel/UC2e4Ukj5Pfr7cb3KpJAFBdQ",
            "엔하이픈": "https://socialblade.com/youtube/channel/UCArLZtok93cO5R9RI4_Y5Jw",
            "EXO": "https://socialblade.com/youtube/user/exok",
            "엑소 백현": "https://socialblade.com/youtube/channel/UCUyr5000laFgF79tWJB3rXQ",
            "iKON": "https://socialblade.com/youtube/user/officialikon",
            "ITZY": "https://socialblade.com/youtube/channel/UCDhM2k2Cua-JdobAh5moMFg",
            "NCT": "https://socialblade.com/youtube/channel/UCwgtORdDtUKhpjE1VBv6XfA",
            "NCT 127": "https://socialblade.com/youtube/channel/UCk2E0dbAyEJWnrN2bbQOcbg",
            "NCT DREAM": "https://socialblade.com/youtube/channel/UCXURHJRGr4-EB3l87kcbElw",
            "NCT U": "",
            "더보이즈": "https://socialblade.com/youtube/channel/UCkJ1rbOrsyPfBuHNfnLPm-Q",
            "TREASURE": "https://socialblade.com/youtube/channel/UCx9hXYOCvUYwrprEqe4ZQHA",
            "TXT": "https://socialblade.com/youtube/channel/UCtiObj3CsEAdNU6ZPWDsddQ",
            "WayV": "https://socialblade.com/youtube/channel/UC-ZHt5Zgadfx-B1CM63Lqew",
            "청하": "https://www.youtube.com/c/CHUNGHA_OFFICIAL/about",
            "선미": "https://socialblade.com/youtube/channel/UCsVpgRB8YHLWA0ZrkhtHvTA",
            "전소미": "",
            "AKMU": "https://socialblade.com/youtube/user/officialakmu",
            "AKMU 이수현": "https://socialblade.com/youtube/channel/UCOiM8FuCUFJkuUjCmB14rgg",
            "아이유": "https://socialblade.com/youtube/channel/UC3SyT4_WLHzN7JmHQwKQZww",
            "헤이즈": "https://socialblade.com/youtube/channel/UCsXigGjbC_l4ttk-oahTfVg",
            "소녀시대": "https://socialblade.com/youtube/user/girlsgeneration",
            "소녀시대 태연": "https://socialblade.com/youtube/channel/UC5z2fxN6rs69cSyXur6X6Mg",
            "이하이": "https://socialblade.com/youtube/user/officialleehi",
            "정은지": "https://socialblade.com/youtube/channel/UCHTZl9wrDAV45L8IPS7ZYzg",
            "젝스키스": "https://socialblade.com/youtube/channel/UCcADqTjMyMol8B8mWm9n6rA",
            "백예린": "https://socialblade.com/youtube/channel/UCYoNPLKd1kXh4v3bvIx1pTA",
            "볼빨간사춘기": "https://www.youtube.com/c/BOL4OFFICIAL/about",
            "현아": "https://socialblade.com/youtube/channel/UC0uTcuuOtUFwtn9aKUVGjXg",
            "비투비": "https://socialblade.com/youtube/user/officialbtob",
            "SF9": "https://socialblade.com/youtube/channel/UC8HNshpReWjQv1WpwzhPHjA",
            "스테이씨": "https://www.youtube.com/c/STAYC/about",
            "오마이걸": "https://socialblade.com/youtube/channel/UC-qYkzKFdekoEniRu_FS3zg",
            "위클리": "https://socialblade.com/youtube/c/weeekly",
            "HYBE LABELS": "https://socialblade.com/youtube/c/hybelabels",
            "SM ENTERTAINMENT": "https://socialblade.com/youtube/user/smtown",
            "JYP ENTERTAINMENT": "https://socialblade.com/youtube/user/jypentertainment",
        }
        for artist, url in artist_url.items():
            print("artist : {}, url : {}, url_len: {}".format(
                artist, url, len(url)))
            if len(url) > 0:
                if urlparse(url).netloc == SOCIALBLADE_DOMAIN:
                    yield scrapy.Request(url=url, callback=self.parse_social, encoding='utf-8', meta={'artist': artist})
                else:
                    yield scrapy.Request(url=url, callback=self.parse_youtube, encoding='utf-8', meta={'artist': artist})
            else:
                continue

    # 구독자 문자열을 정수형 숫자로 반환
    def parse_subscribers(self, subs_text):
        subs_param = subs_text[-1].strip()
        subs_num = float(subs_text[0:-1].strip())
        result = subs_num
        if subs_param == 'M':
            result = int(subs_num * 1000000)  # 1000을 곱해준 정수값을 반환
        elif subs_param == 'K':
            result = int(subs_num * 1000)  # 정수값을 반환
        return int(result)

    # '1,334,635,139' 형태의 숫자를 정수형 변수로 반환
    def parse_comma_text(self, view_text):
        result = view_text.replace(',', '')
        return int(result)

    def parse_social(self, response):
        if response.request.url == SOCIALBLADE_ROBOT:
            pass
        else:
            artist = response.request.meta['artist']
            uploads = response.xpath(
                '//*[@id="YouTubeUserTopInfoBlock"]/div[2]/span[2]/text()').get()
            uploads = self.parse_comma_text(uploads)
            subscribers = response.xpath(
                '//*[@id="YouTubeUserTopInfoBlock"]/div[3]/span[2]/text()').get()
            subscribers = self.parse_subscribers(subscribers)
            view_text = response.xpath(
                '//*[@id="YouTubeUserTopInfoBlock"]/div[4]/span[2]/text()').get()
            views = self.parse_comma_text(view_text)
            user_created = response.xpath(
                '//*[@id="YouTubeUserTopInfoBlock"]/div[7]/span[2]/text()').get()
            item = SocialbladeYoutubeItem()
            item["artist"] = artist
            item["uploads"] = uploads
            item["subscribers"] = subscribers
            item["views"] = views
            item["user_created"] = user_created
            # item["platform"] = self.name
            item["url"] = response.url
            yield item

    def parse_youtube(self, response):
        if response.request.url == YOUTUBE_ROBOT:
            pass
        else:
            artist = response.request.meta['artist']
            uploads = -1
            subscribers = -1
            view_text = response.xpath(
                '//*[@id="right-column"]/yt-formatted-string[3]/text()').get()
            # '조회수 168,048,278회' 형태의 문자열에서 조회수에 해당하는 숫자만 추출
            view_text = view_text[:-5].strip()
            views = self.parse_comma_text(view_text)
            user_created = response.xpath(
                '//*[@id="right-column"]/yt-formatted-string[2]/span[2]/text()').get()
            item = SocialbladeYoutubeItem()
            item["artist"] = artist
            item["uploads"] = uploads
            item["subscribers"] = subscribers
            item["views"] = views
            item["user_created"] = user_created
            # item["platform"] = self.name
            item["url"] = response.url
            yield item