# 용도 : crawler 관련 API들
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19

import os
import requests
import json
from datetime import datetime, timedelta

# api utilities
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from utils.shortcuts import get_env

# django_celery_beat models
from django_celery_beat.models import PeriodicTask, CrontabSchedule

# celery
from .tasks import direct_crawling

# crawler models
from crawler.models import SocialbladeYoutube, SocialbladeTwitter, SocialbladeTwitter2, SocialbladeTiktok, Melon, Vlive, \
    Spotify, Weverse, CrowdtangleFacebook, CrowdtangleInstagram

# crawler models 종합
DataModels = {
    "youtube": SocialbladeYoutube,
    "twitter": SocialbladeTwitter,
    "twitter2": SocialbladeTwitter2,
    "tiktok": SocialbladeTiktok,
    "melon": Melon,
    "spotify": Spotify,
    "weverse": Weverse,
    "facebook": CrowdtangleFacebook,
    "instagram": CrowdtangleInstagram,
    "vlive": Vlive,
}

# celery flower domain 설정 부분
flower_domain = ""
production_env = get_env("YG_ENV", "dev") == "production"
if production_env:
    flower_domain = "http://yg-celery-flower:5555/"
else:
    flower_domain = "http://0.0.0.0:5555/"


# 정의 : crawl(request : api request)
# 목적 : 크롤러 테스트 페이지에서 [크롤링 즉시 실행] 버튼을 누르면 direct_crawl task를 실행하는 api 함수
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19
@csrf_exempt
@require_http_methods(["POST"])
def crawl(request):
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)  # body값 추출
        platform = body.get("platform")
        task = direct_crawling.apply_async(args=[platform, "daily"])
        return JsonResponse({"task_id": task.id, "status": "started"})


# 정의 : show_data(request : api request)
# 목적 : 크롤러 테스트 페이지에서 [크롤링 데이터 보기] 버튼을 누르면 해당 플랫폼의 데이터를 불러오는 api 함수
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19
@csrf_exempt
@require_http_methods(["GET"])  # only get and post
def show_data(request):
    platform = request.GET.get("platform", None)
    if DataModels[platform].objects.exists():
        platform_queryset_values = DataModels[platform].objects.values()
        platform_datas = []
        for queryset_value in platform_queryset_values:
            platform_datas.append(queryset_value)
        return JsonResponse(data={"success": True, "data": platform_datas})
    else:
        return JsonResponse(status=400, data={"success": False})


# 정의 : get_schedules(schedule_type : "daily" or "hour")
# 목적 : 스케줄들을 불러오는 함수
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19
def get_schedules(schedule_type):
    schedule_list = []
    task_list = PeriodicTask.objects.values()
    if schedule_type is not None:  # schedule_type이 정해져 있으면 해당 하는 schedule_type의 스케줄들을 불러옴
        for task in task_list:
            if schedule_type in task["name"]:
                crontab_id = task["crontab_id"]
                crontab_info = CrontabSchedule.objects.filter(id=crontab_id).values()
                hour = crontab_info[0]["hour"]
                minute = crontab_info[0]["minute"]
                schedule_dict = dict(id=task["id"], name=task["name"], hour=hour, minute=minute,
                                     last_run=task["last_run_at"],
                                     enabled=task["enabled"])
                schedule_list.append(schedule_dict)
    else:  # schedule_type이 정해져 있지 않으면 모든 스케줄들을 불러옴
        for task in task_list:
            if "crawling" in task["name"]:
                crontab_id = task["crontab_id"]
                crontab_info = CrontabSchedule.objects.filter(id=crontab_id).values()
                hour = crontab_info[0]["hour"]
                minute = crontab_info[0]["minute"]
                schedule_dict = dict(id=task["id"], name=task["name"], hour=hour, minute=minute,
                                     last_run=task["last_run_at"],
                                     enabled=task["enabled"])
                schedule_list.append(schedule_dict)
    return schedule_list


