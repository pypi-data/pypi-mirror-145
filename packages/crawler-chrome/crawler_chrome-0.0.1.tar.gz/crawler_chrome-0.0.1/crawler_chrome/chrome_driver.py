import datetime
import json
import os
import re
import time
import logging
from retry import retry
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def date_to_str(date=None, format_str="%Y-%m-%d %H:%M:%S"):
    """时期格式化成字符
        :param date: 时间
        :param format_str: %Y-%m-%d %H:%M:%S
    """
    if date is None:
        date = datetime.datetime.now()
    return date.strftime(format_str)


class ChromeDriver(WebDriver):
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pwd = os.path.dirname(__file__)
        self.close()

    def __init__(self, headless=True, rec_log=True):
        self.screenshot_list = []
        caps = {
            'browserName': 'chrome',
            'loggingPrefs': {
                'browser': 'ALL',
                'driver': 'ALL',
                'performance': 'ALL',
            },
            'goog:chromeOptions': {
                'perfLoggingPrefs': {
                    'enableNetwork': True,
                },
                'w3c': False,
            },
        }

        if os.path.exists(".webdriver"):
            executable_path = open(".webdriver", "r").read()
        else:
            executable_path = ChromeDriverManager().install()
            open(".webdriver", "w+").write(executable_path)

        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'performance': 'ALL'}

        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        if rec_log:
            chrome_options.add_experimental_option('w3c', False)

        super().__init__(executable_path=executable_path, desired_capabilities=d, options=chrome_options)
        self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        self.execute_cdp_cmd("Emulation.setUserAgentOverride", {
            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
            # "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 micromessenger/8.0.15(0x18000f27) NetType/4G Language/zh_CN"
        })
        self.set_window_position(0, 0)
        self.set_window_size(1900, 1000)

    def open(self, tab_index=0, url=None):
        try:
            handles = self.window_handles  # 获取当前窗口句柄集合（列表类型）
            if len(handles) < tab_index + 1:
                self.execute_script('window.open("","_blank");')
                while True:
                    time.sleep(0.1)
                    handles = self.window_handles  # 获取当前窗
                    if len(handles) > tab_index:
                        break
            if self.current_window_handle != handles[tab_index]:
                self.switch_to.window(handles[tab_index])
        except Exception:
            pass
        if url is not None:
            logging.info(f"chrome open {url}")
            self.get(url)

    def close_tab(self, tab_index):
        handles = self.window_handles  # 获取当前窗口句柄集合（列表类型）
        if len(handles) < tab_index + 1:
            return

        self.switch_to.window(handles[tab_index])
        self.close()

    def get_headers(self):
        try:
            headers = {}
            cookie = [item["name"] + "=" + item["value"] for item in self.get_cookies()]
            cookiestr = ';'.join(item for item in cookie)
            headers["cookie"] = cookiestr
            # token = re.search(r'"token": ".*?"', str(info))[0][10:-1]
            # s.headers["token"] = token
            # s.headers["Authorization"] = token
            return headers
        except:
            return None

    def scroll_end_page(self):
        elements = self.find_elements_by_xpath("//*")
        for element in elements:
            try:
                self.execute_script("arguments[0].scrollIntoView();", element)
            except:
                pass
            # self.execute_script("document.body.scrollTop=document.body.scrollHeight")

    def switch_tab(self, tab_index):
        if len(self.window_handles) < tab_index + 1:
            return
        self.switch_to.window(self.window_handles[tab_index])

    @retry(Exception, tries=10, delay=2)
    def element_click(self, element):
        self.execute_script("arguments[0].click();", element)

    def wait_id_element(self, id_, timeout=10):
        WebDriverWait(self, timeout).until(EC.presence_of_element_located((By.ID, id_)))
        element = self.find_element_by_id(id_)
        element.click = lambda: self.execute_script("arguments[0].click();", element)
        return element

    def wait_css_element(self, cls, timeout=10):
        WebDriverWait(self, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, cls)))
        return self.find_element_by_css_selector(cls)

    @retry(Exception, tries=2, delay=1)
    def wait_xpath_element(self, path, timeout=10, delay=0, next_delay=0):
        time.sleep(delay)
        WebDriverWait(self, timeout).until(EC.presence_of_element_located((By.XPATH, path)))
        element = self.find_element_by_xpath(path)
        element.click = lambda: self.element_click(element)
        time.sleep(next_delay)
        return element

    @retry(Exception, tries=10, delay=3, backoff=2)
    def regex_findall(self, rule):
        text = self.page_source
        result = re.findall(rule, text)
        if len(result) == 0:
            raise Exception("not find")
        return result

    def wait_url(self, url, timeout=10):
        while timeout > 0:
            time.sleep(1)
            timeout -= 1
            if str(self.current_url).startswith(url):
                return

        raise Exception("TimeOut wait url")

    def save_screen(self, name, screenshot_path="./screenshot", delay=1):
        print(name)
        time.sleep(delay)
        os.makedirs(screenshot_path, exist_ok=True)
        path = os.path.join(screenshot_path, date_to_str(format_str="%Y-%m-%d %H:%M:%S ") + name + ".png")
        self.save_screenshot(path)
        self.screenshot_list.append(os.path.abspath(path))

    def wait_for_one(self, elements, timeout=10, check_second=0.5):
        """
        r, v = self.firefox.wait_for_one({
            False: [{"re": "没有找到相关企业"}, {"re": "我们只是确认一下你不是机器人"}],
            True: [{"css": ".tips-num"}]
        })

        :param elements:
        :param timeout: 
        :param check_second: 
        :return: 
        """
        def find_by(by: str, value):
            find = False
            if by == "xpath":
                try:
                    self.find_element_by_xpath(value)
                    find = True
                except Exception:
                    pass
            elif by == "css":
                try:
                    self.find_element_by_css_selector(value)
                    find = True
                except Exception:
                    pass
            elif by == "id":
                try:
                    self.find_element_by_id(value)
                    find = True
                except Exception:
                    pass
            elif by == "tag":
                try:
                    self.find_element_by_tag_name(value)
                    find = True
                except Exception:
                    pass
            elif by == "re":
                text = self.page_source
                if re.search(value, text) is not None:
                    find = True

            return find

        while timeout > 0:
            for key in elements.keys():
                try:
                    el = elements[key]
                    if isinstance(el, list):
                        for e in el:
                            by, v = list(e.keys())[0], list(e.values())[0]
                            if find_by(by, v):
                                return key, v
                    else:
                        by, v = list(el.keys())[0], list(el.values())[0]
                        if find_by(by, v):
                            return key, v
                except Exception as e:
                    logging.exception(e)

            time.sleep(check_second)
            timeout -= check_second
        raise TimeoutError()

    def get_logs(self):
        logs = [json.loads(log['message'])['message'] for log in self.get_log('performance')]
        return logs
