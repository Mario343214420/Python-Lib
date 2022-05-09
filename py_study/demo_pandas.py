import pandas as pd
from datetime import datetime
# print(pd.__version__)
# sd = pd.Series([1., 2., 3.], index=['2021-04-06', '2021-04-07', '2021-04-08'])
# print(sd)
# pd.set_option('display.expend_frame_repr', False)
# pd.set_option('display.max_rows', 10)
# pd.set_option('display.max_columns', 6)
# pd.set_option('precision', 2)
import pandas_datareader.data as web
dt_stockload = web.DataReader('000001.ss', 'yahoo', datetime(2019,2,1), datetime(2019,3,1))
print(dt_stockload.head())