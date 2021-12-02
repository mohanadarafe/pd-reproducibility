'''
Once the experiemnt has ran, there should be a lot of sub* folders in the root directory.
This is due to the fact that the Zenodo used with Boutques sets FreeSurfer's default subjects
directory to PWD. Therefore, we move the stats files to appropriate locations and convert the
stats to dataframes. In the end, one large CSV file includes all the volumes from each subject.
'''

import utils, os, glob, json
import pandas as pd
from os import path

def convert_stats_to_df(patientType: str, subId: int):
    filePath = f"data/subjects/{patientType}/sub{subId}/aseg.stats"

    if (os.path.isfile(filePath)):
        with open("subIdMap.json") as f:
            subIdDict = json.load(f)

        # Convert stats to CSV files and create one large dataframe
        csvFileName = f"{subId}_stats.csv"
        utils.convert_stats_to_csv(filePath, csvFileName)

        # Convert CSV to DF and add subject ID column
        subjectId = subIdDict[f"{patientType}_sub{subId}"]
        subjectDf = pd.read_csv(csvFileName, sep="\t", index_col=False)
        subjectDf.insert(0, column="subjectId", value=[subjectId])

        # Remove temp files
        os.system(f"rm {csvFileName}") # remove temp file

        return subjectDf


if __name__ == '__main__':
    df_list = []
    for subId in range(63):
        NC_DF = convert_stats_to_df("NC", subId)
        NC_DF["class"] = "NC"
        df_list.append(NC_DF)
    
    for subId in range(63, 216):
        if subId == 164:
            continue
        PD_DF = convert_stats_to_df("PD", subId)
        PD_DF["class"] = "PD"
        df_list.append(PD_DF)

    FINAL_DF = pd.concat(df_list, ignore_index=True)
    FINAL_DF.to_csv("ml/final.csv")
