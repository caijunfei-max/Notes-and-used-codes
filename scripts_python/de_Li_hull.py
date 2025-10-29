# -*- coding: utf-8 -*-
# @Time    : 2024/12/24 15:09
# @Author  : JunFei Cai
# @File    : de_Li_hull.py
# @Software: PyCharm

from pymatgen.core import Structure
import numpy as np


"""
本脚本用于convex hull计算工作流，直接挖取运行一次会随机挖取一个锂离子、生成对应的结构。
"""
sites = [i for i in range(16)]
structure = Structure.from_file("CONTCAR")
de_structure = structure.copy()
de_structure.remove_sites(np.random.choice(sites, size=12, replace=False))

de_structure.to(filename="de_CONTCAR", fmt="poscar")
