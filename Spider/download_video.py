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
    file_name = "麻辣小龙虾的正确做法，厨师长全过程视频演示，揭秘详细配料秘方.mp4"
    url = "https://v1-tt.ixigua.com/66bdc84fa6a8bb4ff2fb0955ac2afecc/5da87119/video/m/22071ef3d3f8c1f47f2bfd08e0c4075cbd311612a3da0000adc5080ed4bf/?a=1768&amp;br=1081&amp;cr=0&amp;cs=0&amp;dr=0&amp;ds=3&amp;er=&amp;l=201910172044160100140510930CBA0EFC&amp;lr=&amp;rc=MzhpbGVneTl0ajMzPDczM0ApOTw2ODY4ZDtoNzw4aTs1ZmdqcTNjNGkzX2dfLS1jLS9zczUyNC9jNTJhYS5hYmBgLTM6Yw%3D%3D"
    url = "http://v1-tt.ixigua.com/6cfda817c4caf963d6d71e1036a03eb4/5da955d2/video/m/22015706c7cba2448c9b8456b520afe7d75116134f160000357f29442a7e/?a=1768&br=1286&cr=0&cs=0&dr=0&ds=3&er=&l=201910181302170100140510941221B93D&lr=&rc=ajk3bHZzZDM2ajMzZjczM0ApOWk0ZjozaGRkN2ZlZmQ1O2cyaGA0Yi9sMmpfLS00LS9zc2BgMDJhYTU1My9iX2JeXy06Yw%3D%3D"
    url = "http://v1-tt.ixigua.com/c13d1bf9d357aaed5515b9dbe926ba77/5da979f1/video/m/220b57e65dd4b754bcbab5bc5e61a0bd48b1161b57e80000a07459629f5a/?a=1768&br=1953&cr=0&cs=0&dr=0&ds=3&er=&l=20191018153600010014051091172B7B3C&lr=&rc=M2hpeXlmczVnbDMzOzczM0ApNjQ0OGdmOjs7NzY3aTo5M2dlanBhL2dtL2NfLS01LS9zcy80YDViNi0vYDRjXjZhYy06Yw%3D%3D"
    url = "http://v1-tt.ixigua.com/fa52d841ecbe184f0910061c2ef191cf/5da98fb2/video/m/220b57e65dd4b754bcbab5bc5e61a0bd48b1161b57e80000a07459629f5a/?a=1768&br=1953&cr=0&cs=0&dr=0&ds=3&er=&l=201910181708490100140510822D1FFECC&lr=&rc=M2hpeXlmczVnbDMzOzczM0ApNjQ0OGdmOjs7NzY3aTo5M2dlanBhL2dtL2NfLS01LS9zcy80YDViNi0vYDRjXjZhYy06Yw%3D%3D"
    url = "http://v1-tt.ixigua.com/500a427a7c6e9c70abe27c433f9a577b/5da9a19e/video/m/220e7fec543b5eb47f7968b7740b3fb97d611574c300000619fc4cab46c/?a=1768&br=1630&cr=0&cs=0&dr=0&ds=3&er=&l=201910181824590100140510950C0BB126&lr=&rc=ank2ZG43dGV3ZTMzODczM0ApaTllZjRmZmVmNztoN2g8OWcucy1lcHBwcnNfLS1jLS9zczJjMTQzLzQ1Ml4yMmMzNDU6Yw%3D%3D"
    get_video(file_name, url)


if __name__ == '__main__':
    main()
