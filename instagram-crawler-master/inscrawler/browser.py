import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from .utils import randmized_sleep

from fake_useragent import UserAgent


class Browser:
    def __init__(self, has_screen):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        service_args = ["--ignore-ssl-errors=true"]
        chrome_options = Options()
        if not has_screen:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("user-agent=" + UserAgent().random)
        self.driver = webdriver.Chrome(
            executable_path="%s/bin/chromedriver" % dir_path,
            service_args=service_args,
            chrome_options=chrome_options,
        )
        self.driver.implicitly_wait(5)

    @property
    def page_height(self):
        return self.driver.execute_script("return document.body.scrollHeight")

    def get(self, url):
        self.driver.get(url)

    @property
    def current_url(self):
        return self.driver.current_url

    def implicitly_wait(self, t):
        self.driver.implicitly_wait(t)

    def find_one(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver

        if waittime:
            WebDriverWait(obj, waittime).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )

        try:
            return obj.find_element(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None

    def find_class_one(self, selector, elem=None, waittime=0):
        obj = elem or self.driver

        if waittime:
            WebDriverWait(obj, waittime).until(
                EC.presence_of_element_located((By.CLASS_NAME, selector))
            )

        try:
            return obj.find_element(By.CLASS_NAME, selector)
        except NoSuchElementException:
            return None

    def find(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver

        try:
            if waittime:
                WebDriverWait(obj, waittime).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
                )
        except TimeoutException:
            return None

        try:
            return obj.find_elements(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None

    def find_class(self, css_selector, elem=None, waittime=0):
        obj = elem or self.driver
        # html = obj.page_source
        # print(html)

        try:
            if waittime:
                WebDriverWait(obj, waittime).until(
                    EC.presence_of_element_located((By.CLASS_NAME, css_selector))
                )
        except TimeoutException:
            return None

        try:
            return obj.find_elements(By.CLASS_NAME, css_selector)
        except NoSuchElementException:
            return None

    def find_following(self, elem=None, waittime=3):
        obj = elem or self.driver
        html = obj.page_source
        soup = BeautifulSoup(html, "html.parser")
        # print(soup)
        result = dict()
        following = []

        # images data
        content = soup.select("div._aaep")
        # print(f"content : {len(content)}")
        for i in content:
            link = i.find("a")
            # print(f"link content : {link['href'].replace('/', '')}")
            following.append(link['href'].replace('/', ''))
        result["following"] = following

        return result

    def find_image(self, get_userinfo, elem=None, waittime=3):
        obj = elem or self.driver
        html = obj.page_source
        soup = BeautifulSoup(html, "html.parser")
        # print(soup)
        result = dict()
        userid = []
        usernick = []
        imagelist = []


        if get_userinfo == "Y":
            # user id
            content = soup.select("div._aa_m")
            for i in content:
                h2 = i.find("h2")
                # print(f"user id : {h2.text}")
                userid.append(h2.text)
            # user nick
            content = soup.select("div._aa_c")
            for i in content:
                span = i.find("span")
                # print(f"user nick : {span.text}")
                usernick.append(span.text)

            result["userid"] = userid
            result["usernick"] = usernick

        # images data
        content = soup.select("div._aagv")
        for i in content:
            img = i.find("img")
            # print(f"image content : {img['src']}")
            imagelist.append(img['src'])
        result["images"] = imagelist

        return result

    def scroll_down(self, wait=0.3):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        randmized_sleep(wait)

    def scroll_up(self, offset=-1, wait=2):
        if offset == -1:
            self.driver.execute_script("window.scrollTo(0, 0)")
        else:
            self.driver.execute_script("window.scrollBy(0, -%s)" % offset)
        randmized_sleep(wait)

    def js_click(self, elem):
        self.driver.execute_script("arguments[0].click();", elem)

    def open_new_tab(self, url):
        self.driver.execute_script("window.open('%s');" % url)
        self.driver.switch_to.window(self.driver.window_handles[1])

    def close_current_tab(self):
        self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])

    def __del__(self):
        try:
            self.driver.quit()
        except Exception:
            pass
