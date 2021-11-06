import pypmi.bids, os, glob

def block_reader(path):
    filePaths = []
    try:
        for fileName in glob.glob(f'{path}' + '/sub-*/ses-1/anat/*.nii.gz'):
            filePaths.append(fileName)
        
    except FileNotFoundError:
        print("File not found!")
    
    return filePaths

def convert_data_to_bids(raw_dir, out_dir):
    pypmi.bids.convert_ppmi(raw_dir=raw_dir, 
                        out_dir=out_dir, 
                        ignore_bad=True,
                        coerce_study_uids=False)