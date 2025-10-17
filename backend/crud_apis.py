from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import utils, auth_token_required, roles_required

from backend.database import db
from backend.models import *

class SubjectAPI(Resource):
    def get(self):
        subjects = Subject.query.all()
        sub = [
            {
                'subject_id': subject.subject_id,
                'name': subject.name,
                'description': subject.description
            } for subject in subjects
        ]
        return {'subjects': sub}

class AddSubjectAPI(Resource):
    def post(self):
        credential = request.get_json()

        if not credential:
            result = {
                'message': 'All credentials are required.'
            }
            return make_response(jsonify(result), 400)
        
        name = credential.get('name', None)
        description = credential.get('description', None)
        
        if not name or not description:
            result = {
                'message': 'All the credentials are required.'
            }
            return make_response(jsonify(result), 409)
        
        if Subject.query.filter_by(name=name).first():
            result = {
                'message': 'Subject already exists.'
            }
            return make_response(jsonify(result), 409)
        
        addsub = Subject(
            name = name,
            description = description
        )
        db.session.add(addsub)
        db.session.commit()

        response = {
            'message': 'Subject Added Successfully!'
            }
        return make_response(jsonify(response), 201)

class getSubjectAPI(Resource):
    def get(self, subject_id):
        subject = Subject.query.get(subject_id)
        if not subject:
            return {'message': 'Subject not found'}, 404
        return {
            'subject_id': subject.subject_id,
            'name': subject.name,
            'description': subject.description
        }, 200

class EditSubjectAPI(Resource):
    def put(self, subject_id):
        data = request.get_json()

        subject = Subject.query.get(subject_id)
        if not subject:
            return {'message': 'Subject not found'}, 404

        subject.name = data.get('name', subject.name)
        subject.description = data.get('description', subject.description)

        db.session.commit()

        return {'message': 'Subject updated successfully'}, 200
    
class DeleteSubjectAPI(Resource):
    def delete(self, subject_id):
        subject = Subject.query.get(subject_id)
        if not subject:
            return {'message': 'Subject Not Found'}, 404
        
        chapters = Chapter.query.filter_by(subj_id=subject_id).all()

        for chapter in chapters:
            quizzes = Quiz.query.filter_by(chap_id=chapter.chapter_id).all()
            for quiz in quizzes:
                Question.query.filter_by(quiz_id=quiz.Quiz_id).delete()
                Scores.query.filter_by(quiz_id=quiz.Quiz_id).delete()
                db.session.delete(quiz)
            db.session.delete(chapter)
        db.session.delete(subject)

        db.session.commit()
        return{'message': 'Subjects and all other related information are deleted.'}, 200
 
class ChapterAPI(Resource):
    def get(self, subject_id):
        chapters = Chapter.query.filter_by(subj_id = subject_id).all()
        
        chap = [
            {
                'chapter_id': chapter.chapter_id,
                'name': chapter.name,
                'description': chapter.description
            } for chapter in chapters
        ]
        return {'chapters': chap}, 200
    
class AddChapterAPI(Resource):
    def post(self, subject_id):
        credential = request.get_json()

        if not credential:
            result = {
                'message': 'All credentials are required.'
            }
            return make_response(jsonify(result), 400)
        
        name = credential.get('name', None)
        description = credential.get('description', None)
        
        if not name or not description:
            result = {
                'message': 'All the credentials are required.'
            }
            return make_response(jsonify(result), 409)
        
        if Chapter.query.filter_by(name=name).first():
            result = {
                'message': 'Chapter already exists.'
            }
            return make_response(jsonify(result), 409)
        
        addchap = Chapter(
            name = name,
            description = description,
            subj_id = subject_id
        )
        db.session.add(addchap)
        db.session.commit()

        response = {
            'message': 'Chapter Added Successfully!'
            }
        return make_response(jsonify(response), 201)

