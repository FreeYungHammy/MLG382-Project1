import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import joblib
import os

# Load the trained inference pipeline 
pipeline = joblib.load("grade_predictor_inference_pipeline.pkl")

# Initialize Dash 
app = dash.Dash(__name__, assets_folder="assets")
server = app.server  # for Render deployment

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

# Import page layouts & callback registrars 
from pages.home      import layout as home_layout
from pages.analytics import layout as analytics_layout
from pages.info      import layout as info_layout
from pages.predict   import layout as predict_layout, register_callbacks as register_predict
from pages.feedback  import layout as feedback_layout, register_callbacks as register_feedback

# Register page‑specific callbacks 
register_predict(app, pipeline)
register_feedback(app)

# Main app layout with client‑side routing 
app.layout = html.Div(className="app-container", children=[
    dcc.Location(id="url", refresh=False),
    sidebar(),
    html.Div(id="page-content", className="content")
])

# Router: swap page content based on URL
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

# Run the server 
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=True, host="0.0.0.0", port=port)
