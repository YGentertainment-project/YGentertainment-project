import logging, os
from billiard.context import Process

from .celery import app

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from crawler.scrapy_app.spiders.socialblade_youtube import YoutubeSpider
from crawler.scrapy_app.spiders.socialblade_twitter import TwitterSpider
from crawler.scrapy_app.spiders.socialblade_twitter2 import Twitter2Spider
from crawler.scrapy_app.spiders.socialblade_tiktok import TiktokSpider
from crawler.scrapy_app.spiders.crowdtangle_facebook import FacebookSpider
from crawler.scrapy_app.spiders.crowdtangle_instagram import InstagramSpider
from crawler.scrapy_app.spiders.vlive import VliveSpider
from crawler.scrapy_app.spiders.weverse import WeverseSpider
from celery import shared_task
from celery.utils.log import get_task_logger

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




@shared_task(name="crawling", bind=True, default_retry_delay=10, max_retries=5, soft_time_limit=250)
def crawling(self, platform):

    try:
        proc = Process(target=crawling_start, args=[platform, self.request.id])
        proc.start()
        proc.join()
    except:
        crawling.retry()
        print(f'Error with Crawling task')
