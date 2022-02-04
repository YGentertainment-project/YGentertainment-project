import sys, os, requests, json
from datetime import datetime, timedelta

# api utilities
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from utils.shortcuts import get_env
from dataprocess.models import CollectTarget
from dataprocess.models import Artist
from dataprocess.models import Platform
from config.models import Schedule
from django.db.models import Q
from django.apps import apps

# django_celery_beat models
from django_celery_beat.models import PeriodicTask, CrontabSchedule

# celery
from .tasks import direct_crawling

DataModels = {
    model._meta.db_table: model for model in apps.get_app_config('crawler').get_models()
}

# flower domain config
flower_domain = ""
production_env = get_env("YG_ENV", "dev") == "production"
if production_env:
    flower_domain = "http://yg-celery-flower:5555/"
else:
    flower_domain = "http://0.0.0.0:5555/"


def extract_target_list(platform):
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
        if Schedule.objects.get(collect_target_id=crawl_info.id).active == 1:
            artist_name = Artist.objects.get(id=crawl_info.artist_id).name
            target_url = crawl_info.target_url

            crawl_target_row['id'] = crawl_info.id
            crawl_target_row['artist_name'] = artist_name
            crawl_target_row['target_url'] = target_url

            if platform == "melon" or platform == "spotify":
                crawl_target_row['target_url_2'] = crawl_info.target_url_2

            crawl_target.append(crawl_target_row)
    return crawl_target


@csrf_exempt
@require_http_methods(["POST"])  # only post
def crawl(request):
    # 새로운 Task를 생성하는 POST 요청
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)  # body값 추출
        platform = body.get("platform")
        crawl_target = extract_target_list(platform)
        task = direct_crawling.apply_async(args=[platform, crawl_target])
        return JsonResponse({"task_id": task.id, "status": "started"})


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


def get_schedules():
    schedule_list = []
    task_list = PeriodicTask.objects.values()
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


# Schedule 생성, 조회, 삭제 API
@csrf_exempt
@require_http_methods(["POST", "GET", "DELETE"])
def schedules(request):
    # 스케줄 생성 요청
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")  # body값 추출
        body = json.loads(body_unicode)
        platform = body.get("platform")
        hour = body.get("hours")
        minutes = body.get("minutes")
        if hour == "":
            hour = "*"
        try:
            schedule, created = CrontabSchedule.objects.get_or_create(
                hour="{}".format(hour),
                minute="{}".format(minutes),
                timezone="Asia/Seoul",
            )
            # 존재하는 task는 상태 및 interval만 업데이트
            if PeriodicTask.objects.filter(name="{}_{}_schedule_crawling".format(platform, hour)).exists():
                task = PeriodicTask.objects.get(name="{}_{}_schedule_crawling".format(platform, hour))
                task.enabled = True
                task.crontab = schedule
                task.save()
            else:
                crawl_target = extract_target_list(platform)
                PeriodicTask.objects.create(
                    crontab=schedule,
                    name="{}_{}_schedule_crawling".format(platform, hour),
                    task="schedule_crawling",
                    args=json.dumps((platform, crawl_target,)),
                )
            return JsonResponse(data={"success": True})
        except Exception as e:
            return JsonResponse(status=400, data={"error": str(e)})
    # 스케줄 리스트 업
    elif request.method == "GET":
        try:
            schedule_list = get_schedules()
            return JsonResponse(data={"schedules": schedule_list})
        except Exception as e:
            print(e)
            return JsonResponse(status=400, data={"error": str(e)})
    else:
        body_unicode = request.body.decode("utf-8")  # body값 추출
        body = json.loads(body_unicode)
        scheduleId = body.get("id")
        schedule = PeriodicTask.objects.get(id=scheduleId)
        schedule.delete()

        try:
            schedule_list = get_schedules()
            return JsonResponse(data={"schedules": schedule_list})
        except Exception as e:
            print(e)
            return JsonResponse(status=400, data={"error": str(e)})


