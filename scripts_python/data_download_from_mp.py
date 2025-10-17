# @Time    : 2025/10/16 23:31
# @Author  : JunFei Cai
# @File    : data_download.py

from mp_api.client import MPRester
# download data from material project


#%%
API_KEY = "fqPPo7Czb5mkbFh8mltlZd0I33csuKv0"
mpr = MPRester(API_KEY)

#%%
help(mpr.materials.summary.search)

#%%
docs=mpr.materials.summary.search(formula="Li*O2", all_fields=False,
                                  fields=['material_id', 'structure', 'symmetry', 'formula_pretty'])

#%%
for structure in docs:
    symmetry_symbol = structure.symmetry.symbol
    safe_name = symmetry_symbol.replace("\\", "_").replace("/", "_")
    formula = structure.formula_pretty
    mp_id = structure.material_id.string.split('-')[1]
    structure.structure.to(
        safe_name+"-"+mp_id+"-"+formula+'.cif'
    )

