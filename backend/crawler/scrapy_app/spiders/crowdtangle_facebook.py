import scrapy
from ..items import CrowdtangleFacebookItem


class FacebookSpider(scrapy.Spider):
    name = 'facebook'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.scrapy_app.middlewares.LoginDownloaderMiddleware': 100
        },
    }

    def start_requests(self):
        artist_url = {
            "(여자)아이들": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=3308154&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "강다니엘": "",
            "뉴이스트": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=36150&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "레드벨벳": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=277252&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "레드벨벳 아이린": "",
            "레드벨벳 슬기": "",
            "레드벨벳 조이": "",
            "레드벨벳 웬디": "",
            "레드벨벳 예리": "",
            "마마무": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=277244&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "마마무 화사": "",
            "몬스타엑스": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=277250&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "방탄소년단": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=131305&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "BLACKPINK": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=1244299&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "BLACKPINK 로제": "",
            "BLACKPINK 리사": "",
            "BLACKPINK 제니": "",
            "BLACKPINK 지수": "",
            "BIGBANG": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=29235&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "BIGBANG 지드래곤": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=30248&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "샤이니": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=29660&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "세븐틴": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=400412&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "슈퍼주니어": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=29204&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "스트레이키즈": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=2739682&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "아스트로": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=675188&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "아스트로 차은우": "",
            "에스파": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=12894761&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "WINNER": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=131224&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "크래비티": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=11010164&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "트와이스": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=372717&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "AB6IX": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=6847803&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "에이티즈": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=3961468&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "엔하이픈": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=12564018&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "EXO": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=2145424&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "엑소 백현": "",
            "iKON": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=378038&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "ITZY": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=5762823&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "NCT": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=712416&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "NCT 127": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=4195277&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "NCT DREAM": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=3134896&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "NCT U": "",
            "더보이즈": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=2570752&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "TREASURE": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=6273134&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "TXT": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=5696221&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "WayV": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=6087930&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "청하": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=3865087&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "선미": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=4201542&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "전소미": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=11233418&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "AKMU": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=131304&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "AKMU 이수현": "",
            "아이유": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=131251&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "헤이즈": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=3147364&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "소녀시대": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=29426&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "소녀시대 태연": "",
            "이하이": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=131279&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "정은지": "",
            "젝스키스": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=1310857&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "백예린": "",
            "볼빨간사춘기": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=1852801&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "현아": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=3335159&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "비투비": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=131263&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "SF9": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=1353150&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "스테이씨": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=13314737&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "오마이걸": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=704341&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
            "위클리": "https://apps.crowdtangle.com/ygentertainmentfacebook/reporting/intelligence?accountType=facebook_page&accounts=11985965&brandedContentType=none&comparisonType=none&followersBreakdownType=followerCount&followersShowByType=total&graphType=subscriber_count&interval=day&platform=facebook&reportTimeframe=3months",
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
        # artist = response.xpath('//span[@class="omni-select-value-label"]/text()').extract()[0]
        artist = response.meta['artist']
        follower_num = response.xpath('//span[@class="ct-tooltip right arrow-middle"]/text()').extract()[0]
        item = CrowdtangleFacebookItem()
        item['artist'] = artist
        item['followers'] = follower_num.replace(',', '')
        item['url'] = response.url
        yield item
