# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from django.utils import timezone
from crawler.models import SocialbladeItem

class ScrapyAppPipeline(object):
    def process_item(self, item, spider):
        socialbladeItem = SocialbladeItem(artist=item.get('artist'),
                                          uploads=item.get('uploads'),
                                          subscribers=item.get('subscribers'),
                                          views=item.get('views'),
                                          user_created=item.get('user_created'),
                                          platform=item.get('platform'),
                                          url=item.get('url')
                                          )

        # 이미 존재하는 아이템에 대해서는 업데이트만 진행
        if SocialbladeItem.objects.filter(artist=item.get('artist')).exists():
            existingItem = SocialbladeItem.objects.get(artist=item.get('artist'))
            existingItem.uploads = item.get('uploads')
            existingItem.subscribers = item.get('subscribers')
            existingItem.views = item.get('views')
            existingItem.recorded_date = timezone.now()
            existingItem.save()
        else:
            socialbladeItem.save()
        return item
