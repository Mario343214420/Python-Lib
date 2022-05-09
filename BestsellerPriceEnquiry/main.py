import requests
import time
import json
import re
import xlwings as xw
import datetime

def crawl_jd_books():
    # 设置请求头部，伪装ua
    headers = {
        'User-Agent': 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'referer': 'https://book.jd.com/'}
    # 设置存储图书信息的列表，当然也可以用其他的方式存储
    books_info = []
    # 页面只有5页，设置一个循环就可以
    for n in range(1, 6):
        # 方式一：直接复制数据包里编码好的url进行访问
        # url = f'https://gw-e.jd.com/client.action?callback=func&body=%7B%22moduleType%22%3A1%2C%22page%22%3A{n}%2C%22pageSize%22%3A20%2C%22scopeType%22%3A1%7D&functionId=bookRank&client=e.jd.com&_={str(int(round(time.time() * 1000)))}'
        # response = requests.get(url,headers=headers)
        # 方式二：通过json解码进行dumps这个，通过params方式提交
        # moduleType取值（1，2）代表图书销量榜和新书热卖榜，page代表页数，scopetype(1,2,3)表示榜单的选择（其中月榜后面会多一个month的参数代表月份）
        # {"moduleType":1,"page":1,"pageSize":20,"scopeType":3,"month":1}
        body = json.dumps({"moduleType": 1, "page": n, "pageSize": 20, "scopeType": 1})
        param = {
            "callback": "func",
            "body": body,
            "functionId": "bookRank",
            "client": "e.jd.com",
            "_": int(round(time.time() * 1000))  # 13位时间戳
        }
        url = 'https://gw-e.jd.com/client.action'
        response = requests.get(url, params=param, headers=headers)
        # 返回的并非标准的json格式，通过正则进行处理取值，然后通过json处理标准
        json_deal = re.search('func\((.*?)\}\)', response.text).group(1) + '}'
        json_back = json.loads(json_deal)
        book_list = json_back['data']['books']
        for i in book_list:
            # 图书id
            book_id = i['bookId']
            # 图书名称
            book_name = i['bookName']
            # 图书出版社
            publisher = i['publisher']
            # 图书链接
            item_url = f'https://item.jd.com/{book_id}.html'
            # 京东售价
            sell_price = i['sellPrice']
            # 原有定价
            define_price = i['definePrice']
            if define_price == '':
                old_price = 0
            else:
                old_price = define_price
            books_info.append((book_id, book_name, sell_price, old_price, publisher, item_url))
    return books_info


if __name__ == '__main__':
    ft = open("a.txt", 'w')
    wb = xw.Book("e:\example.xlsx")
    sht = wb.sheets["sheet1"]

    sht.range('A1').value = crawl_jd_books()
    for entry in crawl_jd_books():
        print(entry)
    ft.close()