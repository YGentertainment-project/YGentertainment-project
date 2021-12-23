from django.urls import path
from django.conf.urls import url
# from config.views import *
from config import views


app_name = 'config'

urlpatterns = [
    url(r'^platforms$', views.Platform_all),
]