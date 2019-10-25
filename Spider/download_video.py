import requests
from my_user_agent import get_user_agent


def get_video(file_name, url):
    '''
    拿到视频能下载的url地址，并下载
    :param: file_name 名字
    :param  url 下载链接
    :return:
    '''
    # 使用requests发出请求，下载
    response = requests.get(url, stream=True, headers=get_user_agent())
    if response.status_code == 200:
        # 写入收到的视频数据
        with open(file_name, 'ab') as f:
            f.write(response.content)
            # 刷新缓冲区
            f.flush()
            print("下载成功")
    else:
        print("找不到该视频。。。。")


def main():
    # file_name = input("请输入要保存的名字: ")
    # url = input("请输入要下载视频的地址: ")
    file_name = "2019天猫双11开幕盛典 易烊千玺开场献唱，一开口好听到爆.mp4"
    url = "http://v1-tt.ixigua.com/a50cbf284f6a14683404ae39061423fd/5dad3153/video/tos/cn/tos-cn-ve-26/8d8d52acc0094169b05ab0257c7f97bc/?a=1768&br=959&cr=0&cs=0&dr=0&ds=3&er=&l=20191021111230010014051083125DC2AC&lr=&rc=M3A5N2gzOnlmcDMzM2QzM0ApNzc1ZWhlNmRnNzM2ODtnM2cwYW4xb3JeLmpfLS0zLi9zczNeLjI0YGIzYGBgYTYzMDM6Yw%3D%3D"
    url = "http://vd2.bdstatic.com/mda-jjkuwpja1nzxybe3/sc/mda-jjkuwpja1nzxybe3.mp4"
    get_video(file_name, url)


if __name__ == '__main__':
    main()
