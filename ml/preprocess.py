import pandas as pd
import numpy as np
import utils, json, os
from joblib import Parallel, delayed
from os import path

from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RepeatedStratifiedKFold

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
        
    cols = list(df.columns.values)
    cols.pop(cols.index("subjectId"))
    df = df[["subjectId"]+cols]
    
    return df

def normalize1(df, mean, std):
    if mean is None and std is None:
        mean = df.mean(axis=0)
        std = df.std(axis=0)
        normalizedDf = (df - mean)/std
        return normalizedDf.values, mean, std

    normalizedDf = (df - mean)/std
    return normalizedDf.values
            
def normalize2(df):
    df_no_id = df.drop(columns=["subjectId", "class"])
    metadata_df = utils.parse_metadata()
    merged_df = pd.merge(df, metadata_df, on=["subjectId"])
    
    stats = {}
    for scanner in merged_df["scannerType"].unique():
        mean, std = utils.get_mean_and_stats(merged_df.drop(columns="subjectId"), scanner)
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

def train(clf, train_index, test_index, X, y, normalize, columns, performanceDict, modelType, reportKey, iteration):
    print(f"=================Iteration #{iteration}=================")
        
    # Get fold data train/test sets
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    print(f'Shape of train set: {X_train.shape}')
    print(f'Shape of test set: {X_test.shape}')
    
    # Normalize model data
    print("Normalizing data...")
    if normalize.__name__ == "normalize1":
        trainDf = pd.DataFrame(X_train, columns=columns).drop(columns=["subjectId", "class"])
        testDf = pd.DataFrame(X_test, columns=columns).drop(columns=["subjectId", "class"])
        X_train_normalized, mean_train, std_train = normalize(trainDf, None, None)
        X_test_normalized = normalize(testDf, mean_train, std_train)

    elif normalize.__name__ == "normalize2":
        trainDf = pd.DataFrame(X_train, columns=columns)
        testDf = pd.DataFrame(X_test, columns=columns)
        X_train_normalized = normalize2(trainDf)
        X_test_normalized = normalize2(testDf)
        
    print("Done normalizing data")
        
    print(f"Fitting {modelType} model #{iteration}...")
    model = clf.fit(X_train_normalized, y_train)
    print("Done fitting model")
    
    print(f"Computing results metrics for {modelType} model #{iteration}...")
    utils.performance_report(performanceDict, model, modelType, reportKey, iteration, X_train_normalized, X_test_normalized, y_train, y_test)
    print("Done computing results metrics\n")

    return performanceDict

def model(df, modelType, reportKey, normalize, paramGrid, dataFile, ROI, heuristic=None):
    print(f"\n======================Running {modelType} with the following parameters======================\nNormalization: {normalize.__name__}\nParam Grid: {paramGrid}\nData: {dataFile}\nROI: {ROI}")

    if not os.path.isdir(modelType):
        os.mkdir(modelType)

    performanceDict = {}
    X = df.values
    y = utils.convert_Y(X[:, -1])
    columns = df.columns
    
    # Setup CV
    cv = RepeatedStratifiedKFold(n_splits=2, n_repeats=3, random_state=42)

    # Define model type
    if modelType == "SVM":
        clf = GridSearchCV(SVC(random_state=0), paramGrid)
    elif modelType == "RF":
        clf = GridSearchCV(RandomForestClassifier(random_state=0, n_jobs = -1), paramGrid)
    elif modelType == "LR":
        clf = GridSearchCV(LogisticRegression(random_state=0), paramGrid)
    
    output = Parallel(n_jobs=-1)(delayed(train)(clf, train_index, test_index, X, y, normalize, columns, performanceDict, modelType, reportKey, iteration) for iteration, (train_index, test_index) in enumerate(cv.split(X, y)))

    with open(f"{modelType}/{reportKey}_report.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
        
    return performanceDict