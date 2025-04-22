# pages/predict.py
from dash import html, dcc, Input, Output, State
import pandas as pd

# metadata for input fields
feature_info = {
    "Age":             { "placeholder":"15–18", "min":15, "max":18, "step":1, "desc":"Student age in years." },
    "Gender":          { "placeholder":"Male = 0, Female = 1", "min":0, "max":1, "step":1, "desc":"0 for Male, 1 for Female." },
    "Ethnicity":       { "placeholder":"Choose between 0–3", "min":0, "max":3, "step":1, "desc":"Caucasian = 0, African/American = 1, Asian = 2, Other = 3." },
    "GPA":             { "placeholder":"Choose between 2.0–4.0", "min":2.0, "max":4.0, "step":0.01, "desc":"Grade Point Average." },
    "StudyTimeWeekly": { "placeholder":"Choose between 0–20", "min":0, "max":20, "step":0.5, "desc":"Hours spent studying per week." },
    "Absences":        { "placeholder":"Choose between 0–30", "min":0, "max":30, "step":1, "desc":"Number of absences in the year." },
    "Tutoring":        { "placeholder":"Yes = 1, No = 0", "min":0, "max":1, "step":1, "desc":"1 if student uses a tutor, 0 otherwise." },
    "ParentalSupport": { "placeholder":"Choose between 0–4", "min":0, "max":4, "step":1, "desc":"0=None → 4=Very High support." },
    "Extracurricular": { "placeholder":"Yes = 1, No = 0", "min":0, "max":1, "step":1, "desc":"Student does extracurricular activities = 1, otherwise 0." },
    "Sports":          { "placeholder":"Yes = 1, No = 0", "min":0, "max":1, "step":1, "desc":"Student participates in sports = 1, otherwise 0." },
    "Music":           { "placeholder":"Yes = 1, No = 0", "min":0, "max":1, "step":1, "desc":"Student participates in music = 1, otherwise 0." },
    "Volunteering":    { "placeholder":"Yes = 1, No = 0", "min":0, "max":1, "step":1, "desc":"Student volunteers = 1, otherwise 0." }
}
feature_cols = list(feature_info.keys())

#input cards 
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
                style={"width": "100%"}
            ),
            html.Small(info["desc"], style={"color": "#ccc", "fontSize": "0.8em"})
        ])
    )

# layout
layout = html.Div(className="content", children=[
    html.H1("Make a Prediction"),

    html.Div(
        children=input_cards[:-2],  # except last 2 inputs
        style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
            "gap": "20px"
        }
    ),

    html.Div(  
        children=[
            html.Div(input_cards[-2], style={"width": "250px"}),
            html.Div(input_cards[-1], style={"width": "250px"})
        ],
        style={"display": "flex", "justifyContent": "center", "gap": "20px", "marginTop": "30px"}
    ),

    html.Div(  
        html.Button("Predict", id="predict-btn", n_clicks=0),
        style={"textAlign": "center", "marginTop": "30px"}
    ),

    html.Div(  
        id="prediction-output",
        style={
            "marginTop": "30px",
            "maxWidth": "600px",
            "marginLeft": "auto",
            "marginRight": "auto",
            "padding": "20px",
            "borderRadius": "8px",
            "backgroundColor": "#0f3460",
            "fontSize": "22px",
            "color": "#ffffff",
            "textAlign": "center"
        }
    )
])

#callback
def register_callbacks(app, pipeline):
    @app.callback(
        Output("prediction-output", "children"),
        Input("predict-btn", "n_clicks"),
        [State(f"input-{col}", "value") for col in feature_cols]
    )
    def predict(n_clicks, *vals):
        if not n_clicks or None in vals:
            return ""

        # Data preprocessing
        raw = pd.DataFrame([vals], columns=feature_cols).astype(float)
        raw['SupportScore'] = raw['ParentalSupport'] * raw['Extracurricular']
        raw['SupportedGPA'] = raw['GPA'] + 0.1 * raw['ParentalSupport']
        raw['ExtraWork'] = raw['StudyTimeWeekly'] * raw['Tutoring']

        # Prepare model input
        scaler = pipeline.named_steps['scaler']
        required = list(scaler.feature_names_in_)
        X_model = raw[required]
        X_scaled = scaler.transform(X_model)

        # Prediction
        pred = pipeline.named_steps['mlp'].predict(X_scaled)[0]
        grade_map = {0: "A", 1: "B", 2: "C", 3: "D", 4: "F"}

        return f"Predicted GradeClass: {grade_map[pred]}"
