import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import joblib
import numpy as np

# loading the model and scaler
model = joblib.load("mlp_model.pkl")
scaler = joblib.load("scaler.pkl")

# intialize dash
app = dash.Dash(__name__)
server = app.server  # Needed for Render deployment

#layout of html 
app.layout = html.Div(style={
    'backgroundColor': '#0b132b',
    'padding': '40px',
    'minHeight': '100vh',
    'fontFamily': 'Segoe UI, sans-serif',
    'color': '#fff'
}, children=[
    html.H1("📘 Student Grade Predictor", style={
        'textAlign': 'center',
        'marginBottom': '50px',
        'color': '#5bc0be',
        'fontSize': '36px'
    }),

    html.Div([
        html.Div([
            html.Label("GPA:", style={'color': '#fff'}),
            dcc.Input(id='gpa', type='number', min=0, max=4, step=0.01,
                      style={'width': '100%', 'padding': '10px', 'borderRadius': '5px', 'border': '1px solid #3a506b', 'backgroundColor': '#1c2541', 'color': 'white'})
        ]),

        html.Div([
            html.Label("Study Time Weekly (hours):", style={'color': '#fff'}),
            dcc.Input(id='study_time', type='number', min=0, step=0.1,
                      style={'width': '100%', 'padding': '10px', 'borderRadius': '5px', 'border': '1px solid #3a506b', 'backgroundColor': '#1c2541', 'color': 'white'})
        ]),

        html.Div([
            html.Label("Absences:", style={'color': '#fff'}),
            dcc.Input(id='absences', type='number', min=0,
                      style={'width': '100%', 'padding': '10px', 'borderRadius': '5px', 'border': '1px solid #3a506b', 'backgroundColor': '#1c2541', 'color': 'white'})
        ]),

        html.Div([
            html.Label("Parental Support (0–4):", style={'color': '#fff'}),
            dcc.Input(id='parental_support', type='number', min=0, max=4,
                      style={'width': '100%', 'padding': '10px', 'borderRadius': '5px', 'border': '1px solid #3a506b', 'backgroundColor': '#1c2541', 'color': 'white'})
        ]),

        html.Div([
            html.Label("Parental Education (0–4):", style={'color': '#fff'}),
            dcc.Input(id='parental_edu', type='number', min=0, max=4,
                      style={'width': '100%', 'padding': '10px', 'borderRadius': '5px', 'border': '1px solid #3a506b', 'backgroundColor': '#1c2541', 'color': 'white'})
        ])
    ], style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(240px, 1fr))',
        'gap': '20px',
        'marginBottom': '30px'
    }),

    html.Div([
        html.Button('🎯 Predict Grade', id='predict-btn', n_clicks=0, style={
            'marginTop': '20px',
            'padding': '15px 30px',
            'fontSize': '16px',
            'backgroundColor': '#1c2541',
            'color': '#5bc0be',
            'border': '2px solid #5bc0be',
            'borderRadius': '5px',
            'cursor': 'pointer'
        })
    ], style={'textAlign': 'center'}),

    html.Div(id='prediction-output', style={
        'marginTop': '40px',
        'textAlign': 'center',
        'fontSize': '24px',
        'color': '#edf2f4'
    })
])


# logic for callbacks when buttons are clicked
@app.callback(
    Output('prediction-output', 'children'),
    Input('predict-btn', 'n_clicks'),
    State('gpa', 'value'),
    State('study_time', 'value'),
    State('absences', 'value'),
    State('parental_support', 'value'),
    State('parental_edu', 'value')
)

# predicting the grade 
def predict_grade(n_clicks, gpa, study_time, absences, support, edu):
    if None in [gpa, study_time, absences, support, edu]:
        return "❗ Please fill in all fields."

    input_data = np.array([[study_time, absences, 0, support, gpa]])  # Tutoring is hardcoded = 0
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]

    grade_map = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "F"
    }

    return f" Predicted Grade: {grade_map.get(prediction, '?')}"

#running the app
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=True, host="0.0.0.0", port=port)

