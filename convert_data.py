import utils, os, glob
import pandas as pd

def convert_stats_to_df(patientType: str):
    df_list = []
    subId = 0

    for pathToStats in glob.glob(f"data/subjects/{patientType}/*/*.stats"):
        csvFileName = f"sub{subId}_stats.csv"
        utils.convert_stats_to_csv(subId, csvFileName)
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
    DF.to_csv("volumes.csv")
