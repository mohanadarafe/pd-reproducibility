import pandas as pd
import numpy as np
import utils, glob
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import PredefinedSplit
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score

def get_data(csvFileName: str, ROI: [], heuristic = None, getDf = False):
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
        
    if (getDf):
        cols = list(df.columns.values)
        cols.pop(cols.index("subjectId"))
        df = df[["subjectId"]+cols]
        return df
    else:
        df = df.drop("subjectId", 1)
        
    arr = df.values
    X = arr[:, :-1]
    y = utils.convert_Y(arr[:, -1])
    
    return X,y

def normalize1(data, mean, std):
    df = pd.DataFrame(data=data)

    if mean is None and std is None:
        mean = df.mean(axis=0)
        std = df.std(axis=0)
        normalizedDf = (df - mean)/std
        return normalizedDf.values, mean, std

    normalizedDf = (df - mean)/std
    return normalizedDf.values
            
def normalize2(df):
    df_no_id = df.drop(["subjectId", "class"], 1)
    metadata_df = utils.parse_metadata()
    merged_df = pd.merge(df, metadata_df, on=["subjectId"])
    
    stats = {}
    for scanner in merged_df["scannerType"].unique():
        mean, std = utils.get_mean_and_stats(merged_df.drop("subjectId",1), scanner)
        stats[scanner] = {
            "mean": mean.to_dict(),
            "std": std.to_dict()
        }
        
    for index in merged_df.index:
        rowInfo = merged_df.iloc[index]
        scanner = rowInfo["scannerType"]
        mean = list(stats[scanner]["mean"].values())
        std = list(stats[scanner]["std"].values())
        df_no_id.iloc[index] = (df_no_id.iloc[index]-mean)/std
        
    return df_no_id.values

def split_data(X, y, training_split):
    '''
    The following function splits the training and testing data sets
    according to a split [0 - 1] passed.
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = training_split, random_state = 42)
    return X_train, X_test, y_train, y_test

def split_data(X, y, training_split):
    '''
    The following function splits the training and testing data sets
    according to a split [0 - 1] passed.
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = training_split, random_state = 42)
    return X_train, X_test, y_train, y_test

def build_validation_set(X_train, y_train, X_val, y_val):
    X_grid = np.concatenate((X_train, X_val))
    y_grid = np.concatenate((y_train, y_val))
    separation_boundary = [-1 for _ in y_train] + [0 for _ in y_val]
    ps = PredefinedSplit(separation_boundary)
    return X_grid, y_grid, separation_boundary, ps

def get_model_score(model, X_train, y_train, X_test, y_test):
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    return train_acc, test_acc

def model(X, y, modelType, dataSplit, normalize, paramGrid, dataFile, ROI, heuristic=None):
    print(f"\n======================Running {modelType} with the following parameters======================\nData split: {dataSplit}\nNormalization: {normalize.__name__}\nParam Grid: {paramGrid}\nData: {dataFile}\nROI: {ROI}")
    
    # Define training, validation and test sets
    X_train, X_test, y_train, y_test = split_data(X, y, dataSplit)
    print("Done splitting data.")

    # Setup CV
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=50, random_state=42)
    
    # Define model type
    if modelType == "SVM":
        clf = GridSearchCV(SVC(random_state=42), paramGrid, n_jobs=-1, cv=cv)
    elif modelType == "RF":
        clf = GridSearchCV(RandomForestClassifier(random_state=42), paramGrid, n_jobs=-1, cv=cv)
    elif modelType == "LR":
        clf = GridSearchCV(LogisticRegression(random_state=42), paramGrid, n_jobs=-1, cv=cv)
        
    # Normalize model data
    if normalize.__name__ == "normalize1":
        X_train_normalized, mean_train, std_train = normalize(X_train, None, None)
        X_test_normalized = normalize(X_test, mean_train, std_train)
    elif normalize.__name__ == "normalize2":
        df = get_data(dataFile, ROI, heuristic, getDf=True)
        X_train, X_test, y_train, y_test = split_data(df, y, dataSplit)
        X_train_normalized = normalize(X_train)
        X_test_normalized = normalize(X_test)

    print("Done normalizing data")
        
    # Fit and predict
    model = clf.fit(X_train_normalized, y_train)
    train_acc = cross_val_score(model, X_train_normalized, y_train, scoring='accuracy', cv=cv, n_jobs=-1)
    test_acc = cross_val_score(model, X_test_normalized, y_test, scoring='accuracy', cv=cv, n_jobs=-1)
    # train_acc, test_acc = get_model_score(model, X_train_normalized, y_train, X_test_normalized, y_test)

    print(f'training score: {train_acc}')
    print(f'testing score: {test_acc}')
    print(f'Best model params: {model.best_params_}\n============================================')