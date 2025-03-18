# @Time    : 2025/2/11 20:08
# @Author  : JunFei Cai
# @File    : math_operation.py
"""
用于保存所有自定义的数学操作
"""
import numpy as np
from scipy.integrate import simpson


def symbol_judge(number):
    """
    judge the symbol of number
    :param number: a number type data
    :return: True for positive number and False for negative number
    """
    if number > 0:
        return True
    elif number == 0:
        return None
    elif number < 0:
        return False


def data_integration(x, y, x_min, x_max):
    """
    基于辛普森法则，对给定离散数据进行定积分
    :param x: 横坐标数据
    :param y: 纵坐标数据
    :param x_min: 定积分下限
    :param x_max: 定积分上限
    :return: 积分值
    """
    x = np.array(x)
    y = np.array(y)

    mask = (x >= x_min) & (x <= x_max)

    x_filtered = x[mask]
    y_filtered = y[mask]

    if len(x_filtered) < 2:
        raise ValueError('No enough data to calculate the integration')

    integral = simpson(y=y_filtered, x=x_filtered)

    return integral
