# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from django.utils import timezone
from crawler.models import SocialbladeYoutube, SocialbladeTiktok, SocialbladeTwitter, SocialbladeTwitter2


class SocialbladeYoutubePipeline(object):
    def process_item(self, item, spider):
        item["recorded_date"] = timezone.now()

        # 이미 존재하는 아이템에 대해서는 업데이트만 진행
        if SocialbladeYoutube.objects.filter(artist=item.get('artist')).exists():
            existingItem = SocialbladeYoutube.objects.get(artist=item.get('artist'))
            existingItem.uploads = item.get('uploads')
            existingItem.subscribers = item.get('subscribers')
            existingItem.views = item.get('views')
            existingItem.recorded_date = timezone.now()
            existingItem.save()
        else:
            item.save()
        return item


class SocialbladeTiktokPipeline(object):
    def process_item(self, item, spider):
        item["recorded_date"] = timezone.now()

        if SocialbladeTiktok.objects.filter(artist=item.get('artist')).exists():
            existingItem = SocialbladeTiktok.objects.get(artist=item.get('artist'))
            existingItem.followers = item.get('followers')
            existingItem.uploads = item.get('uploads')
            existingItem.likes = item.get('likes')
            existingItem.recorded_date = timezone.now()
            existingItem.save()
        else:
            item.save()
        return item


class SocialbladeTwitterPipeline(object):
    def process_item(self, item, spider):
        item["recorded_date"] = timezone.now()

        if SocialbladeTwitter.objects.filter(artist=item.get('artist')).exists():
            existingItem = SocialbladeTwitter.objects.get(artist=item.get('artist'))
            existingItem.followers = item.get('followers')
            existingItem.twits = item.get('twits')
            existingItem.recorded_date = timezone.now()
            existingItem.save()
        else:
            item.save()
        return item


class SocialbladeTwitter2Pipeline(object):
    def process_item(self, item, spider):
        item["recorded_date"] = timezone.now()

        if SocialbladeTwitter2.objects.filter(artist=item.get('artist')).exists():
            existingItem = SocialbladeTwitter2.objects.get(artist=item.get('artist'))
            existingItem.followers = item.get('followers')
            existingItem.twits = item.get('twits')
            existingItem.recorded_date = timezone.now()
            existingItem.save()
        else:
            item.save()
        return item
