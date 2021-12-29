from django.contrib.auth.models import Permission
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.renderers import HTMLFormRenderer, TemplateHTMLRenderer


# Create your views here.

def base(request):
    values = {
      'first_depth' : '데이터 리포트',
    }
    return render(request, 'config/main.html',values)

def daily(request):
    values = {
      'first_depth' : '데이터 리포트',
      'second_depth': '시간별 리포트'
    }
    return render(request, 'config/daily.html',values)