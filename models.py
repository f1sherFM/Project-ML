"""
#from flask_sqlalchemy import SQLAlchemy
#from app import app as app  # Импортируем экземпляр Flask

db = SQLAlchemy()  # Создаем экземпляр SQLAlchemy, связанный с Flask-приложением

class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question1 = db.Column(db.String(255))
    question2 = db.Column(db.Integer)  # Пример числового ответа
    question3 = db.Column(db.Text)  # Пример текстового ответа
    #  age = db.Column(db.Integer)
    #  gender = db.Column(db.String(50))

    def __repr__(self):
        return f'<SurveyResponse {self.id}>'
        """
