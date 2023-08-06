import pandas as pd
import os
from datetime import datetime, timedelta
import time



# ==========辅助功能函数==========
def next_run_time(time_interval, ahead_seconds=5):
    """
    根据time_interval，计算下次运行的时间，下一个整点时刻。
    目前只支持分钟和小时。
    :param time_interval: 运行的周期，15m，1h
    :param ahead_seconds: 预留的目标时间和当前时间的间隙
    :return: 下次运行的时间
    案例：
    15m  当前时间为：12:50:51  返回时间为：13:00:00
    15m  当前时间为：12:39:51  返回时间为：12:45:00
    10m  当前时间为：12:38:51  返回时间为：12:40:00
    5m  当前时间为：12:33:51  返回时间为：12:35:00
    5m  当前时间为：12:34:51  返回时间为：12:35:00

    1h  当前时间为：14:37:51  返回时间为：15:00:00
    2h  当前时间为：00:37:51  返回时间为：02:00:00

    30m  当前时间为：21日的23:33:51  返回时间为：22日的00:00:00
    5m  当前时间为：21日的23:57:51  返回时间为：22日的00:00:00

    ahead_seconds = 5
    15m  当前时间为：12:59:57  返回时间为：13:15:00，而不是 13:00:00
    """
    if time_interval.endswith('m') or time_interval.endswith('h'):
        pass
    elif time_interval.endswith('T'):
        time_interval = time_interval.replace('T', 'm')
    elif time_interval.endswith('H'):
        time_interval = time_interval.replace('H', 'h')
    else:
        print('time_interval格式不符合规范。程序exit')
        exit()

    ti = pd.to_timedelta(time_interval)
    now_time = datetime.now()
    # now_time = datetime(2019, 5, 9, 23, 50, 30)  # 指定now_time，可用于测试
    this_midnight = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
    min_step = timedelta(minutes=1)

    target_time = now_time.replace(second=0, microsecond=0)

    while True:
        target_time = target_time + min_step
        delta = target_time - this_midnight
        if delta.seconds % ti.seconds == 0 and (target_time - now_time).seconds >= ahead_seconds:
            # 当符合运行周期，并且目标时间有足够大的余地，默认为60s
            break

    print('\n程序下次运行的时间：', target_time, '\n')
    return target_time


# ===依据时间间隔, 自动计算并休眠到指定时间
def sleep_until_run_time(time_interval = '6h', ahead_time=1, if_sleep=True):
    """
    根据next_run_time()函数计算出下次程序运行的时候，然后sleep至该时间
    :param time_interval:
    :param ahead_time:
    :param if_sleep:
    :return:
    """

    # 计算下次运行时间
    run_time = next_run_time(time_interval, ahead_time)

    # sleep
    if if_sleep:
        time.sleep(max(0, (run_time - datetime.now()).seconds))
        # 可以考察：print(run_time - n)、print((run_time - n).seconds)
        while True:  # 在靠近目标时间时
            if datetime.now() > run_time:
                break

    return run_time

#获取当天的时间
def getTodayTime():
    """
    获取当天的时间
    :return:
    """
    #today_day_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    time_date = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
    print('当前时间:',time_date)
    return time_date
    #self.today_date_time = time.strftime('%Y-%m-%d 00:00:00', time.localtime(time.time()))
    #today_date = exchange.parse8601(today_date_time)

def get_todayt_date():
    time_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    return time_date

def dict_to_str(dict_msg):
    """
    字典转钉钉输出信息
    :param dict_msg:
    :return:
    """
    string = ''
    for i in dict_msg.keys():
        string += i + ':' + str(dict_msg[i])
        string += '\n'
    return string





