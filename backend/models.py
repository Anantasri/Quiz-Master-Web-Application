from backend.database import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Text
from datetime import datetime 

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    email = db.Column(db.String(50), unique = True , nullable = False)
    name = db.Column(db.Text , nullable = False)
    password = db.Column(db.String(250) , nullable = False)
    qualification = db.Column(db.Text , nullable = False)
    DOB = db.Column(db.Date , nullable = False)
    active = db.Column(db.Boolean(), default=True)

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=True)
    
    roles = db.relationship('Role', secondary="user_roles")

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Subject(db.Model):
    __tablename__ = "subject"
    subject_id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    name = db.Column(db.String(250), nullable = False)
    description = db.Column(db.Text, nullable = False)

class Chapter(db.Model):
    __tablename__ = "chapter"
    chapter_id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    subj_id = db.Column(db.Integer , db.ForeignKey('subject.subject_id') , nullable = False)
    name = db.Column(db.String(250), nullable = False)
    description = db.Column(db.Text, nullable = False)
    subject = db.relationship('Subject' , backref = db.backref('chapter' , lazy = True))

class Quiz(db.Model):
    __tablename__ = "quiz"
    Quiz_id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    chap_id = db.Column(db.Integer , db.ForeignKey('chapter.chapter_id') , nullable = False)
    date_of_quiz = db.Column(db.Date, nullable = False)
    time_duration = db.Column(db.Integer, nullable = False)
    remarks = db.Column(db.Text)
    chapter = db.relationship('Chapter' , backref = db.backref('quiz' , lazy = True))

class Question(db.Model):
    __tablename__ = "question"
    question_id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    quiz_id = db.Column(db.Integer , db.ForeignKey('quiz.Quiz_id') , nullable = False)
    Question_title = db.Column(db.String(500), nullable = False)
    Question_statement = db.Column(db.Text , nullable = False)
    option_a = db.Column(db.Text, nullable = False)
    option_b = db.Column(db.Text, nullable = False)
    option_c = db.Column(db.Text, nullable = False)
    option_d = db.Column(db.Text, nullable = False)
    answer = db.Column(db.String, nullable = False)
    quiz = db.relationship('Quiz' , backref = db.backref('question' , lazy = True))

class Scores(db.Model):
    __tablename__ = "scores"
    score_id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    quiz_id = db.Column(db.Integer , db.ForeignKey('quiz.Quiz_id') , nullable = False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.user_id') , nullable = False)
    total_scored = db.Column(db.Integer)
    time_stamp_of_attempt = db.Column(db.DateTime)
    time_taken = db.Column(db.Integer)
    quiz = db.relationship('Quiz' , backref = db.backref('scores' , lazy = True))
    user = db.relationship('User' , backref = db.backref('scores' , lazy = True))

