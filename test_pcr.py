# -*- coding: utf-8 -*-
import tushare as ts
import pandas as pd

token = '9f06b4c64140c3184073d227f677103ebceafcd1855da1e7bd1789c7'
pro = ts.pro_api(token)

basic = pro.opt_basic(exchange='SSE', fields='ts_code,opt_code,call_put')
print('50ETF合约数:', len(basic[basic['opt_code'] == 'OP510050.SH']))
print('300ETF合约数:', len(basic[basic['opt_code'] == 'OP510300.SH']))

codes50_c = set(basic[(basic['opt_code'] == 'OP510050.SH') & (basic['call_put'] == 'C')]['ts_code'])
codes50_p = set(basic[(basic['opt_code'] == 'OP510050.SH') & (basic['call_put'] == 'P')]['ts_code'])
codes300_c = set(basic[(basic['opt_code'] == 'OP510300.SH') & (basic['call_put'] == 'C')]['ts_code'])
codes300_p = set(basic[(basic['opt_code'] == 'OP510300.SH') & (basic['call_put'] == 'P')]['ts_code'])

for td in ['20261013', '20261010', '20261009']:
    df = pro.opt_daily(trade_date=td, fields='ts_code,trade_date,vol,oi')
    c50 = df[df['ts_code'].isin(codes50_c)]
    p50 = df[df['ts_code'].isin(codes50_p)]
    c300 = df[df['ts_code'].isin(codes300_c)]
    p300 = df[df['ts_code'].isin(codes300_p)]

    oi50_c = c50['oi'].sum()
    oi50_p = p50['oi'].sum()
    oi300_c = c300['oi'].sum()
    oi300_p = p300['oi'].sum()

    print(f'\n{td}:')
    print(f'  50ETF:  Call_OI={oi50_c:.0f}, Put_OI={oi50_p:.0f}, PCR={oi50_p/oi50_c:.4f}')
    print(f'  300ETF: Call_OI={oi300_c:.0f}, Put_OI={oi300_p:.0f}, PCR={oi300_p/oi300_c:.4f}')
