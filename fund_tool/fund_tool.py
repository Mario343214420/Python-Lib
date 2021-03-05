import requests
from selenium import webdriver
import requests
import re
from lxml import etree
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

chrome_options = Options()
chrome_options.add_argument('--headless')
b = webdriver.Chrome(options=chrome_options)
while (True):
    b.get('http://m.eastmoney.com/kuaixun')
    r_time = b.find_element_by_xpath('//*[@id="kxlist"]/div[1]/div[1]').text
    r_text = b.find_element_by_xpath('//*[@id="kxlist"]/div[1]/div[2]/div[1]/div[1]/span').text
    really_text = r_time + '\n' + r_text
    text = ''
    print(text)
    try:
        if really_text != text:
            text = really_text
            mail_host = "smtp.qq.com"  # 设置的邮件服务器host必须是发送邮箱的服务器，与接收邮箱无关。
            mail_user = "1173281341@qq.com"  # qq邮箱登陆名
            mail_pass = "ionubjkihqudbadd"  # 开启stmp服务的时候并设置的授权码，注意！不是QQ密码。

            sender = '1173281341@qq.com'  # 发送方qq邮箱
            receivers = ['739880760@qq.com']  # 接收方qq邮箱

            message = MIMEText(text, 'plain', 'utf-8')
            message['From'] = Header("happy", 'utf-8')  # 设置显示在邮件里的发件人
            message['To'] = Header("Mario", 'utf-8')  # 设置显示在邮件里的收件人

            subject = '每日新闻'
            message['Subject'] = Header(subject, 'utf-8')  # 设置主题和格式

            try:
                smtpobj = smtplib.SMTP_SSL(mail_host, 465)  # 本地如果有本地服务器，则用localhost ,默认端口２５,腾讯的（端口465或587）
                smtpobj.set_debuglevel(1)
                smtpobj.login(mail_user, mail_pass)  # 登陆QQ邮箱服务器
                smtpobj.sendmail(sender, receivers, message.as_string())  # 发送邮件
                smtpobj.quit()  # 退出
                print("邮件发送成功")
                time.sleep(1200)
                b.refresh()
                continue
            except smtplib.SMTPException as e:
                print("Error:无法发送邮件")
                print(e)
                b.refresh()
                continue
    except:
        print('热点暂未更新')
        time.sleep(1200)
        b.refresh()
        continue