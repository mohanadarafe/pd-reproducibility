import models, preprocess

DATA = "volumes.csv"
ROI = [
      "subjectId", "class",
      "Left-Putamen", "Right-Putamen", 
      "Right-Caudate", "Left-Caudate", 
      "Right-Thalamus-Proper", "Left-Thalamus-Proper", 
      "Left-Pallidum", "Right-Pallidum", 
      "CerebralWhiteMatterVol", 
      "3rd-Ventricle", "4th-Ventricle"
]
X, y = preprocess.get_data(DATA, ROI, "combine")

models.svm(X, y, 0.7, preprocess.normalize1)
# models.logistic_regression(X, y, 0.7, preprocess.normalize1)
# models.random_forest(X, y, 0.7, preprocess.normalize1)