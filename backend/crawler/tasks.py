from celery.utils.log import get_task_logger
from crawler.scrapy_app.spiders.weverse import WeverseSpider
from celery import shared_task
from crawler.scrapy_app.spiders.vlive import VliveSpider
from crawler.scrapy_app.spiders.crowdtangle_instagram import InstagramSpider
from crawler.scrapy_app.spiders.crowdtangle_facebook import FacebookSpider
from crawler.scrapy_app.spiders.socialblade_tiktok import TiktokSpider
from crawler.scrapy_app.spiders.socialblade_twitter2 import Twitter2Spider
from crawler.scrapy_app.spiders.socialblade_twitter import TwitterSpider
from crawler.scrapy_app.spiders.socialblade_youtube import YoutubeSpider
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
import scrapy
from .celery import app
from billiard.context import Process
import os
import logging

settings = Settings()
os.environ['SCRAPY_SETTINGS_MODULE'] = 'crawler.scrapy_app.settings'
settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
settings.setmodule(settings_module_path, priority='project')

# TODO: DB에서 참조하도록 수정
spiders = {
    'youtube': YoutubeSpider,
    'twitter': TwitterSpider,
    'twitter2': Twitter2Spider,
    'tiktok': TiktokSpider,
    'weverse': WeverseSpider,
    'facebook': FacebookSpider,
    'instagram': InstagramSpider,
    'vlive': VliveSpider,
}


def crawling_start(platform, task_id):
    process = CrawlerProcess(settings)
    log_path = "crawler/logs/tasks/{}.log".format(task_id)
    settings.set('LOG_FILE', log_path)
    process.crawl(spiders[platform])
    process.start()

@shared_task(name="crawling_platform", bind=True, default_retry_delay=10, max_retries=5)
def crawling_platform(self, platform):
    try:
        proc = Process(target=crawling_start, args=[platform, self.request.id])
        proc.start()
        proc.join()
    except:
        crawling_platform.retry()
        print(f'Error with Crawling task')

def crawling(platform, request_id):
    proc = Process(target=crawling_start, args=[platform, request_id])
    proc.start()
    proc.join()


# @shared_task(name="crawling", bind=True, default_retry_delay=10, max_retries=5, soft_time_limit=250)
@shared_task(name="youtube_crawling", bind=True, default_retry_delay=10, max_retries=5)
def youtube_crawling(self):
    try:
        crawling('youtube', self.request.id)
    except:
        youtube_crawling.retry()
        print(f'Error with Crawling task')

# @shared_task(name="crawling", bind=True, default_retry_delay=10, max_retries=5, soft_time_limit=250)
@shared_task(name="twitter_crawling", bind=True, default_retry_delay=10, max_retries=5)
def twitter_crawling(self):
    try:
        crawling('twitter', self.request.id)
    except:
        twitter_crawling.retry()
        print(f'Error with Crawling task')

# @shared_task(name="crawling", bind=True, default_retry_delay=10, max_retries=5, soft_time_limit=250)
@shared_task(name="twitter2_crawling", bind=True, default_retry_delay=10, max_retries=5)
def twitter2_crawling(self):
    try:
        crawling('twitter2', self.request.id)
    except:
        twitter2_crawling.retry()
        print(f'Error with Crawling task')

# @shared_task(name="crawling", bind=True, default_retry_delay=10, max_retries=5, soft_time_limit=250)
@shared_task(name="tiktok_crawling", bind=True, default_retry_delay=10, max_retries=5)
def tiktok_crawling(self):
    try:
        crawling('tiktok', self.request.id)
    except:
        tiktok_crawling.retry()
        print(f'Error with Crawling task')

# @shared_task(name="crawling", bind=True, default_retry_delay=10, max_retries=5, soft_time_limit=250)
@shared_task(name="weverse_crawling", bind=True, default_retry_delay=10, max_retries=5)
def weverse_crawling(self):
    try:
        crawling('weverse', self.request.id)
    except:
        weverse_crawling.retry()
        print(f'Error with Crawling task')

# @shared_task(name="crawling", bind=True, default_retry_delay=10, max_retries=5, soft_time_limit=250)
@shared_task(name="facebook_crawling", bind=True, default_retry_delay=10, max_retries=5)
def facebook_crawling(self):
    try:
        crawling('facebook', self.request.id)
    except:
        facebook_crawling.retry()
        print(f'Error with Crawling task')

# @shared_task(name="crawling", bind=True, default_retry_delay=10, max_retries=5, soft_time_limit=250)
@shared_task(name="instagram_crawling", bind=True, default_retry_delay=10, max_retries=5)
def instagram_crawling(self):
    try:
        crawling('instagram', self.request.id)
    except:
        instagram_crawling.retry()
        print(f'Error with Crawling task')

# @shared_task(name="crawling", bind=True, default_retry_delay=10, max_retries=5, soft_time_limit=250)
@shared_task(name="vlive_crawling", bind=True, default_retry_delay=10, max_retries=5)
def vlive_crawling(self):
    try:
        crawling('vlive', self.request.id)
    except:
        vlive_crawling.retry()
        print(f'Error with Crawling task')