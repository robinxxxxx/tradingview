# -*- coding: utf-8 -*-
import tushare as ts

token = '9f06b4c64140c3184073d227f677103ebceafcd1855da1e7bd1789c7'
pro = ts.pro_api(token)

# 看 opt_daily 中上交所的期权 ts_code 长什么样
df = pro.opt_daily(trade_date='20261013', fields='ts_code,trade_date,vol,oi,exchange')
print('交易所分布:')
print(df['exchange'].value_counts())
print()

sse = df[df['exchange'] == 'SSE']
print(f'SSE期权合约数: {len(sse)}')
print('SSE ts_code 样例:')
print(sse['ts_code'].head(20).tolist())
print()

# opt_basic 里的 ts_code
basic = pro.opt_basic(exchange='SSE', fields='ts_code,opt_code,call_put,name')
print('opt_basic ts_code 样例:')
print(basic['ts_code'].head(10).tolist())
print()
print('opt_basic name 样例:')
print(basic['name'].head(10).tolist())
