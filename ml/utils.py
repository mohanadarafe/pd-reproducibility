import pandas as pd
import numpy as np
import glob, os, json
from os import path
from bs4 import BeautifulSoup as bs
from sklearn.metrics import accuracy_score
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score

def remove_unwanted_columns(df, ROI):
    '''
    Given a list of ROIs, the function will drop columns that are not desired.
    '''
    for column in df.columns:
        if column not in ROI:
            df = df.drop(columns=column)
    return df

def reorder_df(df, area):
    '''
    Reorders the columns in proper order
    '''
    cols = list(df.columns.values)
    cols.pop(cols.index(area))
    df = df[[area]+cols]
    return df

def combine_left_right_vol(df):
    '''
    Heuristic - Combine the Left and Right volumes into one column
    '''
    for column in df.columns:
        if "Left" in column:
            area = "-".join(column.split("-")[1:])
            left_area = f"Left-{area}"
            right_area = f"Right-{area}"
            df[area] = df[left_area] + df[right_area]
            df = df.drop(columns = [left_area, right_area])
            df = reorder_df(df, area)
    return df

def convert_Y(data):
    '''
    The following function converts PD/NC to 1's/0's
    '''
    data = np.where(data == "PD", 1, data)
    data = np.where(data == "NC", 0, data)
    return data.astype(int)

def get_mean_and_stats(df, scannerType, numOfFeatures):
    '''
    Calculate mean and std for normalization 2
    '''
    queryDf = df.loc[((df['scannerType'] == scannerType) & (df['class']  == 'NC'))]

    if queryDf.shape[0] > 1:
        mean = queryDf.mean()
        std = queryDf.std()
    else:
        mean = pd.Series(np.zeros(numOfFeatures,))
        std = pd.Series(np.ones(numOfFeatures,))

    return mean, std

def parse_metadata():
    '''
    Get DatFrame table consisting of two columns: subjectId and scannerType
    '''
    df = pd.DataFrame(columns=["subjectId", "scannerType"])
    for index, mdFilePath in enumerate(glob.glob("../data/metadata/*")):
        with open(mdFilePath, "r") as file:
            content = file.readlines()
            content = "".join(content)
            bs_content = bs(content, "lxml")
            subjectId = bs_content.find("subject").find("subjectidentifier").getText()
            scannerType = bs_content.find_all("protocol", attrs={'term':'Manufacturer'})[0].string
            model = bs_content.find_all("protocol", attrs={'term':'Mfg Model'})[0].string
            df = df.append({
                "subjectId": int(subjectId),
                "scannerType": f"{scannerType} {model}"
            }, ignore_index=True)
            df["subjectId"] = df["subjectId"].astype('int64')

    return df 

def performance_report(model, modelType, reportKey, iteration, X_train, X_test, y_train, y_test):
    '''
    Produces JSON report after fitting model
    '''
    performanceDict = {}
    y_train_predict = model.predict(X_train)
    y_test_predict = model.predict(X_test)

    # Accuracy
    train_accuracy = accuracy_score(y_train, y_train_predict)
    test_accuracy = accuracy_score(y_test, y_test_predict)

    # F1
    train_f1 = f1_score(y_train, y_train_predict)
    test_f1 = f1_score(y_test, y_test_predict)

    # BA
    train_ba = balanced_accuracy_score(y_train, y_train_predict)
    test_ba = balanced_accuracy_score(y_test, y_test_predict)

    # ROC AUC
    train_auc = roc_auc_score(y_train, y_train_predict)
    test_auc = roc_auc_score(y_test, y_test_predict)

    # Sensitivity & Specificity
    tn_train, fp_train, fn_train, tp_train = confusion_matrix(y_train, y_train_predict).ravel()
    tn_test, fp_test, fn_test, tp_test = confusion_matrix(y_test, y_test_predict).ravel()

    specificity_train = tn_train / (tn_train + fp_train)
    specificity_test = tn_test / (tn_test + fp_test)

    sensitivity_train = recall_score(y_train, y_train_predict)
    sensitivity_test = recall_score(y_test, y_test_predict)

    normalization = "Normalization 1" if reportKey.split("_")[-1] == "norm1" else "Normalization 2"
 
    modelInfo = {
        "model": modelType,
        "normalization": normalization,
        "parameters": model.best_params_,
        "iteration": iteration
    }

    trainMetrics = {
        "accuracy": train_accuracy,
        "f1_score": train_f1,
        "balanced_accuracy": train_ba,
        "auc": train_auc,
        "sensitivity": sensitivity_train,
        "specificity": specificity_train
    }

    testMetrics = {
        "accuracy": test_accuracy,
        "f1_score": test_f1,
        "balanced_accuracy": test_ba,
        "auc": test_auc,
        "sensitivity": sensitivity_test,
        "specificity": specificity_test
    }

    performanceDict = {
        "modelInfo": modelInfo,
        "train": trainMetrics,
        "test": testMetrics
    }

    return performanceDict