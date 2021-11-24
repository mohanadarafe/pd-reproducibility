import os, glob, json
from boutiques.descriptor2func import function
from os import path

def go_to_root_folder():
    '''
    The following function returns to the root directory
    '''
    while 'environment.yml' not in os.listdir():
        os.chdir("..")

def prepare_data_folder():
    '''
    The following function creates the necessary folders in case they are missing
    '''
    ML_PATH = "./ml"
    DATA_PATH = "./data"
    BASH_SCRIPTS = "./scripts"
    NC_PATH = "data/subjects/NC"
    PD_PATH = "data/subjects/PD"
    JSON_INPUT = "data/json_input"

    if (not os.path.isdir(ML_PATH)):
        os.mkdir(ML_PATH)

    if (not os.path.isdir(DATA_PATH)):
        os.mkdir(DATA_PATH)

    if (not os.path.isdir(BASH_SCRIPTS)):
        os.mkdir(BASH_SCRIPTS)

    if (not os.path.isdir(NC_PATH)):
        os.makedirs(NC_PATH)

    if (not os.path.isdir(PD_PATH)):
        os.makedirs(PD_PATH)

    if (not os.path.isdir(JSON_INPUT)):
        os.makedirs(JSON_INPUT)

def create_json_input(patientType: str):
    '''
    The following function creates the JSON input files for Boutques recon-all
    '''
    subId = 0
    for mri in glob.glob(f"data/{patientType}/*/*"):
        input_json = {"license": "license.txt", "subjid": f"{patientType}_sub{subId}", "input": mri, "qcache_flag": True}
        with open(f"data/json_input/{patientType}_sub{subId}_json.json", "w") as outfile:
            json.dump(input_json, outfile)
        subId += 1
    
    return subId

def create_slurm_scripts():
    '''
    Creates a SLURM script for each NiFTI
    '''
    for jsonInputPath in glob.glob("data/json_input/*.json"):
        patient_type = jsonInputPath.split("/")[2].split("_")[1]
        with open(f"scripts/{patient_type}.sh", "w") as f:
            f.write(f"#!/bin/bash\n")
            f.write(f"#SBATCH --nodes=1\n")
            f.write(f"#SBATCH --ntasks=1\n")
            f.write(f"#SBATCH --cpus-per-task=2\n")
            f.write(f"#SBATCH --mem=32gb\n")
            f.write(f"#SBATCH --time=20:00:00\n\n")
            f.write(f"bosh exec launch -s zenodo.4043546 {jsonInputPath}\n")  

def prepare_input():
    '''
    Prepare the data to be created before running volumejob.sh
    '''
    prepare_data_folder()
    create_json_input("NC")
    create_json_input("PD")
    create_slurm_scripts("NC")
    create_slurm_scripts("PD")

def recon_patient(mri_scan: str, subjectId: int):
    '''
    @DEPRECATED: not using this at the moment
    Calls FreeSurfer's recon-all method to get brain volumes
    @mri_scan: input NiFTi file
    @subjectId: subject ID
    '''
    subject = f'sub{subjectId}'
    recon_all = function("zenodo.4043546")
    recon_all(
        input=mri_scan, 
        subjid=subject, 
        license="license.txt",
        qcache_flag=True
    )

def get_mri_scans(dataType: str) -> list:
    '''
    The following function returns a list of file paths to NiFTI data
    @dataType: PD or NC
    '''
    files = []
    path = f"data/{dataType}/*"

    for filepath in glob.glob(f"{path}/*"):
        files.append(filepath)

    return files

def move_volume_stats_from_job():
    '''
    Moves all stats files from recon-all to proper location
    '''
    for subFolderName in glob.glob("*_sub*"):
        patient_type = subFolderName[0:2]
        folder_name = subFolderName.split("_")[1]

        if (not os.path.isdir(f"data/subjects/{patient_type}/{folder_name}")):
            os.mkdir(f"data/subjects/{patient_type}/{folder_name}")

        os.system(f"cp {subFolderName}/stats/aseg.stats data/subjects/{patient_type}/{folder_name}")
        
def convert_stats_to_csv(inputStatsFile: int, outputCsvFile: str):
    '''
    Converts the aseg.stats file produced from recon-all to a CSV file
    '''
    os.system(f"singularity exec freesurfer-freesurfer-7.1.1.simg asegstats2table -i {inputStatsFile} --meas volume --tablefile {outputCsvFile}")
