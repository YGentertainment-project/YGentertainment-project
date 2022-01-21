from scrapy.crawler import CrawlerRunner
from crawler.scrapy_app.spiders.socialblade_youtube import YoutubeSpider
from twisted.internet import reactor

# taskId = task의 id
# platforms = crawling할 platform의 이름이 담긴 배열

spiders = {
    "youtube": YoutubeSpider,
}


def create_task(taskid, platforms):
    log_path = "crawler/logs/tasks/{}.txt".format(taskid)
    # process = CrawlerProcess(settings={
    #     "LOG_FILE": log_path,
    # })
    runner = CrawlerRunner(settings={
        "LOG_FILE": log_path,
    })

    for platform in platforms:
        # process.crawl(spiders[platform])
        runner.crawl(spiders[platform])
    d = runner.join()
    # process.start()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
