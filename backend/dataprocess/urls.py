from django.urls.conf import path
from dataprocess.views import base
from django.urls import path
from django.conf.urls import url
from dataprocess.views import *
from dataprocess import views

app_name = 'dataprocess'

urlpatterns = [
    path('', base ,name='base'),
    path('daily/',daily,name='daily'),
    path('platform/',platform,name='platform'),
    path('platform/platformread/', views.platform_read, name='platform_read'),
    path('platform/platformcreate', views.platform_create, name='platform_create'),
    path('platform/platformupdate', views.platform_update, name='platform_update'),
    path('artist/artistread/', views.artist_read, name='artist_read'),
    path('artist/platformread/', views.platforms_of_artist_read, name='platforms_of_artist_read'),
    path('artist/platformupdate', views.platforms_of_artist_update, name='platforms_of_artist_update'),
    path('artist/collectitemread/', views.collecttargetitems_read, name='collectitem_read'),
    path('artist/collectitemupdate', views.collecttargetitems_update, name='collectitem_update'),
    path('artist/artistcreate', views.artist_create, name='artist_create'),
    path('artist/artistupdate', views.artist_update, name='artist_update'),
]