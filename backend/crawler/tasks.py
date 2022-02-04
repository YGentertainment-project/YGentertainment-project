import os, sys
import traceback

from .celery import app

from scrapy import spiderloader
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from django.utils import timezone
from billiard.context import Process

settings = Settings()
os.environ["SCRAPY_SETTINGS_MODULE"] = "crawler.scrapy_app.settings"
settings_module_path = os.environ["SCRAPY_SETTINGS_MODULE"]
settings.setmodule(settings_module_path, priority="project")

spider_loader = spiderloader.SpiderLoader.from_settings(settings)

# crawling_start에서 경로 설정을 위해 절대경로 변경
sys.path.append(os.path.dirname(os.path.abspath('.')))


def crawling_start(platform, task_id, crawl_target):
    process = CrawlerProcess(settings)
    date_str = timezone.localdate().strftime('%Y-%m-%d')
    crawler_dir = "./data/log/crawler"
    if os.path.isdir(crawler_dir) is False:
        os.mkdir(crawler_dir)
    platform_dir = "./data/log/crawler/{}".format(platform)
    if os.path.isdir(platform_dir) is False:
        os.mkdir(platform_dir)
    log_dir = "./data/log/crawler/{}/{}".format(platform, date_str)
    if os.path.isdir(log_dir) is False:
        os.mkdir(log_dir)
    log_path = "./data/log/crawler/{}/{}/{}.log".format(platform, date_str, task_id)
    settings.set("LOG_FILE", log_path)
    process.crawl(spider_loader.load(platform), crawl_target=crawl_target)
    process.start()


@app.task(name="direct_crawling", bind=True, default_retry_delay=30, max_retries=2)
def direct_crawling(self, platform, crawl_target):
    try:
        process = Process(target=crawling_start, args=[platform, self.request.id, crawl_target])
        process.start()
        process.join()
    except Exception as e:
        traceback.print_exc()
        print('Error with direct {} crawling {}'.format(platform, e))
    return {'artists': len(crawl_target)}


@app.task(name="schedule_crawling", bind=True, default_retry_delay=30, max_retries=2)
def schedule_crawling(self, platform, crawl_target):
    try:
        process = Process(target=crawling_start, args=[platform, self.request.id, crawl_target])
        process.start()
        process.join()
    except Exception as e:
        traceback.print_exc()
        print("Error with scheduled {} crawling : {}".format(platform, e))
    return {'artists': len(crawl_target)}