# 정의 : schedules(request : api request)
# 목적 : schedule 생성, 조회, 삭제 API 함수
# 멤버함수 : get_schedules
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19
@csrf_exempt
@require_http_methods(["POST", "GET", "DELETE"])
def schedules(request):
    # 스케줄 생성 요청 (POST 요청)
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")  # body값 추출
        body = json.loads(body_unicode)
        schedule_type = body.get("schedule_type")
        platform = body.get("platform")

        # 일별 스케줄링
        if schedule_type == 'daily':
            hour = body.get("hours")
            minutes = body.get("minutes")
            if hour == "" or int(hour) < 0:
                return JsonResponse(status=400, data={"error": "스케줄링 시간 입력이 잘못되었습니다."})
            try:
                schedule, created = CrontabSchedule.objects.get_or_create(
                    hour="{}".format(hour),
                    minute="{}".format(minutes),
                    timezone="Asia/Seoul",
                )
                # 존재하는 task는 상태 및 interval만 업데이트
                if PeriodicTask.objects.filter(name="{}_{}_daily_crawling".format(platform, hour)).exists():
                    task = PeriodicTask.objects.get(name="{}_{}_daily_crawling".format(platform, hour))
                    task.enabled = True
                    task.crontab = schedule
                    task.save()
                else:
                    PeriodicTask.objects.create(
                        crontab=schedule,
                        name="{}_{}_daily_crawling".format(platform, hour),
                        task="schedule_crawling",
                        args=json.dumps((platform, schedule_type,)),
                    )
                return JsonResponse(data={"success": True})
            except Exception as e:
                return JsonResponse(status=400, data={"error": str(e)})
        # 시간별 스케줄링
        elif schedule_type == 'hour':
            try:
                period = body.get('period')
                execute_time_minute = body.get('execute_time_minute')
                # crontab schedule 생성
                schedule, created = CrontabSchedule.objects.get_or_create(
                    hour="*/{}".format(period),
                    minute="{}".format(execute_time_minute),
                    timezone="Asia/Seoul",
                )

                if PeriodicTask.objects.filter(name="{}_hour_crawling".format(platform)).exists():
                    task = PeriodicTask.objects.get(name="{}_hour_crawling".format(platform))
                    task.enabled = True
                    task.crontab = schedule
                    task.save()
                else:
                    PeriodicTask.objects.create(
                        crontab=schedule,
                        name="{}_hour_crawling".format(platform),
                        task="schedule_crawling",
                        args=json.dumps((platform, schedule_type,)),
                    )
                return JsonResponse(data={"success": True})
            except Exception as e:
                return JsonResponse(status=400, data={"error": str(e)})
    # 스케줄 조회(GET 요청)
    elif request.method == "GET":
        schedule_type = request.GET.get("schedule_type", None)
        try:
            schedule_list = get_schedules(schedule_type)
            return JsonResponse(data={"schedules": schedule_list})
        except Exception as e:
            print(e)
            return JsonResponse(status=400, data={"error": str(e)})
    # 스케줄 삭제 (DELETE 요청) 후 남은 스케줄 정보들 반환
    else:
        body_unicode = request.body.decode("utf-8")  # body값 추출
        body = json.loads(body_unicode)
        scheduleId = body.get("id")
        schedule = PeriodicTask.objects.get(id=scheduleId)
        schedule.delete()
        try:
            schedule_list = get_schedules(None)
            return JsonResponse(data={"schedules": schedule_list})
        except Exception as e:
            print(e)
            return JsonResponse(status=400, data={"error": str(e)})


# 정의 : get_all_flower_tasks()
# 목적 : celery flower 로부터 스케줄 정보들을 불러오는 함수
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19
def get_all_flower_tasks():
    flower_url = flower_domain + "api/tasks"
    response = requests.get(flower_url)
    tasks_json = json.loads(response.content.decode("utf-8"))
    return tasks_json


# 정의 : taskinfos(request : api request)
# 목적 : 실행된 task 정보를 불러오는 API 함수
# 멤버함수 : get_all_flower_tasks
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19
@csrf_exempt
@require_http_methods(["GET"])
def taskinfos(request):
    if request.method == "GET":
        schedule_id = request.GET.get("id", None)
        collect_list = ["uuid", "name", "state", "started", "args", "runtime"]
        tasks_json = get_all_flower_tasks()
        if schedule_id is None:  # 모든 task 정보들을 호출 하는 경우
            task_infos = []
            for task in tasks_json.values():
                task_info = dict()
                for key, value in task.items():
                    if key in collect_list:
                        if key == "started":
                            datetimestr = datetime.fromtimestamp(int(value)).strftime("%Y-%m-%d %H:%M:%S")
                            task_info[key] = datetimestr
                        elif key == "args":
                            platform = value.split(',')[0].strip('[').strip("'")
                            task_info['platform'] = platform
                        else:
                            task_info[key] = value
                task_infos.append(task_info)
            return JsonResponse(data={"taskinfos": task_infos})
        else:  # 특정 task의 정보들을 호출 하는 경우
            task_info = dict()
            for task in tasks_json.values():
                if task["uuid"] == schedule_id:
                    for key, value in task.items():
                        if key in collect_list:
                            task_info[key] = value
                    break

            return JsonResponse(data={"taskinfo": task_info})


