from django.urls.conf import path
from dataprocess.views import base
from django.urls import path
from django.conf.urls import url
from dataprocess.views import *
from dataprocess import views

app_name = 'dataprocess'

urlpatterns = [
    path('base/', base ,name='base'),
    url(r'^collectdatas$', views.CollectData_all),
    url(r'^collectdatas/(?P<pk>[0-9]+)$', views.CollectData_single),
    url(r'^artists$', views.Artist_all),
    url(r'^artistprofiles$', views.ArtistProfile_all),
    url(r'^collecttargets$', views.CollectTarget_all),
]