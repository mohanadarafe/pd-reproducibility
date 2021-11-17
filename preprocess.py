import utils, os, glob
import pandas as pd

def get_volumes_from_freesurfer(patientType: str):
    '''
    Preprocessing pipeline for NC or PD patients.
    Returns a dataframe
    @patientType: NC or PD
    '''
    data = utils.get_mri_scans(patientType)
    subjectId = 0

    # Get brain ROI volumes from FreeSurfer
    for mri_scan in data[0:1]:
        print(f"Extract volumes for subject{subjectId}")
        utils.recon_patient(mri_scan, subjectId)
        os.mkdir(f"data/subjects/{patientType}/sub{subjectId}")
        os.system(f"mv sub{subjectId}/stats/aseg.stats data/subjects/{patientType}/sub{subjectId}")
        os.system(f"rm -rf sub{subjectId}")
        subjectId+=1

if __name__ == '__main__':
    utils.prepare_data_folder()
    get_volumes_from_freesurfer("NC")
    get_volumes_from_freesurfer("PD")