# @Time    : 2024/12/24 15:21
# @Author  : JunFei Cai
# @File    : get_charged.py

from pymatgen.core import Structure
"""
全脱锂结构
"""

init_structure = Structure.from_file("POSCAR")
structure = Structure.from_file("POSCAR")
structure.remove_species(["Li"])
structure.to("charged_POSCAR")
