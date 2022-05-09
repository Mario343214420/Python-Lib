
import requests
import json
import re
import pandas as pd
import time

def get_data(code,name,page=233):
    df_list = []
    for index in range(page):
        url = 'http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery18308375575830705777_1615814760997&fundCode={}&pageIndex={}&pageSize=20&startDate=&endDate=&_=1615815223845'.format(code,index)
        headers = {
            'Referer': 'http://fund.eastmoney.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        resp = requests.get(url, headers = headers)
        html = resp.text
        res = re.findall('\((.*?)\)',html)
        datas = json.loads(res[0])["Data"]["LSJZList"]
        df = pd.DataFrame(datas)
        print(df)
        df_list.append(df)
    df_data = pd.concat(df_list)
    df_data.to_csv('./{}.csv'.format(name,code),encoding='utf-8-sig' ,index=False)
    print(df_data)

def get_fund_ranking(num):
    base_url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=6yzf&st=desc&sd=2020-03-15&ed=2021-03-15&qdii=&tabSubtype=,,,,,&pi={}&pn=50&dx=1&v=0.9215528965887285'.format(num)
    headers = {
        # 防盗链 确定来路
        'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
        # 身份证
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    response = requests.get(base_url, headers=headers)
    # print(response.text)
    result = re.findall('"(.*?)"', response.text)
    print(result)
    print(len(result))
    for i in result:
        code = i.split(',')[0]
        name = i.split(',')[1]
        get_data(code, name)
        time.sleep(5)

get_fund_ranking(1)