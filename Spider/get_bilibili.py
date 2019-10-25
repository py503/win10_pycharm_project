import os
from queue import Queue
import requests
import json
from gevent import monkey
import gevent
import random

# 有耗时操作时需要
monkey.patch_all()  # 将程序中用到的耗时操作的代码,换为genvent中自已实现的模块

path = r"C:\\Users\\Administrator\\Desktop\\youtube\\youku\\"

def get_json(url):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }

    params = {
        'page_size': 10,
        'next_offset': str(num),
        'tag': '今日热门',
        'platform': 'pc'
    }
    try:
        html = requests.get(url ,params=params ,headers=headers)
        print(html.url)
        print(html.json())
        return html.json()

    except BaseException:
        print('request error')
        pass

# 处理视频数据
def get_info(dicts, info_q):
    video_infos = []
    info = {}
    res_list = dicts['data']['items'] # 从字典中取出信息
    for i in res_list:
        info['id'] = i['item']['id']
        info['description'] = i['item']['description']
        info['video_playurl'] = i['item']['video_playurl']
        video_infos.append(info)
        info_q.put(info)
        print(info)
    print(video_infos)


# 下载视频
def download(info):
    url = info['video_playurl']
    cmd = 'you-get -o {} {}'.format(path, url)
    print(cmd)
    os.system(cmd)
    print("{}===========下载完成".format(info['description']))


if __name__ == '__main__':
    url = "http://api.vc.bilibili.com/board/v1/ranking/top?"
    num = 21
    info_q = Queue()
    get_info(get_json(url), info_q)
    print("所有的视频下载完成!!!!")
