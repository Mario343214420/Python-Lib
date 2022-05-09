import datetime
import pandas_datareader.data as web
df_stockload = web.DataReader("000001.SS", "yahoo", datetime.datetime(2021,4,18), datetime.datetime(2021,4,19))
print(df_stockload.head())
print(1)