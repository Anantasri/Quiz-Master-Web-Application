from flask_restful import Resource
from flask import jsonify
from flask_security import auth_token_required, current_user
from backend.database import db
from backend.models import *

class SummaryAPI(Resource):
    @auth_token_required
    def get(self):
        if current_user.has_role('admin'):
            subjectlabel=[]
            attempts=[]
            subjects = db.session.query(Subject).all()
            for subject in subjects:
                subjectlabel.append(subject.name)
                user_attempt = db.session.query(Quiz).join(Chapter).filter(Chapter.subj_id == subject.subject_id).count()
                attempts.append(user_attempt)
            
            topscore=[]
            for subject in subjects:
                top_score = 0
                for chapter in db.session.query(Chapter).filter_by(subj_id=subject.subject_id).all():
                    for quiz in db.session.query(Quiz).filter_by(chap_id = chapter.chapter_id).all():
                        for scores in db.session.query(Scores).filter_by(quiz_id=quiz.Quiz_id).all():
                            if scores.total_scored > top_score:
                                top_score = scores.total_scored
                topscore.append(top_score)
            return jsonify({
                "role":"admin",
                "subject_attempt":{
                    "subjects": subjectlabel,
                    "attempts": attempts
                },
                "topScores":{
                    "subjects":subjectlabel,
                    "scores": topscore
                }
            })

        else:
            subjectlabel=[]
            quizpersub=[]
            subjects = db.session.query(Subject).all()
            for subject in subjects:
                subjectlabel.append(subject.name)
                no_of_quizes = db.session.query(Quiz).join(Chapter).filter(Chapter.subj_id == subject.subject_id).count()
                quizpersub.append(no_of_quizes)
            monthlabel=[]
            quizpermonth=[]
            month1=[]
            quizes = db.session.query(Quiz).all()
            for quiz in quizes:
                month1.append(quiz.date_of_quiz.month)
            months = sorted(set(month1))
            month_map = {
                            1: "January", 2: "February", 3: "March", 4: "April",
                            5: "May", 6: "June", 7: "July", 8: "August",
                            9: "September", 10: "October", 11: "November", 12: "December"
                        }
            for month in months:
                monthlabel.append(month_map[month])
                quizpermonth.append(month1.count(month))

            return jsonify({
                "role": "user",
                "quiz_counts": {
                    "subjects": subjectlabel,
                    "quizcount": quizpersub
                },
                "monthlyQuiz":{
                    "month": monthlabel,
                    "quizcount": quizpermonth
                }
            })


