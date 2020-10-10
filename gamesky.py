import requests
import os, stat
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
path = './images/'
def download_page(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r = requests.get(url, headers=headers)
    return r.text


def get_content(html, page):
    soup = BeautifulSoup(html, 'html5lib')
    con = soup.find('body')
    con_list = con.find('div', class_="Mid2L_con")
    imgList = con_list.find_all("img", class_='picact')
    for index in range(len(imgList)):
        print('p:', page, index)
        for j in range(len(imgList)):
            save_img(imgList[j]['src'])
    # for i in con_list:
    #     print(i)
    # for i in range(len(con_list)):
    #     imgList = con_list[i].find_all("img", class_='picact')
    #     for j in range(len(imgList)):
    #         save_img(imgList[j]['src'])


def save_img(src):
    try:
        # 是否有这个路径
        if not os.path.exists(path):
            # 创建路径
            os.makedirs(path)
            # 获得图片后缀
        file_suffix = os.path.splitext(src)[1]
        name = os.path.basename(src)
        # downloadPath = './images/{a}{b}'.format(a=name, b=file_suffix)
        downloadPath = './images/{a}'.format(a=name)
        print(downloadPath)
        urlretrieve(src, downloadPath)
    except IOError as e:
        print("IOError")
    except Exception as e:
        print("Exception")

def main():
    # 我们点击下面链接，在页面下方可以看到共有13页，可以构造如下 url，
    # 当然我们最好是用 Beautiful Soup找到页面底部有多少页。
    for i in range(2, 40):
        url = 'https://www.gamersky.com/ent/202010/1327173_{}.shtml'.format(i)
        html = download_page(url)
        get_content(html, i)

if __name__ == '__main__':
    main()