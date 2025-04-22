from dash import html

layout = html.Div(className="content", children=[
    html.H1("Welcome to BrightPath Academy"),
    html.P(
        "This app predicts a student’s GradeClass "
        "based on demographics, study habits, and activities."
    ),
    html.P("Use the sidebar to navigate.")
])
