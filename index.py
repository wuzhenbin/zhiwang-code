
# chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\package\selenium"
# 'Google Chrome' --remote-debugging-port=9222 --user-data-dir="/Users/chenpin/Downloads/package/seleium"

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
import re, time, os
from PIL import Image
import pytesseract

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
        if 'id' in getCodeID:
            pattern =  re.compile('.*id=(.*)',re.S)
            result =  re.match(pattern,getCodeID)
            return result[1]
        else:
            return 'first_code'

    def img_handle(self,target):
        fromImage = Image.open(os.getcwd()+'\\'+target)
        fromImage = fromImage.convert('L') 
        threshold = 135 
        table = [] 
        for i in range(256): 
            if i < threshold: 
                table.append(0)

            else: 
                table.append(1)

        fromImage = fromImage.point(table,'1') 
        fromImage.save(os.getcwd()+'\\'+target)

    # 获取多张训练图片
    def mult_get_code_img(self):
        for item in range(20):
            checkcode_tap = self.wait.until(EC.presence_of_element_located((By.ID, 'checkcode')))
            save_path = './imgs/{}.png'.format(self.get_code_name())

            # 截图
            ele = self.browser.find_element_by_id('checkcode')
            ele.screenshot(save_path)

            checkcode_tap.click()
            time.sleep(1)

    # 测试训练集
    def test_code(self):
        txtOldCheckCode = self.wait.until(EC.presence_of_element_located((By.ID, 'txtOldCheckCode')))

        file = self.get_code_name() + '.png'
        save_path = './{}'.format(file)

        # 截图
        ele = self.browser.find_element_by_id('checkcode')
        ele.screenshot(save_path)

        # 二值化灰度处理
        self.img_handle(file)

        # 识别
        image = Image.open(file) 
        res = pytesseract.image_to_string(image,lang='font')

        # 将识别结果放入对应输入框
        txtOldCheckCode.clear()
        txtOldCheckCode.send_keys(res)


if __name__ == '__main__':
    crack = Crack()
    crack.test_code()