import pandas as pd
from datetime import datetime, timedelta, timezone
def calaculate_capital_curve(equity_curve):
    """
    根据账户市值计算账户资金曲线
    :return:
    """
    # =====计算资金曲线
    equity_curve['equity_change'] = equity_curve['net_value'].pct_change()

    equity_curve['equity_change'].fillna(value=0, inplace=True)
    equity_curve['equity_curve'] = (1 + equity_curve['equity_change']).cumprod()

    # ===新建一个dataframe保存回测指标
    #results = pd.DataFrame()

    # ===计算累积净值
    #results.loc[0, '累积净值'] = round(equity_curve['equity_curve'].iloc[-1], 2)

    # ===计算年化收益
    #print(type(equity_curve['time'].iloc[0]))

    #equity_curve['annual_return'] = (equity_curve['equity_curve']/ equity_curve['equity_curve'].iloc[0]) ** ('1 days 00:00:00' / (equity_curve['time'] - equity_curve['time'].iloc[0]) * 365) - 1

    #results.loc[0, '年化收益'] = str(round(annual_return, 2)) + ' 倍'

    # ===计算最大回撤，最大回撤的含义：《如何通过3行代码计算最大回撤》https://mp.weixin.qq.com/s/Dwt4lkKR_PEnWRprLlvPVw

    # # 计算当日之前的资金曲线的最高点
    # equity_curve['max2here'] = equity_curve['equity_curve'].expanding().max()
    # # 计算到历史最高值到当日的跌幅，drowdwon
    # equity_curve['dd2here'] = equity_curve['equity_curve'] / equity_curve['max2here'] - 1
    #
    # # 计算最大回撤，以及最大回撤结束时间
    # end_date, max_draw_down = tuple(equity_curve.sort_values(by=['dd2here']).iloc[0][['candle_begin_time', 'dd2here']])
    # # 计算最大回撤开始时间
    # start_date = \
    # equity_curve[equity_curve['candle_begin_time'] <= end_date].sort_values(by='equity_curve', ascending=False).iloc[0][
    #     'candle_begin_time']
    # # 将无关的变量删除
    # equity_curve.drop(['max2here', 'dd2here'], axis=1, inplace=True)
    # results.loc[0, '最大回撤'] = format(max_draw_down, '.2%')
    # results.loc[0, '最大回撤开始时间'] = str(start_date)
    # results.loc[0, '最大回撤结束时间'] = str(end_date)
    #
    # # ===年化收益/回撤比
    # results.loc[0, '年化收益/回撤比'] = round(abs(annual_return / max_draw_down), 2)


    return equity_curve


