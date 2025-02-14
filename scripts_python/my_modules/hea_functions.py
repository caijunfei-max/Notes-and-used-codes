# @Time    : 2025/2/14 16:16
# @Author  : JunFei Cai
# @File    : hea_functions.py

"""
储存一系列处理高熵合金的函数
"""
import itertools
import random


def hea_generation(elements, combination_length=5, random_yield_num=0, random_seed=1):
    """
    此函数用于获得高熵合金的元素组合
    :param elements: 一个包含可遍历的列表
    :param combination_length: 高熵合金中应该具有哪些元素
    :param random_yield_num: 默认是不随机取样，如果设置了数值，则随机从所有组合中取样对应数量
    :param random_seed: 设置随机种子
    :return: 返回一个列表，包含了所有的元素组合
    """
    # 使用itertools.combinations生成所有长度为combination_length的组合
    combinations = list(itertools.combinations(elements, combination_length))
    if random_yield_num:
        random.seed(random_seed)
        hea_list = random.sample(combinations, random_yield_num)
    else:
        hea_list = combinations

    return hea_list


def generate_yaml_config(elements, output_file="h_entropy.yaml"):
    """
    根据元素元组生成YAML格式配置文件
    :param elements: 包含5个元素的元组，如 ("Cr", "Mn", "Fe", "Co", "Ni")
    :param output_file: 输出文件名
    :return: 生成一个yaml文件，用于sqsgenerator
    """
    # 验证输入元组长度
    if len(elements) != 5:
        raise ValueError("输入元组必须包含5个元素")

    # 生成YAML内容模板
    yaml_content = f"""structure:
  supercell: [2, 2, 2]
  file: Pt.vasp
iterations: 1e8
shell_weights:
  1: 1.0
composition:
  {elements[0]}: 6
  {elements[1]}: 8
  {elements[2]}: 6
  {elements[3]}: 6
  {elements[4]}: 6
"""

    # 写入文件
    with open(output_file, "w") as f:
        f.write(yaml_content)
        print(f"配置文件已生成：{output_file}")
