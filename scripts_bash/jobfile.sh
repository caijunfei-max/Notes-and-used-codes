#!/bin/bash

echo "Enter the job priority (default is 'normal')"
read priority
priority=${priority:-normal}

echo "Enter the job name (default is 'sol-test'): "
read job_name
job_name=${job_name:-sol-test}


echo "Enter the nodes (default is '1')"
read nodes
nodes=${nodes:-1}

ntasks_per_node=32

total_tasks=$((nodes * ntasks_per_node))

filename="run.sh"

cat << EOF > $filename
#!/bin/bash
#SBATCH -o job.%j.out
#SBATCH -p C032M0128G
#SBATCH --qos=$priority
#SBATCH -J $job_name
#SBATCH --nodes=$nodes
#SBATCH --ntasks-per-node=32

module load intel/2017.1
module load vasp/5.4.4-intel-2017.1

srun hostname -s | sort -n > slurm.hosts
mpirun -n $total_tasks -machinefile slurm.hosts vasp_std > log
EOF

echo "File '$filename' has been created with the job name '$job_name'."

