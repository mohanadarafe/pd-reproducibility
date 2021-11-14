import os, glob

def recon_all(mri_scan: str, subjectId: int):
    '''
    TODO: Change this to Boutiques/Docker
    Calls FreeSurfer's recon-all method to get brain volumes
    @mri_scan: input NiFTi file
    @subjectId: subject ID
    '''
    subject = f'sub{subjectId}'
    os.system(f"recon-all -i {mri_scan} -s {subject} -all -qcache")

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