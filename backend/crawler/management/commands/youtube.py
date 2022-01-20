from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from crawler.scrapy_app.spiders.socialblade_youtube import YoutubeSpider

# settings_file_path = "crawler."

# required arguments : spider, taskid


class Command(BaseCommand):
    name = "youtube"
    help = "Scrape the socialblade youtube"

    def add_arguments(self, parser):
        # parser.add_argument("spider", type=str)
        parser.add_argument("taskid", type=str)

    def handle(self, *args, **options):
        taskid = options["taskid"]
        log_path = "crawler/logs/tasks/{}.txt".format(taskid)
        process = CrawlerProcess(settings={
            "LOG_FILE": log_path,
        })

        process.crawl(YoutubeSpider)
        process.start()
        self.stdout.write(self.style.SUCCESS("Successful to handle youtube scraping"))
