from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length

class SurveyForm(FlaskForm):
    question1 = StringField('What is your name?', validators=[DataRequired(), Length(max=255)])
    question2 = IntegerField('How old are you?', validators=[DataRequired(), NumberRange(min=0, max=120)])
    question3 = TextAreaField('What is your favorite color?', validators=[DataRequired()])
    # Пример вопроса с вариантами ответа (выпадающий список)
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])

    submit = SubmitField('Submit')