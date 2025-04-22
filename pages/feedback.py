from dash import html, dcc, Input, Output
from app import app

layout = html.Div(className="content", children=[
    html.H1("Feedback"),
    dcc.Textarea(
        id="feedback-box",
        placeholder="Share your thoughts...",
        style={"width":"100%", "height":"150px"}
    ),
    html.Button("Submit", id="submit-feedback", n_clicks=0),
    html.Div(id="feedback-response", style={"marginTop":"20px"})
])

@app.callback(
    Output("feedback-response","children"),
    Input("submit-feedback","n_clicks"),
    State("feedback-box","value")
)
def handle_feedback(n, text):
    if n and text:
        # (you could log to a file or database here)
        return "Thanks for your feedback!"
    return ""
