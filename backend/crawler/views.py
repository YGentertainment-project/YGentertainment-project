import json

# api utilities
from uuid import uuid4
from urllib.parse import urlparse
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from dataprocess.models import Artist

# crawler models
from crawler.models import SocialbladeYoutube, SocialbladeTiktok, SocialbladeTwitter, SocialbladeTwitter2, \
    Weverse, CrowdtangleInstagram, CrowdtangleFacebook, Vlive, Melon, Spotify

# django_celery_beat models
from django_celery_beat.models import PeriodicTask, CrontabSchedule


# celery
from .tasks import crawling_platform
from .celery import app
from celery.result import AsyncResult

# data models
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


@csrf_exempt
@require_http_methods(['POST', 'GET'])  # only get and post
def crawl(request):
    # 새로운 Task를 생성하는 POST 요청
    if request.method == 'POST':
        unique_id = str(uuid4())  # create a unique ID.
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)  # body값 추출
        platform = body.get("platform")

        task = crawling_platform.apply_async(args=[platform])
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
    if DataModels[platform].objects.exists():
        platform_queryset_values = DataModels[platform].objects.values()
        platform_datas = []
        for queryset_value in platform_queryset_values:
            platform_datas.append(queryset_value)
        return JsonResponse(data={'success': True, 'data': platform_datas})
    else:
        return JsonResponse(status=400, data={'success': False})


def get_schedules():
    schedule_list = []
    task_list = PeriodicTask.objects.values()
    for task in task_list:
        if('crawling' in task['name']):
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
            if PeriodicTask.objects.filter(name='{}_crawling'.format(platform)).exists():
                task = PeriodicTask.objects.get(name='{}_crawling'.format(platform))
                task.enabled = True
                task.crontab = schedule
                task.save()
            else:
                PeriodicTask.objects.create(
                    crontab=schedule,
                    name='{}_crawling'.format(platform),
                    task='{}_crawling'.format(platform),
                    # args=json.dumps((platform,)),
                )
            return JsonResponse(data={'success': True})
        except Exception as e:
            return JsonResponse(status=400,  data={'error': str(e)})
    # 스케줄 리스트 업
    elif request.method == 'GET':
        try:
            schedule_list = get_schedules()
            return JsonResponse(data={'schedules': schedule_list})
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
            schedule_list = get_schedules()
            return JsonResponse(data={'schedules': schedule_list})
        except Exception as e:
            print(e)
            return JsonResponse(status=400, data={'error': str(e)})


# @csrf_exempt
# @require_http_methods(['POST'])  # only post
# def daily_update(request):
#     platform = request.POST.get('platform_name', None)
#     artists = request.POST.getlist('artists[]')
#     uploads = request.POST.getlist('uploads[]')
#     subscribers = request.POST.getlist('subscribers[]')
#     views = request.POST.getlist('views[]')
#     members = request.POST.getlist('members[]')
#     videos = request.POST.getlist('videos[]')
#     likes = request.POST.getlist('likes[]')
#     plays = request.POST.getlist('plays[]')
#     followers = request.POST.getlist('followers[]')
#     twits = request.POST.getlist('twits[]')
#     weverses = request.POST.getlist('weverses[]')

#     for index, artist in enumerate(artists):
#         obj = DataModels[platform].objects.filter(artist=artist)
#         if platform == 'youtube':
#             obj.update(uploads=uploads[index], subscribers=subscribers[index], views=views[index])
#         elif platform == 'vlive':
#             obj.update(members=members[index], videos=videos[index], likes=likes[index], plays=plays[index])
#         elif platform == 'instagram' or platform == 'facebook':
#             obj.update(followers=followers[index])
#         elif platform == 'twitter' or platform == 'twitter2':
#             obj.update(followers=followers[index], twits=twits[index])
#         elif platform == 'tiktok':
#             obj.update(followers=followers[index], uploads=uploads[index], likes=likes[index])
#         elif platform == 'weverse':
#             obj.update(weverses=weverses[index])
#     platform_queryset_values = DataModels[platform].objects.values()
#     platform_datas = []
#     for queryset_value in platform_queryset_values:
#         platform_datas.append(queryset_value)
#     return JsonResponse(data={'success': True, 'data': platform_datas})
