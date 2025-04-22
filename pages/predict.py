# pages/predict.py
from dash import html, dcc, Input, Output, State
import pandas as pd

# 11 raw inputs + metadata

feature_info = {
    "Age":             { "placeholder":"15–18",    "min":15, "max":18,   "step":1,    "desc":"Student age in years." },
    "Gender":          { "placeholder":"Female = 1, Male = 0", "min":0,  "max":1,    "step":1,    "desc":"0 for Male, 1 for Female." },
    "Ethnicity":       { "placeholder":"0–3",      "min":0,  "max":3,    "step":1,    "desc":"Caucasian = 0, African American = 1, Asian = 2, Other = 3." },
    "GPA":             { "placeholder":"2.0–4.0",  "min":2.0,"max":4.0,  "step":0.01, "desc":"Grade Point Average." },
    "StudyTimeWeekly": { "placeholder":"0–20",     "min":0,  "max":20,   "step":0.5,  "desc":"Hours spent studying per week." },
    "Absences":        { "placeholder":"0–30",     "min":0,  "max":30,   "step":1,    "desc":"Number of absences in the year." },
    "Tutoring":        { "placeholder":"Yes = 1, No = 0",   "min":0,  "max":1,    "step":1,    "desc":"1 if student uses a tutor, 0 otherwise." },
    "ParentalSupport": { "placeholder":"0–4",      "min":0,  "max":4,    "step":1,    "desc":"Very high parental support = 4, none = 0." },
    "Extracurricular": { "placeholder":"Yes = 1, No = 0",   "min":0,  "max":1,    "step":1,    "desc":"1 if the student has extracurricular activities, 0 otherwise." },
    "Sports":          { "placeholder":"Yes = 1, No = 0",   "min":0,  "max":1,    "step":1,    "desc":"1 if the student participates in sports, 0 otherwise." },
    "Music":           { "placeholder":"Yes = 1, No = 0",   "min":0,  "max":1,    "step":1,    "desc":"1 if the student participates in music, 0 otherwise." },
    "Volunteering":    { "placeholder":"Yes = 1, No = 0",   "min":0,  "max":1,    "step":1,    "desc":"1 if the student volunteers, 0 otherwise." },
}

feature_cols = list(feature_info.keys())

# Build each input card with placeholder + helper
input_cards = []
for col in feature_cols:
    info = feature_info[col]
    input_cards.append(
        html.Div(className="input-card", children=[
            html.Label(col),
            dcc.Input(
                id=f"input-{col}",
                type="number",
                placeholder=info["placeholder"],
                min=info["min"],
                max=info["max"],
                step=info["step"],
                style={"width":"100%"}
            ),
            html.Small(info["desc"], style={"color":"#ccc", "fontSize":"0.8em"})
        ])
    )

# Layout
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
        Output("prediction-output","children"),
        Input("predict-btn","n_clicks"),
        [State(f"input-{col}","value") for col in feature_cols]
    )
    def predict(n_clicks, *vals):
        if not n_clicks or None in vals:
            return ""
        raw = pd.DataFrame([vals], columns=feature_cols).astype(float)
        raw['SupportScore']   = raw['ParentalSupport'] * raw['Extracurricular']
        raw['SupportedGPA']   = raw['GPA'] + 0.1 * raw['ParentalSupport']
        raw['ExtraWork']      = raw['StudyTimeWeekly'] * raw['Tutoring']
        X_model = raw[[
            'StudyTimeWeekly','Absences','Tutoring','ParentalSupport',
            'GPA','SupportScore','SupportedGPA','ExtraWork'
        ]]
        pred = pipeline.predict(X_model)[0]
        grade_map = {0:"A",1:"B",2:"C",3:"D",4:"F"}
        return f"🎯 Predicted GradeClass: {grade_map[pred]}"
