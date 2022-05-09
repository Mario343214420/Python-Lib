import requests
import time
import re
import pandas as pd
import math
from openpyxl.workbook import Workbook
dict_type = {'pg':'偏股型','gp':'股票型','hh':'混合型','zq':'债券型','zs':'指数型','qdii':'QDII','fof':'FOF','dqzq':'定开债券'}

def parse_stock():
    result = []
    for key in dict_type:
        # 获取页数
        url = f'https://fundapi.eastmoney.com/fundtradenew.aspx?ft={key}&sc=1n&st=desc&pi=1&pn=100&cp=&ct=&cd=&ms=&fr=&plevel=&fst=&ftype=&fr1=&fl=0&isab=1'
        headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Referer': 'http://fund.eastmoney.com/trade/zq.html'
        }
        response = requests.get(url, headers=headers)
        # if response.status_code = 200:
        html = response.text
        parrent = re.compile('datas:\["(.*?)\"],allRecords:(.*?),pageIndex', re.S)
        eastmoney_cnt = parrent.search(html).group(2)
        # print(eastmoney_cnt)

        # 查看每一个类型有多少页数
        eastmoney_cnt1 = math.ceil(int(eastmoney_cnt) / 100)+1
        # print(eastmoney_cnt1)

        for j in range(1,eastmoney_cnt1):
            # print(j)
            url = f'https://fundapi.eastmoney.com/fundtradenew.aspx?ft={key}&sc=1n&st=desc&pi={j}&pn=100&cp=&ct=&cd=&ms=&fr=&plevel=&fst=&ftype=&fr1=&fl=0&isab=1'
            headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Referer': 'http://fund.eastmoney.com/trade/zq.html'
            }
            response = requests.get(url,headers = headers)
            # if response.status_code = 200:
            html = response.text

            parrent = re.compile('datas:\["(.*?)\"],allRecords:(.*?),pageIndex', re.S)
            # eastmoney_links = re.findall(parrent, html)
            # if html:
            eastmoney_links = parrent.search(html).group(1)
            eastmoney_cnt = parrent.search(html).group(2)
            # print(eastmoney_cnt)

            # 查看每一个类型有多少页数
            eastmoney_cnt1 = math.ceil(int(eastmoney_cnt) / 100)

            print(eastmoney_cnt1)
            # print(eastmoney_links)
            resStr = re.sub(r'\|\|',',',eastmoney_links)
            resStr1 = re.sub(r'\|',',',resStr)
            # resStr1 = re.sub(r'\|',',',resStr)
            # print(resStr1)
            resStr_list = re.split(',',resStr1)
            # print(resStr_list)
            tmplist = []
            i = 0
            for res_result in resStr_list:
                tmplist.append(res_result)
                i = i+1
                # print(res_result)
                if re.search("\"$",res_result):
                    tmplist.insert(0,dict_type.get(key))
                    result.append(tmplist)
                    tmplist = []
            print(f'--------------其中{key}中的第{j}页已经打印完毕---------')
            time.sleep(2)

    # print("z转换字符串为列表：",result)
    html_list = []
    for item in result:
        # print(item)
        html_dict = {}
        if item[0].strip() in ['偏股型','FOF','定开债券']:
            html_dict['stock_type'] = item[0].strip()
            html_dict['stock_id'] = item[1].replace('\"','')
            html_dict['stock_name'] = item[2].strip()
            html_dict['stock_dwjz'] = item[3].strip()
            html_dict['stock_date'] = item[4].strip()
            html_dict['stock_rzzl'] = item[5].strip()
            html_dict['stock_jyz'] = item[6].strip()
            html_dict['stock_jyy'] = item[7].strip()
            html_dict['stock_jsy'] = item[8].strip()
            html_dict['stock_jly'] = item[9].strip()
            html_dict['stock_jyn'] = item[10].strip()
            html_dict['stock_jln'] = item[11].strip()
            html_dict['stock_jsn'] = item[12].strip()
            html_dict['stock_jnl'] = item[13].strip()
            html_dict['stock_cll'] = item[14].strip()
            html_dict['stock_sxf'] = item[-2].strip()
            html_dict['stock_qgje'] = item[-5].strip()
            html_list.append(html_dict)

        else:
            html_dict['stock_type'] = item[0].strip()
            html_dict['stock_id'] = item[1].replace('\"','')
            html_dict['stock_name'] = item[2].strip()
            html_dict['stock_dwjz'] = item[4].strip()
            html_dict['stock_date'] = item[5].strip()
            html_dict['stock_rzzl'] = item[6].strip()
            html_dict['stock_jyz'] = item[7].strip()
            html_dict['stock_jyy'] = item[8].strip()
            html_dict['stock_jsy'] = item[9].strip()
            html_dict['stock_jly'] = item[10].strip()
            html_dict['stock_jyn'] = item[11].strip()
            html_dict['stock_jln'] = item[12].strip()
            html_dict['stock_jsn'] = item[13].strip()
            html_dict['stock_jnl'] = item[14].strip()
            html_dict['stock_cll'] = item[15].strip()
            html_dict['stock_sxf'] = item[-2].strip()
            html_dict['stock_qgje'] = item[-5].strip()
            html_list.append(html_dict)

    # print(html_list)
    print('-----------------全部打印完成----------------')
    return html_list

# list_type = ['pg','gp','hh','zq','zs','qdii','fof','dqzq']

def html_to_csv():
    items = parse_stock()
    df = pd.DataFrame(items)
    df.columns = ['基金类型','基金代码','基金名称','日期','单位净值','日增长率','近1周','近1月','近3月','近6月','近1年','近2年','近3年','今年来','成立来','手续费','起购金额']
    # print(df)
    df.to_excel('./[size=13.0667px]基金清单汇总.xlsx',sheet_name='20210410',index=False)

if __name__ == '__main__':
        html_to_csv()