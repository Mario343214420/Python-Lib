import requests
from bs4 import BeautifulSoup


def getUrl():
    headers = {
        "referer": "https://www.baidu.com/link?url=GgeDs1AzZQg7jAVgRWaaQVemNzUYNHFpN-PiFmUIyUHeaMQeoPb14_8g1oL7GmBggm70mm4e2EkM5F7lmQMUVq&wd=&eqid=fdcd73c000068a5900000004605ac987",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0"
    }
    url = 'https://www.tupianzj.com/meinv/mm/nkmv/'  # 其实这里改改 可以爬取更多分类 图片下面有显示

    urllist = []
    H = requests.get(url, headers=headers).text

    soup = BeautifulSoup(H, 'lxml').select('ul.d1.ico3>li>a')

    ullist = [i.get('href') for i in soup]
    for i in ullist:
        if '/meinv/' in i:
            urllist.append(i)
    return urllist


def getpage(imglist):
    for l in imglist:
        headers = {
            "referer": "https://www.baidu.com/link?url=GgeDs1AzZQg7jAVgRWaaQVemNzUYNHFpN-PiFmUIyUHeaMQeoPb14_8g1oL7GmBggm70mm4e2EkM5F7lmQMUVq&wd=&eqid=fdcd73c000068a5900000004605ac987",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0"
        }
        R = requests.get(f"https://www.tupianzj.com{l}", headers=headers).content.decode('gbk')
        imgsoup = BeautifulSoup(R, 'lxml').select('.pages > ul:nth-child(1) > li:nth-last-child(2)>a')[0].text
        for i in range(1, int(imgsoup) + 1):
            if i == 1:
                imgurl = BeautifulSoup(R, 'lxml').select('#bigpicimg')[0].get('src')
                tittle = BeautifulSoup(R, 'lxml').select('div.list_con:nth-child(3) > h1:nth-child(1)')[0].text
                with open(tittle + '.' + imgurl.split('.')[-1], 'wb') as f:
                    f.write(requests.get(imgurl, headers=headers).content)
                    f.close()
                print(tittle + "           保存成功！")
            else:
                imgurl = 'https://www.tupianzj.com' + l.replace('.html', '') + f'_{i}.html'
                req = requests.get(imgurl, headers=headers).content.decode('gbk')
                u = BeautifulSoup(req, 'lxml').select('#bigpicimg')[0].get('src')
                tittle = BeautifulSoup(req, 'lxml').select('div.list_con:nth-child(3) > h1:nth-child(1)')[0].text
                with open(tittle + '.' + u.split('.')[-1], 'wb') as f:
                    f.write(requests.get(u, headers=headers).content)
                    f.close()
                print(tittle + "           保存成功！")


if __name__ == '__main__':
    listur = getUrl()
    getpage(listur)