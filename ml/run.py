import models, preprocess

DATA_FILE = "volumes.csv"
ROI = [
      "subjectId", "class",
      "Left-Putamen", "Right-Putamen", 
      "Right-Caudate", "Left-Caudate", 
      "Right-Thalamus-Proper", "Left-Thalamus-Proper", 
      "Left-Pallidum", "Right-Pallidum", 
      "Left-Cerebellum-White-Matter", "Right-Cerebellum-White-Matter", 
      "Left-Cerebellum-Cortex", "Right-Cerebellum-Cortex",
      "3rd-Ventricle", 
      "4th-Ventricle"
]
HEURISTIC = "combine"

df = preprocess.get_data(DATA_FILE, ROI, HEURISTIC)

models.svm(df, preprocess.normalize1, "norm1", DATA_FILE, ROI, heuristic="combine")
models.svm(df, preprocess.normalize2, "norm2", DATA_FILE, ROI, heuristic="combine")

models.logistic_regression(df, preprocess.normalize1, "norm1", DATA_FILE, ROI, heuristic="combine")
models.logistic_regression(df, preprocess.normalize2, "norm2", DATA_FILE, ROI, heuristic="combine")

models.random_forest(df, preprocess.normalize1, "norm1", DATA_FILE, ROI, heuristic="combine")
models.random_forest(df, preprocess.normalize2, "norm2", DATA_FILE, ROI, heuristic="combine")