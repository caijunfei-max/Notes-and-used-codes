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


def rotate_x(theta):
    """
    获取绕X轴的旋转矩阵
    :param theta: 旋转的角度
    :return: 旋转矩阵
    """
    theta = np.radians(theta)
    return np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta), np.cos(theta)]
    ])


def rotate_y(theta):
    """
    获取绕Y轴的旋转矩阵
    :param theta: 旋转角度
    :return: 旋转矩阵
    """
    theta = np.radians(theta)
    return np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])


def rotate_z(theta):
    """
    获取绕Z轴的旋转矩阵
    :param theta: 旋转角度
    :return: 旋转矩阵
    """
    theta = np.radians(theta)
    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])


def compute_axis_and_angle(theta_x, theta_y, theta_z):
    """
    给定三个旋转轴的角度，返回一个特定方向和一个弧度
    :param theta_x:
    :param theta_y:
    :param theta_z:
    :return: 一个方向和一个弧度
    """
    # 计算每个轴的旋转矩阵
    r_x = rotate_x(theta_x)
    r_y = rotate_y(theta_y)
    r_z = rotate_z(theta_z)

    # 合成旋转矩阵
    r = np.dot(r_z, np.dot(r_y, r_x))

    # 从旋转矩阵提取旋转角度和旋转轴
    cos_theta = (np.trace(r) - 1) / 2
    theta = np.arccos(cos_theta)  # 旋转角度

    # 计算旋转轴 (单位向量)
    if np.abs(theta) > 1e-6:  # 如果角度不为0
        axis = np.array([
            r[2, 1] - r[1, 2],
            r[0, 2] - r[2, 0],
            r[1, 0] - r[0, 1]
        ])
        axis = axis / np.linalg.norm(axis)  # 归一化旋转轴
    else:
        axis = np.array([1, 0, 0])  # 如果没有旋转，轴任意选择，假设为X轴

    return axis, np.radians(theta)


def get_midpoint(coord1, coord2):
    midpoint_coord = (np.array(coord1) + np.array(coord2)) / 2
    return midpoint_coord


# 仅测试函数用
if __name__ == '__main__':
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    print(get_midpoint(a, b))