def get_all_tasks():
    flower_url = flower_domain + "api/tasks"
    response = requests.get(flower_domain + "api/tasks")
    tasks_json = json.loads(response.content.decode("utf-8"))
    return tasks_json


@csrf_exempt
@require_http_methods(["POST", "GET"])
def taskinfos(request):
    if request.method == "GET":
        schedule_id = request.GET.get("id", None)
        collect_list = ["uuid", "name", "state", "started", "args", "runtime"]
        tasks_json = get_all_tasks()
        if schedule_id is None:
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
        else:
            task_info = dict()
            for task in tasks_json.values():
                if task["uuid"] == schedule_id:
                    for key, value in task.items():
                        if key in collect_list:
                            task_info[key] = value
                    break

            return JsonResponse(data={"taskinfo": task_info})


def get_task_result(id):
    response = requests.get(flower_domain + f"api/task/info/{id}")
    if response.status_code == 200:
        task_json = json.loads(response.content.decode("utf-8"))
        if task_json['state'] == 'SUCCESS':
            return eval(task_json['result'])
        elif task_json['state'] == 'started':
            return 'started'
        else:
            return None
    else:
        return None

def parse_logfile(filepath):
    error_infos = []
    errors = 0
    with open(f'{filepath}', 'r') as log_file:
        for log_line in log_file:
            log_words = log_line.rstrip().split(' ')
            last_word = log_words[-1]
            if "https" in last_word:
                error_info = dict()
                error_info['type'] = log_words[4].strip('[]')
                error_info['artist'] = log_words[5]
                error_info['platform'] = log_words[7]
                error_info['url'] = last_word
                error_infos.append(error_info)
                errors += 1
    return errors, error_infos

@csrf_exempt
@require_http_methods(["GET"])
def monitors(request):
    if request.method == "GET":
        from_date_str = request.GET.get("fromdate", None)
        to_date_str = request.GET.get("todate", None)
        print('from_date_str : ',from_date_str)
        print('to_date_str : ',to_date_str)
        try:
            from_date_obj = datetime.strptime(from_date_str, '%Y-%m-%d')
            to_date_obj = datetime.strptime(to_date_str, '%Y-%m-%d')
        except Exception as e:
            return JsonResponse(status=500, data={"error": "Input Date Format Error"})


        day_diff = (to_date_obj - from_date_obj).days

        # 처리한 아티스트 개수 => flower에서 task의 result로부터 가져오기
        # 에러 발생한 아티스트 개수 => log에서 파싱
        # 생성된 로그 파일을 기준으로 모두 체크하되,
        # flower에서 완료되지 않은 태스크는 모니터링 카운트에서 배제한다.
        # crawling_start에서 경로 설정을 위해 절대경로 변경
        # sys.path.append(os.path.dirname(os.path.abspath('..')))

        platforms = ["crowdtangle", "melon", "spotify", "tiktok", "twitter", "twitter2", "vlive", "weverse", "youtube"]
        total_artists = 0 # 처리한 총 아티스트 개수
        total_errors = 0 # 총 에러개수
        total_exec = 0 # 총 실행중 개수
        error_details = [] # 전체 에러 디테일
        for day in range(0, day_diff + 1):
            for platform in platforms:
                title_date = from_date_obj + timedelta(days=day)
                title_str = title_date.strftime("%Y-%m-%d")
                log_dir = f"./data/log/crawler/{platform}/{title_str}"
                if os.path.isdir(log_dir) is True:
                    file_list = os.listdir(log_dir)
                    for file_name in file_list:
                        task_id = file_name.split('.')[0]
                        task_result = get_task_result(task_id)
                        if task_result == "started":
                            total_exec += 1
                        elif task_result is not None:
                            total_artists += task_result['artists']
                            errors, error_infos = parse_logfile(f'{log_dir}/{file_name}')
                            total_errors += errors
                            for error_info in error_infos:
                                error_details.append(error_info)

        return JsonResponse(data={"normals": total_artists - total_errors, "execs": total_exec, "errors": total_errors, "details": error_details})
