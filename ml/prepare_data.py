import glob
import pandas as pd
import numpy as np
import utils

def sanitize_data(csvFileName: str, ROI: [], heuristic = None):
    '''
    The following function will sanitize data and build a numpy array with X ROI's volumes and y being the class [NC, PD]
    '''
    df = pd.read_csv(csvFileName)
    df = utils.remove_unwanted_columns(df, ROI)
    
    if heuristic == "combine":
        df = utils.combine_left_right_vol(df)
        
    arr = df.values
    X = arr[:, :-1]
    y = utils.convert_Y(arr[:, -1])
    return X,y
    

if __name__ == '__main__':
   ROI = [
      "class",
      "Left-Putamen", "Right-Putamen", 
      "Right-Caudate", "Left-Caudate", 
      "Right-Thalamus-Proper", "Left-Thalamus-Proper", 
      "Left-Pallidum", "Right-Pallidum", 
      "Left-Cerebellum-Cortex", "Right-Cerebellum-Cortex", "lhCortexVol", "rhCortexVol", "CortexVol",
      "Left-Cerebellum-White-Matter", "Right-Cerebellum-White-Matter",
      "CerebralWhiteMatterVol", 
      "3rd-Ventricle", "4th-Ventricle"
   ]
   X, y = sanitize_data("ml/volumes.csv", ROI, "combine")
   print(X,y)