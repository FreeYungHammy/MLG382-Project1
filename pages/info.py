# pages/info.py
from dash import html, dcc
import pandas as pd
import dash_table 
import os

# displaying dataset
filename = "Student_performance_data .csv"  
if os.path.exists(filename):
    df = pd.read_csv(filename)
    stat_summary = df.describe().round(2).reset_index()
else:
    df = pd.DataFrame()
    stat_summary = pd.DataFrame()

layout = html.Div(className="content", children=[

    # title and intro
    html.H1("BrightPath Academy - Information Page"),
    html.P("We aim to empower students by identifying at-risk learners early on, "
           "providing actionable insights, and enabling targeted support strategies."),

    html.H2("Challenges in Education"),
    html.Ul([
        html.Li("Delayed Identification of At-Risk Students"),
        html.Li("Lack of Targeted Support Strategies"),
        html.Li("Data Overload Without Actionable Insights"),
    ]),

    # dataset preview
    html.H2("Dataset Preview"),
    html.Div([
        dash_table.DataTable(
            data=df.head(10).to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center', 'padding': '8px'},
            style_header={'backgroundColor': '#16213e', 'color': 'white', 'fontWeight': 'bold'},
            style_data={'backgroundColor': '#1a1a2e', 'color': 'white'}
        )
    ], style={'marginBottom': '40px'}),

    # statistical summary
    html.H2("Statistical Summary"),
    html.Div([
        dash_table.DataTable(
            data=stat_summary.to_dict('records'),
            columns=[{"name": i, "id": i} for i in stat_summary.columns],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center', 'padding': '8px'},
            style_header={'backgroundColor': '#16213e', 'color': 'white', 'fontWeight': 'bold'},
            style_data={'backgroundColor': '#1a1a2e', 'color': 'white'}
        )
    ]),

    html.Div("Note: This summary helps understand trends and data distributions "
             "used in the modeling process.", style={'marginTop': '20px', 'fontStyle': 'italic'})
])
