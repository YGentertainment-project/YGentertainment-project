import os
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes
from urllib.parse import urlparse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils.shortcuts import get_env
from requests import get
from ..tasks import crawlinglogger

production_env = get_env("YG_ENV", "dev") == "production"

ROBOTS_TXT = "robots.txt"

SOCIALBLADE_DOMAIN = "socialblade.com"
YOUTUBE_DOMAIN = "youtube.com"
GUYSOME_DOMAIN = "xn--o39an51b2re.com"
MELON_DOMAIN = "melon.com"

# 로그인이 필요한 플랫폼별 ID와 PW값
WEVERSE_ID = "sunrinkingh2160@gmail.com"
WEVERSE_PW = "!eogksalsrnr123"
CROWDTANGLE_ID = "jaewon@ygmail.net"
CROWDTANGLE_PW = "Ygfamily1234@"

# 정의 : Melon을 크롤링할 때 필요한 Selenium Custom Wait
# 목적 : driver가 가르키고 있는 현재 페이지에서 전달 받은 locator로 수집하고자 하는 element를 찾는데, 이 값이 0 이상일 경우 해당 요소를 return, 아닐 경우 false return
#       WebDriverWait(self.driver, 10).until()로 기다리고 있으므로 해당 return값이 false가 아닐 때까지 반복하여 기다린다.
#       Melon의 경우 팬 수를 나타내는 값이 0에서 시작하여 실제 값이 화면에 나타나는 script가 있는데 이를 기다리기 위함.
#       새로운 아티스트가 추가되어 실제로 팬 수가 0일 경우 계속해서 Wait하게 되지만 최대 10초까지 기다리기 때문에 큰 Overhead로 예상되지 않음.
#       자세한 내용은 기술문서에 추가로 작성되어 있음.
# 담당자 : 성균관대학교 김정규, sunrinkingh2160@gmail.com
# 수정일 : 2022-02-23
class MelonElementIsPositive(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if int(element.text.replace(",", "")) > 0:
            return element
        else:
            return False


class ScrapyAppSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
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
        spider.logger.info("Spider opened: %s" % spider.name)

# 정의 : driver_setting(), 크롤링을 담당하는 Selenium driver에 대한 기본적인 설정들을 수행.
# 목적 : 크롤링하는 데 있어서 꼭 필요한 기능들과 성능 향상을 위한 옵션들이 담겨있음.
#       주요 옵션들로는 Bot detection bypass를 위한 user-agent값 추가, 실제로 화면을 띄우지 않고 진행하는 headless 모드, 성능 향상을 위해 불필요한 기능들을 preferences 값을 2로 설정하여 disable하고 있음.
# 담당자 : 성균관대학교 김정규, sunrinkingh2160@gmail.com
# 수정일 : 2022-02-23
def driver_setting():
    chrome_options = Options()
    prefs = {
        "profile.default_content_setting_values": {
            "images": 2,
            "plugins": 2,
            "popups": 2,
            "geolocation": 2,
            "notifications": 2,
            "auto_select_certificate": 2,
            "fullscreen": 2,
            "mouselock": 2,
            "mixed_script": 2,
            "media_stream": 2,
            "media_stream_mic": 2,
            "media_stream_camera": 2,
            "protocol_handlers": 2,
            "ppapi_broker": 2,
            "automatic_downloads": 2,
            "midi_sysex": 2,
            "push_messaging": 2,
            "ssl_cert_decisions": 2,
            "metro_switch_to_desktop": 2,
            "protected_media_identifier": 2,
            "app_banner": 2,
            "site_engagement": 2,
            "durable_storage": 2
        }
    }
    chrome_options.add_argument("--headless")                                            # Headless Mode
    chrome_options.add_argument("--no-sandbox")                                          # Bypass OS security model
    chrome_options.add_argument("--disable-gpu")                                         # 그래픽 카드 작동해제 => 성능 향상
    chrome_options.add_experimental_option("useAutomationExtension", False)              # disabling infobars
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")                             # user-agent 값 삽입 -> 봇 감지 방지
    chrome_options.add_argument("--start-maximized")                                    # open browser in maximized mode
    chrome_options.add_argument("lang=ko_KR")                                           # language setting at plug-in
    chrome_options.add_argument("--disable-extensions")                                 # disabling extensions
    chrome_options.add_experimental_option("prefs", prefs)                              # custom settings, disable = 2
    chrome_options.add_argument("log-level=3")
    chrome_options.add_argument("--disable-dev-shm-usage")                              # overcome limited resource problems

    if production_env == "production":
        executable_path = "/usr/local/bin/chromedriver"
        s = Service(executable_path=executable_path)
    else:
        s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver

# 정의 : Selenium을 사용하는 Spider들을 위한 DownloaderMiddleware 중 로그인 기능이 필요 없는 Spider들에 해당.
# 목적 : 각 Spider의 Request들이 yield되면 spider_opened() 메소드가 실행되어 위에 설정한 대로 Selenium Driver를 생성합니다.
#       이후, process_request()에서 플랫폼 별로 수집할 대상을 나타내는 element의 locator에 따라서 해당 element가 현재 driver에 load될 때까지 Wait하고
#       그 결과를 HtmlResponse로 바꿔 각 Spider의 지정된 call_back함수로 넘겨줍니다.
#       이 과정이 모두 끝나면, spider_closed에서 Spider가 닫히면서 사용했던 driver object도 종료합니다.
# 담당자 : 성균관대학교 김정규, sunrinkingh2160@gmail.com
# 수정일 : 2022-02-23
class NoLoginDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        self.driver.get(request.url)
        domain = urlparse(request.url).netloc
        print("crawling url : {}".format(request.url))
        artist_name = request.meta["artist"]

        # Selenium의 경우 따로 특정 HttpResponse에 대한 모듈이 없는 것 같아서
        # python에서 제공하는 requests 속 get 모듈을 활용했습니다.
        # 404, 499 등 200이 아닌 경우에는 return None을 통해 크롤링을 진행하지 않도록 했습니다.
        # Socialblade의 경우 499 Response의 경우에도 User-Agent를 통한 우회를 진행하고 있으므로 계속해서 수행해야 합니다.
        # Melon의 경우 비슷한 맥락으로 406 Response를 받고 있습니다. 이 경우는 robots 정책을 ignore하며 진행하므로 계속해서 수행해야 합니다.
        tmp = get(request.url)
        if tmp.status_code == 404:
            crawlinglogger.error(f"[400], {artist_name}, {spider.name}, {request.url}")
            return None

        # Socialblade Case
        if domain == SOCIALBLADE_DOMAIN:
            if ROBOTS_TXT not in request.url:
                try:
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located(
                            (By.ID, "YouTubeUserTopInfoBlock")
                        )
                    )
                except TimeoutException:
                    pass
                except Exception:
                    crawlinglogger.error(f"[499]")

        # Youtube Channel Case
        elif domain == YOUTUBE_DOMAIN:
            if ROBOTS_TXT not in request.url:
                try:
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located(
                            (By.ID, "right-column")
                        )
                    )
                except TimeoutException:
                    pass
                except Exception:
                    crawlinglogger.error(f"[499]")

        # 가이섬 Channel Case
        elif domain == GUYSOME_DOMAIN:
            if ROBOTS_TXT not in request.url:
                try:
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, "list-style-none")
                        )
                    )
                except TimeoutException:
                    pass
                except Exception:
                    crawlinglogger.error(f"[499]")
        elif domain == MELON_DOMAIN:
            if ROBOTS_TXT not in request.url:
                try:
                    WebDriverWait(self.driver, 10).until(
                        MelonElementIsPositive((By.ID, "d_like_count"))
                    )
                except TimeoutException:
                    pass
                except Exception:
                    crawlinglogger.error(f"[499]")
        body = to_bytes(text=self.driver.page_source)
        return HtmlResponse(url=request.url, body=body, encoding="utf-8", request=request)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        self.driver = driver_setting()

    def spider_closed(self, spider):
        self.driver.close()
        self.driver.quit()
        self.driver = None

