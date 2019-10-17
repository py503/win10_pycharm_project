#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-11-1 下午10:26
# @Author  : Py503
# @Email   : 172409222@qq.com
# @File    : 28.多线程的使用.py.py
# @Project : 13天搞定爬虫
# @Software: PyCharm
from queue import Queue
import requests
import my_user_agent
from threading import Thread
from lxml import etree


# 爬虫类
class CrawlInfo(Thread):
    def __init__(self, url_queue, html_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
        self.html_queue = html_queue

    def run(self):

        headers = my_user_agent.get_user_agent()
        # 判断队列中url_queue,是否为空,为空就停止
        while self.url_queue.empty() == False:
            response = requests.get(self.url_queue.get(), headers=headers)
            if response.status_code == 200:
                self.html_queue.put(response.text)
            # print(response.text)
            print("*" * 60)
            print(response.url)
            print("*" * 60)


# 解析类
class ParseInfo(Thread):
    def __init__(self, html_queue):
        Thread.__init__(self)
        self.html_queue = html_queue

    def run(self):
        num = 1
        while self.html_queue.empty() == False:
            Selector = etree.HTML(html_queue.get())
            span_text = Selector.xpath('//div[@class="content"]/span[1]')
            print(span_text)

            # with open("多线程爬取糗事百科.txt", 'a', encoding='utf-8') as f:
            #     for i in span_text:
            #         text = i.xpath('./text()[1]')
            #         f.write("".join(text) + "\n")
            #         print("*" * 60)
            #         print(text)
            #         print("*" * 60)
            #     print("解析第%d页" % num)
            #     num += 1


if __name__ == '__main__':
    # 存储url的容器
    url_queue = Queue()
    # 存储内容的容器
    html_queue = Queue()

    base_url = "http://www.qiushibaike.com/text/page/{}/"
    # 总共有13页
    for i in range(1, 14):
        url = base_url.format(i)
        url_queue.put(url)
        # print(url_queue.get())
        # print(url_queue)
        # print(url_queue)
    # # 创建一个爬虫
    # crawlinfo = CrawlInfo(url_queue)
    # # 开启爬虫
    # crawlinfo.start()

    # 创建三个线程爬数据
    crawl_list = []
    for i in range(0, 3):
        crawl_x = CrawlInfo(url_queue, html_queue)
        crawl_list.append(crawl_x)
        crawl_x.start()
    for crawl_x in crawl_list:
        crawl_x.join()

    # 创建三个线程保存数据
    parse_list = []
    for i in range(0, 3):
        parse_x = ParseInfo(html_queue)
        parse_list.append(parse_x)
        parse_x.start()
    for parse_x in parse_list:
        parse_x.join()
