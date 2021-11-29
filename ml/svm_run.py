import preprocess
import pandas as pd
import numpy as np
import glob, utils, sys
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import PredefinedSplit

def svm_run(X, y, kernelType: str, dataSplit: float, normalize):
    '''
    Run the SVM model with a kernel type defined.
    @kernelType: linear or radial
    @dataSplit: train/validate/test split number
    '''
    print(f"Running SVM with the following parameters: \nKernel type: {kernelType}\nNormalization method: {normalize.__name__}")
    X_train, X_test, y_train, y_test = preprocess.split_data(normalize(X), y, dataSplit)
    X_val, X_test, y_val, y_test = preprocess.split_data(X_test, y_test, 0.5)
    print(f"X_train: {X_train.shape}")
    print(f"y_train: {y_train.shape}")
    print(f"X_test: {X_train.shape}")
    print(f"y_test: {y_test.shape}")
    
    X_grid = np.concatenate((X_train, X_val))
    y_grid = np.concatenate((y_train, y_val))
    separation_boundary = [-1 for _ in y_train] + [0 for _ in y_val]
    ps = PredefinedSplit(separation_boundary)

    print(f"separation_boundary: {separation_boundary}")
    
    param_grid = {
        'C': [1.0, 10.0, 100.0, 1000.0],
        'gamma': [0.01, 0.10, 1.00, 10.00],
        'kernel': [kernelType]
    }

    print(f"param_grid: {param_grid}")

    clf = GridSearchCV(SVC(random_state=0), param_grid, cv=ps)

    model = clf.fit(X_grid, y_grid)
    train_acc = model.score(X_train, y_train)
    val_acc = model.score(X_val, y_val)
    test_acc = model.score(X_test, y_test)
    print(f'training score: {round(train_acc, 3)}')
    print(f'validation score: {round(val_acc, 3)}')
    print(f'testing score: {round(test_acc, 3)}')
    print(f'Best model params: {model.best_params_}')
    
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
X, y = preprocess.get_data("volumes.csv", ROI, "combine")
svm_run(X, y, "linear", 0.6, preprocess.normalize1)