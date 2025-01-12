# -*- coding: utf-8 -*-
# @Time    : 2024/9/19 14:39
# @Author  : JunFei cai(蔡俊飞)
# @File    : functions.py
# @Software: PyCharm

import os
from mendeleev import element
import pickle
import json
import re
import random
import math
from functools import reduce
import itertools
import numpy as np
from scipy.integrate import simpson
from pymatgen.core import Structure


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


def sum_calc(data: tuple | list) -> float:
    """
    本函数用于简便地计算元组或者列表等类似结构中数据的和
    :param data: 可遍历的数据结构，要求内部全部是数字
    :return: 和，类型浮点数
    """
    result = 0
    for i in data:
        result += i
    return result


def find_symbol(atoms):
    numbers = atoms.numbers
    symbols = []
    for atomic_number in numbers:
        number_symbol = element(int(atomic_number)).symbol
        symbols.append(number_symbol)

    return symbols


# generate chemical symbols for the cluster expansion
def chemical_symbols_generate(structure, replace_dict):
    """
    作者：蔡俊飞
    :param structure: Atoms object in ase
    :param replace_dict: a dict for replace in the elements in structure
    :return: a chemical symbols used for the cluster_expansion
    """
    numbers = structure.numbers
    symbols = []
    for atomic_number in numbers:
        symbol = element(int(atomic_number)).symbol
        symbols.append(symbol)

    chemical_symbols = []
    for symbol in symbols:
        if symbol in list(replace_dict.keys()):
            print(True)
            chemical_symbols.append(replace_dict[symbol])
        else:
            print(False)
            chemical_symbols.append([symbol])

    return chemical_symbols


# json write
def write_json(save_path, data):
    """
    :param save_path: path for save the json file
    :param data: json type data
    :return: save a file containing json data
    """
    assert save_path.split(".")[-1] == "json"
    with open(save_path, "w") as file:
        json.dump(data, file)


# json write
def read_json(file_path):
    """
    :param file_path:  load a json file
    :return: a json object from a json file
    """
    assert file_path.split(".")[-1] == "json"
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def write_pkl(save_path, data):
    with open(save_path, "wb") as file:
        pickle.dump(data, file)


def read_pkl(file_path):
    with open(file_path, "rb") as file:
        data = pickle.load(file)
    return data


def extract_symbols(ion):
    """
    extract symbols from an ion string
    for example: get "Na", "V" from "Na+", "V5+"
    :param ion: ion-like string, such as "V5+", "Na+", "Cl-"
    :return: element-like string, such as "V", "Na", "Cl"
    """
    match = re.match(r"([A-Z][a-z]?)", ion)
    symbol = match.group(0)
    return symbol


def random_sample(input_list: list,
                  n: int,
                  seed: int | None = None):
    if seed is not None:
        random.seed(seed)

    return random.sample(input_list, n)


def find_atomic_combinations(atomic_dict: dict,
                             n: int) -> list[dict]:
    """
    Input an atomic_dict and an n, this function will find all possible combinations of atom numbers
    to realize charge balance. This function was wrote to perform substitution for structures.
    :param atomic_dict: format like {"Mn": 2, "Co": 3, "Ni": 2, "Fe": 3}
    :param n: an integer
    :return: a list of all possible combinations of atom numbers
    """
    for key, value in atomic_dict.items():
        assert type(key) is str, f"{key} in atomic_dict is not a string"
        assert type(value) is int, f"{value} in atomic_dict is not an integer"

    assert type(n) is int, f"{n} must be integer"
    target_sum = -n
    initial_combination = {ele: 1 for ele in atomic_dict}  # at least one atom for each atom
    remaining_target = target_sum - sum(atomic_dict[ele] for ele in initial_combination)
    results = []

    # 处理组合
    if remaining_target < 0:
        results = "No possible combinations"  # 直接返回初始组合
    else:
        current_combination = initial_combination.copy()

        # 使用栈来模拟递归
        stack = [(current_combination.copy(), remaining_target)]

        while stack:
            current_combination, current_target = stack.pop()

            if current_target == 0:
                results.append(current_combination)
                continue
            if current_target < 0:
                continue

            for ele, valence in atomic_dict.items():
                current_combination[ele] += 1
                stack.append((current_combination.copy(), current_target - valence))
                current_combination[ele] -= 1

    return results


# calculate all the possible combinations for ions for charge balance
def substitution_charge_balancer(charge_number_dict: dict,
                                 substitution_charge_dict: dict,
                                 atom_number):
    """
    :param charge_number_dict: A dictionary of charge numbers for identified elements,
    which contains charge as key and number as values. key and values should be integer
    for example: {-2: 3,  -3: 2}
    :param substitution_charge_dict: A dictionary of charge of elements for substitution.
    for example: {"Mn":2, "Ni":3 , "Co":2}， the max length is 4
    :param atom_number: the number of substitution atoms
    :return: All possible substitution combination in a list, The list include
    """
    identified_charge = 0
    for key, value in charge_number_dict.items():
        assert type(key) is int and type(value) is int, \
            "The key and value in charge_number_dict should be integer"
        identified_charge += key * value

    for key, charge in substitution_charge_dict.items():
        assert type(charge) is int, \
            "The value in substitution_charge_dict should be integer"
        assert symbol_judge(charge) is True, \
            "Only positive charge allowed in as substitution atoms"
    target_number = identified_charge
    all_combinations = find_atomic_combinations(substitution_charge_dict, target_number)

    result = []
    for combination in all_combinations:
        combination_values = list(combination.values())
        if sum(combination_values) == atom_number:
            result.append(combination)

    assert len(result) > 0, \
        "No possible combinations found"

    return result


