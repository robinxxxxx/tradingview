# -*- coding: utf-8 -*-
import tushare as ts

token = '9f06b4c64140c3184073d227f677103ebceafcd1855da1e7bd1789c7'
pro = ts.pro_api(token)

# 试 exchange='SSE'
try:
    df = pro.opt_daily(trade_date='20261013', exchange='SSE',
                       fields='ts_code,trade_date,vol,oi')
    print(f'exchange=SSE: {len(df)} 行')
    if not df.empty:
        print(df.head(10).to_string())
except Exception as e:
    print(f'exchange=SSE 失败: {e}')

print()

# 试只拉50ETF期权的所有合约，按ts_code批量
# 先看看活跃的合约（2026年10月到期的）
basic = pro.opt_basic(exchange='SSE', opt_code='OP510050.SH',
                       fields='ts_code,name,call_put,list_date,delist_date')
print(f'50ETF全部合约: {len(basic)}')
# 只看近期的
active = basic[basic['delist_date'] > '20261013']
print(f'未到期合约: {len(active)}')
print(active.head(10).to_string())
