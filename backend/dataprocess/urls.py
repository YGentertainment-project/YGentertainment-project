from django.urls.conf import path
from dataprocess.views import base
from django.urls import path
from django.conf.urls import url
from dataprocess.views import *
from dataprocess import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'dataprocess'

urlpatterns = [
    path('', base ,name='base'),
    path('daily/',daily,name='daily'),
    path('platform/',platform,name='platform'),
    path('artist/',artist,name='artist'),
    path('artist/add/',artist_add,name='artist_add'),
    path('login/',login,name='login'),

    path('api/daily/', csrf_exempt(views.DataReportAPI.as_view()), name='datareport_api'),
    path('api/platform/', csrf_exempt(views.PlatformAPI.as_view()), name='platform_api'),
    path('api/artist/', csrf_exempt(views.ArtistAPI.as_view()), name='artist_api'),
    path('api/platform_of_artist/', csrf_exempt(views.PlatformOfArtistAPI.as_view()), name='platform_of_artist_api'),
    path('api/collect_target_item/', csrf_exempt(views.CollectTargetItemAPI.as_view()), name='collect_target_item_api'),
    path('api/platform_target_item/', csrf_exempt(views.PlatformTargetItemAPI.as_view()), name='platform_target_item_api'),
]