from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core import serializers
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.models import Socialblade
import json
import datetime

# process = CrawlerProcess(get_project_settings())

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')

@csrf_exempt
@require_http_methods(['POST', 'GET'])  # only get and post
def crawl(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':
        # unique_id = str(uuid4())  # create a unique ID.
        body = json.loads(request.body.decode('utf-8'))  # body값 추출
        platform = body.get("platform")
        settings = {
            # 'unique_id': unique_id,  # unique ID for each record for DB
            'platform': platform,
        }
        # POST 요청에서 보내는 platform 인자 값에 따라 동적으로 spider를 실행
        task = scrapyd.schedule('default', platform, settings=settings)
        # process.crawl(platform)
        # process.start()
        # return JsonResponse({'status': 'started'})
        return JsonResponse({'task_id': task, 'status': 'started'})

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

    if Socialblade.objects.filter(platform=platform).exists():
        platform_queryset_values = Socialblade.objects.filter(platform=platform).values()
        platform_datas = []
        for queryset_value in platform_queryset_values:
            platform_datas.append(queryset_value)
        return JsonResponse(data={'success': True, 'data': platform_datas})
    else:
        return JsonResponse(status=400, data={'success': False})


#daily read API
@csrf_exempt
@require_http_methods(['GET'])  # only get and post
def daily_read(request):
    platform = request.GET.get('platform', None)
    type = request.GET.get('type', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if type=="누적":
        start_date_dateobject = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        filter_objects = Socialblade.objects.filter(platform=platform, recorded_date__year=start_date_dateobject.year,
             recorded_date__month=start_date_dateobject.month, recorded_date__day=start_date_dateobject.day)
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
    elif type=="기간별":
        # 전날 값을 구함
        start_date_dateobject = datetime.datetime.strptime(start_date, '%Y-%m-%d').date() - datetime.timedelta(1)
        end_date_dateobject = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        filter_objects_start = Socialblade.objects.filter(platform=platform, recorded_date__year=start_date_dateobject.year,
             recorded_date__month=start_date_dateobject.month, recorded_date__day=start_date_dateobject.day)
        filter_objects_end = Socialblade.objects.filter(platform=platform, recorded_date__year=end_date_dateobject.year,
             recorded_date__month=end_date_dateobject.month, recorded_date__day=end_date_dateobject.day)
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
        return JsonResponse(data={'success': True, 'data': {'start':filter_datas_start, 'end':filter_datas_end}})
    else:
        if Socialblade.objects.filter(platform=platform).exists():
            platform_queryset_values = Socialblade.objects.filter(platform=platform).values()
            platform_datas = []
            for queryset_value in platform_queryset_values:
                platform_datas.append(queryset_value)
            return JsonResponse(data={'success': True, 'data': platform_datas})
        else:
            return JsonResponse(status=400, data={'success': False})