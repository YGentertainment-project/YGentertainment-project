from django.urls.conf import path
from dataprocess.views import base

app_name = 'dataprocess'

urlpatterns = [
    path('base/', base ,name='base'),
]