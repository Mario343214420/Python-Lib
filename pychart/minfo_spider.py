import re
# import html5lib
from urllib import request
from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent
base_url = 'http://www.66ip.cn/mo.php?sxb=&tqsl=2000&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea='
starturl = 'http://www.66ip.cn'
url = 'https://www.89ip.cn/tqdl.html?num=60&address=&kill_address=&port=&kill_port=&isp='
ua = FakeUserAgent()
headinfo = {'UserAgent': ua.random}
reqhd = request.Request(url, headers=headinfo)
req = request.urlopen(reqhd)
con = req.read().decode('utf-8')
obj = BeautifulSoup(con, 'html5lib')
list_ip = [item for item in obj.stripped_strings if re.match(r'((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))', item)]
print(len(list_ip))
