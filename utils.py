import modules.pypmi.bids as pypmi
import os, glob, shutil

def return_to_project_root_dir() -> bool:
    '''
    The following function returns the current path to project directory
    '''
    while 'environment.yml' not in os.listdir():
        os.chdir('..')
        
def nifti_file_paths(path: str):
    '''
    The following function returns an array containing the file paths to the NiFTI data
    @path: SUBJECTS_DIR
    '''
    filePaths = []
    try:
        for fileName in glob.glob(f'{path}' + '/sub-*/ses-1/anat/*.nii.gz'):
            filePaths.append(fileName)
        
    except FileNotFoundError:
        print("File not found!")
    
    return filePaths

def convert_data_to_bids(raw_dir, out_dir):
    '''
    The following function converts the PPIM data to BIDS format
    @raw_dir: Directory of PPMI data
    @out_dir: Directory to output BIDS
    '''
    pypmi.convert_ppmi(raw_dir=raw_dir, 
                        out_dir=out_dir, 
                        ignore_bad=True,
                        coerce_study_uids=False)

def export_volumes(directory: str, subId: str):
    '''
    The following function converts volume stats to a csv file and places them inside the data folder.
    directory -- SUBJECTS_DIR
    @subId: ID of subject
    '''
    statsFileName = f"sub{subId}_volume_stats.csv"
    subjectDir = f'sub{subId}'
    
    os.chdir("data/subjects")
    if os.path.isdir(subjectDir) == 0:
        os.mkdir(subjectDir)
    else:
        shutil.rmtree(subjectDir)
        os.mkdir(subjectDir)
    
    os.chdir(subjectDir)
    os.system(f"python2 $FREESURFER_HOME/bin/asegstats2table asegstats2table --subjects sub{subId} --meas volume --tablefile {statsFileName}")
    return_to_project_root_dir()