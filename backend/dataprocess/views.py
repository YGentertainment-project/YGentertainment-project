from django.contrib.auth.models import Permission
from django.shortcuts import redirect, render
from django.urls import reverse
from django.urls.base import set_script_prefix
from rest_framework.renderers import HTMLFormRenderer, TemplateHTMLRenderer
from config.serializers import CollectTargetItemSerializer

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
    values = {
      'first_depth' : '플랫폼 관리',
      'second_depth': '플랫폼 관리'
    }
    return render(request, 'dataprocess/platform.html',values)

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

from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from config.models import CollectTargetItem


@api_view(['GET', 'POST'])
def Platform_all(request):
    # GET list of collect datas
    if request.method == 'GET':
        Platforms = Platform.objects.all()
        
        Platform_serializer = PlatformSerializer(Platforms, many=True)
        return JsonResponse(Platform_serializer.data, safe=False)
    
    # POST a new collect data
    elif request.method == 'POST':
        Platforms = JSONParser().parse(request)
        Platform_serializer = PlatformSerializer(data=Platforms)
        if Platform_serializer.is_valid():
            Platform_serializer.save()
            return JsonResponse(Platform_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(Platform_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'POST'])
def CollectData_all(request):
    # GET list of collect datas
    if request.method == 'GET':
        CollectDatas = CollectData.objects.all()
        
        CollectData_serializer = CollectDataSerializer(CollectDatas, many=True)
        return JsonResponse(CollectData_serializer.data, safe=False)
        #return render(request, "dataprocess/collect_data.html",{'collect_datas':CollectData_serializer.data, 'collect_data': CollectDatas})
    
    # POST a new collect data
    elif request.method == 'POST':
        CollectData_data = JSONParser().parse(request)
        CollectData_serializer = CollectDataSerializer(data=CollectData_data)
        if CollectData_serializer.is_valid():
            CollectData_serializer.save()
            return JsonResponse(CollectData_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(CollectData_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete all collect datas from db
    # elif request.method == 'DELETE':
    #     count = CollectData.objects.all().delete()
    #     return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

 
@api_view(['PUT', 'DELETE'])
def CollectData_single(request, pk):
    # find collect data by pk (id)
    try: 
        collectData = CollectData.objects.get(pk=pk)

        # # Find a single collect data with the specified id:
        # if request.method == 'GET': 
        #     CollectData_serializer = CollectDataSerializer(collectData)
        #     return JsonResponse(CollectData_serializer.data)

        # Update a single collect data with the specified id:
        if request.method == 'PUT':
            CollectData_data = JSONParser().parse(request)
            CollectData_serializer = CollectDataSerializer(collectData, data=CollectData_data) 
            if CollectData_serializer.is_valid():
                CollectData_serializer.save()
                return JsonResponse(CollectData_serializer.data) 
            return JsonResponse(CollectData_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

        # Delete a single collect data with the specified id:
        elif request.method == 'DELETE':
            collectData.delete()
            return JsonResponse({'message': 'CollectData was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except CollectData.DoesNotExist:
        return JsonResponse({'message': 'The CollectData does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def Artist_all(request):
    # GET list of collect datas
    if request.method == 'GET':
        Artists = Artist.objects.all()
        
        Artist_serializer = ArtistSerializer(Artists, many=True)
        return JsonResponse(Artist_serializer.data, safe=False)
    
    # POST a new collect data
    elif request.method == 'POST':
        Artists = JSONParser().parse(request)
        Artist_serializer = ArtistSerializer(data=Artists)
        if Artist_serializer.is_valid():
            Artist_serializer.save()
            return JsonResponse(Artist_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(Artist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete all collect datas from db
    # elif request.method == 'DELETE':
    #     count = CollectData.objects.all().delete()
    #     return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@renderer_classes((HTMLFormRenderer,))
def ArtistProfile_all(request):
    # GET list of collect datas
    if request.method == 'GET':
        ArtistProfiles = ArtistProfile.objects.all()
        
        ArtistProfile_serializer = ArtistProfileSerializer(ArtistProfiles, many=True)
        #return JsonResponse(ArtistProfile_serializer.data, safe=False)
        return render(request, "dataprocess/collect_data.html",{'serializer':ArtistProfile_serializer,'artists': ArtistProfiles})
    
    # POST a new collect data
    elif request.method == 'POST':
        ArtistProfiles_ = ArtistProfile.objects.all()
        ArtistProfiles = JSONParser().parse(request)
        ArtistProfile_serializer = ArtistProfileSerializer(data=ArtistProfiles)
        if ArtistProfile_serializer.is_valid():
            ArtistProfile_serializer.save()
            return redirect('dataprocess:artist_profile')
            #return JsonResponse(ArtistProfile_serializer.data, status=status.HTTP_201_CREATED) 
        return render(request, "dataprocess/collect_data.html",{'serializer':ArtistProfile_serializer,'artists': ArtistProfiles_})

class ArtistProfileView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dataprocess/collect_data.html'

    def get(self, request):
        profile =ArtistProfile.objects.all()
        serializer = ArtistProfileSerializer(profile)
        return Response({'serializer': serializer, 'artists': profile})

    def post(self, request):
        profile =ArtistProfile.objects.all()
        serializer = ArtistProfileSerializer(profile, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'artists': profile})
        serializer.save()
        return redirect('dataprocess:artist_profile')

@api_view(['GET', 'POST'])
def CollectTarget_all(request):
    # GET list of collect datas
    if request.method == 'GET':
        CollectTargets = CollectTarget.objects.all()
        
        CollectTarget_Serializer = CollectTargetSerializer(CollectTargets, many=True)
        return JsonResponse(CollectTarget_Serializer.data, safe=False)
    
    # POST a new collect data
    elif request.method == 'POST':
        CollectTargets = JSONParser().parse(request)
        CollectTarget_Serializer = CollectTargetSerializer(data=CollectTargets)
        if CollectTarget_Serializer.is_valid():
            CollectTarget_Serializer.save()
            return JsonResponse(CollectTarget_Serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(CollectTarget_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#======platform=======
#platform read
@csrf_exempt
@require_http_methods(['GET'])  # only get
def platform_read(request):
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

#platform create
@csrf_exempt
@require_http_methods(['POST'])  # only post
def platform_create(request):
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

#platform update
@csrf_exempt
@require_http_methods(['PUT'])  # only put
def platform_update(request):
    try:
        platform_list = JSONParser().parse(request)
        for platform_object in platform_list:
            platform_data = Platform.objects.get(pk=platform_object["id"])
            platform_serializer = PlatformSerializer(platform_data, data=platform_object)
            if platform_serializer.is_valid():
                platform_serializer.save()
            else:
                return JsonResponse(data={'success': False,'data': platform_serializer.errors}, status=400)
        return JsonResponse(data={'success': True}, status=status.HTTP_201_CREATED)
    except:
        return JsonResponse(data={'success': False}, status=400)


#======artist=======
#artist read
@csrf_exempt
@require_http_methods(['GET'])  # only get
def artist_read(request):
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

#artist-platform read
@csrf_exempt
@require_http_methods(['GET'])  # only get
def platforms_of_artist_read(request):
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
                    'id': collecttarget_value['id'],
                    'name': platform_object.name,
                    'target_url':collecttarget_value['target_url']
                })
            return JsonResponse(data={'success': True, 'data': platform_datas})
        else:
            return JsonResponse(data={'success': True, 'data': []})
    except:
        return JsonResponse(status=400, data={'success': False})


#artist-platform update
@csrf_exempt
@require_http_methods(['PUT'])  # only put
def platforms_of_artist_update(request):
    try:
        collecttarget_list = JSONParser().parse(request)
        for collecttarget_object in collecttarget_list:
            print(collecttarget_object['target_url'])
            CollectTarget.objects.filter(pk=collecttarget_object['id']).update(target_url=collecttarget_object['target_url'])
            print("ss")
        return JsonResponse(data={'success': True}, status=status.HTTP_201_CREATED)
    except:
        return JsonResponse(data={'success': False}, status=400)

#artist-platform-collecttargetitem read
@csrf_exempt
@require_http_methods(['GET'])  # only get
def collecttargetitems_read(request):
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

#artist-platform-collecttargetitem update
@csrf_exempt
@require_http_methods(['PUT'])  # only put
def collecttargetitems_update(request):
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

#artist create
@csrf_exempt
@require_http_methods(['POST'])  # only post
def artist_create(request):
    try:
        artist_object = JSONParser().parse(request)
        artist_serializer = ArtistSerializer(data=artist_object)
        if artist_serializer.is_valid():
            # 1. artist 생성
            artist_serializer.save()
            # 2. 현재 존재하는 모든 platform에 대해 collect_target 생성 -> artist와 연결
            platform_objects = Platform.objects.all()
            platform_objects_values = platform_objects.values()
            for index,platform_objects_value in enumerate(platform_objects_values):
                platform_target_url = artist_object['urls'][index]
                collecttarget = CollectTarget(
                    platform_id = platform_objects_value['id'],
                    artist_id = artist_serializer.data['id'],
                    target_url = platform_target_url
                )
                collecttarget.save()
            return JsonResponse(data={'success': True, 'data': artist_serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse(data={'success': False,'data': artist_serializer.errors }, status=400)
    except:
        return JsonResponse(data={'success': False}, status=400)


#artist update
@csrf_exempt
@require_http_methods(['PUT'])  # only put
def artist_update(request):
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