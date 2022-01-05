import json, datetime, os

# api utilities
from uuid import uuid4
from urllib.parse import urlparse
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt

# crawler models
from crawler.models import SocialbladeYoutube, SocialbladeTiktok, SocialbladeTwitter, SocialbladeTwitter2, \
    Weverse, CrowdtangleInstagram, CrowdtangleFacebook, Vlive, Melon, Spotify

# django_celery_beat models
from django_celery_beat.models import PeriodicTask, CrontabSchedule


# celery
from .tasks import crawling
from .celery import app
from celery.result import AsyncResult


@csrf_exempt
@require_http_methods(['POST', 'GET'])  # only get and post
def crawl(request):
    # 새로운 Task를 생성하는 POST 요청
    if request.method == 'POST':
        unique_id = str(uuid4())  # create a unique ID.
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)  # body값 추출
        platform = body.get("platform")

        task = crawling.apply_async(args=[platform])
        return JsonResponse({'task_id': task.id, 'status': 'started'})

    # Task 상태를 체크하는 GET 요청
    elif request.method == 'GET':
        task_id = request.GET.get('task_id', None)
        if not task_id:
            return JsonResponse(status=400, data={'error': 'Missing args'})
        result = AsyncResult(id=task_id, app=app)
        status = result.state
        try:
            return JsonResponse({'status': status})
        except Exception as e:
            return JsonResponse(status=400, data={'error': str(e)})


@csrf_exempt
@require_http_methods(['GET'])  # only get and post
def show_data(request):
    platform = request.GET.get('platform', None)

    DataModels = {
        "youtube": SocialbladeYoutube,
        "tiktok": SocialbladeTiktok,
        "twitter": SocialbladeTwitter,
        "twitter2": SocialbladeTwitter2,
        "weverse": Weverse,
        "instagram": CrowdtangleInstagram,
        "facebook": CrowdtangleFacebook,
        "vlive": Vlive,
        "melon": Melon,
        "spotify": Spotify,
    }
    if DataModels[platform].objects.exists():
        platform_queryset_values = DataModels[platform].objects.values()
        platform_datas = []
        for queryset_value in platform_queryset_values:
            platform_datas.append(queryset_value)
        return JsonResponse(data={'success': True, 'data': platform_datas})
    else:
        return JsonResponse(status=400, data={'success': False})


# daily read API
# main이랑 merge할 때 conflict나면 main 버리고 이거를 살리기
@csrf_exempt
@require_http_methods(['GET'])  # only get and post
def daily_read(request):
    DataModels = {
        "youtube": SocialbladeYoutube,
        "tiktok": SocialbladeTiktok,
        "twitter": SocialbladeTwitter,
        "twitter2": SocialbladeTwitter2,
        "weverse": Weverse,
        "instagram": CrowdtangleInstagram,
        "facebook": CrowdtangleFacebook,
        "vlive": Vlive,
        "melon": Melon,
        "spotify": Spotify,
    }
    platform = request.GET.get('platform', None)
    type = request.GET.get('type', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if type == "누적":
        start_date_dateobject = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        filter_objects = DataModels[platform].objects.filter(recorded_date__year=start_date_dateobject.year,
                                                             recorded_date__month=start_date_dateobject.month,
                                                             recorded_date__day=start_date_dateobject.day)
        if filter_objects.exists():
            filter_objects_values = filter_objects.values()
            filter_datas = []
            for filter_value in filter_objects_values:
                filter_datas.append(filter_value)
            return JsonResponse(data={'success': True, 'data': filter_datas})
        else:
            return JsonResponse(status=400, data={'success': True, 'data': []})
    # elif type=="기간별"://기간별에 속하는 모든 data 전송
    #     start_date_dateobject = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').date()
    #     end_date_dateobject = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').date()
    #     db_start_date = datetime.datetime.combine(start_date_dateobject, datetime.time.min)
    #     db_end_date = datetime.datetime.combine(end_date_dateobject, datetime.time.max) #change to 23:59:59
    #     filter_objects = Socialblade.objects.filter(platform=platform, recorded_date__range=(db_start_date,db_end_date))
    #     if filter_objects.exists():
    #         filter_objects_values = filter_objects.values()
    #         filter_datas = []
    #         for filter_value in filter_objects_values:
    #             filter_datas.append(filter_value)
    #         return JsonResponse(data={'success': True, 'data': filter_datas})
    #     else:
    #         return JsonResponse(status=400, data={'success': True, 'data': []})
    elif type == "기간별":
        # 전날 값을 구함
        start_date_dateobject = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').date() - datetime.timedelta(
            1)
        end_date_dateobject = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').date()
        filter_objects_start = DataModels[platform].objects.filter(recorded_date__year=start_date_dateobject.year,
                                                                   recorded_date__month=start_date_dateobject.month,
                                                                   recorded_date__day=start_date_dateobject.day)
        filter_objects_end = DataModels[platform].objects.filter(recorded_date__year=end_date_dateobject.year,
                                                                 recorded_date__month=end_date_dateobject.month,
                                                                 recorded_date__day=end_date_dateobject.day)
        filter_datas_start = []
        filter_datas_end = []
        if filter_objects_start.exists():
            filter_objects_start_values = filter_objects_start.values()
            for filter_value in filter_objects_start_values:
                filter_datas_start.append(filter_value)
        if filter_objects_end.exists():
            filter_objects_end_values = filter_objects_end.values()
            filter_datas_end = []
            for filter_value in filter_objects_end_values:
                filter_datas_end.append(filter_value)
        return JsonResponse(data={'success': True, 'data': {'start': filter_datas_start, 'end': filter_datas_end}})
    else:
        return JsonResponse(status=400, data={'success': False})


