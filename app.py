import dash
from dash import html, dcc, Input, Output, State
import joblib
import pandas as pd
import numpy as np
import os

# Load the trained pipeline
pipeline = joblib.load("grade_predictor_final_pipeline.pkl")

# Initialize Dash
app = dash.Dash(__name__)
server = app.server  # for Render

# Style constants
dark_bg = '#1a1a2e'
accent = '#e94560'
input_bg = '#16213e'
text_color = '#ffffff'
card_bg = '#0f3460'

# Features list for dynamic input generation
feature_cols = [
    'Age', 'Gender', 'Ethnicity', 'StudyTimeWeekly', 'Absences',
    'Tutoring', 'ParentalSupport', 'Extracurricular', 'Sports',
    'Music', 'Volunteering'
]

# Layout
app.layout = html.Div(style={
    'backgroundColor': dark_bg,
    'color': text_color,
    'minHeight': '100vh',
    'padding': '40px',
    'fontFamily': 'Arial, sans-serif'
}, children=[
    html.H1("🎓 BrightPath GradeClass Predictor", style={
        'textAlign': 'center',
        'color': accent,
        'marginBottom': '30px'
    }),

    # Input grid
    html.Div([
        html.Div([
            html.Label(col, style={'color': text_color}),
            dcc.Input(
                id=f"input-{col}",
                type='number',
                min=0,
                step=0.1,
                style={
                    'width': '100%',
                    'padding': '8px',
                    'borderRadius': '4px',
                    'border': '1px solid #3a506b',
                    'backgroundColor': input_bg,
                    'color': text_color
                }
            )
        ], style={'marginBottom': '20px'})
        for col in feature_cols
    ], style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fill, minmax(200px, 1fr))',
        'gap': '20px'
    }),

    html.Div(html.Button('Predict Grade', id='predict-btn', n_clicks=0, style={
        'backgroundColor': accent,
        'color': text_color,
        'border': 'none',
        'padding': '12px 24px',
        'fontSize': '16px',
        'borderRadius': '4px',
        'cursor': 'pointer',
        'marginTop': '20px'
    }), style={'textAlign': 'center'}),

    html.Div(id='prediction-output', style={
        'marginTop': '30px',
        'textAlign': 'center',
        'fontSize': '24px'
    })
])

# Callback
def format_input(values):
    # Convert list of values to numpy array for prediction
    arr = np.array(values, dtype=float).reshape(1, -1)
    return arr

@app.callback(
    Output('prediction-output', 'children'),
    Input('predict-btn', 'n_clicks'),
    [State(f"input-{col}", 'value') for col in feature_cols]
)
def predict(n_clicks, *vals):
    if n_clicks and None not in vals:
        data = format_input(vals)
        pred_class = pipeline.predict(data)[0]
        grade_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'F'}
        return f"Predicted GradeClass: {grade_map.get(pred_class, '?')}"
    return "❗ Please enter all feature values and click Predict."

# Run
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(debug=True, host='0.0.0.0', port=port)
