
from django.conf import settings
from django.conf.urls import static
from django.urls import re_path, path
from django.views.generic import TemplateView

from crawler import views

app_name = "crawler"

urlpatterns = [
    re_path(r"^$", TemplateView.as_view(template_name="socialblade.html"), name="home"),
    re_path(r"^api/crawl/", views.crawl, name="crawl"),
    re_path(r"^api/schedules/", views.schedules, name="schedules"),
    re_path(r"^api/taskinfos/", views.taskinfos, name="taskinfos"),
    re_path(r"^api/monitors/", views.monitors, name="monitors"),
    # re_path(r"^api/scheduletasks/", views.scheduletasks, name="scheduletasks"),
    path("api/showdata/", views.show_data, name="show_data"),
]

if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
