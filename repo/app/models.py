from Database import db
from datetime import datetime
# from flask_login import UserMixin

# REMINDER: IF NEED COLUMN IN CHRONOLOGICAL ORDER (SUCH AS POSTS TABLE) MAKE SURE index=TRUE FOR THE NECESSARY COLUMN


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(62), unique=True, nullable=False)
    nickname = db.Column(db.String(50))
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

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
    group = db.Column(db.Integer, db.ForeignKey('Groups.groupId'), nullable=False)
    member = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)

class Posts(db.Model):
    __tablename__ = 'Posts'
    postId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postDateTime = db.Column(db.String(255), nullable=False)
    poster = db.Column(db.Integer, db.ForeignKey('User.id'))
    groupAssociation = db.Column(db.Integer, default=0)
    description = db.Column(db.Text(4096), nullable=False)
    postTags = db.Column(db.String(255))
    postImage = db.Column(db.Text(50000))
    postLikes = db.Column(db.Integer)
    postTitle = db.Column(db.String(255))

class PostLikes(db.Model):
    __tablename__ = 'PostLikes'
    postId = db.Column(db.Integer, db.ForeignKey('Posts.postId'), primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)