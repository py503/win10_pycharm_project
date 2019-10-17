from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.ixigua.com/channel/meishi/"
chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
browser = webdriver.Chrome(chromedriver)
browser.get(url)
for i in range(3):
    time.sleep(3)
    # 鼠标拉动滚动条
    # 向下偏移了10000个像素，到达底部。
    js = "var q=document.documentElement.scrollTop=10000"
    browser.execute_script(js)
source = browser.page_source
browser.quit()
print(source)
