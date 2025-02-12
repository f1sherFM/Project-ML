import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from flask import Flask
from flask import current_app as flask_app  # Import current_app
from models import db, SurveyResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config  # Import Config class

# Initialize Dash with the Flask app
dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname='/dash/')  # Mount Dash at /dash/

# Configuration for database connection
config = Config()
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

dash_app.layout = html.Div(children=[
    html.H1(children='Survey Results Dashboard'),

    dcc.Graph(
        id='example-graph',
        figure={}  # Initialize as an empty dictionary
    )
])

@dash_app.callback(
    dash.Output('example-graph', 'figure'),
    dash.Input('example-graph', 'clickData'))  # Added Input for callback
def update_graph(clickData):
    # Create a session
    session = Session()
    try:
        # Fetch data from the database
        results = session.query(SurveyResponse).all()
        df = pd.DataFrame([(r.question1, r.question2, r.question3) for r in results],
                          columns=['Question1', 'Question2', 'Question3'])

        # Create a scatter plot
        fig = px.scatter(df, x='Question1', y='Question2', hover_data=['Question3'])

        return fig
    finally:
        session.close()  # Ensure the session is closed