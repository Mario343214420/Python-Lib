import requests
import time
import re
import pandas as pd
import math

def get_url():
    list_url = []
    df = pd.read_excel('./基金清单汇总.xlsx',sheet_name='Sheet5',index_col=None)
    # print(df)
    data = df['基金代码']
    # print(data)

    for data_item in data:
        stock_dict ={}
        test = (6-len(str(data_item))) * '0'
        stock_id = test + str(data_item)
        url = f'http://fund.eastmoney.com/{stock_id}.html?spm=search'
        # print(url)
        list_url.append(url)
    # print(list_url)
    return list_url

def parse_stock():
    list_url = get_url()
    html_list = []
    i = 0
    for url in list_url:
        # print(url)
        headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Referer': 'http://fund.eastmoney.com/'
        }
        response = requests.get(url, headers=headers)
        # print(response.apparent_encoding)
        html = response.content.decode('UTF-8-SIG')
        # print(html)
        parrent = re.compile('"><title>(.*?)基金净值_估值_行情走势—天天基金网.*?基金类型：.*?">(.*?)</a>.*?基金规模</a>：(.*?)</td><td>基金经理：<a href="(.*?)">(.*?)</a>.*?成 立 日</span>：(.*?)</td><td>.*?管 理 人</span>：<a href="(.*?)">(.*?)</a></td><td><a class="floatleft" href="(.*?)">基金评级.*?</span><div class="(.*?)">',re.S)
        items = re.findall(parrent, html)
        # print(items)
        for item in items:
            html_list.append(item)
        time.sleep(2)
        i = i+1
        print(f'----------开始打印第{i}条数据------------------')
    # print(html_list)
    return html_list

def trans_df():
    html_list = []
    result = parse_stock()
    for item in result:
        # print(item)
        html_dict = {}
        html_dict['stock_name'] = item[0].strip()
        html_dict['stock_type'] = item[1].strip()
        html_dict['stock_zjje'] = item[2].strip()
        html_dict['stock_url'] = item[3].strip()
        html_dict['stock_jjjl'] = item[4].strip()
        html_dict['stock_clrq'] = item[5].strip()
        html_dict['stock_jlurl'] = item[6].strip()
        html_dict['stock_jjglr'] = item[7].strip()
        html_dict['stock_glrurl'] = item[8].strip()
        html_dict['stock_jjpj'] = item[9].strip()
        html_list.append(html_dict)
    print(html_list)
    return html_list

def html_to_csv():
    items = parse_stock()
    df = pd.DataFrame(items)
    df.columns = ['基金名称','基金类型','基金规模','净值链接','基金经理','成立日期','基金经理链接','基金管理人','基金管理人链接','基金评级']
    # print(df)
    df.to_excel('./基金基本情况-股票型.xlsx',sheet_name='20210410',index=False)

if __name__ == "__main__":
    html_to_csv()