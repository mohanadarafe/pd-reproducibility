import utils, os

def prep_data(raw_dir, out_dir):
    # Convert archive DICOM to BIDS
    # utils.convert_data_to_bids(raw_dir, out_dir)

    # Get NIFTI file paths
    filePaths = utils.block_reader(out_dir)
    print("Done preparing BIDS data.")

    # Add variable paths
    os.putenv("$FREESURFER_HOME", "/usr/local/freesurfer")
    os.putenv("$SUBJECTS_DIR", "./data/subjects")

    # Recon-all every subject
    subjectId = 0
    for patient in filePaths:
        print(f"File path: {patient}")
        print(f"Processing reconstruction of subject {subjectId}.")
        subject = f'sub{subjectId}'
        os.system(f"recon-all -i {patient} -s {subject} -all")
        subjectId += 1
    
prep_data("./data/ppmi/original", "./data/ppmi/BIDS")