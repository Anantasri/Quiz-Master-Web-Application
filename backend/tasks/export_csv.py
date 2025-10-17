import csv
from flask import url_for
from app import celery, db
from backend.models import *
from flask_mail import Message
from flask_mail import Mail
from datetime import datetime

@celery.task
def export_user_scores(user_id):
    user = User.query(user_id)
    scores = Scores.query.filter_by(user_id=user_id).all()

    filename = f'export_{user_id}_{datetime.utcnow().isoformat()}.csv'
    filepath = f'backend/exports/{filename}'

    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Quiz ID','Score'])
        for score in scores:
            writer.writerow([score.quiz_id, score.total_scored])
        
    msg = Message(
        subjects='Your Quiz CSV Export',
        recipients=[user.email],
        body='Here is your exported quiz data.',
    )
    with open(filepath,'rb') as f:
        msg.attach(filename, 'text/csv', f.read())
    Mail.send(msg)