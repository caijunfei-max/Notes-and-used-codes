#!/bin/bash
CURRENT_DIR=$(pwd)
for dir in *; do
    cd "$dir" || continue

    echo -e "102\n2\n0.04\n" | vaspkit
    sbatch run.sh
    
    cd $CURRENT_DIR
done
