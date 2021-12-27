from django.urls.conf import path
from dataprocess.views import base
from django.urls import path
from django.conf.urls import url
from dataprocess.views import *
from dataprocess import views

app_name = 'dataprocess'

urlpatterns = [
    path('', base ,name='base'),
    url(r'^daily$', daily ,name='daily'),
    url(r'^platforms$', views.Platform_all),
    url(r'^collectdatas$', views.CollectData_all),
    url(r'^collectdatas/(?P<pk>[0-9]+)$', views.CollectData_single),
    url(r'^artists$', views.ArtistView.as_view(),name='add_artist'),
    url(r'^artistprofiles$', views.ArtistProfileView.as_view(),name='artist_profile'),
    url(r'^collecttargets$', views.CollectTarget_all),
]