class EditChapterAPI(Resource):
    def get(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {'message': 'chapter not found'}, 401
        return {
            'chapter_id': chapter.chapter_id,
            'name': chapter.name,
            'description': chapter.description
        }, 200
    
    def put(self, chapter_id):
        data = request.get_json()
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {'message': 'Chapter not found'}, 404

        chapter.name = data.get('name', chapter.name)
        chapter.description = data.get('description', chapter.description)

        db.session.commit()

        return {'message': 'chapter updated successfully'}, 200
      
class DeleteChapterAPI(Resource):
    def delete(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {'message': 'Chapter Not Found'}, 404
        
        quizzes = Quiz.query.filter_by(chap_id=chapter.chapter_id).all()
        for quiz in quizzes:
            Question.query.filter_by(quiz_id=quiz.Quiz_id).delete()
            Scores.query.filter_by(quiz_id=quiz.Quiz_id).delete()
            db.session.delete(quiz)
        db.session.delete(chapter)
     
        db.session.commit()
        return{'message': 'Chapter and all other related information are deleted.'}, 200

class QuizAPI(Resource):
    def get(self):
        quizzes = Quiz.query.all()
        qlist=[]
        for quiz in quizzes:
            qlist.append({
                'Quiz_id': quiz.Quiz_id,
                'chap_id': quiz.chap_id,
                'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d'),
                'time_duration': quiz.time_duration
            })
        return {'quizzes': qlist}, 200

class AddQuizAPI(Resource):
    def post(self):
        credential = request.get_json()

        if not credential:
            result = {
                'message': 'All credentials are required.'
            }
            return make_response(jsonify(result), 400)
        
        chapter_id = credential.get('chapter_id', None)
        date_of_quiz = credential.get('date_of_quiz', None)
        doq=datetime.strptime(date_of_quiz,'%Y-%m-%d').date()
        time_duration = credential.get('time_duration', None)
        remarks = credential.get('remarks', None)
        
        if not chapter_id or not doq or not time_duration or not remarks:
            result = {
                'message': 'All the credentials are required.'
            }
            return make_response(jsonify(result), 409)
        
        addquiz = Quiz(
            chap_id = chapter_id,
            date_of_quiz = doq,
            time_duration = time_duration,
            remarks = remarks
        )
        db.session.add(addquiz)
        db.session.commit()

        response = {
            'message': 'Quiz Added Successfully!'
            }
        return make_response(jsonify(response), 201)
    
class EditQuizAPI(Resource):
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        return {
            'quiz_id': quiz.Quiz_id,
            'chap_id': quiz.chap_id,
            'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d'),
            'time_duration': quiz.time_duration,
            'remarks': quiz.remarks
        }, 200
    
    def put(self,quiz_id):
        data = request.get_json()
        quiz= Quiz.query.get(quiz_id)
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        quiz.chap_id = data.get('chap_id',quiz.chap_id)
        quiz.date_of_quiz = datetime.strptime(data.get('date_of_quiz',quiz.date_of_quiz.strftime("%Y-%m-%d")),'%Y-%m-%d').date()
        quiz.time_duration = data.get('time_duration',quiz.time_duration)
        quiz.remarks = data.get('remarks',quiz.remarks)
        db.session.commit()
        return {'message': "Quiz updated successfully"}, 200

