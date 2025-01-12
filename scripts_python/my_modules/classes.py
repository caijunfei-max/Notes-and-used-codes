# -*- coding: utf-8 -*-
# @Time    : 2024/10/12 19:52
# @Author  : JunFei cai(蔡俊飞)
# @File    : classes.py
# @Software: PyCharm

# from emmet.core.vasp.calculation import Calculation
# from icet import ClusterExpansion

from my_modules.functions import *
import random
import copy
# from scipy.integrate import simpson
from itertools import combinations
# from pymatgen.electronic_structure.dos import CompleteDos
from pymatgen.core import Structure
# from pymatgen.transformations.standard_transformations import SubstitutionTransformation


class BalancedStructure(Structure):
    def __init__(self,
                 lattice,
                 species,
                 coords,
                 ion_combination: tuple | None = None,
                 charge_combination: tuple | None = None,
                 charge: float | None = None,
                 validate_proximity: bool = False,
                 to_unit_cell: bool = False,
                 coords_are_cartesian: bool = False,
                 site_properties: dict | None = None
                 ):
        super(Structure, self).__init__(
            lattice,
            species,
            coords,
            charge=charge,
            validate_proximity=validate_proximity,
            to_unit_cell=to_unit_cell,
            coords_are_cartesian=coords_are_cartesian,
            site_properties=site_properties
        )
        self.ion_combination = ion_combination
        self.charge_combination = charge_combination
        # self.ion_ratio = 1 / len(self.ion_combination)

    def update_ion_charge(self, ion_combination, charge_combination):
        self.ion_combination = ion_combination
        self.charge_combination = charge_combination

    def get_species_map(self, initial_atom: str):
        assert self.ion_combination is not None, "No ion combination is update"
        assert self.charge_combination is not None, "No charge combination is update"
        new_atom_map = {}
        ion_ratio = 1/len(self.ion_combination)
        for ion in self.ion_combination:
            # atom = extract_symbols(ion)
            ratio = ion_ratio
            new_atom_map[ion] = ratio
        species_map = {initial_atom: new_atom_map}

        return species_map


class CathodeDeIntercalationGroup:
    """
    一组结构，包括未脱锂的结构以及指定脱锂数量的正极结构，这个类只适用于锂离子正极，如果使用钠离子正极需要进行一定的修改
    # 这一个类在课题四中脱锂脱一半使用到，泛用需要进一步修改
    """
    def __init__(self,
                 initial_structure: Structure,
                 de_intercalation_nums: [int]
                 ):
        self.initial_structure = initial_structure
        self.de_intercalation_nums = de_intercalation_nums
        self.charged_structure = None  # 全脱锂结构，初始为None，需要运行get_charged_structure以获得
        self.de_intercalation_dict = None  # 根据脱锂数生成的{脱锂数：脱锂结构}字典，可以通过

    # @staticmethod
    def get_charged_structure(self):
        """
        获得全脱锂结构，返回一个pymatgen.core.Structure，不需要参数
        :param self:
        :return:全部脱锂的结构
        """
        charged_structure = copy.deepcopy(self.initial_structure)
        charged_structure.remove_species(['Li'])
        self.charged_structure = charged_structure

    def de_intercalation_cathodes_randomly(self, structure_num=None, seed=1):
        """
        随机脱锂，并且根据structure_num对每个脱锂态随机选取结构用于计算
        :param structure_num: 正整数，用于指定返回的结构数量用于计算
        :param seed: 设定随机取值的种子，默认为1
        :return: 更新类的属性，de_intercalation_dict, 字典，键为self.de_intercalation)nums里面的数字，值为特定的脱锂结构组成的列表
        """
        # 保护性，如果总结构数量大于100，那么强行设定只能输出100个结构，避免输出远超实际需要的结构量
        li_indices = [i for i, site in enumerate(self.initial_structure.sites)
                      if site.specie.symbol == "Li"]  # 找到锂离子的index
        de_intercalation_structures = {}
        random.seed(seed)
        for num in self.de_intercalation_nums:
            li_combination = list(combinations(li_indices, num))
            if structure_num is not None:
                assert (type(structure_num) is int and
                        0 < structure_num < len(li_indices)), \
                    "structure_num must be an positive integer, and its value can't larger than the number of Li sites"
                de_struct_list = random.sample(li_combination, structure_num)
            elif structure_num is None and len(li_combination) > 100:
                sample_num = 100  # 如果组合数大于100，设定取值为100个
                de_struct_list = random.sample(li_combination, sample_num)
            else:
                de_struct_list = li_combination

            num_structure = []  # 脱锂数中存的结构
            for i in de_struct_list:
                de_intercalation_structure = copy.deepcopy(self.initial_structure)
                de_intercalation_structure.remove_sites(i)
                num_structure.append(de_intercalation_structure)

            de_intercalation_structures[num] = num_structure

        self.de_intercalation_dict = de_intercalation_structures


class OxygenEnvironment:
    def __init__(self,
                 original_structure: Structure):
        self.structure = original_structure
        o_index = [i for i, site in enumerate(self.structure)
                   if site.specie.symbol == 'O']
        self.o_index = o_index

    def get_nearest_atom(self, r=3.0):
        """
        获得self.structure中所有氧原子周围最近邻的原子（不包括其他氧原子）
        :param r:
        :return:
        """
        # 获得所有氧原子最近的过渡金属，如果是八面体配位即是6个过渡金属或者Li。
        oxygen_neighbors = {}  # 字典，键为氧的索引，值为该氧周围的环境

        for index in self.o_index:
            remove_index = get_complement(self.o_index, index)
            structure_i = copy.deepcopy(self.structure)
            structure_i.remove_sites(remove_index)
            neighbors_i = structure_i.get_neighbors(structure_i[self.o_index[0]], r)

            oxygen_neighbors[index] = neighbors_i
            # 因为把其他氧原子全删掉，剩下的氧原子索引就是原本第一个氧原子的索引

        return oxygen_neighbors


# testing block
if __name__ == "__main__":
    print("testing text")