def get_schedules():
    schedule_list = []
    task_list = PeriodicTask.objects.filter(task='crawling').values()
    for task in task_list:
        crontab_id = task['crontab_id']
        crontab_info = CrontabSchedule.objects.filter(id=crontab_id).values()
        minute = crontab_info[0]['minute']
        schedule_dict = dict(id=task['id'], name=task['name'], minute=minute, last_run=task['last_run_at'],
                                 enabled=task['enabled'])
        schedule_list.append(schedule_dict)
    return schedule_list


# Schedule 생성, 조회, 삭제 API
@csrf_exempt
@require_http_methods(['POST', 'GET', 'DELETE'])
def schedules(request):
    # 스케줄 생성 요청
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')  # body값 추출
        body = json.loads(body_unicode)
        platform = body.get("platform")
        minutes = body.get("minutes")
        try:
            schedule, created = CrontabSchedule.objects.get_or_create(
                minute='{}'.format(minutes),
                timezone='Asia/Seoul',
            )
            # 존재하는 task는 상태 및 interval만 업데이트
            if PeriodicTask.objects.filter(name='{}_task'.format(platform)).exists():
                task = PeriodicTask.objects.get(name='{}_task'.format(platform))
                task.enabled=True
                task.crontab=schedule
                task.save()
                print('Save is done')
            else:
                PeriodicTask.objects.create(
                    crontab=schedule,
                    name='{}_task'.format(platform),
                    task='crawling',
                    args=json.dumps((platform,)),
                )
            return JsonResponse(data={'success': True})
        except Exception as e:
            return JsonResponse(status=400,  data={'error': str(e)})

    # 스케줄 리스트 업
    elif request.method == 'GET':
        try:
            if PeriodicTask.objects.filter(task='crawling').exists():
                schedule_list = get_schedules()
                return JsonResponse(data={'schedules': schedule_list})
            else:
                return JsonResponse(data={'schedules': []})
        except Exception as e:
            print(e)
            return JsonResponse(status=400, data={'error': str(e)})
    else:
        body_unicode = request.body.decode('utf-8')  # body값 추출
        body = json.loads(body_unicode)
        scheduleId = body.get("id")
        schedule = PeriodicTask.objects.get(id=scheduleId)
        schedule.delete()

        try:
            if PeriodicTask.objects.filter(task='crawling').exists():
                schedule_list = get_schedules()
                return JsonResponse(data={'schedules': schedule_list})
            else:
                return JsonResponse(data={'schedules': []})
        except Exception as e:
            print(e)
            return JsonResponse(status=400, data={'error': str(e)})
