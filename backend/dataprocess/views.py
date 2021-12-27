from django.contrib.auth.models import Permission
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.renderers import HTMLFormRenderer, TemplateHTMLRenderer


# Create your views here.

def base(request):
    return render(request, 'dataprocess/main.html')

def daily(request):
    return render(request, 'dataprocess/daily.html')

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

class ArtistView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dataprocess/add_artist.html'

    def get(self, request):
        Artists = Artist.objects.all()
        
        serializer = ArtistSerializer(Artists, many=True)
        return Response({'serializer': serializer, 'artists': Artists})

    def post(self, request):
        Artists =Artist.objects.all()
        serializer = ArtistSerializer(Artists, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'artists':Artists})
        serializer.save()
        return redirect('dataprocess:base')


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
        profile = ArtistProfile.objects.all()
        serializer = ArtistProfileSerializer(data=request.data)
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