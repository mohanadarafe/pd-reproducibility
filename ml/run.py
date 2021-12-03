import models, preprocess

DATA_FILE = "volumes.csv"
ROI = [
      "subjectId", "class",
      "Left-Putamen", "Right-Putamen", 
      "Right-Caudate", "Left-Caudate", 
      "Right-Thalamus-Proper", "Left-Thalamus-Proper", 
      "Left-Pallidum", "Right-Pallidum", 
      "CerebralWhiteMatterVol", 
      "3rd-Ventricle", "4th-Ventricle"
]
HEURISTIC = "combine"

X, y = preprocess.get_data(DATA_FILE, ROI, HEURISTIC)

models.svm(X, y, 0.7, preprocess.normalize1, DATA_FILE, ROI, heuristic=HEURISTIC)
# models.svm(X, y, 0.7, preprocess.normalize2, DATA_FILE, ROI, heuristic=HEURISTIC)

# models.logistic_regression(X, y, 0.7, preprocess.normalize1, DATA_FILE, ROI, heuristic=HEURISTIC)
# models.logistic_regression(X, y, 0.7, preprocess.normalize2, DATA_FILE, ROI, heuristic=HEURISTIC)

# models.random_forest(X, y, 0.7, preprocess.normalize1, DATA_FILE, ROI, heuristic=HEURISTIC)
# models.random_forest(X, y, 0.7, preprocess.normalize2, DATA_FILE, ROI, heuristic=HEURISTIC)