# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from django.utils import timezone
from crawler.models import Socialblade

class ScrapyAppPipeline(object):
    def process_item(self, item, spider):
        item["recorded_date"] = timezone.now()

        # 이미 존재하는 아이템에 대해서는 업데이트만 진행
        if Socialblade.objects.filter(artist=item.get('artist')).exists():
            existingItem = Socialblade.objects.get(artist=item.get('artist'))
            existingItem.uploads = item.get('uploads')
            existingItem.subscribers = item.get('subscribers')
            existingItem.views = item.get('views')
            existingItem.recorded_date = timezone.now()
            existingItem.sa ve()
        else:
            item.save()
        return item
