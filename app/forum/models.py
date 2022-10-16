from unicodedata import category
from app.forum import forum_db, login
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from datetime import datetime


class User(UserMixin,forum_db.Model):
    id = forum_db.Column(forum_db.Integer, primary_key=True)
    username = forum_db.Column(forum_db.String(64), index=True, unique=True)
    name = forum_db.Column(forum_db.String(64), index=True, unique=False)
    surname = forum_db.Column(forum_db.String(64), index=True, unique=False)
    email = forum_db.Column(forum_db.String(120), index=True, unique=True)
    password_hash = forum_db.Column(forum_db.String(128))
    question = forum_db.relationship('Question', backref='author', lazy='dynamic')
    answer = forum_db.relationship('Answer', backref='author', lazy='dynamic')
    last_seen = forum_db.Column(forum_db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Question(forum_db.Model):
    __tablename__ = 'questions'
    id = forum_db.Column(forum_db.Integer, primary_key=True)
    title = forum_db.Column(forum_db.String(120))
    body = forum_db.Column(forum_db.String(280))
    category = forum_db.Column(forum_db.String(20))
    timestamp = forum_db.Column(forum_db.DateTime, index=True, default=datetime.utcnow)
    user_id = forum_db.Column(forum_db.Integer, forum_db.ForeignKey('user.id'))
    answers = forum_db.relationship('Answer', backref='question', lazy='dynamic')
    
    
    def __repr__(self):
        return f'<Question {self.body}>'



class Answer(forum_db.Model):
    __tablename__ = 'answers'
    id = forum_db.Column(forum_db.Integer, primary_key=True)
    title = forum_db.Column(forum_db.String(120))
    body = forum_db.Column(forum_db.String(280))
    timestamp = forum_db.Column(forum_db.DateTime, index=True, default=datetime.utcnow)
    user_id = forum_db.Column(forum_db.Integer, forum_db.ForeignKey('user.id'))
    question_id = forum_db.Column(forum_db.Integer, forum_db.ForeignKey('questions.id'))
    

    def __repr__(self):
        return f'<Answer {self.body}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))