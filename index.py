
# chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\package\selenium"
# 'Google Chrome' --remote-debugging-port=9222 --user-data-dir="/Users/chenpin/Downloads/package/seleium"

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
import re
import time

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")


class Crack():
    def __init__(self):
        self.url = 'http://my.cnki.net/elibregister/commonRegister.aspx#'
        self.browser = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.browser, 100)
        # self.browser.get(self.url)

    def get_code_name(self):
        doc = pq(self.browser.page_source)
        getCodeID = doc('#checkcode').attr('src')
        pattern =  re.compile('.*id=(.*)',re.S)
        result =  re.match(pattern,getCodeID)
        return result[1]

    def mult_get_code_img(self):
        checkcode_tap = self.wait.until(EC.presence_of_element_located((By.ID, 'checkcode')))
        save_path = './imgs/{}.png'.format(self.get_code_name())

        # 截图
        ele = self.browser.find_element_by_id('checkcode')
        ele.screenshot(save_path)

        checkcode_tap.click()
        time.sleep(1)

if __name__ == '__main__':
    crack = Crack()
    # for item in range(20):
    #     crack.mult_get_code_img()