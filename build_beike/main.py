import requests, codecs
import pymongo, time
from lxml import html
from multiprocessing import Pool
import json,re
import time

get_size = 60

community_list = []

def query_location(address):
    response = requests.get(
        'https://restapi.amap.com/v3/place/text?s=rsv3&children=&key=8325164e247e15eea68b59e89200988b&page=1&offset=10&city=320300&language=zh_cn&callback=jsonp_923197_&platform=JS&logversion=2.0&sdkversion=1.3&appname=https%3A%2F%2Flbs.amap.com%2Fconsole%2Fshow%2Fpicker&csid=EBD1553A-0C2B-4635-8D3E-A8DFF782C578&keywords=徐州' + address)

    res = str(response.content, encoding='utf-8')
    reStr = res.replace("jsonp_923197_(", '').replace(":[]}]})", ":[]}]}")
    # data = json.loads(reStr)
    locationData = re.search("\"location\"(.*?)\"tel\"",reStr).group()
    return locationData.replace(r'"location":"',"").replace(r'","tel"',"")

def get_content(j):
    print('正在爬取第 %s 页，还剩 %s 页' %(j, get_size - j))
    # print('正在爬取第{}页,还剩{}页'.format(j, 561 - j))

    url = 'https://xz.ke.com/ershoufang/pg'

    r = requests.get(url + str(j))

    if r.status_code == 200:

        text = html.fromstring(r.text)

        lenth = len(text.xpath('//li[@class="clear"]'))

        try:

            for i in range(0, lenth):
                # 链接
                urls = text.xpath('//li[@class="clear"]/a/@href')[i]

                # 小区
                community = text.xpath('//li[@class="clear"]/div/div[@class="address"]/div[@class="flood"]/div[@class="positionInfo"]/a')[i].text

                location = query_location(community)

                # 房屋信息
                info = html.tostring(text.xpath('//li[@class="clear"]/div/div[@class="address"]/div[@class="houseInfo"]')[i],encoding="utf8").decode('utf8').split('</span>')[1]

                # houseInfo = text.xpath('//li[@class="clear"]/div/div[@class="address"]/div[@class="houseInfo"]')[i].get()
                houseInfo = info.split('</div>')[0].replace('\n', '').replace('\r', '').replace(' ', '')

                # 成交价
                # deal = text.xpath('//li[@class="clear"]/div/div[@class="address"]/div[@class="priceInfo"]/div[@class="totalPrice"]/span')[i].text

                # 总价 （单位：万）
                totalprice = text.xpath('//li[@class="clear"]/div/div[@class="address"]/div[@class="priceInfo"]/div[@class="totalPrice"]/span')[i].text

                # 单价 （单位：元）
                avgprice = text.xpath('//li[@class="clear"]/div/div[@class="address"]/div[@class="priceInfo"]/div[@class="unitPrice"]/span')[i].text.replace('元/平米','').replace('单价','')

                # print('%s 万' %(deal))
                # onsale = text.xpath('//li[@class="clear"]/div/div[@class="address"]/div[@class="priceInfo"]/div[@class="totalPrice"]/span')[i].text
                # print(onsale)
                # 租金
                # rent = r.xpath('//ul[@class="pList"]/li[{0}]//div[2]/div[1]/p[1]/span[3]/a/text()'.format(i))[0].replace(
                #     '\r', '').replace('\n', '').strip()
                # 区域
                # addr = text.xpath('//ul[@class="pList"]/li[{0}]/div[2]/div[1]/p[3]/text()'.format(i))[0].replace('\r','').replace('\n','').strip()

                #
                # totalprice = r.xpath('//ul[@class="pList"]/li[{0}]//div[2]/div[1]/div/p[2]/text()'.format(i))[0]
                #
                output = "{}\t{}\t{}\t{}\t{}\t{}\n".format(community, avgprice, totalprice, urls, houseInfo, location)

                # print(output)
                savetoexcel(output)


        except Exception as e:

            print(e)

            print('爬取失败')
    else:
        return 'end'
def savetoexcel (output):
    try:
        time_stamp = time.strftime('%Y-%m-%d', time.localtime())
        f = codecs.open('house%s.xls'%time_stamp,'a+','utf-8')
        f.write(output)
        f.close()
    except Exception as e:
        print('写入失败')
        print(e)

# get_content(1)

stop_flag = True
page = 1
while stop_flag:
    res = get_content(page)
    page += 1
    if page == get_size:
        break


