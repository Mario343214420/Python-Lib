import requests
import re
import numpy as np
from lxml import etree
import json
from pyecharts.charts import Line
from pyecharts import options as opts
code = input('请输入代码：') or '005609'
start_date = input('请输入开始日期：') or '2020-05-01'
end_date = input('请输入结束日期：') or '2020-06-30'
base_url = 'https://fundf10.eastmoney.com/F10DataApi.aspx?type=lsjz&code=%s&page=1&per=65535&sdate=%s&edate=%s'%(code, start_date, end_date)
res = requests.get(base_url)
name = requests.get('http://fundgz.1234567.com.cn/js/%s.js'%(code))
# 正则表达式
pattern = r'^jsonpgz\((.*)\)'
# 查找结果
search = re.findall(pattern, name.text)
# 遍历结果
codeStr = ''
for i in search:
  data = json.loads(i)
  # print(data,type(data))
  codeStr = "基金: {},收益率: {}".format(data['name'],data['gsz'])

html = res.text.split('"')[1]
content = etree.HTML(html)
list = np.array(content.xpath('//table/tbody/tr/td/text()'))
print(list)
y = int(len(list)/6)
res_list = np.delete(list.reshape(y, 6)[::-1],  [0, -1, -2], axis=1)
print(res_list)
# 日期列表（x轴坐标）
# 日增长率为百分比字符串，故暂不与单位净值同时显示
# line_names = ["单位净值", "累计净值", "日增长率"]
line_names = ["单位净值", "累计净值"]
line = Line()
xAxis = np.array(list).reshape(y, 6)[:, 0]
print(xAxis[::-1])
# line.add_xaxis(xAxis)
# line.add_yaxis("单位净值", yAxis)
line.add_xaxis(xAxis[::-1].tolist())

for i in range(len(line_names)):
    yAxis = res_list[:, i]
    line.add_yaxis(line_names[i], yAxis.tolist())

line.set_global_opts(title_opts=opts.TitleOpts(title=code, subtitle=codeStr),yaxis_opts=opts.AxisOpts(
    type_="value",
    min_="min",
    axistick_opts=opts.AxisTickOpts(is_show=True),
    splitline_opts=opts.SplitLineOpts(is_show=True),
))
line.render()