# @Time    : 2024/12/24 15:21
# @Author  : JunFei Cai
# @File    : get_charged.py

from pymatgen.core import Structure
import random
import copy
import re

"""
获得脱锂结构，默认全部脱锂。
"""

init_structure = Structure.from_file("POSCAR")

def get_element_quantity(element, formula):
    """
    通过正则表达式来获取一个公式里面元素的数量
    :param element: 表示元素的字符串，Mn，Li啥的。
    :param formula: structure结构的formula， 形式类似Li24 Mn4 Al4 Ru4 O36， 可以直接通过structure.formula获得
    :return: 一个数字
    """
    # 正则表达式：匹配指定元素和它后面的数字
    pattern = r'(' + re.escape(element) + r')(\d+)'  # 用re.escape保证元素符号的特殊字符不会出错
    match = re.search(pattern, formula)  # 使用search匹配第一个符合的元素

    # 如果找到了匹配的元素，则返回该元素的数量
    if match:
        return int(match.group(2))  # 获取该元素后的数字部分
    return 0  # 如果没有找到，返回0


def get_charged(structure, ion_type=None, de_ion_number=None):
    """
    获得脱锂的结构，需要自己设置脱去离子的数量，如果没有输入，就脱去全部离子
    2024/12/24:如果输入就全部输入，要么都用默认，不然会报错（没时间debug了，好累）
    :param structure: 初始结构
    :param ion_type: 输运离子的类型，默认为POSCAR结构的第一个原子类型
    :param de_ion_number: 脱去结构的数量，默认为全部
    :return: 脱锂后的结构
    """
    # 如果没有指定脱嵌元素，设定POSCAR第一个元素类型为脱嵌元素
    if ion_type is None:
        ion_type = structure[0]

    # 如果没有指定数量，全部脱嵌
    if de_ion_number is None:
        charged_structure = copy.deepcopy(structure).remove_species(ion_type.species)


    elif type(de_ion_number) == int and type(ion_type) == str :
        # 搜索脱嵌离子的索引
        ion_indices =  [i for i, site in enumerate(init_structure.sites)
                      if site.specie.symbol == ion_type]
        # 随机抽样去掉离子的索引
        remove_sites = random.sample(ion_indices, de_ion_number)
        charged_structure = copy.deepcopy(structure).remove_sites(remove_sites)

    else:
        charged_structure = None

    return charged_structure

# 从外部获取需要脱嵌的离子类型和脱嵌的数量
de_ion_type = input("please input the type ion for de-intercalation")
if de_ion_type == "":
    de_ion_type = None

de_intercalation_num = input("please input the number of ions to de-intercalation:")
if de_intercalation_num == "":
    de_intercalation_num = None

# 如果外部没有输入脱嵌数量，用默认值
if de_intercalation_num is None:
    print("test")
    de_intercalation_struct = get_charged(init_structure,
                                          ion_type=de_ion_type,
                                          de_ion_number=de_intercalation_num)
# 如果外部输入了脱嵌数量，则用外部设定值
else:
    de_intercalation_struct = get_charged(init_structure,
                                       ion_type=de_ion_type,
                                       de_ion_number=int(de_intercalation_num))

print(de_intercalation_struct)
# de_intercalation_struct.to("charged_POSCAR")

