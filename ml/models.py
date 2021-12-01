import preprocess

def svm(X, y, dataSplit, normalize):
    param_grid = {
        'C': [1.0, 10.0, 100.0, 1000.0],
        'gamma': [0.01, 0.10, 1.00, 10.00]
    }
    for kernelType in ["linear", "rbf"]:
        param_grid["kernel"] = [kernelType]
        preprocess.model(X, y, "SVM", dataSplit, normalize, param_grid)


def logistic_regression(X, y, dataSplit, normalize):
    param_grid = {
        'penalty': ["l1", "l2", "elasticnet"],
        'C': [1.0, 10.0, 100.0, 1000.0]
    }
    preprocess.model(X, y, "LR", dataSplit, normalize, param_grid)
    

def random_forest(X, y, dataSplit: float, normalize):
    param_grid = {
        'n_estimators': [100, 500, 1000],
        'criterion': ['gini', 'entropy'],
        'min_samples_split': [2, 4, 5, 10, 13],
        'min_samples_leaf': [1, 2, 5, 8, 13]
    }
    preprocess.model(X, y, "RF", dataSplit, normalize, param_grid)