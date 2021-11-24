'''
Once the experiemnt has ran, there should be a lot of sub* folders in the root directory.
This is due to the fact that the Zenodo used with Boutques sets FreeSurfer's default subjects
directory to PWD. Therefore, we move the stats files to appropriate locations and convert the
stats to dataframes. In the end, one large CSV file includes all the volumes from each subject.
'''

import utils, os, glob
import pandas as pd

def convert_stats_to_df(patientType: str):
    df_list = []
    subId = 0

    # Move all sub stats files to data folder
    print("Copying stats files over to data folder")
    utils.move_volume_stats_from_job()

    # Convert stats to CSV files and create one large dataframe
    for pathToStats in glob.glob(f"data/subjects/{patientType}/*/*.stats"):
        print(f"Working on: {pathToStats}")
        csvFileName = f"sub{subId}_stats.csv"
        utils.convert_stats_to_csv(pathToStats, csvFileName)
        print("Converted stats file to CSV")
        subjectDf = pd.read_csv(csvFileName, sep="\t")
        df_list.append(subjectDf)
        os.system(f"rm {csvFileName}") # remove temp file
        subId+=1

    df = pd.concat(df_list, ignore_index=True)
    return df


if __name__ == '__main__':
    NC_DF = convert_stats_to_df("NC")
    NC_DF["class"] = "NC"
    PD_DF = convert_stats_to_df("PD")
    PD_DF["class"] = "PD"
    DF = pd.concat([NC_DF, PD_DF])
    DF.to_csv("ml/volumes.csv")
