from flask_restful import Resource
from flask import jsonify, request
from flask_security import auth_token_required, current_user
from datetime import date
from backend.database import db
from backend.models import *

class AllChaptersAPI(Resource):
    def get(self):
        chapters = Chapter.query.all()
        result = [
            {
                "chapter_id": chapter.chapter_id,
                "name": chapter.name,
                "subject_id": chapter.subj_id
            } for chapter in chapters
        ]
        return jsonify(result)
    
class UpcomingQuizAPI(Resource):
    def get(self):
        today = date.today()
        upcoming_quiz = Quiz.query.filter(Quiz.date_of_quiz >= today).all()
        result = []
        for quiz in upcoming_quiz:
            result.append({
                "Quiz_id": quiz.Quiz_id,
                "chap_id": quiz.chap_id,
                "date_of_quiz": quiz.date_of_quiz.isoformat(),
                "time_duration": quiz.time_duration
            })
        return jsonify(result)

class UserViewQuizAPI(Resource):
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"error": "Quiz not found"}, 404
        chapter = Chapter.query.get(quiz.chap_id)
        if not chapter:
            return {"error": "Chapter not found"}, 404
        subject = Subject.query.get(chapter.subj_id)
        if not subject:
            return {"error": "Subject not found"}, 404
        
        question_count = Question.query.filter_by(quiz_id=quiz_id).count()

        return jsonify({
            "quiz":{
            "Quiz_id": quiz.Quiz_id,
            "date_of_quiz": quiz.date_of_quiz.isoformat(),
            "time_duration": quiz.time_duration,
            "remarks": quiz.remarks
        },
        "chapter": {
            "name": chapter.name,
            "description": chapter.description
        },
        "subject": {
            "name": subject.name,
            "description": subject.description
        },
        "question_count": question_count
        })

class QuizAttemptAPI(Resource):
    @auth_token_required
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message":"Quiz not found"}, 404
        
        today = datetime.today().date()
        if quiz.date_of_quiz != today:
            return {"message": "This Quiz is not scheduled for today."},403
        
        chapter = Chapter.query.get(quiz.chap_id)
        questions = Question.query.filter_by(quiz_id=quiz_id).all()

        return jsonify({
            "quiz":{
                "Quiz_id": quiz.Quiz_id,
                "time_duration": quiz.time_duration,
                "date_of_quiz": quiz.date_of_quiz,
                "remarks": quiz.remarks
            },
            "chapter": {
                "name": chapter.name
            },
            "questions": [
                {
                    "question_id": q.question_id,
                    "Question_statement": q.Question_statement,
                    "option_a": q.option_a,
                    "option_b": q.option_b,
                    "option_c": q.option_c,
                    "option_d": q.option_d
                } for q in questions
            ]
        })

class SubmitQuizAPI(Resource):
    @auth_token_required
    def post(self, quiz_id):
        user_email = current_user.email
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return {"message": "User not found"}, 404
        
        data = request.json
        answers = data.get("answers", {})
        time_taken = data.get("time_taken", 0)

        questions = Question.query.filter_by(quiz_id = quiz_id).all()
        total = 0
        for q in questions:
            option = {
                "a": q.option_a,
                "b": q.option_b,
                "c": q.option_b,
                "d": q.option_d
             }
            correct_ans = option.get(q.answer.lower(), q.answer)
            selected = answers.get(str(q.question_id))
            print(f"user selected:, '{selected}'")
            print(f"Correct asnwer: '{q.answer}'")
                  
            if selected and selected.strip().lower() == correct_ans:
                total += 1
        info = Scores.query.filter_by(user_id=user.user_id, quiz_id=quiz_id).first()
        if info:
            info.total_scored = total
            info.time_stamp_of_attempt = datetime.now()
            info.time_taken = time_taken
        else:
            addscore = Scores(
                user_id = user.user_id,
                quiz_id = quiz_id,
                total_scored = total,
                time_stamp_of_attempt=datetime.now(),
                time_taken=time_taken
            )
            db.session.add(addscore)
            db.session.commit()
        return {"message": "Quiz Submitted successfully"}, 200

class UserScoresAPI(Resource):
    @auth_token_required
    def get(self):
        user_id = current_user.user_id
        scores = Scores.query.filter_by(user_id=user_id).all()
        quizzes = Quiz.query.all()
        chapters = Chapter.query.all()
        questions = Question.query.all()

        score = [
            {
                "quiz_id": s.quiz_id,
                "total_scored": s.total_scored
            } for s in scores
        ]
        quiz = [
            {
                "Quiz_id": q.Quiz_id,
                "chap_id": q.chap_id
            } for q in quizzes
        ]
        chap = [
            {
                "chapter_id": c.chapter_id,
                "name": c.name
            } for c in chapters
        ]
        ques = [
            {
                "quiz_id": q.quiz_id
            } for q in questions
        ]
        return jsonify({
            "scores": score,
            "quizzes": quiz,
            "chapters": chap,
            "questions": ques
        })



