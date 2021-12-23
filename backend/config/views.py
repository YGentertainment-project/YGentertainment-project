from django.shortcuts import get_object_or_404, render

from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from config.serializers import PlatformSerializer

# Create your views here.
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