# -*- coding: utf-8 -*-
"""
期权PCR数据自动拉取 → TradingView CSV → GitHub Push
"""
import os, sys, time, datetime, subprocess

# ============ CONFIG ============
TUSHARE_TOKEN = "9f06b4c64140c3184073d227f677103ebceafcd1855da1e7bd1789c7"
GIT_REPO_URL = "https://github.com/robinxxxxx/tradingview.git"
GIT_BRANCH = "main"
GIT_USER_NAME = "robinxxxxx"
GIT_USER_EMAIL = "david7664259@gmail.com"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
START_DATE = "20240101"
END_DATE = datetime.datetime.now().strftime("%Y%m%d")
UNDERLYINGS = {"50ETF": "OP510050.SH", "300ETF": "OP510300.SH"}
# ================================


def main():
    import tushare as ts
    import pandas as pd

    pro = ts.pro_api(TUSHARE_TOKEN)
    print("Tushare 连接成功")

    # 1. 获取合约映射
    basic = pro.opt_basic(exchange='SSE', fields='ts_code,opt_code,call_put')
    contract_map = {}
    for label, opt_code in UNDERLYINGS.items():
        sub = basic[basic['opt_code'] == opt_code]
        c_codes = set(sub[sub['call_put'] == 'C']['ts_code'])
        p_codes = set(sub[sub['call_put'] == 'P']['ts_code'])
        contract_map[label] = (c_codes, p_codes)
        print(f"  {label}: Call {len(c_codes)}, Put {len(p_codes)}")

    # 2. 交易日历
    cal = pro.trade_cal(exchange='SSE', start_date=START_DATE, end_date=END_DATE, is_open='1')
    trade_dates = sorted(cal['cal_date'].tolist())
    print(f"  共 {len(trade_dates)} 个交易日")

    # 3. 逐日拉取
    rows = []
    for i, td in enumerate(trade_dates):
        try:
            df = pro.opt_daily(trade_date=td, exchange='SSE',
                               fields='ts_code,trade_date,vol,oi')
            if df is None or df.empty:
                continue

            for label, (c_codes, p_codes) in contract_map.items():
                dc = df[df['ts_code'].isin(c_codes)]
                dp = df[df['ts_code'].isin(p_codes)]
                co, po = dc['oi'].sum(), dp['oi'].sum()
                cv, pv = dc['vol'].sum(), dp['vol'].sum()
                rows.append({
                    'trade_date': td, 'etf': label,
                    'call_oi': int(co), 'put_oi': int(po),
                    'pcr_oi': round(po/co, 4) if co > 0 else None,
                    'call_vol': int(cv), 'put_vol': int(pv),
                    'pcr_vol': round(pv/cv, 4) if cv > 0 else None,
                })
            if (i+1) % 30 == 0:
                print(f"    进度 {i+1}/{len(trade_dates)}")
            time.sleep(0.3)
        except Exception as e:
            print(f"  [WARN] {td}: {e}")
            time.sleep(1)

    result = pd.DataFrame(rows)
    result['trade_date'] = pd.to_datetime(result['trade_date'])
    result = result.sort_values(['etf', 'trade_date']).reset_index(drop=True)
    print(f"\n共 {len(result)} 条记录")
    print(result.groupby('etf').tail(3).to_string())

    # 4. 输出 CSV
    files = []
    for etf in UNDERLYINGS:
        sub = result[result['etf'] == etf]
        # TradingView PCR
        out = pd.DataFrame({
            'time': sub['trade_date'].dt.strftime('%Y-%m-%d'),
            'open': sub['pcr_oi'], 'high': sub['pcr_oi'],
            'low': sub['pcr_oi'], 'close': sub['pcr_oi'],
        })
        p1 = os.path.join(OUTPUT_DIR, f"{etf}_pcr_oi.csv")
        out.to_csv(p1, index=False)
        files.append(p1)

        out2 = pd.DataFrame({
            'time': sub['trade_date'].dt.strftime('%Y-%m-%d'),
            'open': sub['pcr_vol'], 'high': sub['pcr_vol'],
            'low': sub['pcr_vol'], 'close': sub['pcr_vol'],
        })
        p2 = os.path.join(OUTPUT_DIR, f"{etf}_pcr_vol.csv")
        out2.to_csv(p2, index=False)
        files.append(p2)

        p3 = os.path.join(OUTPUT_DIR, f"{etf}_pcr_full.csv")
        sub.to_csv(p3, index=False)
        files.append(p3)
        print(f"  保存: {p1} ({len(out)}行)")

    # 5. Git push
    if GIT_REPO_URL:
        os.chdir(OUTPUT_DIR)
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'branch', '-M', GIT_BRANCH], check=True)
            subprocess.run(['git', 'remote', 'add', 'origin', GIT_REPO_URL], check=True)
            subprocess.run(['git', 'config', 'user.name', GIT_USER_NAME], check=True)
            subprocess.run(['git', 'config', 'user.email', GIT_USER_EMAIL], check=True)
        for f in files:
            subprocess.run(['git', 'add', f], check=True)
        subprocess.run(['git', 'commit', '-m', f'update pcr {datetime.datetime.now():%Y-%m-%d %H:%M}'],
                       capture_output=True)
        r = subprocess.run(['git', 'push', '-u', 'origin', GIT_BRANCH],
                           capture_output=True, text=True)
        print(f"  push: {'成功' if r.returncode==0 else r.stderr}")

    print(f"\n完成! 目录: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
