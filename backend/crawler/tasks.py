# 용도 : Celery app이 실행시킬 task들을 정의하는 파일
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19

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
import logging

# scrapy_app의 settings.py에서 설정된 기본 설정값 불러오기
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


# 정의 : extract_target_list(platform : 크롤러가 수집할 플랫폼 이름, schedule_type : 스케줄 방식을 정의[daily or hour] )
# 목적 : 크롤러가 크롤링을 진행 하기전에 Database로부터 조건에 맞는 수집 대상 정보를 불러오는 함수
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19
def extract_target_list(platform, schedule_type="daily"):
    if platform == "crowdtangle" or platform == "crowdtangle-past": # crowdtangle은 facebook, instagram의 정보들을 추출
        facebook_id = Platform.objects.get(name="facebook").id
        instagram_id = Platform.objects.get(name="instagram").id
        crawl_infos = CollectTarget.objects.filter(Q(platform_id=facebook_id) | Q(platform_id=instagram_id))
    else: # 나머지는 각자의 플랫폼의 수집 정보들을 추출
        platform_id = Platform.objects.get(name=platform).id
        crawl_infos = CollectTarget.objects.filter(platform_id=platform_id)

    crawl_target = [] # 수집 대상이 담길 List

    # DB에서 긁어온 수집대상 정보 중에서 조건에 해당 하는 대상들을 최종 선정
    for crawl_info in crawl_infos:
        crawl_target_row = dict()

        # 수집 대상별로 각자 할당된 스케줄 정보를 DB에서 추출
        if platform == "crowdtangle-past":
            try:
                # crowdtangle-past의 경우 수집대상 id가 일치하는 스케줄 정보 모두를 추출
                schedule_info = Schedule.objects.get(collect_target_id=crawl_info.id)
            except Schedule.DoesNotExist:
                schedule_info = None
        else:
            try:
                # 수집대상 id와 schedule_type(daily인지 hour인지) 일치하는 스케줄 정보 모두를 추출
                schedule_info = Schedule.objects.get(collect_target_id=crawl_info.id, schedule_type=schedule_type)
            except Schedule.DoesNotExist:
                schedule_info = None

        # 해당 하는 수집 대상에게 해당 되는 스케줄 정보가 있으며 최종 수집 대상으로 선정
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


# 정의 : crawling_start(platform : 크롤러가 수집할 플랫폼 이름, task_id : celery가 생성한 task의 id, crawl_target : DB에서 불러온 수집대상 정보)
# 목적 : 크롤러가 크롤링을 실행하기 위해 실행되는 함수로 1) logger 경로 및 포맷 설정, 2) spider를 trigger하는 프로세스 생성 및 실행의 기능을 가짐
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19
def crawling_start(platform, task_id, crawl_target):
    # logger 경로 설정 및 포맷 설정
    date_str = timezone.localdate().strftime('%Y-%m-%d')
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
    crawlinglogger.error(f"[INFO], {platform}, {len(crawl_target)}")

    # scrapy_app의 기본 설정값에 맞는 크롤링 프로세스 생성 및 실행
    process = CrawlerProcess(settings)
    process.crawl(spider_loader.load(platform), crawl_target=crawl_target, crawl_logger=crawlinglogger)
    process.start()


# 정의 : direct_crawling(platform : 크롤러가 수집할 플랫폼 이름, schedule_type : 스케줄 방식을 정의[daily or hour])
# 목적 : 스케줄링에 관계 없이 바로 크롤러를 실행하는 Celery task, 테스트 목적으로 사용되며, 기본적으로 daily로 수집하기로한 아티스트들을 수집대상으로 선정
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19
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


# 정의 : schedule_crawling(platform : 크롤러가 수집할 플랫폼 이름, schedule_type : 스케줄 방식을 정의[daily or hour])
# 목적 : 스케줄링 정보에 맞춰 크롤러를 실행하는 Celery task, 기본적으로 스케줄링 되었을때 실행되는 Task
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19
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
