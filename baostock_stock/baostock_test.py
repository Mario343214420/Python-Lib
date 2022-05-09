import baostock as bs
from pyecharts.charts import Line
from pyecharts import options as opts
bs.login()
fields = "date,open,high,low,close,volume"
code = 'sh.600585'
df_bs = bs.query_history_k_data(code,fields,start_date='2020-10-1',end_date='2020-11-30',frequency='d',adjustflag='3')
print(dir(df_bs))
print(df_bs.code_name)
list_stock = df_bs.data
# 日期列表（x轴坐标）
xaxis_list = []
yaxis_list = []
# line_names = ["开盘", "最高", "最低", "收盘", "交易量"]
line_names = ["开盘", "最高", "最低", "收盘"]
line = Line()

class some_obj():
    def __setitem__(self, k, v):
        self.__setattr__(k, v)

    def __getitem(self, k):
        try:
            return self.__getattribute__(k)
        except AttributeError:
            return None
for i in range(len(line_names)):
    line_data = []
    for i2 in range(len(list_stock)):
        line_data.append(list_stock[i2][i+1])
    obj = some_obj()
    obj.label = line_names[i]
    obj.data = line_data
    yaxis_list.append(obj)
for index in range(len(list_stock)):
    str = list_stock[index][0]
    xaxis_list.append(str)
#     obj = some_obj()
#     date_data_list = []
#     for i in range(len(line_names)):
#         obj.label = line_names[i]
#         date_data_list.append(list_stock[index][i+1])
#         obj.data = date_data_list
#         yaxis_list.append(obj)
#
line.add_xaxis(xaxis_list)
for index in range(len(yaxis_list)):
    line.add_yaxis(yaxis_list[index].label,yaxis_list[index].data)

line.set_global_opts(title_opts=opts.TitleOpts(title=code),yaxis_opts=opts.AxisOpts(
    type_="value",
    #min_=26,
    min_="min",
    #max_="max",
    axistick_opts=opts.AxisTickOpts(is_show=True),
    splitline_opts=opts.SplitLineOpts(is_show=True),
))
line.yaxis_min = 'dataMin'
line.render()