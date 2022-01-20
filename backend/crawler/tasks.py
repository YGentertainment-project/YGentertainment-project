import os
from billiard.context import Process

from .celery import app

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from crawler.scrapy_app.spiders.socialblade_youtube import YoutubeSpider
from crawler.scrapy_app.spiders.socialblade_twitter import TwitterSpider
from crawler.scrapy_app.spiders.socialblade_twitter2 import Twitter2Spider
from crawler.scrapy_app.spiders.socialblade_tiktok import TiktokSpider
from crawler.scrapy_app.spiders.crowdtangle import CrowdTangleSpider
from crawler.scrapy_app.spiders.vlive import VliveSpider
from crawler.scrapy_app.spiders.weverse import WeverseSpider
from crawler.scrapy_app.spiders.melon import MelonSpider
from crawler.scrapy_app.spiders.spotify import SpotifySpider

settings = Settings()
os.environ["SCRAPY_SETTINGS_MODULE"] = "crawler.scrapy_app.settings"
settings_module_path = os.environ["SCRAPY_SETTINGS_MODULE"]
settings.setmodule(settings_module_path, priority="project")

# TODO: DB에서 참조하도록 수정
spiders = {
    "youtube": YoutubeSpider,
    "twitter": TwitterSpider,
    "twitter2": Twitter2Spider,
    "tiktok": TiktokSpider,
    "weverse": WeverseSpider,
    "crowdtangle": CrowdTangleSpider,
    "vlive": VliveSpider,
    "melon": MelonSpider,
    "spotify": SpotifySpider,
}


def crawling_start(platform, task_id):
    process = CrawlerProcess(settings)
    # log_path = "crawler/logs/tasks/{}.log".format(task_id)
    # settings.set("LOG_FILE", log_path)
    process.crawl(spiders[platform])
    process.start()


@app.task(name="direct_crawling_platform", bind=True, default_retry_delay=30, max_retries=2, time_limit=500)
def direct_crawling_platform(self, platform):
    try:
        proc = Process(target=crawling_start, args=[platform, self.request.id])
        proc.start()
        proc.join()
    except Exception as e:
        print('Error with direct crawling {} {}'.format(platform, e))    


def crawling(platform, request_id):
    proc = Process(target=crawling_start, args=[platform, request_id])
    proc.start()
    proc.join()


@app.task(name="youtube_schedule_crawling", bind=True, default_retry_delay=30, max_retries=2, time_limit=500)
def youtube_schedule_crawling(self):
    try:
        crawling("youtube", self.request.id)
    except Exception as e:
        print("Error with scheduled youtube task : {}".format(e))


@app.task(name="twitter_schedule_crawling", bind=True, default_retry_delay=30, max_retries=2, time_limit=500)
def twitter_schedule_crawling(self):
    try:
        crawling("twitter", self.request.id)
    except Exception as e:
        print("Error with scheduled twitter task : {}".format(e))


@app.task(name="twitter2_schedule_crawling", bind=True, default_retry_delay=30, max_retries=2, time_limit=500)
def twitter2_schedule_crawling(self):
    try:
        crawling("twitter2", self.request.id)
    except Exception as e:
        print("Error with scheduled twitter2 task : {}".format(e))


@app.task(name="tiktok_schedule_crawling", bind=True, default_retry_delay=30, max_retries=2, time_limit=500)
def tiktok_schedule_crawling(self):
    try:
        crawling("tiktok", self.request.id)
    except Exception as e:
        print("Error with scheduled tiktok task : {}".format(e))


@app.task(name="weverse_schedule_crawling", bind=True, default_retry_delay=30, max_retries=2, time_limit=500)
def weverse_schedule_crawling(self):
    try:
        crawling("weverse", self.request.id)
    except Exception as e:
        print("Error with scheduled weverse task : {}".format(e))


@app.task(name="crowdtangle_schedule_crawling", bind=True, default_retry_delay=30, max_retries=2, time_limit=500)
def crowdtangle_schedule_crawling(self):
    try:
        crawling("crowdtangle", self.request.id)
    except Exception as e:
        print("Error with scheduled crowdtangle task : {}".format(e))


@app.task(name="vlive_schedule_crawling", bind=True, default_retry_delay=30, max_retries=2, time_limit=500)
def vlive_schedule_crawling(self):
    try:
        crawling("vlive", self.request.id)
    except Exception as e:
        print("Error with Crawling task : {}".format(e))


@app.task(name="spotify_schedule_crawling", bind=True, default_retry_delay=30, max_retries=2, time_limit=500)
def spotify_schedule_crawling(self):
    try:
        crawling("spotify", self.request.id)
    except Exception as e:
        print("Error with scheduled spotify task : {}".format(e))


@app.task(name="melon_schedule_crawling", bind=True, default_retry_delay=30, max_retries=2, time_limit=500)
def melon_schedule_crawling(self):
    try:
        crawling("melon", self.request.id)
    except Exception as e:
        print("Error with scheduled melon task : {}".format(e))
