import requests
import time
import hashlib
import random
import json
import os

# 爬取喜马雅的音乐的类
class Ximalaya(object):
    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        }

    def get_server_time(self):
        """
        获取喜马拉雅服务器的时间戳
        :return:
        """
        # 这个地址就是返回服务器时间戳的接口
        s_time_url = "https://www.ximalaya.com/revision/time"
        response = requests.get(s_time_url, headers=self.headers)
        return response.text

    def get_sign(self, server_time):
        """
        生成: xm-sign
        通过分析: xm-sign规则: md5(ximalaya-服务器时间戳)(100以内随机数)服务器时间戳(100以内随机数)现在时间戳
        :param server_time:
        :return:
        """
        now_time = str(round(time.time() * 1000))
        sign = str(hashlib.md5("ximalaya-{}".format(server_time).encode()).hexdigest()) + "({})".format(
            str(round(random.random() * 100))) + server_time + "({})".format(
            str(round(random.random() * 100))) + now_time
        # 将xm-sign添加到请求头中
        self.headers["xm-sign"] = sign
        print(self.headers)
        # return sign

    def get_info(self, albumId, pageNum, sort, pageSize):
        """
        获取数据
        :param albumId: 用户id
        :param pageNum: 第几页
        :param sort: sort
        :param pageSize: 一页有多少数据 默认是30
        :return:
        """
        # 先调用该言法获取xm-sign,添加到headers中
        self.get_sign(self.get_server_time())
        # 将参数写好
        params = {
            'albumId': albumId,
            'pageNum': pageNum,
            'sort': sort,
            'pageSize': pageSize
        }
        # 接口
        url = "https://www.ximalaya.com/revision/play/album"
        response = requests.get(url, params=params, headers=self.headers)
        response.encoding = "utf-8"
        infos = response.text
        # infos = json.loads(response.text)
        print(infos)
        for i in infos["data"]["tracksAudioPlay"]:
            trackName = i["trackName"].replace("【","").replace("】","").replace("！","").replace("：", "").strip()
            src = i["src"]
            self.save(albumId,trackName, src)

    def save(self, albumId, trackName, src):
        """
        下载音频
        :param albumId: 用户ID
        :param trackName: 标题信息
        :param src: 音频内容
        :return:
        """
        # 判断文件夹是否存在
        dir_path = albumId
        filename = trackName
        print(dir_path +"/"+ filename)
        if (os.path.exists(dir_path)):
            pass
            print("目录{}已经存在".format(dir_path))
        else:
            os.mkdir(dir_path)
            print("创建目录{}".format(dir_path))
        # 判断文件是否存在
        if (os.path.exists("./{}/{}".format(dir_path, filename))):
            pass
            print("文件{}已经存在".format(filename))
        else:
            # 读取音频
            print(src)
            response = requests.get(src)
            print(type(response.content))
            with open("./{}/{}".format(dir_path, filename), "wb") as f:
                f.write(response.content)
                print("下载完成!")




if __name__ == '__main__':
    ximalaya = Ximalaya()
    wanban = ximalaya.get_info('2881558','1','1','30')
