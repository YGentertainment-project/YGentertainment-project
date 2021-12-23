from django.contrib import admin
from crawler.models import SocialbladeItem


class SocialbladeItemAdmin(admin.ModelAdmin):
    # 'recorded_date'
    list_display = ('artist', 'uploads', 'subscribers', 'views', 'user_created', 'recorded_date', 'platform', 'url')


# Register your models here.
admin.site.register(SocialbladeItem, SocialbladeItemAdmin)
