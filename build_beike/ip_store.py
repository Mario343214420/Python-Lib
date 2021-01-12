from urllib import request
from fake_useragent import FakeUserAgent
from bs4 import BeautifulSoup
import re
class GetProxy(object):
    def __init__(self, url = ''):
        self.baseurl = ''
        self.ua = FakeUserAgent()
        self.pools = []
    def getIps(self):
        return self.pools
    def getByApi(self, url):
        content = self.reqPage(url)
        if content:
            # 处理content
            obj = BeautifulSoup(content, 'html.parser')
            ip_list = [item for item in obj.stripped_strings if re.match(r'\d', item)]
            self.pools.extend(ip_list)
    def start(self):
        con = self.reqPage(self.baseurl)
        obj = BeautifulSoup(con, 'html.parser')
        areas = obj.find('ul', class_='textlarge22')
        if areas:
            lista = areas.find_all('a')
            if lista:
                for a in lista:
                    step = a.get('href')
                    if step:
                        self.parseArea(self.baseurl + step)
    def getCharset(self, content):
        scon = str(content)
        meta = re.search(r'<meta(.*?)content-type(.*?)>', scon, re.I)
        if meta:
            res = meta.group()
            m = re.search(r'charset=(.*?)[\"\' /]', res, re.I)
            if m:
                charset = m.groups()[0]
                return charset
        return 'utf-8'

    def reqPage(self, url):
        headinfo = {'UserAgent': self.ua.random}
        reqhd = request.Request(url, headers=headinfo)
        try:
            req = request.urlopen(reqhd)
        except Exception as e:
            print('Error:', e)
        if req.code != 200:
            return
        con = req.read()
        charset = self.getCharset(con)
        try:
            con = con.decode(charset)
        except Exception as e:
            print('decode Error:', e)
        return con
    def parsePage(self):
        pass
    def parseArea(self, url):
        print(url)
        con = self.reqPage(url)
        obj = BeautifulSoup(con, 'html.parser')
        listpage
if __name__ =='__main__':
    apiurl = 'http://www.66ip.cn/mo.php?sxb=&tqsl=1000&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea='
    starturl = 'http://www.66ip.cn'
    proxyhd = GetProxy(url = starturl)
    proxyhd.start()
    proxyhd.getByApi(apiurl)
    ips = proxyhd.getIps()
    print(len(ips))
    for ip in ips:
        print(ip)