# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from time import sleep

from scrapy import signals
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class CrawlerprojecctSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class SocialbladeDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        print("NoLoginSelenium Downloader Middleware begin")
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('log-level=3')
        options.add_argument('disable-gpu')
        options.add_argument('user-agent=Chrome/96.0.4664')
        options.add_argument('start-maximized')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver = driver
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        self.driver.close()

    def process_request(self, request, spider):
        self.driver.get(request.url)
        self.driver.implicitly_wait(time_to_wait=5)
        body = to_bytes(text=self.driver.page_source)
        return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

class WeverseDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        print("Weverse Downloader Middleware Begin")
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('log-level=3')
        options.add_argument('disable-gpu')
        options.add_argument('user-agent=Chrome/96.0.4664')
        options.add_argument('start-maximized')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.login_process()
        spider.logger.info('Spider opened: %s' % spider.name)

    def login_process(self):
        self.driver.get('https://www.weverse.io/')
        self.driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/div[2]/div/button[2]').click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        ID_BOX = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/form/div[1]/input')
        ID_BOX.send_keys('sunrinkingh2160@gmail.com')
        PW_BOX = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/form/div[2]/input')
        PW_BOX.send_keys('!eogksalsrnr123')
        self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/form/div[3]/button').click()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.implicitly_wait(time_to_wait=5)

    def spider_closed(self, spider):
        self.driver.close()

    def process_request(self, request, spider):
        self.driver.get(request.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#root > div > section > aside > div > a > div > p'))
        )
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/section/aside/div/div[1]'))
        )
        body = to_bytes(text=self.driver.page_source)
        return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

class CrowdtangleDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        print("Crowdtangle Downloader Middleware Begin")
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument('log-level=3')
        options.add_argument('disable-gpu')
        options.add_argument('user-agent=Chrome/96.0.4664')
        options.add_argument('start-maximized')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.login_process()
        spider.logger.info('Spider opened: %s' % spider.name)

    def login_process(self):
        self.driver.get('https://apps.crowdtangle.com')
        self.driver.find_element(By.XPATH, '//*[@id="account-react"]/div/div/div[2]/div/button').click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        ID_BOX = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/form/div/div[1]/div/input')
        ID_BOX.send_keys('jaewon@ygmail.net')
        PW_BOX = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/form/div/div[2]/div/input')
        PW_BOX.send_keys('Ygfamily1234@')
        self.driver.find_element(By.XPATH, '//*[@id="loginbutton"]').click()
        self.driver.switch_to.window(self.driver.window_handles[0])
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[1]/h1'))
        )

    def spider_closed(self, spider):
        self.driver.close()

    def process_request(self, request, spider):
        self.driver.get(request.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/span[2]'))
        )
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div/div[3]/div[2]/div[1]/div/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div/span[1]'))
        )
        body = to_bytes(text=self.driver.page_source)
        return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass
