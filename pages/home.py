# pages/home.py
import os
from dash import html, dcc
import pandas as pd
import plotly.express as px

# Load data for the GradeClass distribution chart
df = pd.read_csv("Student_performance_data .csv")
grade_counts = (
    df['GradeClass']
      .map({0:'A',1:'B',2:'C',3:'D',4:'F'})
      .value_counts()
      .sort_index()
)
fig = px.bar(
    x=grade_counts.index,
    y=grade_counts.values,
    labels={'x':'Grade Class','y':'Count'},
    title="Dataset GradeClass Distribution",
    color=grade_counts.index,
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# Build download links if files exist 
link_items = []
summary_path = "assets/BrightPath_Summary_Report.pdf"
full_path    = "assets/BrightPath_Academy_Report.pdf"

if os.path.exists(summary_path):
    link_items.append(
        html.A(
            "📥 Download Summary Report",
            href="/assets/BrightPath_Summary_Report.pdf",
            className="sidebar-link",
            style={'marginRight':'20px'}
        )
    )
if os.path.exists(full_path):
    link_items.append(
        html.A(
            "📥 Download Full Report",
            href="/assets/BrightPath_Academy_Report.pdf",
            className="sidebar-link"
        )
    )

# Page layout 
layout = html.Div(className="content", children=[

    # Welcome section
    html.H1("🎓 Welcome to BrightPath GradeClass Predictor"),
    html.P(
        "This interactive app uses a tuned SMOTE‑MLP model to predict "
        "a student’s GradeClass based on demographics, study habits, "
        "and extracurricular involvement."
    ),

    # Distribution chart
    html.Div(dcc.Graph(figure=fig), style={'maxWidth':'600px','margin':'auto'}),

    # Go to Predict button
    html.Div(
        dcc.Link("🚀 Go to Predict", href="/predict", className="sidebar-link"),
        style={'textAlign':'center', 'margin':'30px 0'}
    ),

    # Project Summary download links (or placeholder)
    html.Div(
        link_items if link_items else html.P("Reports coming soon…"),
        style={'textAlign':'center', 'marginBottom':'50px'}
    ),

    # Meet the Team
    html.H2("Meet the Team"),
    html.Ul([
        html.Li([
            html.Strong("Glory Binkatabana: "),
            "Problem Statement, Hypothesis Generation, Getting the system ready and loading the data, Understanding the data"
        ]),
        html.Li([
            html.Strong("Tiaan Wessels: "),
            "Exploratory Data Analysis (Univariate & Bivariate), Missing value and outlier treatment"
        ]),
        html.Li([
            html.Strong("Storm Tarran: "),
            "Evaluation Metrics for classification, Feature engineering, Model Building Part 1 (Logistic Regression, Random Forest, XGBoost)"
        ]),
        html.Li([
            html.Strong("Calvin Ronin Nijenhuis: "),
            "Deep Learning model and Dash App Deployment on Render"
        ]),
    ], style={'lineHeight':'1.8em'}),

    # footer
    html.Div(
        "Powered by Render — Cloud Application Platform",
        style={'textAlign':'center', 'marginTop':'60px', 'fontStyle':'italic', 'fontSize':'0.9em'}
    )
])