def map_generate(initial_species, combination_dict, base_atoms=0):
    """
    Generate a map for substitution transformation in pymatgen.
    :param initial_species: str specified the initial species of atom
    :param combination_dict: dict with species and
    :param base_atoms: how many atoms in initial species is set to unchanged.
    :return: a map dict which can used to be parameter of pymatgen.SubstitutionTransformation
    """
    sum_value = sum(list(combination_dict.values())) + base_atoms
    fraction_map = {}

    for key, value in combination_dict.items():
        fraction_of_atom = value / sum_value
        fraction_map[key] = fraction_of_atom

    if base_atoms > 0:
        fraction_initial = base_atoms / sum_value
        fraction_map[initial_species] = fraction_initial

    species_map = {initial_species: fraction_map}
    return species_map


def ion_taken(ion_list):
    """
    function for find_equal_combination, take ions from three lists
    :param ion_list: [[],[]], include ion information
    :return: combination of ions
    """
    all_ion_combination = set()

    for values in itertools.product(*ion_list):
        if len(set(values)) == len(values):
            combination_tuple = tuple(
                sorted(values, key=lambda x: (ion_list.index([lst for lst in ion_list if x in lst][0])))
            )
            all_ion_combination.add(combination_tuple)

    return list(all_ion_combination)


def find_equal_combinations(target_sum, charges, count, element_count, charge_ion_map):
    """
    作者：蔡俊飞&chatgpt
    给定总数target_sum, 以及一个数字列表nums，每个数字取的数量为count，这几个数字乘以count后相加的和为target_sum，
    首先生成一个列表中含有各种组合以平衡电荷，然后根据这个列表中的组合对charge_ion_map中的电荷、离子对进行取值
    :param target_sum: 数字，目标和
    :param charges: 一个含有电荷值整数的列表，可以重复取值
    :param count: 取多少个数
    :param element_count: 每个数取取多少次
    :param charge_ion_map: 用于设定电荷、离子类型的映射，比如{2:["Mg2+", "Mn2+"]]
    :return: 一个字典，字典的键为一个元组charge_combination（合理的价电子组合），值为列表ion_combinations（包含离子名称）
    如：{(2, 4, 6): [('Ti2+', 'Co4+', 'Mo6+'), ('Ca2+', 'Si4+', 'Mo6+')]}
    """
    # 生成所有可能的四元组组合，允许重复取值
    combinations = itertools.combinations_with_replacement(charges, count)
    valid_combinations = []

    for combo in combinations:
        # 计算组合中每个元素的数量，数量均为element_count
        if sum(combo) * element_count == target_sum:
            valid_combinations.append(combo)
    charge_ion_combination = dict()
    for input_tuple in valid_combinations:

        counts = {x: input_tuple.count(x) for x in set(input_tuple)}
        choices = [charge_ion_map[key] for key, ion_count in counts.items() for _ in range(ion_count)]
        # choices = [charge_ion_map[key] for key in counts.keys()]
        ion_combination = ion_taken(choices)
        charge_ion_combination[input_tuple] = ion_combination

    return charge_ion_combination


def get_complement(original_list, i):
    """
    获得补集，在类OxygenEnvironment中用来删掉目标氧原子之外所有氧原子的函数。
    :param original_list: 一个列表
    :param i: 选定元素，注意该元素必须在original_list中
    :return: 另一个列表，是original_list中关于element的补集
    """
    assert i in original_list, f"{i} is not in the original list"

    original_array = np.array(original_list)
    complement = original_array[original_array != i]
    return complement


def get_unique_neighbors_symbols(neighbor):
    """
    对于本研究所针对的构型，氧原子周围八面体的构型的六个neighbor原子至少含有三个Li原子，而另外三个原子是独特原子
    :param neighbor: Oxygen环境的neighbors
    :return: 三个unique neighbor的符号
    """
    neighbor_symbol = [i.specie.symbol for i in neighbor]
    li_removed = 0
    # 遍历列表，移除三个 "Li"
    for _ in range(3):
        if 'Li' in neighbor_symbol:
            neighbor_symbol.remove('Li')
            li_removed += 1
    return neighbor_symbol


