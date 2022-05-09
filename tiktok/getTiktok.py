#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:ZQ
# datetime:2020/8/24 13:47
# software: PyCharm

import requests, json, re

class DY:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3904.108 Safari/537.36'}
        self.android_headers = {'user-agent': 'Android'}

    def get_share_url(self, url):
        response = requests.get(url, headers=self.headers, allow_redirects=False)
        if 'location' in response.headers.keys():
            return response.headers['location']
        else:
            raise Exception("解析失败")
        pass

    def get_data(self, url):
        response = requests.get(url, headers=self.headers).text
        json_str = json.loads(response)
        download_url = json_str['item_list'][0]['video']['play_addr']['url_list'][0].replace("playwm", "play")
        name = input('===>正在下载保存视频,请输入视频名称：')
        with open(name + '.mp4', 'wb') as f:
            f.write(requests.get(url=download_url, headers=self.android_headers).content)
            pass
        print('视频下载完成!')
        pass

    def run(self):
        share = input("请输入你要去水印的抖音短视频链接：")
        url = re.findall(r'https://v.douyin.com/.*?/', share)[0]
        location = self.get_share_url(url)
        vid = re.findall(r'/share/video/(\d*)', location)[0]
        xhr_url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={}'.format(vid)
        self.get_data(xhr_url)

if __name__ == '__main__':
    dy = DY()
    dy.run()