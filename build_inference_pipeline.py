# build_inference_pipeline.py

import joblib
from sklearn.pipeline import Pipeline

# existing files
old_pipe = joblib.load("grade_predictor_inference_pipeline.pkl")
scaler   = joblib.load("scaler.pkl")

# MLP from your old pipeline
mlp = old_pipe.named_steps['mlp']

# clean inference pipeline
inference_pipe = Pipeline([
    ("scaler", scaler),
    ("mlp",    mlp)
])

# Overwrite inference 
joblib.dump(inference_pipe, "grade_predictor_inference_pipeline.pkl")
print("Rebuilt grade_predictor_inference_pipeline.pkl with just scaler + MLP")
