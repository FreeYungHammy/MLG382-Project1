# pages/home.py
import os
from dash import html, dcc
import pandas as pd
import plotly.express as px

# Load data & build chart
df = pd.read_csv("Student_performance_data .csv")
grade_counts = (
    df['GradeClass'].map({0:'A',1:'B',2:'C',3:'D',4:'F'})
       .value_counts().sort_index()
)
fig = px.bar(
    x=grade_counts.index,
    y=grade_counts.values,
    labels={'x':'Grade Class','y':'Count'},
    title="Dataset GradeClass Distribution",
    color=grade_counts.index,
    color_discrete_sequence=px.colors.qualitative.Pastel
)
# Darken chart background
fig.update_layout(
    plot_bgcolor='#1a1a2e',
    paper_bgcolor='#1a1a2e',
    font_color='#edf2f4'
)

# Build download links if available
link_items = []
if os.path.exists("assets/BrightPath_Summary_Report.pdf"):
    link_items.append(
        html.A("Summary Report",
               href="/assets/BrightPath_Summary_Report.pdf",
               className="sidebar-link home-btn")
    )
if os.path.exists("assets/BrightPath_Academy_Report.pdf"):
    link_items.append(
        html.A("Full Report",
               href="/assets/BrightPath_Academy_Report.pdf",
               className="sidebar-link home-btn")
    )

layout = html.Div(className="content", children=[

    # Wrap everything in a centered “card”
    html.Div(className="home-panel", children=[

        html.H1("Welcome to BrightPath GradeClass Predictor"),
        html.P(
            "This interactive app uses a tuned SMOTE‑MLP model to predict "
            "a student’s GradeClass based on demographics, study habits, "
            "and extracurricular involvement."
        ),

        # Chart
        html.Div(dcc.Graph(figure=fig), style={'margin':'30px 0'}),

        # Rocket button
        html.Div(
            dcc.Link("Go to Predict", href="/predict",
                     className="sidebar-link home-btn"),
            style={'textAlign':'center', 'marginBottom':'30px'}
        ),

        # Summary / Full Report
        html.Div(
            link_items if link_items else html.P("Reports coming soon…"),
            style={'textAlign':'center', 'marginBottom':'50px'}
        ),

        # Meet the Team
        html.H2("Meet the Team"),
        html.Ul([
            html.Li([
                html.Strong("Glory Binkatabana: "),
                "Problem statement, hypothesis, data loading & understanding"
            ]),
            html.Li([
                html.Strong("Tiaan Wessels: "),
                "Univariate & bivariate EDA, missing‐value & outlier treatment"
            ]),
            html.Li([
                html.Strong("Storm Tarran: "),
                "Evaluation metrics, feature engineering, baseline models"
            ]),
            html.Li([
                html.Strong("Calvin Ronin Nijenhuis: "),
                "Deep learning model & app deployment on Render"
            ]),
        ], style={'lineHeight':'1.6em'}),

        # Footer
        html.Div(
            "Powered by Render — Cloud Application Platform",
            style={'textAlign':'center','marginTop':'40px','fontStyle':'italic'}
        ),

    ])

])
