# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes
from urllib.parse import urlparse

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

SOCIALBLADE_DOMAIN = 'socialblade.com'
YOUTUBE_DOMAIN = 'www.youtube.com'
SOCIALBLADE_ROBOT = "https://socialblade.com/robots.txt"

class ScrapyAppSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyAppDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# youtube downloader middleware
class SocialbladeDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        self.driver.get(request.url)
        domain = urlparse(request.url).netloc

        print('crawling url : {}'.format(request.url))

        if(domain == SOCIALBLADE_DOMAIN):
            if(request.url != SOCIALBLADE_ROBOT):
                WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="YouTubeUserTopInfoBlockTop"]')
                    )
                )
        elif(domain == YOUTUBE_DOMAIN):
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="right-column"]')
                )
            )

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="text"]')
                )
            )
            # KEYWORD = request.meta['keyword']
            # WebDriverWait(self.driver, 40).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, '//*[@id="SearchInput"]')
            #     )
            # )
            # search_bar = self.driver.find_element(
            #     By.XPATH, '//*[@id="SearchInput"]'
            # )

            # search_bar.send_keys(searchKeyword)
            # time.sleep(2)
            # search_bar.send_keys(Keys.ENTER)
            # time.sleep(1)
        else:
            print('domain : {} Neither of the domain filterling!!!!'.format(domain))
        body = to_bytes(text=self.driver.page_source)

        return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        WINDOW_SIZE = "1920,1080"
        s = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # browser가 화면 나오는 것 방지
        chrome_options.add_argument("--no-sandbox")  # ???
        chrome_options.add_argument("--disable-gpu")  # 그래픽 카드 작동해제 => 성능 향상
        # user-agent 값 삽입 -> 봇 감지 방지
        user_agent = "Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36"
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")  # 사이즈 변경
        chrome_options.add_argument('lang=ko_KR')
        driver = webdriver.Chrome(service=s, options=chrome_options)
        self.driver = driver