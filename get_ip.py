# -*- codec: utf-8 -*-
import re
from selenium import webdriver

def get_ip():
        driver = webdriver.Safari()
        driver.get('http://www.j4.com.tw/james/remoip/')
        match = re.search('(\d+.\d+.\d+.\d+)', driver.page_source)
        text = match.group(1) if match else '0.0.0.0'
        driver.quit()
        return text
