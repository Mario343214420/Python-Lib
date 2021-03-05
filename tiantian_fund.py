import os, sys
import time
import requests

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('My Lord')

# url = input('请输入网址') or 'https://www.3dmgame.com/bagua/3944.html'
url_base = input('请输入代码：') or '519300'
url = 'http://fund.eastmoney.com/pingzhongdata/%s.js' % url_base

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

time_stamp = time.strftime('%Y-%m-%d', time.localtime())

template = ''

if not os.path.exists(time_stamp):
    os.mkdir(time_stamp)
with open(str(time_stamp) + '/' + url_base + '.js', 'a',encoding='utf-8') as file:
    file.write(start_request(url))
with open(str(time_stamp) + '/' + url_base + '.html', 'a', encoding='utf-8') as file:
    file.write(template)