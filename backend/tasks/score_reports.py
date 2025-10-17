from app import celery, mail, db
from flask_mail import Message
from backend.models import *

@celery.task
def send_report():
    users = User.query.all()

    for user in users:
        scores = Scores.query.filter_by(user_id=user.user_id).all()
        score = [s for s in scores]

        body = f'Hi {user.name}, \n\Here is your quiz activity report\n'
        for s in score:
            body += f'Quiz ID: {score.quiz_id} | Score: {s.total_scored}\n'
        
        msg = Message('Score Report',
                      recipients = [user.email],
                      body = body)
        mail.send(msg)

