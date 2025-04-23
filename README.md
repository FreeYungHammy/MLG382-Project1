# MLG382-Project1 - Project Overview
A collaborative machine learning project for student performance classification using traditional and deep learning techniques.

## Team Members
- Glory Binkatabana: Problem statement to understanding data
- Tiaan Wessels: EDA and cleaning
- Storm Tarran: Classical ML model building
- Calvin Ronin Nijenhuis: Deep learning and deployment

## How to Run

git clone https://github.com/FreeYungHammy/MLG382-Project1.git

cd MLG382-Project1

On Windows (PowerShell):

.venv\Scripts\Activate.ps1

On macOS/Linux:

source .venv/bin/activate

Install dependencies

pip install -r requirements.txt

Run the application

python app.py

Open your browser
Go to: http://localhost:8050

## Deployment
The application is live and hosted using Render: https://grade-predictor-j4yq.onrender.com/

Deployment Steps:

Push code to GitHub

Connect Render to the repo

Configure:

Build command: pip install -r requirements.txt

Start command: python app.py

Set Python version (via runtime.txt or Render settings)

## File Structure
MLG_382_BrightPath.ipynb: Main Jupyter notebook containing the analysis and modeling.

app.py: Dash application script for the web interface.

build_inference_pipeline.py: Script to build the machine learning pipeline.

grade_predictor_inference_pipeline.pkl: Serialized model pipeline.

scaler.pkl: Serialized scaler used for feature normalization.

requirements.txt: List of project dependencies.

Student_performance_data.csv: Dataset used for training and evaluation.

assets/: Directory containing static assets like images.

pages/: Directory for additional web pages or templates.​

archive_pipeline/: Directory containing archived serialized model pipelines.
