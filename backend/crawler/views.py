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
from crawler.models import SocialbladeItem
import json

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

    if SocialbladeItem.objects.filter(platform=platform).exists():
        platform_queryset_values = SocialbladeItem.objects.filter(platform=platform).values()
        platform_datas = []
        for queryset_value in platform_queryset_values:
            platform_datas.append(queryset_value)
        return JsonResponse(data={'success': True, 'data': platform_datas})
    else:
        return JsonResponse(status=400, data={'success': False})
