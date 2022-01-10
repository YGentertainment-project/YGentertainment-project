from time import sleep
import json
import scrapy
from bs4 import BeautifulSoup

from ..items import SpotifyItem

class SpotifySpider(scrapy.Spider):
    name = 'spotify'
    def start_requests(self):
        artist_url = {
            "(여자)아이들": "https://open.spotify.com/artist/2AfmfGFbe0A0WsTYm0SDTx",
            "강다니엘": "https://open.spotify.com/artist/5vGoWnZO65NBgiZYBmi3iW",
            "뉴이스트": "https://open.spotify.com/artist/1iQfn1B8V25iQoolQakyAZ",
            "레드벨벳": "https://open.spotify.com/artist/1z4g3DjTBBZKhvAroFlhOM",
            "레드벨벳 아이린": "",
            "레드벨벳 슬기": "",
            "레드벨벳 조이": "",
            "레드벨벳 웬디": "",
            "레드벨벳 예리": "",
            "마마무": "https://open.spotify.com/artist/0XATRDCYuuGhk0oE7C0o5G",
            "마마무 화사": "https://open.spotify.com/artist/7bmYpVgQub656uNTu6qGNQ",
            "몬스타엑스": "https://open.spotify.com/artist/4TnGh5PKbSjpYqpIdlW5nz",
            "방탄소년단": "https://open.spotify.com/artist/3Nrfpe0tUJi4K4DXYWgMUX",
            "BLACKPINK": "https://open.spotify.com/artist/41MozSoPIsD1dJM0CLPjZF",
            "BLACKPINK 로제": "https://open.spotify.com/artist/3eVa5w3URK5duf6eyVDbu9",
            "BLACKPINK 리사": "https://open.spotify.com/artist/5L1lO4eRHmJ7a0Q6csE5cT",
            "BLACKPINK 제니": "https://open.spotify.com/artist/250b0Wlc5Vk0CoUsaCY84M",
            "BLACKPINK 지수": "",
            "BIGBANG": "https://open.spotify.com/artist/4Kxlr1PRlDKEB0ekOCyHgX",
            "BIGBANG 지드래곤": "https://open.spotify.com/artist/30b9WulBM8sFuBo17nNq9c",
            "샤이니": "https://open.spotify.com/artist/2hRQKC0gqlZGPrmUKbcchR",
            "세븐틴": "https://open.spotify.com/artist/7nqOGRxlXj7N2JYbgNEjYH",
            "슈퍼주니어": "https://open.spotify.com/artist/6gzXCdfYfFe5XKhPKkYqxV",
            "스트레이키즈": "https://open.spotify.com/artist/2dIgFjalVxs4ThymZ67YCE",
            "아스트로": "https://open.spotify.com/artist/4pz4uzOMpJQyV8UTsDy4H8",
            "아스트로 차은우": "",
            "에스파": "https://open.spotify.com/artist/6YVMFz59CuY7ngCxTxjpxE",
            "WINNER": "https://open.spotify.com/artist/5DuzBeOgFwViFcv00Q5PFb",
            "크래비티": "https://open.spotify.com/artist/6FkhUhUwSPl3mGB6mmE8wn",
            "트와이스": "https://open.spotify.com/artist/7n2Ycct7Beij7Dj7meI4X0",
            "AB6IX": "https://open.spotify.com/artist/4y0wFJ5jmCUNRLZfsw1I7g",
            "에이티즈": "https://open.spotify.com/artist/68KmkJeZGfwe1OUaivBa2L",
            "엔하이픈": "https://open.spotify.com/artist/5t5FqBwTcgKTaWmfEbwQY9",
            "EXO": "https://open.spotify.com/artist/3cjEqqelV9zb4BYE3qDQ4O",
            "엑소 백현": "https://open.spotify.com/artist/4ufh0WuMZh6y4Dmdnklvdl",
            "iKON": "https://open.spotify.com/artist/5qRSs6mvI17zrkJpOHkCoM",
            "ITZY": "https://open.spotify.com/artist/2KC9Qb60EaY0kW4eH68vr3",
            "NCT": "",
            "NCT 127": "https://open.spotify.com/artist/7f4ignuCJhLXfZ9giKT7rH",
            "NCT DREAM": "https://open.spotify.com/artist/1gBUSTR3TyDdTVFIaQnc02",
            "NCT U": "https://open.spotify.com/artist/3paGCCtX1Xr4Gx53mSeZuQ",
            "더보이즈": "https://open.spotify.com/artist/0CmvFWTX9zmMNCUi6fHtAx",
            "TREASURE": "https://open.spotify.com/artist/3KonOYiLsU53m4yT7gNotP",
            "TXT": "https://open.spotify.com/artist/0ghlgldX5Dd6720Q3qFyQB",
            "WayV": "https://open.spotify.com/artist/1qBsABYUrxg9afpMtyoFKz",
            "청하": "https://open.spotify.com/artist/2PSJ6YriU7JsFucxACpU7Y",
            "선미": "https://open.spotify.com/artist/6MoXcK2GyGg7FIyxPU5yW6",
            "전소미": "https://open.spotify.com/artist/7zYj9S9SdIunYCfSm7vzAR",
            "AKMU": "https://open.spotify.com/artist/6OwKE9Ez6ALxpTaKcT5ayv",
            "AKMU 이수현": "https://open.spotify.com/artist/6zfPiJgoaqNPHsW3fsUlBN",
            "아이유": "https://open.spotify.com/artist/3HqSLMAZ3g3d5poNaI7GOU",
            "헤이즈": "https://open.spotify.com/artist/5dCvSnVduaFleCnyy98JMo",
            "소녀시대": "https://open.spotify.com/artist/0Sadg1vgvaPqGTOjxu0N6c",
            "소녀시대 태연": "https://open.spotify.com/artist/3qNVuliS40BLgXGxhdBdqu",
            "이하이": "https://open.spotify.com/artist/7cVZApDoQZpS447nHTsNqu",
            "정은지": "https://open.spotify.com/artist/7cgAZ03K2mMaWB70gwZs92",
            "젝스키스": "https://open.spotify.com/artist/6uRyNreOHUvWPNGnKfIo27",
            "백예린": "https://open.spotify.com/artist/6dhfy4ByARPJdPtMyrUYJK",
            "볼빨간사춘기": "https://open.spotify.com/artist/4k5fFEYgkWYrYvtOK3zVBl",
            "현아": "https://open.spotify.com/artist/3UwlejyX2b458azZ7eCnHb",
            "비투비": "https://open.spotify.com/artist/2hcsKca6hCfFMwwdbFvenJ",
            "SF9": "https://open.spotify.com/artist/7LOmc7gyMVMOWF8qwEdn2X",
            "스테이씨": "https://open.spotify.com/artist/01XYiBYaoMJcNhPokrg0l0",
            "오마이걸": "https://open.spotify.com/artist/2019zR22qK2RBvCqtudBaI",
            "위클리": "https://open.spotify.com/artist/73B9bjqS2Z5KLXNGqXf64m",
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
        artist_id = response.url[32:]
        result = soup.select_one('script[id="initial-state"]').text
        json_object = json.loads(result)
        head = 'spotify:artist:'
        dummy = json_object['entities']['items'][head+artist_id]['nodes']
        for target in dummy:
            if not target: continue
            if target['id'] == 'artist_biography_row':
                listen = target['custom']['monthly_listeners_count']
                follow = target['custom']['followers']
        item = SpotifyItem()
        item['artist'] = artist
        item['monthly_listens'] = listen
        item['followers'] = follow
        item['url1'] = response.url
        item['url2'] = None
        yield item