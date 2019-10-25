# 使用selenium爬取淘宝所有商品信息
from selenium import webdriver
import time
import re
import json


# 搜索商品
def search_product():
    browser.find_element_by_id("q").send_keys(keyworld)
    browser.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()
    time.sleep(15)
    # 找到一共有多少页
    # 一登录后,就能加载到最后,所以不用滚动鼠标都能找到最后一页
    token = browser.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[1]').text
    token = int(re.compile('(\d+)').search(token).group(1))
    print(token)
    return token


# 滚动鼠标加载js
def drop_down():
    for i in range(1, 11, 2):
        time.sleep(0.5)
        j = i / 10
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        browser.execute_script(js)
        # print(browser.page_source)


# 拿商品信息
def get_products():
    goods = {}
    # 取出所有div,然后再遍历所有的div,来取行没个商品的数据
    divs = browser.find_elements_by_xpath('//div[@class="items"]/div[@class="item J_MouserOnverReq  "]')
    for div in divs:
        goods["title"] = div.find_element_by_xpath('.//div[@class="row row-2 title"]/a').text
        goods["price"] = div.find_element_by_xpath('.//div[@class="row row-1 g-clearfix"]//strong').text
        goods["deal"] = div.find_element_by_xpath('.//div[@class="deal-cnt"]').text
        goods["shop_name"] = div.find_element_by_xpath('.//div[@class="shop"]').text
        goods["location"] = div.find_element_by_xpath('.//div[@class="location"]').text
        goods["image"] = div.find_element_by_xpath('.//div[@class="pic"]/a/img').get_attribute('src')
        print(goods)
        save(keyworld, goods)


# 保存数据
def save(filename, goods):
    # a+ 为同一文件在文本最后添加
    # 文件名加上时间
    now_time = time.strftime("%Y-%m-%d %H:%M:%S").replace(":", "-")
    filename = filename + now_time
    with open(filename, "a+", encoding="utf-8") as f:
        f.write(json.dumps(goods, ensure_ascii=False) + "\n")
    print("下载完成")


# 下一页url
def next_page():
    '''
    # 第1页
    url = "https://s.taobao.com/search?q=手机&s=0"
    # 第2页
    url = "https://s.taobao.com/search?q=手机&s=44"
    # 第三页
    url = "https://s.taobao.com/search?q=手机&s=88"
    '''
    token = search_product()
    num = 0
    while num != token:
        url = "https://s.taobao.com/search?q={}&s={}".format(keyworld, 44 * num)
        browser.implicitly_wait(10)
        # 加载下一页
        browser.get(url)
        # 滚动鼠标加载js后,再进行下步提取信息
        drop_down()
        # 处理信息并保存
        get_products()
        num += 1
    print("下载完成!")
    # 退出浏览器
    browser.quit()


if __name__ == '__main__':
    keyworld = input("请输入你要搜索的商品名: ")
    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    browser = webdriver.Chrome(chromedriver)
    url = "http://www.taobao.com"
    browser.get(url)
    next_page()
