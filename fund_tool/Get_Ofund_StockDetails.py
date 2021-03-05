import os
import mysql.connector  #mysql数据库操作增加
import requests
import math #进度条实现增加
import time #时间延时实现增加
import sys  #进度条实现增加
import threading    #多线程增加
import re
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


nPos=0  #全局变量，用作进度条显示进度

#多线程
class myThread (threading.Thread):
    def __init__(self, threadID, name,fund_url, fund_name, begin_num, end_num):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.fund_url = fund_url
        self.fund_name = fund_name
        self.begin_num = begin_num
        self.end_num = end_num
    def run(self):
        print ("开始线程：" + self.name)
        Get_stock_detail(self.fund_url, self.fund_name, self.begin_num, self.end_num)
        print ("退出线程：" + self.name)


# 判断字符串中是否含有中文
def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


# selenium通过class name判断元素是否存在，用于判断基金持仓股票详情页中该基金是否有持仓股票；
def is_element(driver, element_class):
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, element_class)))
    except:
        return False
    else:
        return True


# requests请求url的方法,处理后返回text文本
def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    proxies = {
        "http": "http://XX.XX.XXX.XXX:XX"
    }

    response = requests.get(url, headers=headers) #, proxies=proxies
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.text
    else:
        print("请求状态码 != 200,url错误.")
        return None


# 该方法直接将首页的数据请求、返回、处理，组成持仓信息url和股票名字并存储到数组中；
def page_url():
    fund_url = []  # 定义一个数组，存储基金持仓股票详情页面的url
    ofstock_name = []  # 定义一个数组，存储基金的名称
    url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd=2018-11-26&ed=2019-11-26&qdii=&tabSubtype=,,,,,&pi=1&pn=10000&dx=1&v=0.234190661250681"
    result_text = get_one_page(url)
    # print(result_text.replace('\"',','))    #将"替换为,
    # print(result_text.replace('\"',',').split(','))    #以,为分割
    # print(re.findall(r"\d{6}",result_text))     #输出股票的6位代码返回数组；
    for i in result_text.replace('\"', ',').split(','):  # 将"替换为,再以,进行分割，遍历筛选出含有中文的字符(股票的名字)
        result_chinese = is_contain_chinese(i)
        if result_chinese == True:
            ofstock_name.append(i)
    for numbers in re.findall(r"\d{6}", result_text):
        fund_url.append("http://fundf10.eastmoney.com/ccmx_%s.html" % (numbers))  # 将拼接后的url存入列表；
    return fund_url, ofstock_name


# selenium请求[基金持仓股票详情页面url]的方法，爬取基金的持仓股票名称、持仓量；
def hold_a_position(url):
    stock_name = []  # 定义一个数组，存储证券的名称
    amount = [] #定义一个数组，存储证券的持仓

    # 浏览器动作
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)  # 初始化浏览器，无浏览器界面的，保持后台运行；

    driver.get(url)  # 请求基金持仓的信息
    element_result = is_element(driver, "tol")  # 是否存在这个元素，用于判断是否有持仓信息；
    #print(url + '\n')
    if element_result == True:  # 如果有持仓信息则爬取；
        wait = WebDriverWait(driver, 3)  # 设置一个等待时间
        input = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tol')))  # 等待这个class的出现；
        ccmx_page = driver.page_source  # 获取页面的源码
        ccmx_xpath = etree.HTML(ccmx_page)  # 转换成成 xpath 格式
        trs = ccmx_xpath.xpath("//div[@class='txt_cont']//div[@id='cctable']//div[@class='box'][1]//tr")
        if trs:
            #print("开始获取基金持仓信息")
            for tr in trs:
                stock_name_t = tr.xpath("./td[3]//text()")
                if len(stock_name_t) != 0:  #获取成功才返回数据
                    stock_amount_t = tr.xpath("./td[8]//text()")
                    if len(stock_amount_t) != 0:
                        stock_amount = stock_amount_t[0].replace(",", "")   #去除持仓中的逗号
                        if stock_amount.split(".")[-1].isdigit():   #如果是数值则继续，此处还待优化，仍有字母数据返回
                            stock_name.append(stock_name_t[0])
                            amount.append(stock_amount)
            #print(stock_name)
            #print(amount)
            driver.quit()
            return stock_name,amount
    else:  # 如果没有持仓信息，则返回null字符；
        driver.quit()
        return "null","null"


#进度条实现
def progress_bar(portion, total):
    """
    total 总数据大小，portion 已经传送的数据大小
    :param portion: 已经接收的数据量
    :param total: 总数据量
    :return: 接收数据完成，返回True
    """
    part = total / 50  # 1%数据的大小
    count = math.ceil(portion / part)
    sys.stdout.write('\r')
    sys.stdout.write(('[%-50s]%.2f%%' % (('>' * count), portion / total * 100)))
    sys.stdout.flush()

    if portion >= total:
        sys.stdout.write('\n')
        return True


#多线程获取基金持仓明细入口，begin_num是基金列表的开始位置，end_num是基金列表的结束位置
def Get_stock_detail(fund_url, fund_name, begin_num, end_num):
    #初始化mysql连接
    mydb = mysql.connector.connect(
        host="10.23.1.132",
        user="root",
        passwd="abc123",
        database="ofstock"
    )

    cursor = mydb.cursor()

    while begin_num < end_num:
        global nPos
        nPos += 1   #用于进度条显示
        stock_name, amount = hold_a_position(fund_url[begin_num])  # 遍历持仓信息，返回持仓股票名称、持仓量---数组

        for j in range(len(stock_name)):
            sql = "INSERT INTO ofstockinfo (fund_url, fund_name, stock_name, amount) VALUES (%s, %s, %s, %s)" % (
            repr(fund_url[begin_num]), repr(fund_name[begin_num]), repr(stock_name[j]), repr(amount[j]))
            try:
                cursor.execute(sql)
                mydb.commit()
                #print("插入记录成功")
            except Exception as e:
                mydb.rollback()
                print(e.args, "插入记录失败")
        begin_num += 1

    mydb.close()


if __name__ == '__main__':
    fund_url, fund_name = page_url()  # 获取首页数据，返回基金url的数组和基金名称的数组；

    if len(fund_url) == len(fund_name):  # 判断获取的基金url和基金名称数量是否一致
        threadNum = 10  #线程数量
        all_count=len(fund_url)    #基金数量
        threadId = 1    #线程ID
        threads = []    #线程集合

        #开启多线程
        for tName in range(threadNum):
            thread = myThread(threadId,("Thread-%d" % tName),fund_url, fund_name, round(all_count*(threadId-1)/threadNum+1), round(all_count*threadId/threadNum))
            thread.start()
            threads.append(thread)
            threadId += 1

        #显示进度条
        while nPos<all_count:
            progress_bar(nPos,all_count)
            time.sleep(5)

        # 等待所有线程完成
        for t in threads:
            t.join()
        print("退出主线程")

        #保险起见，关闭所有的chrome进程
        os.system('taskkill /im chromedriver.exe /F')
        os.system('taskkill /im chrome.exe /F')

    else:
        print("基金url和基金name数组数量不一致，退出。")
        exit()
