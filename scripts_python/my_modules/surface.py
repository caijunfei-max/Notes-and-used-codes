# @Time    : 2025/2/14 16:17
# @Author  : JunFei Cai
# @File    : surface.py

"""
储存一系列与表面、催化相关的函数
"""

from pymatgen.core.structure import Structure, Molecule
from pymatgen.core.surface import Slab
import numpy as np


class Adsorbate(Molecule):
    """
    专门当作吸附分子的自定义分子类型
    """
    def __init__(self,
                 species,
                 coords,
                 charge,
                 spin_multiplicity,
                 validate_proximity,
                 site_properties,
                 charge_spin_check
                 ):

        super().__init__(
            species,
            coords,
            charge=charge,
            spin_multiplicity=spin_multiplicity,
            validate_proximity=validate_proximity,
            site_properties=site_properties,
            charge_spin_check=charge_spin_check,
        )

    def anchor_reset(self, center=True, index=0):
        """
        一般来说，一个分子mol在读取之后其中心位置处于原点000的位置，
        这不利于进行吸附位点放置、吸附距离判断，因为anchor设为000最好调用
        因此此函数将分子的某个原子设为anchor，默认第一个原子，可自定义
        :param center: 是不是重置为重心
        :param index: 移动到原点的原子索引, 只有在center设置为False的时候有效
        :return: 返回一个新的Molecule
        """
        reset_adsorbate = self.copy()
        if center:
            translate_vector = - self.center_of_mass
        else:
            translate_vector = - self[index].coords

        reset_adsorbate.translate_sites([i for i in range(len(reset_adsorbate))],
                                        vector=translate_vector
                                        )
        return reset_adsorbate


class CustomizedSlab(Structure):
    """
    A customized Slab slab， read surface from one file directly.
    pycharm自带的slab和初始结构是高度挂钩，直接从自定义的简化slab对象用于吸附模型基底的构建，
    因为研究的是一个高熵合金的表面，表面每一个原子都是一个独特的位点，
    因此此函数中吸附位点直接通过表面位点的遍历形成

    """

    def __init__(
            self,
            lattice,
            species,
            coords,
            charge,
            reorient_lattice=True,
            to_unit_cell=False,
            coords_are_cartesian=False,
            validate_proximity=False,
            site_properties=None
    ):
        self.reorient_lattice = reorient_lattice
        if coords_are_cartesian:
            coords = lattice.get_fractional_coords(coords)
            coords_are_cartesian = False

        super().__init__(
            lattice,
            species,
            coords,
            charge,
            validate_proximity=validate_proximity,
            to_unit_cell=to_unit_cell,
            coords_are_cartesian=coords_are_cartesian,
            site_properties=site_properties)

    @property
    def center_of_mass(self):
        """
        Returns the center of the mass of the slab
        :return: 结构原子质心
        """
        weights = [s.species.weight for s in self]
        center_of_mass = np.average(self.frac_coords, weights=weights, axis=0)
        return center_of_mass

    @property
    def surface_index(self, h=4.0):
        """
        返回表面原子的索引，判断基于自定义的高度，高于此值列为
        :param h: 判断为表面的最低高度
        :return: 列表，其中元素为表面原子的索引
        """
        surface_bool = []
        surface_atom_index = 0
        surface_index = []
        for i in self:
            if i.z > h:
                surface_bool.append(True)
                surface_index.append(surface_atom_index)

            else:
                surface_bool.append(False)
            surface_atom_index += 1
        return surface_index

    @property
    def surface_sites(self):
        if "site_properties" in self.site_properties.keys():
            pass
        else:
            self.mark_surface_property()
        return [site for site in self.sites if site.properties["surface_properties"] == "surface"]

    @property
    def subsurface_sites(self):
        if "site_properties" in self.site_properties.keys():
            pass
        else:
            self.mark_surface_property()
        return [site for site in self.sites if site.properties["surface_properties"] == "subsurface"]

    @property
    def normal(self):
        """
        Calculates the surface normal vector of the slab
        """
        normal = np.cross(self.lattice.matrix[0], self.lattice.matrix[1])
        normal /= np.linalg.norm(normal)
        return normal

    def mark_surface_property(self, h=4.0):
        """
        Returns the surface sites dict and add tag to each atom
        :param h: Height of surface atoms
        :return: add or update the surface_properties
        """
        surface_property = []

        for i in self:
            if i.z > h:
                surface_property.append("surface")

            else:
                surface_property.append("subsurface")

        self.add_site_property("surface_properties", surface_property)

    def copy(self, site_properties=None, *args, **kwargs):
        props = self.site_properties
        if site_properties:
            props.update(site_properties)
        return CustomizedSlab(
            self.lattice,
            self.species_and_occu,
            self.frac_coords,
            self.charge,
            site_properties=props,
            reorient_lattice=self.reorient_lattice
        )

    def add_adsorbate(self, molecule, ads_coord, repeat=None,
                      translate=(0, 0, 2.0), rotate_dict=False):
        """
        添加吸附分子，本函数借鉴于structure但是有一部分不一样
        :param molecule: 吸附分子或者原子,可以是pymatgen自带的Molecule，或者自定义的adsorbate，

        :param ads_coord: 吸附位点的位置，需要输入，也可以直接通过 surface_sites来确定
        :param repeat: (3-tuple or list), 决定是不是要对slab进行超晶格化
        :param translate: 是否针对表面位点进行一个位移，默认位移是向z方向位移2埃
        :param rotate_dict: 是不是要对吸附分子进行旋转，默认不旋转。如果旋转，需提供parameter_dict
                        形式如：{"theta": np.pi/2, "axis"=[0, 1, 0], "anchor"=(0, 0, 0)},
                        anchor最好设置为000，可以结合前面写的自定义adsorbate重置一下锚点
        :return:
        """
        struct = self.copy()

        if repeat:
            struct.make_supercell(repeat)
        molecule = molecule.copy()
        if "surface_properties" in struct.site_properties:
            molecule.add_site_property("surface_properties", ["adsorbate"] * molecule.num_sites)
        if "selective_dynamics" in struct.site_properties:
            molecule.add_site_property("selective_dynamics", [[True, True, True]] * molecule.num_sites)

        # translate
        molecule.translate_sites([i for i in range(len(molecule))],
                                 vector=translate)

        # rotate
        if rotate_dict:
            molecule.rotate_sites([i for i in range(len(molecule))],
                            theta=rotate_dict["theta"],
                            axis=rotate_dict["axis"],
                            anchor=rotate_dict["anchor"]
                            )

        for site in molecule:
            struct.append(
                site.specie,
                ads_coord + site.coords,
                coords_are_cartesian=True,
                properties=site.properties
            )
        return struct





