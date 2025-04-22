from dash import html, dcc, Input, Output, State
import pandas as pd
import numpy as np
import joblib
from app import app, pipeline, feature_cols  # adjust import paths if needed

# Build inputs dynamically
input_cards = []
for col in feature_cols:
    input_cards.append(
        html.Div(className="input-card", children=[
            html.Label(col),
            dcc.Input(
                id=f"input-{col}",
                type="number",
                placeholder=col,
                style={"width":"100%"}
            )
        ])
    )

layout = html.Div(className="content", children=[
    html.H1("Make a Prediction"),
    html.Div(input_cards, style={
        "display":"grid",
        "gridTemplateColumns":"repeat(auto-fit, minmax(200px,1fr))",
        "gap":"20px"
    }),
    html.Button("Predict", id="predict-btn", n_clicks=0),
    html.Div(id="prediction-output", style={"marginTop":"20px","fontSize":"24px"})
])

# Callback lives here
@app.callback(
    Output("prediction-output","children"),
    Input("predict-btn","n_clicks"),
    [State(f"input-{c}","value") for c in feature_cols]
)
def predict(n_clicks, *vals):
    if not n_clicks or None in vals:
        return ""
    raw = pd.DataFrame([vals], columns=feature_cols).astype(float)
    # re‑compute engineered features
    raw["SupportScore"]  = raw["ParentalSupport"] * raw["Extracurricular"]
    raw["SupportedGPA"]  = raw["GPA"] + 0.1 * raw["ParentalSupport"]
    raw["ExtraWork"]     = raw["StudyTimeWeekly"] * raw["Tutoring"]
    Xm = raw[[
      "StudyTimeWeekly","Absences","Tutoring","ParentalSupport",
      "GPA","SupportScore","SupportedGPA","ExtraWork"
    ]]
    pred = pipeline.predict(Xm)[0]
    grade_map = {0:"A",1:"B",2:"C",3:"D",4:"F"}
    return f"🎯 Predicted GradeClass: {grade_map[pred]}"
