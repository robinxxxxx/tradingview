# -*- coding: utf-8 -*-
import pandas as pd

# 读取数据
df50 = pd.read_csv(r'C:\Users\m1596\Doubao\chats\2026-09-07\new-chat\50ETF_pcr_full.csv')
df300 = pd.read_csv(r'C:\Users\m1596\Doubao\chats\2026-09-07\new-chat\300ETF_pcr_full.csv')

df50['trade_date'] = pd.to_datetime(df50['trade_date'])
df300['trade_date'] = pd.to_datetime(df300['trade_date'])

# 合并
merged = pd.merge(df50[['trade_date','pcr_oi','pcr_vol']],
                  df300[['trade_date','pcr_oi','pcr_vol']],
                  on='trade_date', suffixes=('_50','_300'))

print('='*60)
print('50ETF PCR vs 300ETF PCR 历史对比')
print('='*60)
print(f'时间范围: {merged["trade_date"].min().date()} ~ {merged["trade_date"].max().date()}')
print(f'总交易日: {len(merged)}')
print()

# 持仓PCR对比
print('--- 持仓PCR ---')
print(f'50ETF 均值:   {merged["pcr_oi_50"].mean():.4f}  (区间 {merged["pcr_oi_50"].min():.4f} ~ {merged["pcr_oi_50"].max():.4f})')
print(f'300ETF 均值:  {merged["pcr_oi_300"].mean():.4f}  (区间 {merged["pcr_oi_300"].min():.4f} ~ {merged["pcr_oi_300"].max():.4f})')
print()

# 谁大谁小
merged['pcr_diff'] = merged['pcr_oi_50'] - merged['pcr_oi_300']
cnt_50_bigger = (merged['pcr_diff'] > 0).sum()
cnt_300_bigger = (merged['pcr_diff'] < 0).sum()
print(f'50ETF PCR > 300ETF PCR 的天数: {cnt_50_bigger} ({cnt_50_bigger/len(merged)*100:.1f}%)')
print(f'300ETF PCR > 50ETF PCR 的天数: {cnt_300_bigger} ({cnt_300_bigger/len(merged)*100:.1f}%)')
print()

# 最近数据
print('--- 最近10个交易日 ---')
print(merged[['trade_date','pcr_oi_50','pcr_oi_300','pcr_diff']].tail(10).to_string(index=False))
print()

# 50ETF PCR > 300ETF PCR 的历史时刻
print('--- 50ETF PCR > 300ETF PCR 的历史时刻（TOP 15 差距最大）---')
bigger = merged[merged['pcr_diff'] > 0].sort_values('pcr_diff', ascending=False)
if len(bigger) > 0:
    print(bigger[['trade_date','pcr_oi_50','pcr_oi_300','pcr_diff']].head(15).to_string(index=False))
else:
    print('  从未出现过！')
print()

# 成交量PCR对比
print('--- 成交量PCR ---')
print(f'50ETF 均值:   {merged["pcr_vol_50"].mean():.4f}')
print(f'300ETF 均值:  {merged["pcr_vol_300"].mean():.4f}')
merged['vol_diff'] = merged['pcr_vol_50'] - merged['pcr_vol_300']
print(f'50ETF > 300: {(merged["vol_diff"]>0).sum()}天 ({(merged["vol_diff"]>0).sum()/len(merged)*100:.1f}%)')
