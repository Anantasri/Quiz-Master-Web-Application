from app import celery, mail, db
from flask_mail import Message
from datetime import datetime
from backend.models import *

@celery.task
def send_daily_reminders():
    today = datetime.utcnow().date
    users = User.query.all()
    quizzes_today = Quiz.query.filter_by(date_of_quiz = today).all()

    for user in users:
        if quizzes_today:
            msg = Message('Daily Reminder',
                          recipients=[user.email],
                          body=f'Hi {user.name}, new quizzes are available on the Quiz Master App. Make sure you check them out!')
            mail.send(msg)