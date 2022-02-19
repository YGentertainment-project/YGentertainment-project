# 용도 : crawler 장고앱의 경로 설정
# 개발자 : 양승찬, uvzone@naver.com
# 최종수정일 : 2022-02-19

from django.conf import settings
from django.conf.urls import static
from django.urls import re_path, path
from django.views.generic import TemplateView
from crawler import views

app_name = "crawler"

# crawler앱 내부 경로 설정
urlpatterns = [
    re_path(r"^$", TemplateView.as_view(template_name="crawler.html"), name="home"),
    re_path(r"^api/crawl/", views.crawl, name="crawl"),
    re_path(r"^api/schedules/", views.schedules, name="schedules"),
    re_path(r"^api/taskinfos/", views.taskinfos, name="taskinfos"),
    re_path(r"^api/monitors/", views.monitors, name="monitors"),
    re_path(r"^api/showdata/", views.show_data, name="show_data"),
]

# static file 경로 설정
if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
