from django.contrib import auth
from django.contrib.auth.models import Permission
from django.shortcuts import redirect, render
from django.urls import reverse
from account.models import User
from dataprocess.functions import export_datareport, import_datareport, import_total
from crawler.models import *
from config.models import PlatformTargetItem
from config.serializers import PlatformTargetItemSerializer
from config.serializers import CollectTargetItemSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.shortcuts import render
from django.http import HttpResponse

import datetime
from tablib import Dataset
import openpyxl
from openpyxl.writer.excel import save_virtual_workbook
from .resources import *
from .models import *

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

# login check using cookie
def logincheck(request):
    # 로그인 정보를 받기 위해 cookie사용
    username = request.COOKIES.get('username')
    if username is not None:
        if User.objects.filter(username=username).exists():
            # 이미 존재하는 username일때만 로그인
            user = User.objects.filter(username=username).first()
            auth.login(request, user)
    return request

# Create your views here.
def base(request):
    values = {
      'first_depth' : '데이터 리포트',
    }
    request = logincheck(request)
    return render(request, 'dataprocess/main.html',values)

@csrf_exempt
def daily(request):
    if request.method == 'GET':
        '''
        general page
        '''
        platforms = Platform.objects.all() #get all platform info from db
        values = {
        'first_depth' : '데이터 리포트',
        'second_depth': '일별 리포트',
        'platforms': platforms
        }
        request = logincheck(request)
        return render(request, 'dataprocess/daily.html',values)
    else:
        type = request.POST['type']
        if type == 'import':
            '''
            import from excel
            '''
            import_file = request.FILES['importData']
            wb = openpyxl.load_workbook(import_file)
            sheets = wb.sheetnames
            worksheet = wb[sheets[0]]
            import_datareport(worksheet)
            platforms = Platform.objects.all() #get all platform info from db
            values = {
                'first_depth' : '데이터 리포트',
                'second_depth': '일별 리포트',
                'platforms': platforms
                }
            request = logincheck(request)
            return render(request, 'dataprocess/daily.html',values)
        elif type == 'export':
            '''
            export to excel
            '''
            book = export_datareport()
            today_date = datetime.datetime.today()
            filename = 'datareport%s-%s-%s.xlsx'%(today_date.year, today_date.month, today_date.day)
            response = HttpResponse(content=save_virtual_workbook(book), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename='+filename
            return response
        elif type == 'import2':
            '''
            import tmp from excel
            '''
            import_file = request.FILES['importData2']
            wb = openpyxl.load_workbook(import_file)
            sheets = wb.sheetnames
            worksheet = wb[sheets[0]]
            import_total(worksheet)
            platforms = Platform.objects.all() #get all platform info from db
            values = {
                'first_depth' : '데이터 리포트',
                'second_depth': '일별 리포트',
                'platforms': platforms
                }
            request = logincheck(request)
            return render(request, 'dataprocess/daily.html',values)

def platform(request):
    if request.method == 'GET':
        '''
        general page
        '''
        values = {
        'first_depth' : '플랫폼 관리',
        'second_depth': '플랫폼 관리'
        }
        request = logincheck(request)
        return render(request, 'dataprocess/platform.html',values)
    
    else:
        type = request.POST['type']
        if type == 'import':
            platform_resource = PlatformResource()
            dataset = Dataset()
            import_file = request.FILES['importData']
            wb = openpyxl.load_workbook(import_file)
            sheets = wb.sheetnames
            worksheet = wb[sheets[0]]
            excel_data = list()
            row_num = 0
            columns = []
            for row in worksheet.iter_rows():
                if row_num == 0:
                    for cell in row:
                        columns.append(str(cell.value))
                    row_num += 1
                    continue
                row_data = {}
                for i, cell in enumerate(row):
                    row_data[columns[i]] = str(cell.value)
                excel_data.append(row_data)
            values = {
                'first_depth' : '플랫폼 관리',
                'second_depth': '플랫폼 관리',
                'excel_data': excel_data
            }
            request = logincheck(request)
            return render(request, 'dataprocess/platform.html',values)
        elif type == 'export':
            platform_resource = PlatformResource()
            dataset = platform_resource.export()
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="platform_data.xlsx"'
            return response

def artist(request):
    artists = Artist.objects.all()
    values = {
      'first_depth' : '아티스트 관리',
      'second_depth': '데이터 URL 관리',
      'artists': artists
    }
    request = logincheck(request)
    return render(request, 'dataprocess/artist.html',values)

@csrf_exempt
def artist_add(request):
    platforms = Platform.objects.all()
    values = {
      'first_depth' : '아티스트 관리',
      'second_depth': '데이터 URL 관리',
      'platforms' : platforms
    }
    request = logincheck(request)
    return render(request, 'dataprocess/artist_add.html',values)

def login(request):
    values = {
      'first_depth' : '로그인'
    }
    request = logincheck(request)
    return render(request, 'dataprocess/login.html',values)

def platform_info(request):
    if request.method == 'GET':
        platform = request.GET.get('platform', None)
        try:
            platform_objects = Platform.objects.get(name = platform)
            
            if platform_objects.exists():
                platform_objects_values = platform_objects.values()
                platform_collect_items = PlatformTargetItem.objects.filter(platform_id = platform_objects_values['id'])
                platform_datas = []
                for platform_item in platform_collect_items:
                    platform_datas.append(platform_item)
                return JsonResponse(data={'success': True, 'data': platform_datas})
            else:
                return JsonResponse(data={'success': True, 'data': []})
        except:
            return JsonResponse(status=400, data={'success': False})


from .serializers import *
from .models import *
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from config.models import CollectTargetItem
from utils.decorators import login_required
from utils.api import APIView, validate_serializer


class PlatformAPI(APIView):
    # @login_required
    def get(self, request):
        """
        Platform read api
        """
        try:
            platform_objects = Platform.objects.all()
            if platform_objects.exists():
                platform_objects_values = platform_objects.values()
                platform_datas = []
                for platform_value in platform_objects_values:
                    platform_datas.append(platform_value)
                return JsonResponse(data={'success': True, 'data': platform_datas})
            else:
                return JsonResponse(data={'success': True, 'data': []})
        except:
            return JsonResponse(status=400, data={'success': False})

    # @login_required
    def post(self, request):
        """
        Platform create api
        """
        try:
            platform_object = JSONParser().parse(request)
            platform_serializer = PlatformSerializer(data=platform_object)
            if platform_serializer.is_valid():
                # 1. platform 생성
                platform_serializer.save()

                #특정 아티스트 전용 collect_target 생성 시 사용할 코드
                # 2. 현재 존재하는 모든 artist에 대해 collect_target 생성 -> platform과 연결
                artist_objects = Artist.objects.all()
                artist_objects_values = artist_objects.values()
                for artist_objects_value in artist_objects_values:
                    collecttarget = CollectTarget(
                        platform_id = platform_serializer.data['id'],
                        artist_id = artist_objects_value['id']
                        )
                    collecttarget.save()
                
                #3. 플랫폼에 대한 platform target 생성
                for collect_item in platform_object['collect_items']:
                    collect_item = PlatformTargetItem(
                        platform_id = platform_serializer.data['id'],
                        target_name = collect_item
                    )
                    collect_item.save()

                return JsonResponse(data={'success': True, 'data': platform_serializer.data}, status=status.HTTP_201_CREATED)
            return JsonResponse(data={'success': False,'data': platform_serializer.errors}, status=400)
        except:
            return JsonResponse(data={'success': False}, status=400)

    # @login_required
    def put(self, request):
        """
        Platform update api
        """
        try:
            platform_list = JSONParser().parse(request)
            for platform_object in platform_list:
                platform_data = Platform.objects.filter(pk=platform_object["id"]).first()
                if platform_data is None:
                    # 원래 없는 건 새로 저장
                    platform_serializer = PlatformSerializer(data=platform_object)
                    if platform_serializer.is_valid():
                        platform_serializer.save()
                else:
                    platform_serializer = PlatformSerializer(platform_data, data=platform_object)
                    if platform_serializer.is_valid():
                        platform_serializer.save()
            return JsonResponse(data={'success': True}, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse(data={'success': False}, status=400)

class ArtistAPI(APIView):
    # @login_required
    def get(self, request):
        """
        Artist read api
        """
        try:
            artist_objects = Artist.objects.all()
            if artist_objects.exists():
                artist_objects_values = artist_objects.values()
                artist_datas = []
                for artist_value in artist_objects_values:
                    artist_datas.append(artist_value)
                return JsonResponse(data={'success': True, 'data': artist_datas})
            else:
                return JsonResponse(data={'success': True, 'data': []})
        except:
            return JsonResponse(status=400, data={'success': False})

    # @login_required
    def post(self, request):
        """
        Artist create api
        """
        try:
            artist_object = JSONParser().parse(request)
            artist_serializer = ArtistSerializer(data=artist_object)
            if artist_serializer.is_valid():
                # 1. artist 생성
                artist_serializer.save()
                # 2. 현재 존재하는 모든 platform에 대해 collect_target 생성 -> artist와 연결
                platform_objects = Platform.objects.all()
                platform_objects_values = platform_objects.values()
                
                url_index = 0

                for platform_objects_value in platform_objects_values:
                    platform_target_url = artist_object['urls'][url_index]
                    platform_target_url_2 = artist_object['urls'][url_index+1]
                    url_index += 2
                    collecttarget = CollectTarget(
                        platform_id = platform_objects_value['id'],
                        artist_id = artist_serializer.data['id'],
                        target_url = platform_target_url,
                        target_url_2 = platform_target_url_2
                    )
                    collecttarget.save()
    
                return JsonResponse(data={'success': True, 'data': artist_serializer.data}, status=status.HTTP_201_CREATED)
            return JsonResponse(data={'success': False,'data': artist_serializer.errors}, status=400)
        except:
            return JsonResponse(data={'success': False}, status=400)

    # @login_required
    def put(self, request):
        """
        Artist update api
        """
        try:
            artist_list = JSONParser().parse(request)
            for artist_object in artist_list:
                artist_data = Artist.objects.get(pk=artist_object["id"])
                artist_serializer = ArtistSerializer(artist_data, data=artist_object)
                if artist_serializer.is_valid():
                    artist_serializer.save()
                else:
                    return JsonResponse(data={'success': False,'data': artist_serializer.errors}, status=400)
            return JsonResponse(data={'success': True}, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse(data={'success': False}, status=400)


class PlatformOfArtistAPI(APIView):
    # @login_required
    def get(self, request):
        """
        Platform of Artist read api
        """
        try:
            artist = request.GET.get('artist', None)
            # 해당 artist 찾기
            artist_object = Artist.objects.filter(name = artist)
            artist_object = artist_object.values()[0]
            # 해당 artist를 가지는 collect_target들 가져오기
            collecttarget_objects = CollectTarget.objects.filter(artist_id=artist_object['id'])
            if collecttarget_objects.exists():
                collecttarget_objects_values = collecttarget_objects.values()
                platform_datas = []
                for collecttarget_value in collecttarget_objects_values:
                    platform_object = Platform.objects.get(pk=collecttarget_value['platform_id'])
                    platform_datas.append({
                        'artist_id':artist_object['id'],
                        'platform_id' : collecttarget_value['platform_id'],
                        'id': collecttarget_value['id'],
                        'name': platform_object.name,
                        'target_url':collecttarget_value['target_url'],
                        'target_url_2': collecttarget_value['target_url_2']
                    })
                return JsonResponse(data={'success': True, 'data': platform_datas})
            else:
                return JsonResponse(data={'success': True, 'data': []})
        except:
            return JsonResponse(status=400, data={'success': False})

    # @login_required
    def put(self, request):
        """
        Platform of Artist update api
        """
        try:
            collecttarget_list = JSONParser().parse(request)
            for collecttarget_object in collecttarget_list:
                print(collecttarget_object['target_url'])
                CollectTarget.objects.filter(pk=collecttarget_object['id']).update(target_url=collecttarget_object['target_url'])
                if collecttarget_object['target_url_2']:
                     CollectTarget.objects.filter(pk=collecttarget_object['id']).update(target_url_2=collecttarget_object['target_url_2'])
            return JsonResponse(data={'success': True}, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse(data={'success': False}, status=400)


class CollectTargetItemAPI(APIView):
    # @login_required
    def get(self, request):
        """
        CollectTargetItem read api
        """
        try:
            artist = request.GET.get('artist', None)
            platform = request.GET.get('platform', None)
            # 해당 artist,platform 찾기
            artist_object = Artist.objects.filter(id = artist)
            artist_object = artist_object.values()[0]
            platform_object = Platform.objects.filter(name = platform)
            platform_object = platform_object.values()[0]
            # 해당 artist와 platform을 가지는 collect_target 가져오기
            collecttarget_objects = CollectTarget.objects.filter(artist_id=artist_object['id'], platform_id = platform_object['id'])
            if collecttarget_objects.exists():
                collecttargetitems_datas = []
                collecttarget_objects_value = collecttarget_objects.values()[0]
                collecttargetitmes_objects = CollectTargetItem.objects.filter(collect_target_id=collecttarget_objects_value['id'])
                collecttargetitmes_values = collecttargetitmes_objects.values()
                for collecttargetitmes_value in collecttargetitmes_values:
                    collecttargetitems_datas.append(collecttargetitmes_value)
                return JsonResponse(data={'success': True, 'data': collecttargetitems_datas})
            else:
                return JsonResponse(data={'success': True, 'data': []})
        except:
            return JsonResponse(status=400, data={'success': False})

    # @login_required
    def put(self, request):
        """
        CollectTargetItem update api
        """
        try:
            collecttargetitem_list = JSONParser().parse(request)
            for collecttargetitem_object in collecttargetitem_list:
                collecttargetitem_data = CollectTargetItem.objects.get(pk=collecttargetitem_object["id"])
                collecttargetitem_serializer = CollectTargetItemSerializer(collecttargetitem_data, data=collecttargetitem_object)
                if collecttargetitem_serializer.is_valid():
                    collecttargetitem_serializer.save()
                else:
                    return JsonResponse(data={'success': False,'data': collecttargetitem_serializer.errors}, status=400)
            return JsonResponse(data={'success': True}, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse(data={'success': False}, status=400)

#platform collect target API 
class PlatformTargetItemAPI(APIView):
    # @login_required
    def get(self, request):
        """
        PlatformTargetItem read api
        """
        try:
            platform = request.GET.get('platform', None)
            # 해당 platform 찾기
            platform_object = Platform.objects.filter(name = platform)
            platform_object = platform_object.values()[0]
            # 해당 platform을 가지는 platform_target 가져오기
            collecttarget_objects = PlatformTargetItem.objects.filter(platform_id = platform_object['id'])
            if collecttarget_objects.exists():
                collecttargetitems_datas = []
                collecttarget_objects_value = collecttarget_objects.values()[0]
                collecttargetitmes_objects = PlatformTargetItem.objects.filter(platform_id=collecttarget_objects_value['platform_id'])
                collecttargetitmes_values = collecttargetitmes_objects.values()
                for collecttargetitmes_value in collecttargetitmes_values:
                    collecttargetitems_datas.append(collecttargetitmes_value)
                return JsonResponse(data={'success': True, 'data': collecttargetitems_datas,'platform_id':collecttarget_objects_value['platform_id']})
            else:
                return JsonResponse(data={'success': True, 'data': []})
        except:
            return JsonResponse(status=400, data={'success': False})

    # @login_required
    def put(self, request):
        """
        PlatformTargetItem update api
        """
        try:
            collecttargetitem_list = JSONParser().parse(request)
            for i,collecttargetitem_object in enumerate(collecttargetitem_list):
                collecttargetitem_data = PlatformTargetItem.objects.filter(platform_id=collecttargetitem_object["platform"])[i]
                collecttargetitem_serializer = PlatformTargetItemSerializer(collecttargetitem_data, data=collecttargetitem_object)
                if collecttargetitem_serializer.is_valid():
                    collecttargetitem_serializer.save()
                else:
                    return JsonResponse(data={'success': False,'data': collecttargetitem_serializer.errors}, status=400)
            return JsonResponse(data={'success': True}, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse(data={'success': False}, status=400)


class DataReportAPI(APIView):
    def get(self, request):
        """
        Data-Reponrt read api
        """
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
                artist_objects = Artist.objects.all()
                artist_objects_values = artist_objects.values()
                filter_datas=[]
                artist_datas = []
                for filter_value in filter_objects_values:
                    filter_datas.append(filter_value)
                for artist in artist_objects_values:
                    artist_datas.append(artist)
                return JsonResponse(data={'success': True, 'data': filter_datas,'artists':artist_datas})
            else:
                return JsonResponse(status=400, data={'success': True, 'data': []})
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
    
    def post(self, request):
        """
        Data-Report update api
        """
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

        for index, artist in enumerate(artists):
            obj = DataModels[platform].objects.filter(artist=artist)
            if platform == 'youtube':
                obj.update(uploads=uploads[index], subscribers=subscribers[index], views=views[index])
            elif platform == 'vlive':
                obj.update(members=members[index], videos=videos[index], likes=likes[index], plays=plays[index])
            elif platform == 'instagram' or platform == 'facebook':
                obj.update(followers=followers[index])
            elif platform == 'twitter' or platform == 'twitter2':
                obj.update(followers=followers[index], twits=twits[index])
            elif platform == 'tiktok':
                obj.update(followers=followers[index], uploads=uploads[index], likes=likes[index])
            elif platform == 'weverse':
                obj.update(weverses=weverses[index])
        platform_queryset_values = DataModels[platform].objects.values()
        platform_datas = []
        for queryset_value in platform_queryset_values:
            platform_datas.append(queryset_value)
        return JsonResponse(data={'success': True, 'data': platform_datas})
