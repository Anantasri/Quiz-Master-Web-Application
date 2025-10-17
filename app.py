from flask import Flask
from flask_security import Security
from flask_restful import Api

from backend.database import db
from backend.backend_config import Config 
from backend.user_datastore import user_datastore
from datetime import datetime

from flask_cors import CORS

from flask_mail import Mail
from celery import Celery, Task

mail = Mail()
celery = Celery(__name__, broker='redis://localhost:6379/0',backend='redis://localhost:6379/0')

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:5173", "http://localhost:5000"])
    app.config.from_object(Config)

    db.init_app(app)
    security = Security(app, user_datastore)
    
   
    
    api = Api(app, prefix='/api')

    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin', description='The Quiz Master')
        user_role = user_datastore.find_or_create_role(name='user', description='Regular user')

        if not user_datastore.find_user(email = "quizmaster1502@gmail.com"):
            user_datastore.create_user(
                email = "quizmaster1502@gmail.com",
                name = "Quiz Master",
                password = "admin1234*",
                qualification = "Graduate",
                DOB = datetime.strptime("2005-02-15", "%Y-%m-%d").date(),
                roles = [admin_role]
            )
        db.session.commit()

    return app, api
    
app, api = create_app()

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super().__call__(*args, **kwargs)
celery.Task = ContextTask

from backend.authentication_apis import *

api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI, '/logout')
api.add_resource(RegisterAPI, '/register')
api.add_resource(CheckEmailAPI, '/check-email')

from backend.crud_apis import *
api.add_resource(SubjectAPI, '/subjects')
api.add_resource(AddSubjectAPI, '/add-subject')
api.add_resource(getSubjectAPI, '/subjects/<int:subject_id>')
api.add_resource(EditSubjectAPI, '/edit-subject/<int:subject_id>')
api.add_resource(DeleteSubjectAPI, '/delete-subject/<int:subject_id>')
api.add_resource(ChapterAPI, '/chapters/<int:subject_id>')
api.add_resource(AddChapterAPI, '/add-chapter/<int:subject_id>')
api.add_resource(EditChapterAPI, '/edit-chapter/<int:chapter_id>')
api.add_resource(DeleteChapterAPI, '/delete-chapter/<int:chapter_id>')
api.add_resource(QuizAPI, '/quizzes')
api.add_resource(AddQuizAPI, '/admin/add-quiz')
api.add_resource(EditQuizAPI, '/admin/edit-quiz/<int:quiz_id>')
api.add_resource(DeleteQuizAPI, '/delete-quiz/<int:quiz_id>')
api.add_resource(QuestionAPI, '/questions')
api.add_resource(AddQuestionAPI, '/admin/add-question/<int:quiz_id>')
api.add_resource(EditQuestionAPI, '/admin/edit-question/<int:question_id>')
api.add_resource(DeleteQuestionAPI, '/delete-question/<int:question_id>')

api.add_resource(SearchAPI, '/admin/search')

from backend.summary_apis import SummaryAPI
api.add_resource(SummaryAPI, '/summary')

from backend.user_apis import *
api.add_resource(AllChaptersAPI, '/chapters')
api.add_resource(UpcomingQuizAPI, '/upcoming-quizzes')
api.add_resource(UserViewQuizAPI, '/quiz-details/<int:quiz_id>')
api.add_resource(QuizAttemptAPI, '/attempt-quiz/<int:quiz_id>')
api.add_resource(SubmitQuizAPI, '/submit-quiz/<int:quiz_id>')
api.add_resource(UserScoresAPI, '/user/scores')

if __name__ == '__main__':
    app.run(debug=True)
