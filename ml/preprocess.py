import glob
import pandas as pd
import numpy as np
import utils
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import PredefinedSplit

def get_data(csvFileName: str, ROI: [], heuristic = None):
    '''
    The following function will sanitize data and build a numpy array with X ROI's volumes and y being the class [NC, PD]
    @csvFileName: input volumes csv
    @ROI: regions of interests desired
    @heuristic: function key
    '''
    df = pd.read_csv(csvFileName)
    df = utils.remove_unwanted_columns(df, ROI)
    
    if heuristic == "combine":
        df = utils.combine_left_right_vol(df)
        
    arr = df.values
    X = arr[:, :-1]
    y = utils.convert_Y(arr[:, -1])
    return X,y

def normalize1(data):
    normalizedX = []
    
    for row in data:
        normalizedRow = []
        for columnIndex, variable in enumerate(row):
            mean = np.mean(data[:, columnIndex])
            std = np.std(data[:, columnIndex])
            normalizedValue = (variable - mean)/std
            normalizedRow.append(normalizedValue)        
        normalizedX.append(normalizedRow)
        
    return np.array(normalizedX)
            
def normalize2():
    print("TODO - Unimplemented")

def split_data(X, y, training_split):
    '''
    The following function splits the training and testing data sets
    according to a split [0 - 1] passed.
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = training_split, random_state = 42)
    return X_train, X_test, y_train, y_test