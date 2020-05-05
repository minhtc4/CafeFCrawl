from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
from icecream import ic
import json
import time
import logging

chrome_drive = "../chromedriver"
os.environ['webdrive.chrome.drive'] = chrome_drive
chrome_options = Options()


class Investing:
    def __init__(self):
        self.num = 0
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_drive)
        self.driver.get('https://vn.investing.com/equities/flc-group-jsc')
        self.driver.execute_script('overlay.overlayLogin();')

        username = self.driver.find_element_by_id("loginFormUser_email")
        username.send_keys('minhtc.uet@gmail.com')
        username = self.driver.find_element_by_id("loginForm_password")
        username.send_keys('minhminh6969')
        self.driver.execute_script('loginFunctions.submitLogin();')

    def _download(self, stock):
        time.sleep(5)
        self.driver.get('https://vn.investing.com{}-historical-data'.format(stock))
        self.driver.implicitly_wait(5)
        date_element = self.driver.find_element_by_id('flatDatePickerCanvasHol')
        date_element.click()
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_id('startDate').clear()
        start_date_element = self.driver.find_element_by_id('startDate')
        start_date_element.send_keys('01/01/2015')
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_id('endDate').clear()
        end_date_element = self.driver.find_element_by_id('endDate')
        end_date_element.send_keys('05/05/2020', Keys.ENTER)
        self.driver.implicitly_wait(5)
        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@title="Tải Dữ Liệu Xuống"]').click()

    def run(self, stocks):
        for stock in stocks:
            ic(self.num)
            try:
                self._download(stock)
            except Exception as e:
                logging.error(stock)
            self.num += 1

with open('../stock.json') as f:
    stocks = json.load(f)

Investing().run(stocks)
