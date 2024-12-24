# -*- coding: utf-8 -*-
# @Time    : 2024/12/24 15:09
# @Author  : JunFei Cai
# @File    : de_Li_hull.py
# @Software: PyCharm

from pymatgen.core import Structure
from itertools import combinations
import random
import copy
import os

"""
本脚本用于convex hull计算工作流，直接挖取运行一次会随机挖取一个锂离子、生成对应的结构。
"""

structure = Structure.from_file("POSCAR")