# 정의 : check_valid_log(log_words: 로그 파일 내부의 한 줄에서 단어들이 담긴 배열)
# 목적 : 로그 파일의 단어들이 유효한 로그인지 아닌지 판단하는 함수
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19
def check_valid_log(log_words):
    if len(log_words) < 6:
        return False
    elif "CRAWLING-LOG" in log_words[2]:
        return True
    else:
        return False


# 정의 : parse_logfile_for_error(filepath: 로그 파일 경로)
# 목적 : 주어진 파일 경로의 로그 파일을 파싱하여 에러 상태를 지표들을 반환하는 함수
# 멤버함수 : check_valid_log
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19
def parse_logfile_for_error(filepath):
    error_infos = []
    errors = 0
    platform_name = None
    platform_artists = None
    with open(f'{filepath}', 'r') as log_file:
        for log_line in log_file:
            log_words = log_line.replace(" ", "").rstrip().split(',')
            if check_valid_log(log_words) is True:
                log_type = log_words[3].strip().strip('[]')
                if log_type == "INFO":  # 플랫폼, 아티스트 정보
                    platform_name = log_words[-2].strip()
                    platform_artists = log_words[-1].strip()
                else:
                    last_word = log_words[-1].strip()
                    if "https" in last_word:
                        error_info = dict()
                        error_info['type'] = log_words[3].strip().strip('[]')
                        error_info['artist'] = log_words[4].strip()
                        error_info['platform'] = log_words[5].strip()
                        error_info['url'] = last_word.strip()
                        error_infos.append(error_info)
                        errors += 1
        return platform_name, platform_artists, errors, error_infos


# 정의 : get_task_result(id : task의 id)
# 목적 : celery flower로부터 해당 id와 일치하는 task의 실행 상태를 조회하는 함수
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19
def get_task_result(id):
    response = requests.get(flower_domain + f"api/task/info/{id}")
    if response.status_code == 200:
        task_json = json.loads(response.content.decode("utf-8"))
        if task_json['state'] == 'SUCCESS':
            return eval(task_json['result'])
        elif task_json['state'] == 'STARTED':
            return 'started'
        else:
            return None
    else:
        return None


# 정의 : monitors(request : api request)
# 목적 : from_date ~ to_date 기간동안 실행된 task들을 모니터링하는 API => 정상 처리 아티스트 개수,  실행중인 task 개수, 에러가 발생한 아티스트 개수, 에러의 세부 정보를 반환
# 멤버함수 : get_task_result, parse_logfile_for_error
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19
@csrf_exempt
@require_http_methods(["GET"])
def monitors(request):
    if request.method == "GET":
        from_date_str = request.GET.get("fromdate", None)
        to_date_str = request.GET.get("todate", None)
        try:
            from_date_obj = datetime.strptime(from_date_str, '%Y-%m-%d')
            to_date_obj = datetime.strptime(to_date_str, '%Y-%m-%d')
        except Exception:
            return JsonResponse(status=500, data={"error": "Input Date Format Error"})

        day_diff = (to_date_obj - from_date_obj).days
        platforms = ["crowdtangle", "melon", "spotify", "tiktok", "twitter", "twitter2", "vlive", "weverse", "youtube"]
        total_artists = 0  # 처리한 총 아티스트 개수
        total_errors = 0  # 총 에러개수
        total_exec = 0  # 총 실행중 개수
        error_details = []  # 전체 에러 디테일
        for day in range(0, day_diff + 1):
            for platform in platforms:
                title_date = from_date_obj + timedelta(days=day)
                title_str = title_date.strftime("%Y-%m-%d")
                if production_env:
                    log_dir = f"../data/log/crawler/{platform}/{title_str}"
                else:
                    log_dir = f"./data/log/crawler/{platform}/{title_str}"
                if os.path.isdir(log_dir) is True:
                    file_list = os.listdir(log_dir) # 해당 플랫폼과 날짜에 해당하는 파일 이름들의 리스트
                    for file_name in file_list: # 해당 리스트 내의 로그 파일들을 분석
                        task_id = file_name.split('.')[0]
                        task_result = get_task_result(task_id) # 실행중인 task들이 있는지 flower에서 조회
                        if task_result is not None and task_result == "started":
                            total_exec += 1
                        else:
                            platform_name, platform_artists, errors, error_infos = parse_logfile_for_error(
                                f'{log_dir}/{file_name}') # 로그 파싱
                            if platform_name is not None:
                                total_artists += int(platform_artists)
                                total_errors += errors
                                for error_info in error_infos:
                                    error_details.append(error_info)
        return JsonResponse(data={"normals": total_artists - total_errors, "execs": total_exec, "errors": total_errors,
                                  "details": error_details})
