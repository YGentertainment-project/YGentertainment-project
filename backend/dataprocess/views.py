from django.shortcuts import render

# Create your views here.


from django.shortcuts import render

# Create your views here.

def base(request):
    return render(request, 'dataprocess/main.html')

from django.shortcuts import get_object_or_404, render

from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

# class CollectDataListAPIView(APIView):
#     # GET list of collect datas
#     def get(self, request):
#         CollectDatas = CollectData.objects.all()
        
#         CollectData_serializer = CollectDataSerializer(CollectDatas, many=True)
#         return JsonResponse(CollectData_serializer.data, safe=False)

#     # POST a new collect data
#     def post(self, request):
#         CollectData_data = JSONParser().parse(request)
#         CollectData_serializer = CollectDataSerializer(data=CollectData_data)
#         if CollectData_serializer.is_valid():
#             CollectData_serializer.save()
#             return JsonResponse(CollectData_serializer.data, status=status.HTTP_201_CREATED) 
#         return JsonResponse(CollectData_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CollectDataDetailAPIView(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(CollectData, pk=pk)

#     # Update a single collect data with the specified id:
#     def put(self, request, pk):
#         try:
#             collectData = self.get_object(pk=pk)
#             CollectData_data = JSONParser().parse(request)
#             CollectData_serializer = CollectDataSerializer(collectData, data=CollectData_data) 
#             if CollectData_serializer.is_valid():
#                 CollectData_serializer.save()
#                 return JsonResponse(CollectData_serializer.data) 
#             return JsonResponse(CollectData_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
#         except CollectData.DoesNotExist:
#             return JsonResponse({'message': 'The CollectData does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
#      # Delete a single collect data with the specified id:
#     def delete(self, request, pk):
#         try:
#             collectData = CollectData.objects.get(pk=pk)
#             collectData.delete()
#             return JsonResponse({'message': 'CollectData was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
#         except CollectData.DoesNotExist:
#             return JsonResponse({'message': 'The CollectData does not exist'}, status=status.HTTP_404_NOT_FOUND)
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
def ArtistProfile_all(request):
    # GET list of collect datas
    if request.method == 'GET':
        ArtistProfiles = ArtistProfile.objects.all()
        
        ArtistProfile_serializer = ArtistProfileSerializer(ArtistProfiles, many=True)
        return JsonResponse(ArtistProfile_serializer.data, safe=False)
    
    # POST a new collect data
    elif request.method == 'POST':
        ArtistProfiles = JSONParser().parse(request)
        ArtistProfile_serializer = ArtistProfileSerializer(data=ArtistProfiles)
        if ArtistProfile_serializer.is_valid():
            ArtistProfile_serializer.save()
            return JsonResponse(ArtistProfile_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(ArtistProfile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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