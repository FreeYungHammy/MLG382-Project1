import dash
from dash import html, dcc, Input, Output, State
import joblib
import pandas as pd
import os

# Load inference pipeline
pipeline = joblib.load("grade_predictor_inference_pipeline.pkl")

# Initialize Dash
app = dash.Dash(__name__, assets_folder="assets")
server = app.server

# Features for inputs
feature_cols = [
    'Age', 'Gender', 'Ethnicity', 'StudyTimeWeekly', 'Absences',
    'Tutoring', 'ParentalSupport', 'Extracurricular', 'Sports',
    'Music', 'Volunteering'
]

# Sidebar component
def sidebar():
    return html.Div(className="sidebar", children=[
        html.H2("BrightPath Academy", className="sidebar-header"),
        html.Ul(className="sidebar-list", children=[
            html.Li(dcc.Link("Home",      href="/",           className="sidebar-link")),
            html.Li(dcc.Link("Analytics", href="/analytics",  className="sidebar-link")),
            html.Li(dcc.Link("Info",      href="/info",       className="sidebar-link")),
            html.Li(dcc.Link("Predict",   href="/predict",    className="sidebar-link")),
            html.Li(dcc.Link("Feedback",  href="/feedback",   className="sidebar-link")),
        ])
    ])

# Import page layouts
from pages import (
    home_layout,
    analytics_layout,
    info_layout,
    predict_layout,
    feedback_layout,
)

# Import and register the Predict‐page callbacks
from pages.predict import register_callbacks as register_predict_callbacks
register_predict_callbacks(app, pipeline)

# Main layout with Location for routing
app.layout = html.Div(className="app-container", children=[
    dcc.Location(id="url", refresh=False),
    sidebar(),
    html.Div(id="page-content", className="content")
])

# Routing callback
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/analytics":
        return analytics_layout
    elif pathname == "/info":
        return info_layout
    elif pathname == "/predict":
        return predict_layout
    elif pathname == "/feedback":
        return feedback_layout
    return home_layout

# Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=True, host="0.0.0.0", port=port)
