import requests
from bs4 import BeautifulSoup
import re
from urllib import parse

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
}
findRegID = re.compile(r'data-val="(\d+)">(.*?)</div>')
findRegtpye = re.compile(r'data-val="\d+">(.*?)</div>')


def main():
    cheack()
    while True:
        reg = input("请输入大区ID，比如是艾欧尼亚，请输入1 \n")
        if reg == "":
            print("游戏大区不能为空")
        pID = input("请输入游戏ID: \n")
        if pID == "":
            print("游戏ID不能为空!")
        else:
            print(pID, reg)
            go(pID, reg)
            # (response)


def go(pID, reg):
    pID = parse.quote(pID, encoding="utf-8")
    url = "https://www.lolhelper.cn/rank_lcu.php?gameid=" + pID + "&server=" + str(reg)
    print(url)
    response = requests.get(url=url, headers=header)
    response = response.text
    soup = BeautifulSoup(response, 'lxml')
    for item in soup.find_all("div", class_="main_item"):
        res = item.text
        res = res.replace('\n', '')
        print(res)


# 获取大区数据
def getReg():
    url = 'https://www.lolhelper.cn'
    response = requests.get(url=url, headers=header)
    response = response.text
    soup = BeautifulSoup(response, 'lxml')
    list = []
    for item in soup.find_all('div', class_="option_sel_item"):
        item = str(item)
        reg = re.findall(findRegID, item)
        list.append(reg)
        # Name = re.findall(findRegName,item)
        # print(Name)
        # print(str(ID)+"."+Name)
    return list


# 检测展示大区数据
def cheack():
    allReg = getReg()
    allReglen = len(allReg)
    print("发现大区%d个\n" % allReglen)
    tupall = ''
    for item in allReg:
        allRegCan = item[0]
        tup = allRegCan[0] + "." + allRegCan[1]
        tupall = tupall + tup
    print(tupall)


# print("发现大区%d个! " % allReglen)

if __name__ == "__main__":
    main()