class DeleteQuizAPI(Resource):
    def delete(self,quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {'message': 'Quiz not found'},404
        scores = Scores.query.filter_by(quiz_id = quiz_id).all()
        for i in scores:
            db.session.delete(i)
        questions = Question.query.filter_by(quiz_id = quiz_id).all()
        for j in questions:
            db.session.delete(j)
       
        db.session.delete(quiz)
        db.session.commit()
        response = {
            'message': 'Quiz deleted Successfully!'
            }
        return make_response(jsonify(response), 201)
   
class QuestionAPI(Resource):
    def get(self):
        questions = Question.query.all()
        queslist = []
        for q in questions:
            queslist.append({
                'question_id': q.question_id,
                'quiz_id': q.quiz_id,
                'Question_title': q.Question_title
            })
        return {'questions': queslist}, 200

class AddQuestionAPI(Resource):
    def post(self, quiz_id):
        credential = request.get_json()

        if not credential:
            result = {
                'message': 'All credentials are required.'
            }
            return make_response(jsonify(result), 400)
        
        question_title = credential.get('question_title', None)
        question_statement = credential.get('question_statement', None)
        option_a = credential.get('option_a', None)
        option_b = credential.get('option_b', None)
        option_c = credential.get('option_c', None)
        option_d = credential.get('option_d', None)
        answer = credential.get('answer', None)
        answer_text = credential.get(answer)
        if not question_title or not question_statement or not option_a or not option_b or not option_c or not option_d or not answer:
            result = {
                'message': 'All the credentials are required.'
            }
            return make_response(jsonify(result), 409)
        
        addques = Question(
            quiz_id = quiz_id,
            Question_title = question_title,
            Question_statement = question_statement,
            option_a = option_a,
            option_b = option_b,
            option_c = option_c,
            option_d = option_d,
            answer = answer_text
        )
        db.session.add(addques)
        db.session.commit()

        response = {
            'message': 'Question Added Successfully!'
            }
        return make_response(jsonify(response), 201)

class EditQuestionAPI(Resource):
    def get(self, question_id):
        ques = Question.query.get(question_id)
        if not ques:
            return {'message': 'Question not found'}, 404
        return {
            'question_id': ques.question_id,
            'Question_title': ques.Question_title,
            'Question_statement': ques.Question_statement,
            "option_a": ques.option_a,
            "option_b": ques.option_b,
            "option_c": ques.option_c,
            "option_d": ques.option_d,
            "answer": ques.answer

        }, 200
    
    def put(self,question_id):
        data = request.get_json()
        ques= Question.query.get(question_id)
        if not ques:
            return {'message': 'Question not found'}, 404
        Question_title = data.get('Question_title', None)
        Question_statement = data.get('Question_statement', None)
        option_a = data.get('option_a', None)
        option_b = data.get('option_b', None)
        option_c = data.get('option_c', None)
        option_d = data.get('option_d', None)
        answer_key = data.get('answer')
        
        answer_text = data.get(answer_key)
        if not answer_text:
            return {'message': 'Invalid answer'}, 404
        ques.question_id = question_id
        ques.Question_title = Question_title
        ques.Question_statement = Question_statement
        ques.option_a = option_a
        ques.option_b = option_b
        ques.option_c = option_c
        ques.option_d = option_d
        ques.answer = answer_text

        db.session.commit()
        return {'message': "Question updated successfully"}, 200
    
class DeleteQuestionAPI(Resource):
    def delete(self, question_id):
        question = Question.query.get(question_id)
        if not question:
            return make_response(jsonify({'message': 'Question does not exist'}), 404)
        db.session.delete(question)
        db.session.commit()
        response = {
            'message': 'Question deleted Successfully!'
            }
        return make_response(jsonify(response), 201)

class SearchAPI(Resource):
    def get(self):
        search_term = request.args.get('search', '').strip()
        key = request.args.get('key','').strip()

        if not search_term or not key:
            return make_response(jsonify({
                'message': 'Both search term and key are required',
                'results': []
            }),400)
        
        results=[]
        like_pattern = '%' + search_term + '%'

        if key == 'user':
            users = User.query.filter(
                (User.name.ilike(like_pattern)) |
                (User.email.ilike(like_pattern))
            ).all()

            for u in users:
                results.append({
                    'name': u.name,
                    'email': u.email,
                    'qualification': u.qualifications,
                    'DOB': str(u.DOB)
                })
        
        elif key == 'subject':
            subjects = Subject.query.filter(
                Subject.name.ilike(like_pattern)
            ).all()

            for s in subjects:
                results.append({
                    'name': s.name,
                    'description': s.description
                })
        
        elif key == 'quiz':
            chapters = Chapter.query.filter(
                Chapter.name.ilike(like_pattern)
            ).all()
            chapter_ids = [ch.chapter_id for ch in chapters]

            quizzes = Quiz.query.filter(
                (Quiz.chap_id.in_(chapter_ids)) 
            ).all()

            for q in quizzes:
                chapter = Chapter.query.filter_by(chapter_id=q.chap_id).first()
                results.append({
                    'quiz_id': q.Quiz_id,
                    'chapter': chapter.name if chapter else 'N/A',
                    'date': str(q.date_of_quiz),
                    'remarks': q.remarks or ''
                })
        else:
            return make_response(jsonify({
                'message':'Invalid search key',
                'results': []
            }), 400)
        return make_response(jsonify({
                'message':'search complete',
                'results': results
            }), 200)