import baostock as bs
import pandas as pd
lg = bs.login()
fields = "date,open,hight,low,close,volume"
df_bs = bs.query_history_k_data('sh.688002',fields,start_date='2009-01-01',end_date='2009-06-01',frequency='d',adjustflag='2')
data_list = []
while (df_bs.error_code == '0') & df_bs.next():
    data_list.append(df_bs.get_row_data())
result = pd.DataFrame(data_list, columns=df_bs.fields)
# result.close = result.close.astype('float64')
# result.open = result.open.astype('float64')
# result.low = result.low.astype('float64')
# result.high = result.high.astype('float64')
# result.volume = result.volume.astype('int')
# result.index = pd.to_datetime(result.date)
print(result.head())