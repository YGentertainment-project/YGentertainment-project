# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from django.utils import timezone
from crawler.models import SocialbladeYoutube, SocialbladeTiktok, SocialbladeTwitter, SocialbladeTwitter2, \
    Weverse, CrowdtangleInstagram, CrowdtangleFacebook, Vlive, Melon, Spotify
from datetime import datetime

DataModels = {
        "youtube": SocialbladeYoutube,
        "tiktok": SocialbladeTiktok,
        "twitter": SocialbladeTwitter,
        "twitter2": SocialbladeTwitter2,
        "weverse": Weverse,
        "instagram": CrowdtangleInstagram,
        "facebook": CrowdtangleFacebook,
        "vlive": Vlive,
        "melon": Melon,
        "spotify": Spotify,
}

def process_itemsave(name, item):
    nowdate = item['recorded_date']
    dayfilter_obj = DataModels[name].objects.filter(artist=item['artist'],
                                                    recorded_date__year=nowdate.year,
                                                    recorded_date__month=nowdate.month,
                                                    recorded_date__day=nowdate.day)
    # 오늘일자로 이미 저장된 아티스트 정보가 있는 경우 => 데이터를 최신버전으로 수정
    if dayfilter_obj.exists():
        if name == "youtube":
            return update_youtube(item)
        elif name == "tiktok":
            return update_tiktok(item)
        elif name == "twitter" or name == "twitter2":
            return update_twitter(item, name)
        elif name == "weverse":
            return update_weverse(item)
        elif name == 'vlive':
            return update_vlive(item)
        elif name == "facebook" or name == "instagram":
            return update_crowdtangle(item, name)
    # 오늘일자로 저장된 데이터가 없는 경우 => 새로 생성
    else:
        item.save()
    return item


def update_youtube(item):
    nowdate = item['recorded_date']
    existingItem = SocialbladeYoutube.objects.get(artist=item['artist'],
                                                     recorded_date__year=nowdate.year,
                                                     recorded_date__month=nowdate.month,
                                                     recorded_date__day=nowdate.day)
    existingItem.uploads = item.get('uploads')
    existingItem.subscribers = item.get('subscribers')
    existingItem.views = item.get('views')
    existingItem.recorded_date = nowdate
    existingItem.save()


def update_tiktok(item):
    nowdate = item['recorded_date']
    existingItem = SocialbladeTiktok.objects.get(artist=item.get('artist'),
                                                 recorded_date__year=nowdate.year,
                                                 recorded_date__month=nowdate.month,
                                                 recorded_date__day=nowdate.day)
    existingItem.followers = item.get('followers')
    existingItem.uploads = item.get('uploads')
    existingItem.likes = item.get('likes')
    existingItem.recorded_date = nowdate
    existingItem.save()




def update_twitter(item, name):
    nowdate = item['recorded_date']
    existingItem = DataModels[name].objects.get(artist=item.get('artist'),
                                                  recorded_date__year=nowdate.year,
                                                  recorded_date__month=nowdate.month,
                                                  recorded_date__day=nowdate.day)
    existingItem.followers = item.get('followers')
    existingItem.twits = item.get('twits')
    existingItem.recorded_date = nowdate
    existingItem.save()

def update_weverse(item):
    nowdate = item['recorded_date']
    existingItem = Weverse.objects.get(artist=item.get('artist'),
                                                   recorded_date__year=nowdate.year,
                                                   recorded_date__month=nowdate.month,
                                                   recorded_date__day=nowdate.day
                                                   )
    existingItem.weverses = item.get('weverses')
    existingItem.recorded_date = nowdate
    existingItem.save()

def update_vlive(item):
    nowdate = item['recorded_date']
    existingItem = Vlive.objects.get(artist=item.get('artist'),
                                     recorded_date__year=nowdate.year,
                                     recorded_date__month=nowdate.month,
                                     recorded_date__day=nowdate.day
                                     )
    existingItem.members = item.get('members')
    existingItem.videos = item.get('videos')
    existingItem.likes = item.get('likes')
    existingItem.plays = item.get('plays')
    existingItem.recorded_date = nowdate
    existingItem.save()

def update_crowdtangle(item, name):
    nowdate = item['recorded_date']
    existingItem = DataModels[name].objects.get(artist=item.get('artist'),
                                     recorded_date__year=nowdate.year,
                                     recorded_date__month=nowdate.month,
                                     recorded_date__day=nowdate.day
                                     )
    existingItem.followers = item.get('followers')
    existingItem.recorded_date = nowdate
    existingItem.save()

class CrawlerPipeline(object):
    def process_item(self, item, spider):
        spider_name = spider.name # spider의 이름을 추출 => 동적으로 spider에 따라 다른 pipeline 적용
        item["recorded_date"] = timezone.now() # 업데이트 시간 기록
        process_itemsave(spider_name, item)