# 정의 : Selenium을 사용하는 Spider들을 위한 DownloaderMiddleware 중 로그인 기능이 필요한 Spider들에 해당.
# 목적 : 각 Spider의 Request들이 yield되면 spider_opened() 메소드가 실행되어 위에 설정한 대로 Selenium Driver를 생성합니다.
#       Driver object가 생성된 뒤 login_process()가 수행됩니다. 현재, 로그인이 필요한 플랫폼은 Weverse와 Crowdtangle이 있는데, 각 플랫폼의 기본 페이지에 접근하여
#       위에 변수로 저장해준 ID와 PW값을 통해 login을 수행합니다. 이후 내용은 같습니다.
#       process_request()에서 플랫폼 별로 수집할 대상을 나타내는 element의 locator에 따라서 해당 element가 현재 driver에 load될 때까지 Wait하고
#       그 결과를 HtmlResponse로 바꿔 각 Spider의 지정된 call_back함수로 넘겨줍니다.
#       이 과정이 모두 끝나면, spider_closed에서 Spider가 닫히면서 사용했던 driver object도 종료합니다.
# 담당자 : 성균관대학교 김정규, sunrinkingh2160@gmail.com
# 수정일 : 2022-02-23
class LoginDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        self.driver = driver_setting()
        self.login_process(spider)
        spider.logger.info("Spider opened: %s" % spider.name)

    def login_process(self, spider):
        if spider.name == "weverse":
            try:
                self.driver.get("https://www.weverse.io")
                self.driver.implicitly_wait(time_to_wait=5)
            except WebDriverException:
                crawlinglogger.error("[401], loginpage, weverse, https://www.weverse.io")
                # 로그인을 진행할 첫 페이지의 URL이 잘못된 형식일 경우 발생합니다.
            except Exception:
                crawlinglogger.error(f"[499]")

            try:
                self.driver.find_element(By.CLASS_NAME, "sc-AxjAm.dhTrPj").click()
            except NoSuchElementException:
                crawlinglogger.error("[401], loginbutton, weverse, https://www.weverse.io")
                # 로그인 버튼이 클릭되지 않을 때 발생합니다.
                # 로그인 페이지가 아닌 다른 페이지가 로딩 됐거나 로그인 버튼에 대한 locator가 변경됐을 때 발생합니다.
            except Exception:
                crawlinglogger.error(f"[499]")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.implicitly_wait(time_to_wait=5)
            try:
                self.driver.find_element(By.NAME, "username").send_keys(WEVERSE_ID)
                self.driver.find_element(By.NAME, "password").send_keys(WEVERSE_PW)
            except NoSuchElementException:
                crawlinglogger.error("[401], logininput, weverse, https://www.weverse.io")
                # ID와 PW를 입력하는 input box에 대한 locator가 변경됐을 때 발생합니다.
            except Exception:
                crawlinglogger.error(f"[499]")
            try:
                self.driver.find_element(By.CLASS_NAME, "sc-Axmtr.hwYQYk.gtm-login-button").click()
            except NoSuchElementException:
                crawlinglogger.error("[401], loginbutton, weverse, https://www.weverse.io")
                # 확인 버튼에 대한 locator가 변경됐을 때 발생합니다.
            except Exception:
                crawlinglogger.error(f"[499]")
            self.driver.switch_to.window(self.driver.window_handles[0])

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "sc-pjHjD.CNlcm"))
                )
            except TimeoutException:
                crawlinglogger.error("[401], afterloginpage, weverse, https://www.weverse.io")
                # 로그인이 정상적으로 진행된 후 로드되는 다음 페이지가 로드되지 않을 때 발생합니다.
            except Exception:
                crawlinglogger.error(f"[499]")
        else:
            try:
                self.driver.get("https://apps.crowdtangle.com")
                self.driver.implicitly_wait(time_to_wait=5)
            except WebDriverException:
                crawlinglogger.error("[401], loginpage, crowdtangle, https://apps.crowdtangle.com")
                # 로그인을 진행할 첫 페이지의 URL이 잘못된 형식일 경우 발생합니다.
            except Exception:
                crawlinglogger.error(f"[499]")
            try:
                self.driver.find_element(By.CLASS_NAME, "facebookLoginButton__authButton--lof0c").click()
            except NoSuchElementException:
                crawlinglogger.error("[401], loginbutton, crowdtangle, https://apps.crowdtangle.com")
                # 로그인 버튼이 클릭되지 않을 때 발생합니다.
                # 로그인 페이지가 아닌 다른 페이지가 로딩 됐거나 로그인 버튼에 대한 locator가 변경됐을 때 발생합니다.
            except Exception:
                crawlinglogger.error(f"[499]")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.implicitly_wait(time_to_wait=5)
            try:
                self.driver.find_element(By.ID, "email").send_keys(CROWDTANGLE_ID)
                self.driver.find_element(By.ID, "pass").send_keys(CROWDTANGLE_PW)
            except NoSuchElementException:
                crawlinglogger.error("[401], logininput, crowdtangle, https://apps.crowdtangle.com")
                # ID와 PW를 입력하는 input box에 대한 locator가 변경됐을 때 발생합니다.
            except Exception:
                crawlinglogger.error(f"[499]")
            try:
                self.driver.find_element(By.ID, "loginbutton").click()
            except NoSuchElementException:
                crawlinglogger.error("[401], loginbutton, crowdtangle, https://apps.crowdtangle.com")
                # 확인 버튼에 대한 locator가 변경됐을 때 발생합니다.
            except Exception:
                crawlinglogger.error(f"[499]")
            self.driver.switch_to.window(self.driver.window_handles[0])
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "app-container"))
                )
            except TimeoutException:
                crawlinglogger.error("[401], afterloginpage, crowdtangle, https://apps.crowdtangle.com")
                # 로그인이 정상적으로 진행된 후 로드되는 다음 페이지가 로드되지 않을 때 발생합니다.
            except Exception:
                crawlinglogger.error(f"[499]")

    def spider_closed(self, spider):
        self.driver.close()
        self.driver.quit()
        self.driver = None

    def process_request(self, request, spider):
        self.driver.get(request.url)
        artist_name = request.meta["artist"]
        print("crawling url : {}".format(request.url))

        # Selenium의 경우 따로 특정 HttpResponse에 대한 모듈이 없는 것 같아서
        # python에서 제공하는 requests 속 get 모듈을 활용했습니다.
        # 404, 499 등 200이 아닌 경우에는 return None을 통해 크롤링을 진행하지 않도록 했습니다.
        tmp = get(request.url)
        if tmp.status_code == 404:
            crawlinglogger.error(f"[400], {artist_name}, {spider.name}, {request.url}")
            return None
        elif tmp.status_code == 403:
            crawlinglogger.error(f"[403], {artist_name}, {spider.name}, {request.url}")
            return None

        if spider.name == "weverse":
            if ROBOTS_TXT not in request.url:
                try:
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "sc-pcxhi"))
                    )
                except TimeoutException:
                    pass
                except Exception:
                    crawlinglogger.error(f"[499]")
        else:
            if ROBOTS_TXT not in request.url:
                try:
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "report-top-level-metrics"))
                    )
                except TimeoutException:
                    pass
                except Exception:
                    crawlinglogger.error(f"[499]")
        body = to_bytes(text=self.driver.page_source)
        return HtmlResponse(url=request.url, body=body, encoding="utf-8", request=request)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass
