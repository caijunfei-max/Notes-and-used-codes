#!/gpfs/share/home/2301112381/.conda/envs/sub_1_cjf/bin/python

# File       : plusU.py
# Time       ：2023/8/27 11:41
# Author: Jun_fei Cai
# Description: Automatically GGA+U editor
from pymatgen.core import Structure

uValue = {"Cu":4.0, "Ni": 6.0, "Mn": 4.38, "Ag":1.5, "Ru": 4.0, 
        "Mo": 4.4, "Nb": 1.5, "Co": 3.4, "Fe": 4.0, "Cr": 3.5, 
        "Ti": 6.6, "Zr":5.0, "In":7.0, "Y": 5.0}
# reference
# Nb https://doi.org/10.1103/PhysRevB.85.155208
# Cu https://doi.org/10.1103/PhysRevB.85.155208
# Fe https://doi.org/10.1103/PhysRevB.85.155208
# Co https://doi.org/10.1103/PhysRevB.85.155208
# Cr https://doi.org/10.1103/PhysRevB.85.155208
# Ni https://doi.org/10.1103/PhysRevB.85.155208
# Mo https://doi.org/10.1103/PhysRevB.85.155208



path1 = "./POSCAR"
path2 = "./INCAR"


def d_switch(element):
    # 返回是否开U
    #if "d" in element.electronic_structure:
    if element.symbol in uValue.keys():
        return True
    else:
        return False


def u_value(element):
    # 设置默认值
    if d_switch(element):
       # if element.symbol in uValue.keys():
        return uValue[element.symbol]
    else:
        return 0


def ele_from_struct(structure):
    species_list = []
    # 从结构中生成元素，输入数据应该是一个pymatgen.core.Structure类
    for i in structure.species:
        if i in species_list:
            continue
        else:
            species_list.append(i)
    return species_list


def pluslist(structure):
    # 返回加u设置的字符串放在列表中
    uswitch = "LDAU = True"

    utype = "LDAUTYPE = 2"

    on_off = []
    for i in ele_from_struct(structure):
        if d_switch(i):
            on_off.append("2")
        else:
            on_off.append("-1")
    u_on_off = "LDAUL = {0}".format(" ".join(on_off))

    value_u = []
    value_j = []
    for ele in ele_from_struct(structure):
        value_u.append(str(u_value(ele)))
        value_j.append("0")
    u = "LDAUU = {0}".format(" ".join(value_u))
    j = "LDAUJ = {0}".format(" ".join(value_j))

    ustr_list = [uswitch, utype, u_on_off, u, j]
    return ustr_list


poscar = Structure.from_file(path1)
with open(path2, "a") as f:
    for parameter in pluslist(poscar):
        f.write(parameter+"\n")
    f.close()
