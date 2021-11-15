import utils, os
import pandas as pd

def get_volumes_dataframe(patientType: str):
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
        os.system(f"mv sub{subjectId}/ data/subjects/{patientType}")
        subjectId+=1
 
    # Convert all stats to one DataFrame
    df_list = []
    for subId in range(subjectId):
        subject = f"sub{subId}"
        csvFileName = f"{subject}_stats.csv"
        utils.convert_stats_to_csv(subId, csvFileName)
        subjectDf = pd.read_csv(csvFileName, sep="\t")
        df_list.append(subjectDf)
        os.system(f"rm {csvFileName}") # remove temp file

    df = pd.concat(df_list, ignore_index=True)
    return df

if __name__ == '__main__':
    NC_DF = get_volumes_dataframe("NC")
    NC_DF.to_csv('NC_RESULT', index=False)
    print(NC_DF)
    # PD_DF = get_volumes_dataframe("PD")