from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
import os
from config import Config1
from forms import SurveyForm
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from flask import Flask, render_template, redirect, url_for, flash
# from flask import current_app
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config.from_object(Config1)
db = SQLAlchemy(app)

redis_client = Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['REDIS_DB'])


class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question1 = db.Column(db.String(255))
    question2 = db.Column(db.Integer)
    question3 = db.Column(db.Text)
    gender = db.Column(db.String(50))

    def __repr__(self):
        return f'<SurveyResponse {self.id}>'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SurveyForm()
    if form.validate_on_submit():
        try:
            response = SurveyResponse(
                question1=form.question1.data,
                question2=form.question2.data,
                question3=form.question3.data,
                gender=form.gender.data
            )
            db.session.add(response)
            db.session.commit()
            flash('Thank you for your submission!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Database Error: {str(e)}', 'error')
            db.session.rollback()

    return render_template('index.html', form=form)


# Create a Dash app
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dash/')
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
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
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


@app.route('/dash')  # Create a route for the Dash app
def serve_dash():
    return dash_app.index()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        Session = sessionmaker(bind=db.engine)  # Move Session creation here
    app.run(debug=True)