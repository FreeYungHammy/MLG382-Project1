# pages/feedback.py
from dash import html, dcc, Input, Output, State

layout = html.Div(className="content", children=[
    html.H1("Feedback"),
    dcc.Textarea(
        id="feedback-box",
        placeholder="Share your thoughts...",
        style={"width": "100%", "height": "150px"}
    ),
    html.Button("Submit", id="submit-feedback", n_clicks=0),
    html.Div(id="feedback-response", style={"marginTop":"20px","fontSize":"18px"})
])

def register_callbacks(app):
    @app.callback(
        Output("feedback-response","children"),
        Input("submit-feedback","n_clicks"),
        State("feedback-box","value")
    )
    def handle_feedback(n_clicks, text):
        if n_clicks and text:
            # (Here you could log to a DB or file)
            return "👍 Thanks for your feedback!"
        return ""
