# -*- coding: utf-8 -*-
# @Time    : 2025/9/8 14:00
# @Author  : JunFei cai(蔡俊飞)
# @File    : aimd.py
# @Software: PyCharm

import numpy as np
import pandas as pd
from pymatgen.core import Structure
from pymatgen.io.vasp import Xdatcar
from tqdm import tqdm


def dimer_count(structure, o_index):
    """
    用于计算结构中氧原子发生dimer的数量
    :param structure: pymatgen中的结构对象
    :param o_index: 所有氧原子的索引，一个列表
    :return: 返回dimer的数量以及dimer占据所有原子对数量的百分比
    """
    dimer_number = 0
    pair_number = 0
    for site_1 in range(len(o_index)):
        for site_2 in range(site_1+1, len(o_index)):
            pair_number += 1 # 氧原子对数量计算
            if (structure[o_index[site_1]].distance(structure[o_index[site_2]])) < 1.7:
                dimer_number += 1  # dimer数量计算
    dimer_percentage = dimer_number / len(o_index) * 100

    return dimer_number, dimer_percentage


def migration_count(pri_structure, dimer_structure, pri_index, dimer_index):
    migration_number = 0
    pair_number = 0
    for site_index in range(len(pri_index)):
        if (pri_structure[pri_index[site_index]].distance(dimer_structure[dimer_index[site_index]])) > 1.3:
            migration_number += 1
    migration_percentage = migration_number / len(pri_index) * 100
    return migration_number, migration_percentage


def xdat_dimer(xdat_path, o_index):
    xdatcar = Xdatcar(xdat_path)
    dimer_data = []
    for i, structure in tqdm(enumerate(xdatcar.structures)):
        dimer_number, dimer_percentage = dimer_count(structure, o_index=o_index)
        dimer_data.append([i, dimer_number, dimer_percentage])
    return np.array(dimer_data)

def xdat_migration(xdat_path, pri_structure, pri_index, dimer_index):
    xdatcar = Xdatcar(xdat_path)
    migration_data = []
    for i, structure in tqdm(enumerate(xdatcar.structures)):
        migration_number, migration_percentage = migration_count(pri_structure, structure, pri_index, dimer_index)
        migration_data.append([i, migration_number, migration_percentage])

    return np.array(migration_data)
