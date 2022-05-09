import tushare as ts
token = 'f3342969e14086ec82413035814b9625d3ee09b51e134c9f3df0d9d1'
pro = ts.pro_api(token)
df_gldq = pro.daily(ts_code='688002.sh', start_date='20210319', end_date='20210418')
print(df_gldq.head())
print('-----------------------------------------------------------------------')
print(df_gldq.tail())
print('-----------------------------------------------------------------------')
print(df_gldq.info())
print('-----------------------------------------------------------------------')
print(df_gldq.axes)