from dash import html

layout = html.Div(className="content", children=[
    html.H1("Info Page"),
    html.P("BrightPath Academy’s mission is to empower students…"),
    html.Ul([
        html.Li("Delayed Identification of At-Risk Students"),
        html.Li("Lack of Targeted Support Strategies"),
        html.Li("Data Overload Without Actionable Insights"),
    ])
])
