# pages/feedback.py
from dash import html, dcc, Input, Output, State

layout = html.Div(className="content", children=[
    html.Div(className="feedback-panel", children=[

        html.H2("We’d love your feedback", style={"marginBottom": "20px"}),

        html.Label("How can we improve BrightPath?", style={"color": "#fff"}),
        dcc.Textarea(
            id="feedback-box",
            placeholder="Share your thoughts, suggestions, or issues...",
            style={
                "width": "100%",
                "height": "150px",
                "padding": "12px",
                "borderRadius": "6px",
                "backgroundColor": "#16213e",
                "color": "white",
                "border": "1px solid #3a506b"
            }
        ),

        html.Button("Submit Feedback", id="submit-feedback", n_clicks=0, style={
            "marginTop": "20px",
            "padding": "10px 20px",
            "backgroundColor": "#e94560",
            "color": "white",
            "border": "none",
            "borderRadius": "4px",
            "cursor": "pointer"
        }),

        html.Div(id="feedback-response", style={
            "marginTop": "20px",
            "color": "#5bc0be",
            "fontSize": "18px"
        })
    ])
])


def register_callbacks(app):
    @app.callback(
        Output("feedback-response", "children"),
        Input("submit-feedback", "n_clicks"),
        State("feedback-box", "value")
    )
    def handle_feedback(n_clicks, text):
        if n_clicks:
            if text and text.strip():
                # Fake storage effect (like saving to database or file)
                return "Your feedback has been received. Thank you!"
            return  "Please enter some feedback before submitting."
        return ""
