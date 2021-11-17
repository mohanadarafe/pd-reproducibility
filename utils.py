import os, glob
from boutiques.descriptor2func import function
from os import path

def go_to_root_folder():
    while 'environment.yml' not in os.listdir():
        os.chdir("..")

def prepare_data_folder():
    NC_PATH = "data/subjects/NC"
    PD_PATH = "data/subjects/PD"

    if (not os.path.isdir(NC_PATH)):
        os.makedirs(NC_PATH)

    if (not os.path.isdir(PD_PATH)):
        os.makedirs(PD_PATH)

def recon_patient(mri_scan: str, subjectId: int):
    '''
    TODO: Change this to Boutiques/Docker
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

def convert_stats_to_csv(subId: int, outputPathName: str):
    '''
    TODO: Change this to Boutiques/Docker
    Converts the aseg.stats file produced from recon-all to a CSV file
    '''
    os.system(f"python2 $FREESURFER_HOME/bin/asegstats2table asegstats2table --subjects sub{subId} --meas volume --tablefile {outputPathName}")