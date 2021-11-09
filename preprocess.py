import utils, os

def prep_data(raw_dir, out_dir):
    
    # Convert archive DICOM to BIDS
    if len(os.listdir(out_dir)) == 0:
        utils.convert_data_to_bids(raw_dir, out_dir)

    # Get NIFTI file paths
    filePaths = utils.nifti_file_paths(out_dir)

    # Add variable paths
    os.putenv("$FREESURFER_HOME", "/usr/local/freesurfer")
    os.putenv("$SUBJECTS_DIR", "./data/subjects")
    os.system("sudo chmod -R a+w $SUBJECTS_DIR")

    # Extract volumes from patients
    subjectId = 0
    for patient in filePaths:
        subject = f'sub{subjectId}'
        os.system(f"recon-all -i {patient} -s {subject} -all -qcache")
        utils.export_volumes(os.getenv("SUBJECTS_DIR"), subjectId)
        subjectId += 1
    
prep_data("./data/ppmi/original", "./data/ppmi/BIDS")