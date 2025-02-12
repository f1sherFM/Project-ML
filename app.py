from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
import os
from config import Config  # Import the Config class
from forms import SurveyForm
from models import db, SurveyResponse # Import the database instance

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from Config class

# Initialize the database
db.init_app(app) # Initialize the database with the Flask app
with app.app_context():
    db.create_all()  # Create database tables if they don't exist

# Initialize Redis
redis_client = Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['REDIS_DB'])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SurveyForm()
    if form.validate_on_submit():
        # Create a new SurveyResponse object
        response = SurveyResponse(
            question1=form.question1.data,
            question2=form.question2.data,
            question3=form.question3.data,
            gender=form.gender.data  # Сохраняем ответ на вопрос о поле
        )

        # Add the response to the database and commit the changes
        db.session.add(response)
        db.session.commit()

        flash('Thank you for your submission!', 'success')
        return redirect(url_for('index'))

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)