import tushare as ts
df_sh_hist = ts.get_hist_data('sh', start='2021-03-19', end='2021-04-18')
print(df_sh_hist.head())
print('------------------------------------------------------------------------')
print(df_sh_hist.tail())
print('------------------------------------------------------------------------')
print(df_sh_hist.info())
print('------------------------------------------------------------------------')