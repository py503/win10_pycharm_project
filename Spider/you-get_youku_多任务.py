import os
import you_get
import sys
path = r"C:\\Users\\Administrator\\Desktop\\youtube\\"


# 使用you-get 下载网络视频
def download(url):
    # 写法1
    # cmd = 'you-get -o {} {}'.format(path, url)
    # print(cmd)
    # os.system(cmd)

    # 写法2
    sys.argv = ['you-get', '-o', path, url]
    you_get.main()
    print("下载完成")

if __name__ == '__main__':
    # url = input("请输入你要下截视频的url: ")
    url = "https://v.youku.com/v_show/id_XNDI0NjcxMzYwOA==.html?spm=a2h0k.11417342.soresults.dposter"
    download(url)
    for i in range(11):
        next_offset = 30 * i
        url = "http: // api.vc.bilibili.com / clip / v1 / video / index?page_size = 30 & need_playurl = 0 & next_offset = {} & has_more = 1 & order = & platform = pc".format(next_offset)
