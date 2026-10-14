# -*- coding: utf-8 -*-
import tushare as ts

token = '9f06b4c64140c3184073d227f677103ebceafcd1855da1e7bd1789c7'
pro = ts.pro_api(token)

# 拿一个50ETF的具体合约试试
basic = pro.opt_basic(exchange='SSE', opt_code='OP510050.SH',
                       fields='ts_code,name,call_put')
sample = basic[basic['call_put'] == 'C'].iloc[0]
print(f'测试合约: {sample["ts_code"]} {sample["name"]}')

# 按ts_code拉日线
df = pro.opt_daily(ts_code=sample['ts_code'], start_date='20261001', end_date='20261013')
print(f'返回行数: {len(df)}')
if not df.empty:
    print(df.to_string())
else:
    print('空数据，换个方式...')
    # 试试 pro_bar
    import tushare as ts2
    df2 = ts2.pro_bar(ts_code=sample['ts_code'], asset='O',
                       start_date='20261001', end_date='20261013', api=pro)
    print(f'pro_bar 返回: {len(df2)}')
    if df2 is not None and not df2.empty:
        print(df2.to_string())
