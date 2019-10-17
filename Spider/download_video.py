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
    file_name = "教你家庭自制油条"
    url = "https://v1-tt.ixigua.com/66bdc84fa6a8bb4ff2fb0955ac2afecc/5da87119/video/m/22071ef3d3f8c1f47f2bfd08e0c4075cbd311612a3da0000adc5080ed4bf/?a=1768&amp;br=1081&amp;cr=0&amp;cs=0&amp;dr=0&amp;ds=3&amp;er=&amp;l=201910172044160100140510930CBA0EFC&amp;lr=&amp;rc=MzhpbGVneTl0ajMzPDczM0ApOTw2ODY4ZDtoNzw4aTs1ZmdqcTNjNGkzX2dfLS1jLS9zczUyNC9jNTJhYS5hYmBgLTM6Yw%3D%3D"
    get_video(file_name, url)


if __name__ == '__main__':
    main()
