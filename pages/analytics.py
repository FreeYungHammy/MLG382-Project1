# pages/analytics.py
from dash import html

layout = html.Div(className="content", children=[

    html.Div(className="home-panel", children=[

        html.H1("Analytics"),
        html.P("The following visual summaries offer insight into the distribution, correlation, and model performance of our dataset."),

        html.H2("Feature Distributions", style={"marginTop": "30px"}),
        html.P("These charts display how various continuous and categorical features are distributed among the student population."),

        html.Img(src="/assets/cleanedfeatures.png", style={"width": "100%", "borderRadius": "8px", "marginTop": "10px"}),

        html.H2("Correlation Heatmap", style={"marginTop": "40px"}),
        html.P("This heatmap shows the strength of correlation between all pairs of input features. The deeper the red or blue, the stronger the relationship."),

        html.Img(src="/assets/corrheatmap.png", style={"width": "100%", "borderRadius": "8px", "marginTop": "10px"}),

        html.H2("Model Confusion Matrix", style={"marginTop": "40px"}),
        html.P("The confusion matrix below reflects the performance of our deployed deep learning model on test data. Diagonal values show correct predictions."),

        html.Img(src="/assets/C-test.png", style={"width": "400px", "borderRadius": "8px", "marginTop": "10px"}),

        html.H2("Feature Importance", style={"marginTop": "40px"}),
        html.P("The bar chart ranks features based on how strongly they influence the predicted GradeClass."),

        html.Img(src="/assets/heatmap.png", style={"width": "100%", "borderRadius": "8px", "marginTop": "10px"}),

    ])
])
