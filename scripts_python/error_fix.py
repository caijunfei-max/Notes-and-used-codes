import os
import shutil
import subprocess
from pathlib import Path
from pymatgen.io.vasp import Incar
"""
for calculation task, if error is happened, this script will help restart the calculation
"""

current_dir = os.getcwd()
subdirs = [d for d in os.listdir(current_dir) if
        os.path.isdir(os.path.join(current_dir, d)) and "_" in d]

for subdir in subdirs:
    work_path = os.path.join(current_dir, subdir, "pri")
    log_path = os.path.join(work_path, "log")

    log_text = Path(log_path).read_text()
    if "reached required accuracy " in log_text:
        print("The job in {0} has completed successfully!".format(subdir))
        continue
    elif "Error EDDDAV" in log_text:

        # change the algorithm
        incar = Incar.from_file(os.path.join(work_path, "INCAR"))
        incar["ALGO"] = "Fast"
        incar.write_file(os.path.join(work_path, "INCAR"))
        subprocess.run(
            ["sbatch", "run.sh"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=work_path,
            text=True
            )
        print("{0}: Algorithm failure, new job has been submitted".format(subdir))
    elif "please rerun with smaller EDIFF" in log_text:
        incar = Incar.from_file(os.path.join(work_path, "INCAR"))
        incar["EDIFF"] = "1E-07"
        incar.write_file(os.path.join(work_path, "INCAR"))
        shutil.copyfile(os.path.join(work_path, "CONTCAR"), os.path.join(work_path, "POSCAR"))
        subprocess.run(
            ["sbatch", "run.sh"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=work_path,
            text=True
            )
        print("EDIFF {0} error: new job has been submitted".format(subdir))
    


    else:
        print("Some unknown error occured in {0}! You need to fix it manually.".format(subdir))
