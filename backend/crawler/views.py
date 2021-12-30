from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core import serializers
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI

from crawler.models import SocialbladeYoutube, SocialbladeTiktok, SocialbladeTwitter, SocialbladeTwitter2, \
    Weverse, CrowdtangleInstagram, CrowdtangleFacebook, Vlive, Melon, Spotify
import json
import os
import datetime

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')


def start_crawl(platform, id):
    os.system('python manage.py {} {}'.format(platform, id))


@csrf_exempt
@require_http_methods(['POST', 'GET'])  # only get and post
def crawl(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':
        unique_id = str(uuid4())  # create a unique ID.
        body = json.loads(request.body.decode('utf-8'))  # body값 추출
        platform = body.get("platform")
        task = scrapyd.schedule('default', spider=platform)
        # start_crawl(platform, unique_id)
        return JsonResponse({'task_id': task, 'status': 'started'})
        # return JsonResponse({'task_id': unique_id, 'status': 'started'})

    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':
        task_id = request.GET.get('task_id', None)
        # unique_id = request.GET.get('unique_id', None)
        # if not task_id or not unique_id:
        if not task_id:
            return JsonResponse(status=400, data={'error': 'Missing args'})
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                return JsonResponse({'status': 'finish'})
            except Exception as e:
                return JsonResponse(status=400, data={'error': str(e)})
        else:
            return JsonResponse({'status': 'onprogress'})


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
        start_date_dateobject = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        filter_objects = DataModels[platform].objects.filter(recorded_date__year=start_date_dateobject.year,
             recorded_date__month=start_date_dateobject.month, recorded_date__day=start_date_dateobject.day)
        if filter_objects.exists():
            filter_objects_values=filter_objects.values()
            filter_datas=[]
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
        start_date_dateobject=datetime.datetime.strptime(start_date, '%Y-%m-%d').date() - datetime.timedelta(1)
        end_date_dateobject=datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        filter_objects_start=DataModels[platform].objects.filter(recorded_date__year=start_date_dateobject.year,
             recorded_date__month=start_date_dateobject.month, recorded_date__day=start_date_dateobject.day)
        filter_objects_end=DataModels[platform].objects.filter(recorded_date__year=end_date_dateobject.year,
             recorded_date__month=end_date_dateobject.month, recorded_date__day=end_date_dateobject.day)
        filter_datas_total=[]
        if filter_objects_start.exists() and filter_objects_end.exists():
            filter_objects_start_values=filter_objects_start.values()

            model_fields = DataModels[platform]._meta.fields
            model_fields_name = []
            artist_datas = set()
            
            for model_field in model_fields:
                model_fields_name.append(model_field.name)
            values_len = len(filter_objects_start_values)

            for i in range(values_len):
                # 이미 넣은 데이터면 pass
                if filter_objects_start_values[i]["artist"] in artist_datas:
                    continue
                artist_datas.add(filter_objects_start_values[i]["artist"])
                # id랑 artist, date 빼고 보내주기
                data_json = {}
                # 현재 보고 있는 거랑 맞는 끝 날짜를 가져오기
                filter_artist_end=DataModels[platform].objects.filter(recorded_date__year=end_date_dateobject.year,
                    recorded_date__month=end_date_dateobject.month, recorded_date__day=end_date_dateobject.day,
                    artist = filter_objects_start_values[i]["artist"])
                filter_artist_end = filter_artist_end.values()
                if not filter_artist_end.exists():
                    continue
                filter_artist_end = filter_artist_end[0]
                for field_name in model_fields_name:
                    if field_name != "id" and field_name != "artist" and field_name != "user_created" and field_name != "recorded_date" and field_name != "platform" and field_name != "url" :
                        data_json[field_name] = filter_artist_end[field_name] - filter_objects_start_values[i][field_name]
                    else:
                        data_json[field_name] = filter_objects_start_values[i][field_name]
                filter_datas_total.append(data_json)
            return JsonResponse(data={'success': True, 'data': filter_datas_total})
    else:
        if DataModels[platform].objects.exists():
            platform_queryset_values = DataModels[platform].objects.values()
            platform_datas = []
            for queryset_value in platform_queryset_values:
                platform_datas.append(queryset_value)
            return JsonResponse(data={'success': True, 'data': platform_datas})
        else:
            return JsonResponse(status=400, data={'success': False})


@csrf_exempt
@require_http_methods(['POST'])  # only get and post
def daily_update(request):
    platform = request.POST.get('platform_name', None)
    artists = request.POST.getlist('artists[]')
    uploads = request.POST.getlist('uploads[]')
    subscribers = request.POST.getlist('subscribers[]')
    views = request.POST.getlist('views[]')
    members = request.POST.getlist('members[]')
    videos = request.POST.getlist('videos[]')
    likes = request.POST.getlist('likes[]')
    plays = request.POST.getlist('plays[]')
    followers = request.POST.getlist('followers[]')
    twits = request.POST.getlist('twits[]')
    weverses = request.POST.getlist('weverses[]')


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

    for index,artist in enumerate(artists):
        obj = DataModels[platform].objects.filter(artist=artist)
        if platform == 'youtube':
            obj.update(uploads=uploads[index],subscribers=subscribers[index],views=views[index])
        elif platform == 'vlive':
            obj.update(members=members[index],videos=videos[index],likes=likes[index],plays=plays[index])
        elif platform == 'instagram' or platform=='facebook':
            obj.update(followers = followers[index])
        elif platform == 'twitter' or platform=='twitter2':
            obj.update(followers = followers[index],twits=twits[index])
        elif platform == 'tiktok':
            obj.update(followers = followers[index],uploads=uploads[index],likes=likes[index])
        elif platform == 'weverse':
            obj.update(weverses= weverses[index])
    platform_queryset_values = DataModels[platform].objects.values()
    platform_datas = []
    for queryset_value in platform_queryset_values:
        platform_datas.append(queryset_value)
    return JsonResponse(data={'success': True, 'data': platform_datas})
