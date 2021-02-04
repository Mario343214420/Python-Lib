import os, sys
import time
import requests
from bs4 import BeautifulSoup
from tqdm import trange

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('My Lord')

# url = input('请输入网址') or 'https://www.3dmgame.com/bagua/3944.html'
url_base = input('请输入网址，截止至.html前  ') or 'https://www.3dmgame.com/bagua/3944'
time_stamp = time.strftime('%Y-%m-%d', time.localtime())

if not os.path.exists(time_stamp):
    os.mkdir(time_stamp)


def start_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    if r.status_code == 200:
        return r.text
    else:
        print('{}地址有误，可能已超过最后一页'.format(url))
        return None


# html = start_request(url, 1)

def save_gif(html_text):
    _str = ''
    soup = BeautifulSoup(html_text, 'html5lib').find_all('p', attrs={"align": "center"})
    def save_img(res_img_url, name):
        res_img = requests.get(res_img_url).content
        with open('./' + time_stamp + '/' + name, 'wb') as f:
            f.write(res_img)
            f.close()

    for i in soup:
        img = i.find('img')
        if img:
            src = img.get('src')
            names = src.split(r"/")
            _src = names[-1].replace(':', '').replace('~', '').replace('-', '')
            if _src.find('.') == -1:
                _src += '.gif'
            save_img(src, _src)
            _str += '\n<img src="%s"/>' % (_src)
    return _str

def save_html(imgs_html):
    def return_html_str(str):
        html_str = '<html lang="en"><head><title>图</title><meta charset="utf-8"><style>%s</style></head><body><br><p class="tip">图片较多，滑到底部需等待加载。</p><br>%s</body></html>' % ("img { display:block; width: 100% } \n.tip {font-size: 3rem}", str)
        return html_str

    with open(time_stamp + '/index.html', 'w', encoding="utf-8") as f:
        html = return_html_str(imgs_html)
        f.write(html)
        f.close()

def request_each_html(url):
    html_str = ''
    html = None
    for i in trange(20):
        if i == 0:
            html = start_request('{}.html'.format(url))
            html_str += save_gif(html)
            save_gif(html)
        else:
            html = start_request('{}_{}.html'.format(url, i + 1))
            html_str += save_gif(html)
            save_gif(html)

    save_html(html_str)
    print('任务完成')


request_each_html(url_base)
