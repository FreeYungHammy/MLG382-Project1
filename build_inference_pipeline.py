# build_inference_pipeline.py

import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

# load your raw data and engineer the same features you use at predict time
df = pd.read_csv("Student_performance_data .csv")
df.columns = df.columns.str.strip()
df['SupportScore']  = df['ParentalSupport'] * df['Extracurricular']
df['SupportedGPA']  = df['GPA'] + 0.1 * df['ParentalSupport']
df['ExtraWork']     = df['StudyTimeWeekly'] * df['Tutoring']

# select exactly the 8 features for inference
inference_features = [
    'StudyTimeWeekly',
    'Absences',
    'Tutoring',
    'ParentalSupport',
    'GPA',
    'SupportScore',
    'SupportedGPA',
    'ExtraWork'
]
X_inf = df[inference_features]

#fit a fresh MinMaxScaler on those 8 columns
scaler = MinMaxScaler()
scaler.fit(X_inf)

# load your old pipeline (which contains the trained MLP)
old_pipe = joblib.load("grade_predictor_inference_pipeline.pkl")
mlp      = old_pipe.named_steps['mlp']

# build a new inference pipeline: [scaler → mlp]
inference_pipe = Pipeline([
    ("scaler", scaler),
    ("mlp",    mlp)
])

# pipeline write
joblib.dump(inference_pipe, "grade_predictor_inference_pipeline.pkl")
print("Rebuilt inference pipeline with 8‑feature scaler + extracted MLP")
