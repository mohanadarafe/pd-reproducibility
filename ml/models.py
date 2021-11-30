import preprocess
import pandas as pd
import numpy as np
import glob, utils, sys
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import PredefinedSplit

def svm(X, y, kernelType: str, dataSplit: float, normalize):
    print(f"Running SVM with the following parameters: \nKernel type: {kernelType}\nNormalization method: {normalize.__name__}")
    X_train, X_test, y_train, y_test = preprocess.split_data(X, y, dataSplit)
    X_val, X_test, y_val, y_test = preprocess.split_data(X_test, y_test, 0.5)
    
    X_grid = np.concatenate((X_train, X_val))
    y_grid = np.concatenate((y_train, y_val))
    separation_boundary = [-1 for _ in y_train] + [0 for _ in y_val]
    ps = PredefinedSplit(separation_boundary)
    
    param_grid = {
        'C': [1.0, 10.0, 100.0, 1000.0],
        'gamma': [0.01, 0.10, 1.00, 10.00],
        'kernel': [kernelType]
    }

    print(f"param_grid: {param_grid}")

    clf = GridSearchCV(SVC(random_state=0), param_grid, cv=ps)

    model = clf.fit(normalize(X_grid), y_grid)
    train_acc = model.score(normalize(X_train), y_train)
    val_acc = model.score(normalize(X_val), y_val)
    test_acc = model.score(normalize(X_test), y_test)
    print(f'training score: {round(train_acc, 3)}')
    print(f'validation score: {round(val_acc, 3)}')
    print(f'testing score: {round(test_acc, 3)}')
    print(f'Best model params: {model.best_params_}')


def logistic_regression(X, y, dataSplit: float, normalize):
    print(f"Running Logistic Regression with the following parameters: \nNormalization method: {normalize.__name__}")
    X_train, X_test, y_train, y_test = preprocess.split_data(X, y, dataSplit)
    X_val, X_test, y_val, y_test = preprocess.split_data(X_test, y_test, 0.5)
    
    X_grid = np.concatenate((X_train, X_val))
    y_grid = np.concatenate((y_train, y_val))
    separation_boundary = [-1 for _ in y_train] + [0 for _ in y_val]
    ps = PredefinedSplit(separation_boundary)
    
    param_grid = {
        'penalty': ["l1", "l2", "elasticnet"],
        'C': [1.0, 10.0, 100.0, 1000.0]
    }
    
    clf = GridSearchCV(LogisticRegression(random_state=0), param_grid, cv=ps)

    model = clf.fit(normalize(X_grid), y_grid)
    train_acc = model.score(normalize(X_train), y_train)
    val_acc = model.score(normalize(X_val), y_val)
    test_acc = model.score(normalize(X_test), y_test)
    print(f'training score: {round(train_acc, 3)}')
    print(f'validation score: {round(val_acc, 3)}')
    print(f'testing score: {round(test_acc, 3)}')
    print(f'Best model params: {model.best_params_}')

def random_forest(X, y, dataSplit: float, normalize):
    print(f"Running Random Forest with the following parameters: \nNormalization method: {normalize.__name__}")
    X_train, X_test, y_train, y_test = preprocess.split_data(X, y, dataSplit)
    X_val, X_test, y_val, y_test = preprocess.split_data(X_test, y_test, 0.5)
    
    X_grid = np.concatenate((X_train, X_val))
    y_grid = np.concatenate((y_train, y_val))
    separation_boundary = [-1 for _ in y_train] + [0 for _ in y_val]
    ps = PredefinedSplit(separation_boundary)
    
    param_grid = {
        'n_estimators': [100, 500, 1000],
        'criterion': ['gini', 'entropy'],
        'min_samples_split': [2, 4, 5, 10, 13],
        'min_samples_leaf': [1, 2, 5, 8, 13]
    }
    
    clf = GridSearchCV(RandomForestClassifier(random_state=0), param_grid, cv=ps)

    model = clf.fit(normalize(X_grid), y_grid)
    train_acc = model.score(normalize(X_train), y_train)
    val_acc = model.score(normalize(X_val), y_val)
    test_acc = model.score(normalize(X_test), y_test)
    print(f'training score: {round(train_acc, 3)}')
    print(f'validation score: {round(val_acc, 3)}')
    print(f'testing score: {round(test_acc, 3)}')
    print(f'Best model params: {model.best_params_}')