def get_integrated_dos(dos, min_energy, max_energy):
    # 用于计算态密度的积分，目前只写了有自旋极化的积分，后面有需要再写无自旋的
    dos_dict = dos.as_dict()
    energy_density_range = {}
    for energy, up, down in zip(dos_dict["energies"],
                                dos_dict["densities"]["1"],
                                dos_dict["densities"]["-1"]):
        if energy > max_energy or energy < min_energy:
            continue
        else:
            energy_density_range[energy] = [up, down]

    energy = [key for key in energy_density_range.keys()]
    up = [density[0] for density in energy_density_range.values()]
    down = [density[1] for density in energy_density_range.values()]

    up_integrated_dos = simpson(y=up, x=energy)
    down_integrated_dos = simpson(y=down, x=energy)
    total_integrated_dos = up_integrated_dos + down_integrated_dos

    return [total_integrated_dos, up_integrated_dos, down_integrated_dos]


def manual_substitution(path="POSCAR", substituted_dict=None, get_primitive=False):
    """
    本函数用于手动设置地对Li2RuO3或者Li2MnO3这样的结构进行掺杂，而非随机化选取，注意只掺杂金属层的三个过渡金属。
    :param path: 给定路径，默认是当前路径下的POSCAR
    :param substituted_dict: 字典，键值分别为想要被掺杂的位点索引和目标类型（含有目标元素的列表）,注意要一一对应
    比如：{4："Li", 6: "Ru"}
    :param get_primitive: 如果设置为True的话，自动查找掺杂后结构的原胞（写这个是因为我要算HSE06）
    :return: 一个掺杂过的结构
    """
    initial_structure = Structure.from_file(path)
    for key, value in substituted_dict.items():
        initial_structure.replace(key, value)

    if get_primitive:
        substituted_structure = initial_structure.get_primitive_structure()
    else:
        substituted_structure = initial_structure

    return substituted_structure


def get_sub_path(path):
    """
    获得指定目录下所有目录并返回其路径列表
    :param path: 指定目录
    :return: 一个列表，列表中包含指定目录中所有目录的绝对路径
    """
    root_paths = []
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            root_paths.append(full_path)
    return root_paths


def find_gcd_of_list(numbers):
    # 获得公因数，作为后续simplify_chemical_formula的辅助函数
    return reduce(math.gcd, numbers)


def simplify_chemical_formula(formula, target_oxygen_count=3, decimal_places=1):
    """
    该函数用于简化化学式，调整元素数量以使得氧元素的数量符合目标数量。
    :param formula: 化学式字符串
    :param target_oxygen_count: 目标氧元素数量，默认为3
    :param decimal_places: 如果出现小数，保留的小数位数，默认为1
    :return: 返回简化后的化学式
    """
    # 去掉空格
    formula = formula.replace(" ", "")

    # 使用正则表达式匹配元素符号和数量
    pattern = r'([A-Za-z]+)(\d*)'
    elements = {}

    # 查找所有匹配的元素和数量
    for match in re.finditer(pattern, formula):
        element_match = match.group(1)
        quantity = match.group(2)
        # 如果没有指定数量，默认为1
        if quantity == '':
            quantity = 1
        else:
            quantity = int(quantity)
        elements[element_match] = quantity

    # 获取氧元素数量
    oxygen_count = elements.get('O', 0)

    # 如果氧的数量不为零，则进行简化处理
    if oxygen_count != 0:
        # 计算比例因子，目标是使氧的数量为 target_oxygen_count
        ratio_factor = target_oxygen_count / oxygen_count

        # 根据比例因子调整所有元素的数量
        for element_match in elements:
            elements[element_match] *= ratio_factor

    # 构造简化后的化学式
    simplified_formula = ''
    for element_match, quantity in elements.items():
        # 如果元素数量接近0，跳过该元素
        if quantity < 1e-6:
            continue

        # 如果数量是1，则只显示元素符号
        if quantity == 1:
            simplified_formula += f'{element_match}'
        else:
            # 格式化数量为整数或保留指定小数位数
            if quantity != int(quantity):
                simplified_formula += f'{element_match}{quantity:.{decimal_places}f}'
            else:
                simplified_formula += f'{element_match}{int(quantity)}'

    return simplified_formula


def formula_to_latex(chemical_formula):
    """
    在画图的时候，formula直接输入的话所有数字都是没有下标的，
    本函数用于自动把所有formula形式的字符串中的数字变为下标
    :param chemical_formula: 类似Li2Zr0.5V0.5O3的字符串
    :return: matplotlib能够识别的latex形式，比如$Li_2Zr_{0.5}V_{0.5}O_3$
    """
    # 正则表达式匹配元素和它们的数量（可以是整数或小数）
    pattern = re.compile(r'([A-Za-z]+)(\d*\.?\d*)')

    # 用于存储最终的 LaTeX 格式字符串
    latex_string = ""

    # 查找所有元素和数量
    for element, quantity in re.findall(pattern, chemical_formula):
        if quantity == "":
            # 没有数量时，表示为 1, 但在 LaTeX中不显示1
            latex_string += f"{element}"
        else:
            # 对数量部分进行处理，如果是小数就加上大括号
            if '.' in quantity:
                latex_string += f"{element}_{{{quantity}}}"
            else:
                latex_string += f"{element}_{quantity}"

    # 添加美元符号使其成为 LaTeX 格式
    return f"${latex_string}$"
