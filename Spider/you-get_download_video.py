import os


path = r"C:\\Users\\Administrator\\Desktop\\youtube\\"


# 使用you-get 下载网络视频
def download(url):
    cmd = 'you-get -o {} {}'.format(path, url)
    print(cmd)
    os.system(cmd)
    print("下载完成")



if __name__ == '__main__':
    # url = input("请输入你要下截视频的url: ")
    url = "https://v.youku.com/v_show/id_XNDI0NjcxMzYwOA==.html?spm=a2h0k.11417342.soresults.dposter"
    download(url)