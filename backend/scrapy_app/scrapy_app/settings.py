import os
import sys

# django integration
sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'yg.settings'

import django
django.setup()


# scrapy settings
BOT_NAME = 'scrapy_app'

SPIDER_MODULES = ['scrapy_app.spiders']
NEWSPIDER_MODULE = 'scrapy_app.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'scrapy_app.pipelines.ScrapyAppPipeline': 300,
}