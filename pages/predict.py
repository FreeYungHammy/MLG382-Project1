# pages/predict.py
from dash import html, dcc, Input, Output, State
import pandas as pd
import numpy as np

# 11 raw inputs
feature_cols = [
    'Age','Gender','Ethnicity','StudyTimeWeekly','Absences',
    'Tutoring','ParentalSupport','Extracurricular','Sports',
    'Music','Volunteering'
]

# Generate one input card per feature
input_cards = [
    html.Div(className="input-card", children=[
        html.Label(col),
        dcc.Input(
            id=f"input-{col}", 
            type="number", 
            placeholder=col, 
            style={"width":"100%"}
        )
    ])
    for col in feature_cols
]

# Layout for the Predict page
layout = html.Div(className="content", children=[
    html.H1("Make a Prediction"),
    html.Div(
        input_cards,
        style={
            "display":"grid",
            "gridTemplateColumns":"repeat(auto-fit, minmax(200px,1fr))",
            "gap":"20px"
        }
    ),
    html.Button("Predict", id="predict-btn", n_clicks=0),
    html.Div(id="prediction-output", style={"marginTop":"20px","fontSize":"24px"})
])

def register_callbacks(app, pipeline):
    @app.callback(
        Output("prediction-output", "children"),
        Input("predict-btn", "n_clicks"),
        [State(f"input-{col}", "value") for col in feature_cols]
    )
    def predict(n_clicks, *vals):
        if not n_clicks or None in vals:
            return ""
        
        # 1) Build raw DataFrame of the 11 inputs
        raw = pd.DataFrame([vals], columns=feature_cols).astype(float)
        
        # 2) Recompute your 3 engineered features
        raw['SupportScore']  = raw['ParentalSupport'] * raw['Extracurricular']
        raw['SupportedGPA']  = raw['GPA'] + 0.1 * raw['ParentalSupport']
        raw['ExtraWork']     = raw['StudyTimeWeekly'] * raw['Tutoring']
        
        # 3) Select only the 8 features your pipeline expects
        X_model = raw[[
            'StudyTimeWeekly','Absences','Tutoring','ParentalSupport',
            'GPA','SupportScore','SupportedGPA','ExtraWork'
        ]]
        
        # 4) Predict and map to letter
        pred = pipeline.predict(X_model)[0]
        grade_map = {0:"A",1:"B",2:"C",3:"D",4:"F"}
        return f"Predicted GradeClass: {grade_map[pred]}"
