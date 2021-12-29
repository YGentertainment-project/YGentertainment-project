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
    url(r'^platforms$', views.Platform_all),
    url(r'^collectdatas$', views.CollectData_all),
    url(r'^collectdatas/(?P<pk>[0-9]+)$', views.CollectData_single),
    url(r'^artists$', views.Artist_all),
    url(r'^artistprofiles$', views.ArtistProfileView.as_view(),name='artist_profile'),
    url(r'^collecttargets$', views.CollectTarget_all),
    path('platform/platformread/', views.platform_read, name='platform_read'),
    path('platform/platformcreate', views.platform_create, name='platform_create'),
    path('platform/platformupdate', views.platform_update, name='platform_update'),
    path('artist/artistread/', views.artist_read, name='artist_read'),
    path('artist/artistcreate', views.artist_create, name='artist_create'),
    path('artist/artistupdate', views.artist_update, name='artist_update'),
]