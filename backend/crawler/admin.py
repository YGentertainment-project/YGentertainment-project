from django.contrib import admin
from crawler.models import SocialbladeYoutube


class SocialbladeYoutubeItemAdmin(admin.ModelAdmin):
    # "recorded_date"
    list_display = ("artist", "uploads", "subscribers", "views", "user_created", "recorded_date", "url")


# Register your models here.
admin.site.register(SocialbladeYoutube, SocialbladeYoutubeItemAdmin)
