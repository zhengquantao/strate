import math
import operator
import os.path as path
import pandas as pd
import numpy as np
from copy import copy


def assert_msg(condition, msg):
    if not condition:
        raise Exception(msg)


def read_file(filename):
    # 获得文件绝对路径
    filepath = path.join(path.dirname(__file__), filename)

    # 判定文件是否存在
    assert_msg(path.exists(filepath), "文件不存在")

    # 读取CSV文件并返回
    return pd.read_csv(filepath,
                       index_col=0,
                       parse_dates=True,
                       infer_datetime_format=True)


def SMA(values, n):
    """
    返回简单滑动平均
    """
    return pd.Series(values).rolling(n).mean()


def EMA(values, period: int = 12, alpha=None):
    """
    指数移动平均
    :param values:
    :param period:
    :param alpha:
    :return:
    """
    end = len(values)
    ema_value = copy(values)
    alpha = alpha
    if alpha is None:
        alpha = 2.0 / (1.0 + period)
    alpha1 = 1.0 - alpha
    prev = values[period - 1]
    for i in range(period, end):
        ema_value[i] = prev = prev * alpha1 + values[i] * alpha
    return ema_value


def MACD(values, period_me1=12, period_me2=26, period_signal=9):
    """
    移动平均趋同/偏离(异同移动平均线
    :return:
    """
    me1 = EMA(values, period=period_me1)
    me2 = EMA(values, period=period_me2)
    macds = np.array(me1) - np.array(me2)
    signal = EMA(macds, period=period_signal)
    histo = np.array(macds) - np.array(signal)
    return macds, signal, histo


def WMA(values, period=30):
    """
    加权移动平均
    :return:
    """
    end = len(values)
    wma_values = copy(values)
    coef = 2.0 / (period * (period + 1.0))
    weights = tuple(float(x) for x in range(1, period + 1))
    for i in range(period, end):
        data = values[i - period + 1: i + 1]
        wma_values[i] = coef * math.fsum(map(operator.mul, data, weights))
    return wma_values


def crossover(series1, series2) -> bool:
    """
    检查两个序列是否在结尾交叉
    :param series1:  序列1
    :param series2:  序列2
    :return:         如果交叉返回True，反之False
    """
    return series1[-2] < series2[-2] and series1[-1] > series2[-1]
