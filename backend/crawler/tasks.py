import os, sys
import traceback

from .celery import app

from scrapy import spiderloader
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from django.utils import timezone
from billiard.context import Process
from django.db.models import Q
from config.models import Schedule
from dataprocess.models import CollectTarget, Platform, Artist
from utils.shortcuts import get_env
from datetime import datetime
import logging

settings = Settings()
os.environ["SCRAPY_SETTINGS_MODULE"] = "crawler.scrapy_app.settings"
settings_module_path = os.environ["SCRAPY_SETTINGS_MODULE"]
settings.setmodule(settings_module_path, priority="project")

spider_loader = spiderloader.SpiderLoader.from_settings(settings)

# crawling_start에서 경로 설정을 위해 절대경로 변경
sys.path.append(os.path.dirname(os.path.abspath('.')))

# crawling logger
crawlinglogger = logging.getLogger("CRAWLING-LOG")

production_env = get_env("YG_ENV", "dev") == "production"
crawlinglogger.setLevel(logging.ERROR)


# platform과 schedule_type에 해당하는 수집 대상들을 추출
def extract_target_list(platform, schedule_type="daily"):
    if platform == "crowdtangle" or platform == "crowdtangle-past":
        facebook_id = Platform.objects.get(name="facebook").id
        instagram_id = Platform.objects.get(name="instagram").id
        crawl_infos = CollectTarget.objects.filter(Q(platform_id=facebook_id) | Q(platform_id=instagram_id))
    else:
        platform_id = Platform.objects.get(name=platform).id
        crawl_infos = CollectTarget.objects.filter(platform_id=platform_id)

    crawl_target = []

    for crawl_info in crawl_infos:
        crawl_target_row = dict()

        try:
            schedule_info = Schedule.objects.get(collect_target_id=crawl_info.id, schedule_type=schedule_type)
        except Schedule.DoesNotExist:
            schedule_info = None

        if schedule_info is not None and schedule_info.active == 1:
            artist_name = Artist.objects.get(id=crawl_info.artist_id).name
            target_url = crawl_info.target_url

            crawl_target_row['id'] = crawl_info.id
            crawl_target_row['artist_name'] = artist_name
            crawl_target_row['target_url'] = target_url

            if platform == "melon" or platform == "spotify":
                crawl_target_row['target_url_2'] = crawl_info.target_url_2

            crawl_target.append(crawl_target_row)
    return crawl_target


def crawling_start(platform, task_id, crawl_target):
    process = CrawlerProcess(settings)
    date_str = timezone.localdate().strftime('%Y-%m-%d')
    if production_env:
        DATA_PATH = "/data/log/crawler"
    else:
        DATA_PATH = "./data/log/crawler"

    formatter = logging.Formatter('[%(asctime)s], [%(levelname)s], [%(name)s:%(lineno)d], %(message)s', '%Y-%m-%d %H:%M:%S')
    
    if os.path.isdir(DATA_PATH) is False:
        os.mkdir(DATA_PATH)
    platform_dir = "{}/{}".format(DATA_PATH, platform)
    if os.path.isdir(platform_dir) is False:
        os.mkdir(platform_dir)
    log_dir = "{}/{}/{}".format(DATA_PATH, platform, date_str)
    if os.path.isdir(log_dir) is False:
        os.mkdir(log_dir)
    log_path = "{}/{}/{}/{}.log".format(DATA_PATH, platform, date_str, task_id)
    trfh = logging.handlers.TimedRotatingFileHandler(
        filename=log_path,
        when="midnight",
        interval=1,
        encoding="utf-8",
    )
    trfh.setFormatter(formatter)
    trfh.setLevel(logging.INFO)
    crawlinglogger.addHandler(trfh)
    process.crawl(spider_loader.load(platform), crawl_target=crawl_target)
    process.start()


@app.task(name="direct_crawling", bind=True, default_retry_delay=30, max_retries=2)
def direct_crawling(self, platform, schedule_type="daily"):
    crawl_target = extract_target_list(platform, schedule_type)
    try:
        process = Process(target=crawling_start, args=[platform, self.request.id, crawl_target])
        process.start()
        process.join()
    except Exception as e:
        traceback.print_exc()
        print('Error with direct {} crawling {}'.format(platform, e))
    return {"platform": platform, "artists": len(crawl_target)}


@app.task(name="schedule_crawling", bind=True, default_retry_delay=30, max_retries=2)
def schedule_crawling(self, platform, schedule_type):
    crawl_target = extract_target_list(platform, schedule_type)
    try:
        process = Process(target=crawling_start, args=[platform, self.request.id, crawl_target])
        process.start()
        process.join()
    except Exception as e:
        traceback.print_exc()
        print("Error with scheduled {} crawling : {}".format(platform, e))
    return {"platform": platform, "artists": len(crawl_target)}
