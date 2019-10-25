import requests
from my_user_agent import get_user_agent
from selenium import webdriver
import time
from lxml import etree
import json
from queue import Queue
from gevent import monkey
import gevent
import random

# 有耗时操作时需要
monkey.patch_all()  # 将程序中用到的耗时操作的代码,换为genvent中自已实现的模块
# 西瓜美食频道
url = "https://www.ixigua.com/channel/meishi/"
headers = get_user_agent()
file_name = input("请输入要保存的文件名：")
path = r"C:\\Users\\Administrator\\Desktop\\youtube\\"
print(path)


chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
# 不加截图片,固定格式
options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
    }
}
options.add_experimental_option('prefs', prefs)
# 创建一个不加载图片的Chrom对象,传入参数
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)


def get_source(url):
    # chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    # browser = webdriver.Chrome(chromedriver)
    browser.get(url)
    time.sleep(2)
    for i in range(3):
        # 鼠标拉动滚动条
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage")
        time.sleep(1)

    source = browser.page_source
    browser.close()
    return source


def get_video_source(url):
    browser.get(url)
    time.sleep(3)
    browser.find_element_by_class_name("xgplayer-start").click()
    time.sleep(2)
    # for i in range(3):
    #     # 鼠标拉动滚动条
    #     browser.execute_script(
    #         "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage")
    #     time.sleep(1)

    source = browser.page_source
    browser.close()
    return source


def get_info(info_queue):
    """
    得到所有视频数据
    :return: 所有视频数据列表
    """
    html = get_source(url)
    # with open('text.html', "r",encoding="utf-8") as f:
    #     html = f.read()
    # print(html)
    e = etree.HTML(html)
    video_list = e.xpath('//div[@class="channel__module channel__module-more"]//div[@class="CardCommon__desc"]')
    # video_list = e.xpath('//div[@class="channel__module channel__module-more"]//div[@class="CardCommon__desc"]/a/@href')
    # print(video_list)
    v_infos = []
    for i in video_list:
        v_info = {}
        v_info["title"] = i.xpath('./a/@title')[0]
        v_info["url"] = "https://www.ixigua.com{}".format(i.xpath('./a/@href')[0])
        v_info["play"] = i.xpath('./p/text()')[0].split("播放")[0]
        v_info["comment"] = i.xpath('./p/text()')[0].split('·')[-1].split("评论")[0].replace("\xa0", "")
        # 保存数据

        # file_name = input("请输入要保存的文件名：")
        save_info(file_name, v_info)
        # 保存数据在列表v_infos中
        v_infos.append(v_info)
        # 保存数据在队列queue中
        info_queue.put(v_info)

        # 下载视频
        # get_video(v_info)
    # 返回所有视频数据 [{},{},..{}]
    return v_infos


def save_info(file_name, video_info):
    # a+ 为同一文件在文本最后添加
    with open(file_name, "a+", encoding="utf-8") as f:
        f.write(json.dumps(video_info, ensure_ascii=False) + "\n")
    print("下载完成")


def get_video(v_info):
    '''
    拿到视频能下载的url地址，并下载
    :param v_info: 视频信息 ：字典类型
    :return:
    '''
    url = v_info["url"]
    html = get_video_source(url)
    # print(html)
    e = etree.HTML(html)
    video_url = e.xpath('//div[@class="playerSection"]//video/@src')
    if len(video_url) > 0:
        video_url = video_url[0]
        print(video_url)
        # 保存视频
        # 使用requests发出请求，下载
        if "blob:" not in video_url:
            response = requests.get("http:" + video_url, stream=True, headers=headers)
            # 写入收到的视频数据
            file_name = "{}.mp4".format(v_info["title"])
            with open(path + file_name, 'ab') as f:
                f.write(response.content)
                # 刷新缓冲区
                f.flush()
                print("{} : 下载成功".format(v_info["title"]))
        else:
            print("这个方法找不到该视频: {}".format(v_info["title"]))
    else:
        print("没有可下载的视频.....")


if __name__ == '__main__':
    # 创建队列info_queue  存放字典数据
    info_queue = Queue()
    get_info(info_queue)
    video_info = info_queue.get()  # 字典
    print(video_info)
    # 多任务下载

    while info_queue.empty() == False:
        gevent.joinall([
            gevent.spawn(get_video, info_queue.get()),
            gevent.spawn(get_video, info_queue.get()),
            gevent.spawn(get_video, info_queue.get()),
            gevent.spawn(get_video, info_queue.get())
        ])
    print("所有的视频下载完成!!!!")
    # 退出浏览器
    # browser.quit()
