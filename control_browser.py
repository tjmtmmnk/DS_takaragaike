from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep


class ControlBrowser():
    def __init__(self, cfg, is_use_headless=True, is_use_heroku=False):
        options = webdriver.chrome.options.Options()

        if (is_use_heroku):
            options.binary_location = '/app/.apt/usr/bin/google-chrome'
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            self.browser = webdriver.Chrome(chrome_options=options)
        else:
            if (is_use_headless):
                options.add_argument("--headless")
                self.browser = webdriver.Chrome(chrome_options=options)
            else:
                self.browser = webdriver.Chrome()

        self.cfg = cfg

    def setURL(self, url):
        self.browser.get(url)

    def setCarType(self, type='02'):  # ATをデフォルト引数に
        car_type_list = self.browser.find_element_by_name('CARTYPE')
        car_type_select = Select(car_type_list)
        car_type_select.select_by_value(type)
        ok_button = self.browser.find_element_by_xpath(
            "/html/body/p/table[2]/tbody/tr[1]/td[2]/form/table/tbody/tr[2]/td[2]/input")
        ok_button.click()
        self.source = self.browser.page_source

    def login(self):
        user_name_field = self.browser.find_element_by_xpath("/html/body/form/table/tbody/tr[1]/td/input")
        user_name_field.send_keys(self.cfg.USERNAME)

        pass_word_field = self.browser.find_element_by_xpath("/html/body/form/table/tbody/tr[2]/td[1]/input")
        pass_word_field.send_keys(self.cfg.PASSWORD)

        submit_button = self.browser.find_element_by_xpath("/html/body/form/table/tbody/tr[3]/td/input")
        submit_button.click()

    def getSource(self):
        return self.source

    def close(self):
        sleep(1)
        print("close browser")
        self.browser.close()
