import os, glob
import numpy as np
import pandas as pd

def initFreeSurfer():
    os.system("export FREESURFER_HOME=/Applications/freesurfer/7.3.0")
    os.system("export SUBJECTS_DIR=$FREESURFER_HOME/subjects")
    os.system("source $FREESURFER_HOME/SetUpFreeSurfer.sh")

def convert_stats_to_csv(statsFile: str, outputCsvFile: str):
    '''
    Converts the aseg.stats file produced from recon-all to a CSV file
    '''
    os.system(f"asegstats2table -i {statsFile} --meas volume --tablefile {outputCsvFile}")

def convert_brainstem_stats_to_dict(brainstemFile):
    stats = {}
    with open(brainstemFile, "r") as f:
        for line in f.readlines():
            row = line.split()
            stats[row[0]] = row[1]
    return stats

def create_brainstem_stats(brainstemFile):
    stats = convert_brainstem_stats_to_dict(brainstemFile)
    with open("brainstem.csv", "w") as f:
        keys = list(stats.keys())
        for key in keys[:-1]:
            f.write(f'{key}\t')
        f.write(f"{keys[-1]}\n")

        for key in keys[:-1]:
            f.write(f"{stats[key]}\t")
        f.write(f"{stats[keys[-1]]}")

def create_cortical_stats(statsDirectory):
    with open(f"{statsDirectory}/insula.txt", "r") as f:
        lines = f.readlines()
        insula_volume = int(lines[1].split()[1]) + int(lines[-1].split()[1])

    with open(f"{statsDirectory}/precentral.txt", "r") as f:
        lines = f.readlines()
        precentral_volume = int(lines[1].split()[1]) + int(lines[-1].split()[1])
    
    d = {"Insula": [insula_volume], "Precentral Cortex": [precentral_volume]}
    df = pd.DataFrame(d)
    return df

if __name__ == '__main__':
    df_list = []

    for subjectDirectory in glob.glob("data/fsstats/*/*"):
        print(f'Extracting data for subject {subjectDirectory.split("/")[3].split("_")[1]}...')
        # get aseg stats
        convert_stats_to_csv(f"{subjectDirectory}/aseg.stats", "stats.csv")
        aseg_df = pd.read_csv("stats.csv", sep="\t")

        # get brainstem stats
        create_brainstem_stats(f"{subjectDirectory}/brainstemSsVolumes.v10.txt")
        brainstem_df = pd.read_csv("brainstem.csv", sep="\t")

        # Convert cortical parcellation stats to CSV
        cortical_df = create_cortical_stats(f"{subjectDirectory}")

        # Create final DF
        df = aseg_df.join([brainstem_df, cortical_df])
        
        # Add subject ID (0: stable, 1: progr)
        subjectType = subjectDirectory.split("/")[3].split("_")[0]
        subjectId = subjectDirectory.split("/")[3].split("_")[1]
        df.insert(0, column="subjectId", value=[subjectId])
        df.insert(len(df.columns), column="group", value=[1 if subjectType=='progr' else 0])

        # Remove temp files
        os.system(f"rm stats.csv")
        os.system(f"rm brainstem.csv")

        df_list.append(df)
    
    volume_df = pd.concat(df_list, ignore_index=True).astype({"subjectId": np.int64})
    volume_df.to_csv("data/volume-data/freeSurferVolumes.csv")
