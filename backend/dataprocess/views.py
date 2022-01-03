from django.contrib.auth.models import Permission
from django.shortcuts import redirect, render
from django.urls import reverse
from config.serializers import CollectTargetItemSerializer

from django.shortcuts import render
from django.http import HttpResponse

from tablib import Dataset
import openpyxl
from .resources import *
from .models import *

# Create your views here.
def base(request):
    values = {
      'first_depth' : '데이터 리포트',
    }
    return render(request, 'dataprocess/main.html',values)

def daily(request):
    values = {
      'first_depth' : '데이터 리포트',
      'second_depth': '시간별 리포트'
    }
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
        return render(request, 'dataprocess/platform.html',values)
    
    else:
        type = request.POST['type']
        if type == 'import':
            if request.method == 'POST':
                platform_resource = PlatformResource()
                dataset = Dataset()
                import_file = request.FILES['importData']
                wb = openpyxl.load_workbook(import_file)
                sheets = wb.sheetnames
                worksheet = wb[sheets[0]]
                excel_data = list()
                # iterating over the rows and
                # getting value from each cell in row
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
                # imported_data = dataset.load(import_file.read().decode('ISO-8859-1'), format='xls')
                # file 확장명 보고 file_format 유추
                # file_format = request.POST['file-format']
                # file_format = import_file.name.split(".")
                # file_format = file_format[-1]
                # result = platform_resource.import_data(dataset, dry_run=True)
                # 어차피 excel로만 받아올거라 밑에 주석처리함 -> 나중에 나눌거면 주석해제
                # if file_format == 'csv':
                #     result = platform_resource.import_data(dataset, dry_run=True)                                                                 
                # elif file_format == 'json':
                #     result = platform_resource.import_data(dataset, dry_run=True) 
                # elif file_format == 'xlsx':
                #     result = platform_resource.import_data(dataset, dry_run=True)
                # if not result.has_errors():
                #     platform_resource.import_data(dataset, dry_run=False)
                values = {
                    'first_depth' : '플랫폼 관리',
                    'second_depth': '플랫폼 관리',
                    'excel_data': excel_data
                }
                return render(request, 'dataprocess/platform.html',values)
        elif type == 'export':
            platform_resource = PlatformResource()
            dataset = platform_resource.export()
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="platform_data.xlsx"'
            return response
            # 어차피 excel(xlsx)로만 저장할거라 밑에 주석처리함 -> 나중에 나눌거면 주석해제
            # file_format = request.POST['file-format']
            # if file_format == 'CSV':
            #     response = HttpResponse(dataset.csv, content_type='text/csv')
            #     response['Content-Disposition'] = 'attachment; filename="platform_data.csv"'
            #     return response        
            # elif file_format == 'JSON':
            #     response = HttpResponse(dataset.json, content_type='application/json')
            #     response['Content-Disposition'] = 'attachment; filename="platform_data.json"'
            #     return response
            # elif file_format == 'XLSX (Excel)':
            #     response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            #     response['Content-Disposition'] = 'attachment; filename="platform_data.xlsx"'
            #     return response

def artist(request):
    artists = Artist.objects.all()
    values = {
      'first_depth' : '아티스트 관리',
      'second_depth': '데이터 URL 관리',
      'artists':artists,
    }
    return render(request, 'dataprocess/artist.html',values)
def artist_add(request):
    platforms = Platform.objects.all()
    values = {
      'first_depth' : '아티스트 관리',
      'second_depth': '데이터 URL 관리',
      'platforms' : platforms
    }
    return render(request, 'dataprocess/artist_add.html',values)



from rest_framework.views import APIView
from .serializers import *
from .models import *
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from config.models import CollectTargetItem
from utils.decorators import login_required
from utils.api import APIView, validate_serializer

#======platform=======
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
                # 2. 현재 존재하는 모든 artist에 대해 collect_target 생성 -> platform과 연결
                artist_objects = Artist.objects.all()
                artist_objects_values = artist_objects.values()
                for artist_objects_value in artist_objects_values:
                    collecttarget = CollectTarget(
                        platform_id = platform_serializer.data['id'],
                        artist_id = artist_objects_value['id']
                        )
                    collecttarget.save()
                    # 3. collect_target_item들 생성 -> collect_target과 연결
                    for collect_item in platform_object['collect_items']:
                        collect_item = CollectTargetItem(
                            collect_target_id=collecttarget.id,
                            target_name=collect_item
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
                    platform = Platform(
                        name = platform_object["name"],
                        url = platform_object["url"],
                        description = platform_object["description"],
                        active = platform_object["active"])
                    platform.save()
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
                for platform_objects_value in platform_objects_values:
                    if artist_object['target_urls'].get(platform_objects_value['name']):
                        platform_target_url = artist_object['target_urls'][platform_objects_value['name']]
                    else:
                        platform_target_url = ""
                    collecttarget = CollectTarget(
                        platform_id = platform_objects_value['id'],
                        artist_id = artist_serializer.data['id'],
                        target_url = platform_target_url
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
                        'id': collecttarget_value['id'],
                        'name': platform_object.name,
                        'target_url':collecttarget_value['target_url']
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
                print("ss")
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
            artist_object = Artist.objects.filter(name = artist)
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
