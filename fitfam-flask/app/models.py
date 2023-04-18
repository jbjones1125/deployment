from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(62), unique=True, nullable=False)
    nickname = db.Column(db.String(50))
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, entered_password):
        self.password = generate_password_hash(entered_password)

    def check_password(self, entered_password):
        return check_password_hash(self.password, entered_password)

    def __repr__(self):
        return f'<User {self.email}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Profile(db.Model):
    __tablename__ = 'Profile'
    userId = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    AboutMe = db.Column(db.String(255))

class SecurityQuestions(db.Model):
    __tablename__ = 'SecurityQuestions'
    userId = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    Question1 = db.Column(db.String(20))
    Answer1 = db.Column(db.String(255))
    Question2 = db.Column(db.String(20))
    Answer2 = db.Column(db.String(255))

    def __repr__(self):
        return f'<{self.Question1}: {self.Answer1}, {self.Question2}: {self.Answer2}>'

class Groups(db.Model):
    __tablename__ = 'Groups'
    groupId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupName = db.Column(db.String(20), nullable=False)
    groupOwner = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

class GroupMembers(db.Model):
    __tablename__ = 'GroupMembers'
    group = db.Column(db.Integer, db.ForeignKey('Groups.groupId'), primary_key=True, nullable=False)
    member = db.Column(db.Integer, db.ForeignKey('User.id'))

class Posts(db.Model):
    __tablename__ = 'Posts'
    postId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postDateTime = db.Column(db.String(255), nullable=False)
    poster = db.Column(db.Integer, db.ForeignKey('User.id'))
    groupAssociation = db.Column(db.Integer, default=0)
    description = db.Column(db.Text(4096), nullable=False)
    postTags = db.Column(db.String(255))
    postImage = db.Column(db.Text(50000))
    postLikes = db.Column(db.Integer, default=0)
    postTitle = db.Column(db.String(255))

class PostLikes(db.Model):
    __tablename__ = 'PostLikes'
    postId = db.Column(db.Integer, db.ForeignKey('Posts.postId'), primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)