import os
import sys

# django integration
sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'yg.settings'

import django
django.setup()


# scrapy settings
BOT_NAME = 'scrapy_app'

SPIDER_MODULES = ['crawler.scrapy_app.spiders']
# NEWSPIDER_MODULE = 'spiders'

LOG_ENABLED = True
# LOG_FILE = './data/log/Crawler.log'
LOG_LEVEL = 'ERROR'
LOG_STDOUT = True
LOG_ENCODING = 'utf-8'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'crawler.scrapy_app.pipelines.CrawlerPipeline': 100,
}

DOWNLOAD_DELAY = 1
