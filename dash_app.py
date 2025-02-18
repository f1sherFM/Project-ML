import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from flask import Flask, current_app
from app import app, db, SurveyResponse  # Import the Flask app
#from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config1

# Configuration for database connection
config = Config1()
#engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
#Session = sessionmaker(bind=db.engine)

# Initialize Dash with the Flask app - use the app context
with app.app_context():
    dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dash/')  # Pass the Flask app
    Session = sessionmaker(bind=db.engine) # Now Session can be created
    dash_app.layout = html.Div(children=[
        html.H1(children='Survey Results Dashboard'),

        dcc.Graph(
            id='example-graph',
            figure={}
        )
    ])


@dash_app.callback(
    dash.Output('example-graph', 'figure'),
    dash.Input('example-graph', 'clickData'))
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
        session.close()