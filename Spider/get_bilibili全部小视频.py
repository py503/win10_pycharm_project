import os
import re
from queue import Queue
from threading import Thread
import requests
import my_user_agent
import json
# from gevent import monkey
import gevent
import random

# 有耗时操作时需要
# monkey.patch_all()  # 将程序中用到的耗时操作的代码,换为genvent中自已实现的模块

path = r"C:\\Users\\Administrator\\Desktop\\youtube\\youku\\"
headers = my_user_agent.get_user_agent()


# 爬虫类(json_url)
class CrawlInfo(Thread):
    def __init__(self, url_q, info_q):
        Thread.__init__(self)
        self.url_q = url_q
        self.info_q = info_q

    def run(self):

        # params = {
        #     'page_size': 10,
        #     'next_offset': str(num),
        #     'tag': '今日热门',
        #     'platform': 'pc'
        # }
        video_infos = []
        while self.url_q.empty() == False:
            url = self.url_q.get()
            html = requests.get(url, headers=headers)
            # print(html.url)
            # print(html.json())
            v_info = html.json()  # 字典类型
            # 处理视频数据
            res_list = v_info['data']['items']  # 从字典中取出信息
            for i in res_list:
                info = {}
                info['id'] = i['item']['id']
                info['description'] = i['item']['description']
                info['video_playurl'] = i['item']['video_playurl']
                video_infos.append(info)
                # 打每个视频信息放入队列
                self.info_q.put(info)


# 下载视频类
class Download(Thread):
    def __init__(self, info_q):
        Thread.__init__(self)
        self.info_q = info_q

    def run(self):
        while self.info_q.empty() == False:
            info = self.info_q.get()
            url = info['video_playurl']

            # 方法1 使用you-get下载
            # cmd = 'you-get -l -o {} {}'.format(path, url)
            # os.system(cmd)
            # print(info['id'], ":" , info['description'], "下载成功")

            # 方法2
            response = requests.get(url, stream=True, headers=headers)
            # 写入收到的视频数据
            if response.status_code == 200:
                # 去除标题特殊字符,用于命名文件名
                res = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
                title = res.sub("", info["description"])
                file_name = "{}.mp4".format(title)
                with open(path + file_name, 'ab') as f:
                    f.write(response.content)
                    # 刷新缓冲区
                    f.flush()
                    print("{} : 下载成功".format(file_name))
            else:
                print("这个方法找不到该视频")


if __name__ == '__main__':
    # 创建url队列
    url_q = Queue()
    # 创建信息队列
    info_q = Queue()
    n = input("请输入想要下载bilibli小视频的页数: ")
    for i in range(int(n)):
        next_offset = 30 * (i)
        url = "http://api.vc.bilibili.com/clip/v1/video/index?page_size=30&need_playurl=0&next_offset={}&has_more=1&order=&platform=pc".format(
            next_offset)
        url_q.put(url)
    # 创建三个线程爬数据
    crawl_list = []
    for i in range(0, 3):
        crawl_x = CrawlInfo(url_q, info_q)
        crawl_list.append(crawl_x)
        crawl_x.start()
    for crawl_x in crawl_list:
        crawl_x.join()

    # 创建三个线程保存数据
    parse_list = []
    for i in range(0, 3):
        parse_x = Download(info_q)
        parse_list.append(parse_x)
        parse_x.start()
    for parse_x in parse_list:
        parse_x.join()

    print("所有的视频下载完成!!!!")
