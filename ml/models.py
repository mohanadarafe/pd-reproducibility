import preprocess

def svm(df, normalize, normType, dataFile, ROI, heuristic=None):
    '''
    Run the SVM model
    @df: DataFrame of volumes
    @normalize: normalization function desired (found in preprocess.py)
    @normType: norm1|norm2
    @dataFile: csv file with volumes
    @ROI: array of ROIs
    @heuristic: combine left and right volumes?
    '''
    param_grid = {
        'C': [1.0, 10.0, 100.0, 1000.0],
        'gamma': [0.01, 0.10, 1.00, 10.00]
    }
    for kernelType in ["linear", "rbf"]:
        param_grid["kernel"] = [kernelType]
        preprocess.model(df, "SVM", f"{kernelType}_svm_{normType}", normalize, param_grid, dataFile, ROI, heuristic="combine")


def logistic_regression(df, normalize, normType, dataFile, ROI, heuristic=None):
    '''
    Run the Logistic Regression model
    @df: DataFrame of volumes
    @normalize: normalization function desired (found in preprocess.py)
    @normType: norm1|norm2
    @dataFile: csv file with volumes
    @ROI: array of ROIs
    @heuristic: combine left and right volumes?
    '''
    param_grid = {
        'solver': ["newton-cg", "lbfgs", "liblinear", "sag", "saga"],
        'C': [1.0, 10.0, 100.0, 1000.0]
    }
    preprocess.model(df, "LR", f"lr_{normType}", normalize, param_grid, dataFile, ROI, heuristic="combine")
    

def random_forest(df, normalize, normType, dataFile, ROI, heuristic=None):
    '''
    Run the Random Forest model
    @df: DataFrame of volumes
    @normalize: normalization function desired (found in preprocess.py)
    @normType: norm1|norm2
    @dataFile: csv file with volumes
    @ROI: array of ROIs
    @heuristic: combine left and right volumes?
    '''
    param_grid = {
        'n_estimators': [100, 500, 1000],
        'criterion': ['gini', 'entropy'],
        'min_samples_split': [2, 4, 5, 10, 13],
        'min_samples_leaf': [1, 2, 5, 8, 13]
    }
    preprocess.model(df, "RF", f"rf_{normType}", normalize, param_grid, dataFile, ROI, heuristic="combine")