#!/bin/bash

# Load up virtual environemnt
source ENV/bin/activate

# Loop through files and execute SLURM jobs
FILES="scripts/*.sh"
for freesurfer_script in $FILES
do
        echo "Submitting job "$freesurfer_script
        sbatch $freesurfer_script
done
