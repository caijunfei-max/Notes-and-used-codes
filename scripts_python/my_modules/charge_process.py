# @Time    : 2025/1/11 20:15
# @Author  : JunFei Cai
# @File    : cohp_process.py
"""
用于处理电子结构的python自编函数库
"""
import numpy as np
import pandas as pd
import seaborn as sns
import math
from my_modules.functions import *
from my_modules.math_operation import *


def cohp_extract(path):
    """
    读取cohp.lobster或者coop.lobster中的数据，分割数据后，把cohp中的作用对和每一列数据对应上
    本次使用只考虑了有考虑自旋的数据
    :param path: 数据文件的路径
    :return: 处理好的数据，dataframe类型。
    """
    with open(path, 'r') as f:
        lines = f.readlines()
    atom_pair = []
    cohp_data = []
    for i in range(3, len(lines)):
        line_str = lines[i].replace("\n", "")
        if lines[i].startswith("No"):
            atom_pair.append(line_str)

        else:
            energy_data = [x for x in line_str.split(" ") if x != ""]
            cohp_data.append(energy_data)

    pair_num = len(atom_pair)
    # data_num = 4 * pair_num + 5
    column_name = []
    column_name.append("Energy")
    column_name.append("average_pCOHP_up")
    column_name.append("average_IpCOHP_up")
    for i in range(pair_num):
        num = i + 1
        column_name.append("pCOHP_up_" + str(num))
        column_name.append("IpCOHP_up_" + str(num))

    column_name.append("average_pCOHP_down")
    column_name.append("average_IpCOHP_down")
    for i in range(pair_num):
        num = i + 1
        column_name.append("pCOHP_down_" + str(num))
        column_name.append("IpCOHP_down_" + str(num))

    data_array = np.array(cohp_data, dtype=float)
    processed_data = pd.DataFrame(data_array, columns=column_name)
    return processed_data


def plot_cohp(cohp_data, ax, parameter_dict,
              pair_index="average",
              ):
    """
    在axes画图。
    :param cohp_data: 通过cohp_extract进行处理过的cohp数据
    :param ax: 通过索引得到axes
    :param pair_index: 对应cohp中的原子对,默认取平均值，也可以通过数字指定，注意从1开始而不是0
    :param parameter_dict: 绘图的参数，标题啊啥的
    """
    if pair_index == "average":
        plot_data = cohp_data.loc[:, ["Energy", "average_pCOHP_up", "average_pCOHP_down"]]

    else:
        column_index_up = "pCOHP_up_" + str(pair_index)
        column_index_down = "pCOHP_down_" + str(pair_index)
        plot_data = cohp_data.loc[:, ["Energy", column_index_up, column_index_down]]

    plot_data["Y1"] = plot_data.iloc[:, 1]  # * -1  # cohp乘以一个负值
    plot_data["Y2"] = plot_data.iloc[:, 2]  # * -1  # cohp乘以一个负值
    # 获取绝对值最大的数字用于设置纵轴范围
    max_abs = plot_data.iloc[:, 1:3].abs().max().max() * 1.2

    # 上自旋曲线
    sns.lineplot(data=plot_data,
                 x="Energy",
                 y="Y1",
                 label=parameter_dict["curve_label"][0],
                 color=parameter_dict["curve_color"][0],
                 linewidth=2.5,
                 ax=ax)
    # 下自旋曲线
    sns.lineplot(data=plot_data,
                 x="Energy",
                 y="Y2",
                 label=parameter_dict["curve_label"][1],
                 color=parameter_dict["curve_color"][1],
                 linewidth=2.5,
                 ax=ax)

    ax.legend(loc="best")  # 自动调整选择最合适的子图图例

    ax.set_xticks(parameter_dict["xticks"])

    ax.axvline(x=0, color="black", linestyle="--", label="Fermi energy")
    ax.axhline(y=0, color="black", linestyle="--")
    # ax.set_title(parameter_dict["title"])
    ax.set_xlabel(parameter_dict["xlabel"])
    ax.set_ylabel(parameter_dict["ylabel"])
    ax.set_xlim(parameter_dict["xlim"])
    ax.set_ylim(-max_abs, max_abs)
    # ax.set_ylim(-0.1, 0.1)


def density_of_states_extract(path, column_reset=False):
    """
    使用vaspkit获得态密度的数据之后，用此函数转化为dataframe数据
    :param path: 原始文件的位置
    :param column_reset: 是否要根据数据判断上下自旋
    :return: 包含数据的dataframe
    """
    with open(path, "r") as f:
        lines = f.readlines()
    lines = [line.rstrip() for line in lines]  # 去掉每一行数据后面的换行符
    states_data = []
    for line in lines:
        line_data = [x for x in line.split(" ") if x != ""]
        states_data.append(line_data)
    initial_title = states_data[0]
    initial_title.remove("#")

    df_title = ["Energy"]

    df_data = np.array(states_data[1:], dtype=float)
    spin_judge = [symbol_judge(x) for x in df_data.mean(axis=0)]
    if column_reset:
        for i in range(1, len(spin_judge)):
            if spin_judge[i]:
                df_title.append(initial_title[i] + "-up")
            else:
                df_title.append(initial_title[i] + "-down")
        states_df = pd.DataFrame(data=df_data, columns=df_title)
    else:
        states_df = pd.DataFrame(data=df_data, columns=initial_title)

    return states_df


def max_finder(data, index_range):
    # 在指定位置找到数据中的最大值，用于设置
    max_abs = data.iloc[index_range[0]: index_range[-1], 1:].abs().max().max()
    return max_abs


def density_of_states_plot(data, energy_range, ax, parameter_dict):
    """
    通过density_of_states_extract后，绘制态密度。
    :param data: 通过density_of_states_extract提取的数据
    :param energy_range: 用于画图的能量范围
    :param ax: 画图的坐标轴
    :param parameter_dict: 画图参数
    :return: 绘制一个dos图
    """
    energy_list = data['Energy'].values
    index_range = find_indices_in_range(energy_list, energy_range[0], energy_range[-1])
    max_abs = max_finder(data, index_range)
    y_column = data.iloc[:, 1:]  # 除了Energy之外的数据列表
    for column in y_column.columns:
        sns.lineplot(data=data,
                     x="Energy",
                     y=column,
                     label=column,
                     linewidth=2.5,
                     ax=ax
                     )

    ax.legend(loc="best")

    ax.set_xticks(parameter_dict['xticks'])

    ax.axvline(x=0, color="black", linestyle="--", label="Fermi energy")

    ax.axhline(y=0, color="black", linestyle="--")
    # ax.set_title(parameter_dict["title"])
    ax.set_xlabel(parameter_dict["xlabel"])
    ax.set_ylabel(parameter_dict["ylabel"])
    ax.set_xlim(parameter_dict["xlim"])
    ax.set_ylim(-max_abs*1.2, max_abs*1.2)


def band_center_calculator(energy, density, energy_min, energy_max, precision=3):
    """
    根据公式计算带中心的函数——即一定范围内：（能量和态密度乘积对能量的积分）/（态密度对能量的积分）
    :param energy: 能量numpy数组数据
    :param density: 态密度numpy数组数据
    :param energy_min: 设定的最低能量值
    :param energy_max: 设定的最高能量
    :param precision: 最后结果的小数位数，默认为3个小数
    :return: 返回能带中心的能量数值
    """

    e_density = energy * density
    e_density_integral = data_integration(energy, e_density, energy_min, energy_max)

    density_integral = data_integration(energy, density, energy_min, energy_max)

    band_center = round(e_density_integral / density_integral, precision)

    return band_center
