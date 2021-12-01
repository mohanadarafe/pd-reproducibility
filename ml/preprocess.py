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

def normalize1(data, mean, std):
    df = pd.DataFrame(data=data)

    if mean is None and std is None:
        mean = df.mean(axis=0)
        std = df.std(axis=0)

    for i in range(df.shape[1]):
        df[i] = df[i].apply(lambda x: (x-mean[i])/std[i])

    return df.values, mean, std
            
def normalize2():
    print("TODO - Unimplemented")

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
    print(f'training score: {round(train_acc, 3)}')
    print(f'testing score: {round(test_acc, 3)}')
    return train_acc, test_acc

def model(X, y, modelType, dataSplit, normalize, paramGrid):
    print(f"Running {modelType} with the following parameters:\nData split: {dataSplit}\nParam Grid: {paramGrid}")
    # Define training, validation and test sets
    X_train, X_test, y_train, y_test = split_data(X, y, dataSplit)
    print("Done splitting data.")

    # Setup CV
    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=42)
    
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
        X_test_normalized, _, _ = normalize(X_test, mean_train, std_train)

    print("Done normalizing data")
        
    # Fit and predict
    model = clf.fit(X_train, y_train)

    print("Done fitting model")

    train_acc = cross_val_score(model, X_train_normalized, y_train, scoring='accuracy', cv=cv, n_jobs=4)
    test_acc = cross_val_score(model, X_test_normalized, y_test, scoring='accuracy', cv=cv, n_jobs=4)
    print(f'training score: {round(train_acc, 3)}')
    print(f'testing score: {round(test_acc, 3)}')
    print('Best Score: %s' % model.best_score_)
    print('Best Hyperparameters: %s' % model.best_params_)

    # train_acc, test_acc = get_model_score(X_grid_normalized, y_grid, X_test_normalized, y_test)
    # print(f'Best model params: {model.best_params_}')