from flask import Flask, redirect, url_for, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from Database import db
#import mysql.connector
import sqlite3

def register_extensions(app):
    db.init_app(app)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    return app

app = create_app(Config)
migrate = Migrate(app, db)


from models import *    # IMPORT THE MODELS

CORS(app, resources={r'/*':{'origins': '*'}})

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("app.db")
    except sqlite3.error as e:
        print(e)
    return conn

Item2 = []
postObjList = []
retrievalStepSize = 10
feedPosition = 0
targetGroupStr = 0
targetPersonsStr = ""

#target persons assignment will be
#" AND poster = targetPersons"

@app.route("/feedmeta", methods=['GET', 'POST'])
def feedMeta():
    if request.method == 'POST':
        global targetGroupStr
        global targetPersonsStr
        info = request.get_json(silent=True)
        targetGroupStr = info['targetGroupTmp']
        #print("target group is " + targetGroupStr)
        targetPersonsStr = info['targetPersonsTmp']
        #print("targetPersonsStr is '" + targetPersonsStr + "'")
        return "Feed targets set"
    else:
        global postObjList
        global feedPosition
        postObjList = []
        conn = db_connection()
        cursor = conn.cursor()
        cursor = conn.execute(
            'SELECT postId FROM Posts'
        )
        feedPosition = len(cursor.fetchall())
        if feedPosition is None:
            feedPosition = 0
        else:
            feedPosition -= retrievalStepSize
        #print("Feed position set")
        return "Feed position set"

@app.route("/posts", methods=['GET', 'POST'])
def posts():
    global feedPosition
    conn = db_connection()
    cursor = conn.cursor()
    global postObjList
    #print("calls made here")
    tmpFeedPosition = feedPosition
    if feedPosition < 0:
        tmpFeedPosition = 0
    #print(feedPosition)
    #print(tmpFeedPosition)
    cursor = conn.execute(
        f"WITH Posts_Numbered AS (SELECT *, ROW_NUMBER() OVER(ORDER BY _ROWID_) RowNum FROM Posts) \
            SELECT Posts_Numbered.*, User.firstName, User.lastName, User.nickname FROM Posts_Numbered \
         LEFT JOIN User ON Posts_Numbered.poster = User.id WHERE \
         RowNum > {tmpFeedPosition} AND ROWNUM <= {feedPosition+retrievalStepSize} AND \
            groupAssociation = {targetGroupStr+targetPersonsStr}"
    )
    #print("call is finished")
    tmpPostObjList = ([
        dict(
            postId=row[0],
            postDateTime=row[1],
            poster=row[2],
            groupAssociation=row[3],
            description=row[4],
            postTags=(row[5].split(',')),
            postImage=row[6],
            postLikes=row[7],
            #postLikeAssociation,
            postTitle=row[8],
            postRow=row[9],
            postFirstName=row[10],
            postLastName=row[11],
            postNickname=row[12]

            #this data needs to be pulled from key relations in other tables
        )
        for row in cursor.fetchall()
    ])
    tmpPostObjList.reverse()
    postObjList = postObjList + tmpPostObjList
    feedPosition -= retrievalStepSize
    #print(postObjList[0])
    #print(len(postObjList))
    return postObjList

@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return "POST method test."
    else:
        return "This message is a test for backend."

@app.route("/profile" , methods=['GET', 'POST'])
def profile():
    info = request.get_json(silent=True)
    userId = info['userId']
    user = User.query.filter_by(id = userId).first()
    profile = Profile.query.filter_by(userId = user.id).first()
    nickName = user.nickname
    aboutMe = profile.AboutMe
    if aboutMe == None:
        aboutMe = "You have nothing in your about me"
    if nickName == None:
        nickName = "Nickname not set yet"
    firstName = user.firstName
    lastName = user.lastName
    backend = {'nickName': nickName, 'realName' : firstName + ' ' + lastName, 'aboutMe': aboutMe}
    return backend

@app.route("/profileEdit" , methods=['GET', 'POST'])
def profileEdit():
    info = request.get_json(silent=True)
    userId = info['userId']
    user = User.query.filter_by(id = userId).first()
    profile = Profile.query.filter_by(userId = user.id).first()
    if request.method == 'POST':
        nickName = info['nickName']
        aboutMe = info['aboutMe']
        user.nickname = nickName
        profile.AboutMe = aboutMe
        db.session.commit()
        return info
    else:
        nickName = user.nickname
        aboutMe = profile.AboutMe
        if aboutMe == None:
            aboutMe = "You have nothing in your about me"
        if nickName == None:
            nickName = "Nickname not set yet"
        firstName = user.firstName
        lastName = user.lastName
        backend = {'nickName': nickName, 'realName' : firstName + ' ' + lastName, 'aboutMe': aboutMe}
        return backend
    return jsonify("valid"), 200

@app.route("/securityQuestionCheck", methods=['Get','POST'])
def securityQuestionCheck():
    info = request.get_json(silent=True)
    userId = info['userId']
    answerStringA = info['answer1']
    answerStringB = info['answer2']
    user = User.query.filter_by(id = userId).first()
    securityQuestions = SecurityQuestions.query.filter_by(userId = user.id).first()
    backend = {'secQuestion1': securityQuestions.Question1, 'secQuestion2': securityQuestions.Question2}
    if request.method == 'POST':
        if securityQuestions.Answer1 == answerStringA and securityQuestions.Answer2 == answerStringB:
            return jsonify("valid"), 200
        else:
            return jsonify("invalid"), 401
    return backend

@app.route("/resetPassword", methods=['GET','POST'])
def resetPassword():
    info = request.get_json(silent=True)
    userId = info['userId']
    passwordInput1 = info['passwordInput1']
    passwordInput2 = info['passwordInput2']
    user = User.query.filter_by(id = userId).first()
    if user is not None and passwordInput1 == passwordInput2:
        password = generate_password_hash(passwordInput1)
        user.password = password
        db.session.commit()
        return jsonify("valid"), 200
    else:
        return jsonify("invalid"), 401

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        info = request.get_json(silent=True)
        userEmail = info['email']
        userPassword = info['password']
        user = User.query.filter_by(email = userEmail).first()
        if user is None or not check_password_hash(user.password, userPassword):
            return jsonify("invalid"), 401
        return jsonify(user.id), 200


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        info = request.get_json(silent=True)
        first = info['first']
        last = info['last']
        email = info['email']
        password = generate_password_hash(info['password'])
        user = User.query.filter_by(email = email).first()
        if user is None:
            user = User(firstName=first, lastName=last, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(email = email).first()
            securityQuestions = SecurityQuestions(userId = user.id)
            profile = Profile(userId = user.id)
            db.session.add(securityQuestions)
            db.session.add(profile)
            db.session.commit()
        else:
            return jsonify("invalid"), 401
        return jsonify(user.id), 200


@app.route("/security_questions", methods=['POST'])
def securityQuestions():
    info = request.get_json(silent=True)
    questionStringA = info['secQuestion1']
    answerStringA = info['answer1']
    questionStringB = info['secQuestion2']
    answerStringB = info['answer2']
    userId = info['userId']
    user = User.query.filter_by(id = userId).first()
    securityQuestions = SecurityQuestions.query.filter_by(userId = user.id).first()
    #securityQuestions.Question1 = questionStringA
    setattr(securityQuestions,'Question1',questionStringA)
    #securityQuestions.Answer1 = answerStringA
    setattr(securityQuestions,'Answer1',answerStringA)
    #securityQuestions.Question2 = questionStringB
    setattr(securityQuestions,'Question2',questionStringB)
    #securityQuestions.Answer2 = answerStringB
    setattr(securityQuestions,'Answer2',answerStringB)
    db.session.commit()
    print(f"\nSecurity Question 1: {questionStringA} \nanswer1: {answerStringA} \nSecurity question2: {questionStringB} \nAnswer2: {answerStringB}")
    return info

@app.route("/")
def default():
    return redirect(url_for("login"))

@app.route("/post", methods=['GET','POST'])
def post():

    # data is the post data put in jsonified format
    data = request.get_json(force=True)

    postTitle = data['title']
    description = data['description']
    postImage = data.get('imagePath')
    poster = data.get('userId')
    postLikes = 0
    postTags = data.get('tags')
    postImage = data.get('image')

    print(postImage)

    post = Posts(postTitle=postTitle, description=description, postDateTime=datetime.today().strftime('%Y-%m-%d'), postImage=postImage, poster=poster, postLikes=postLikes, postTags=postTags)
    db.session.add(post)
    db.session.commit()

    return "All Good"

@app.route("/like", methods=['GET','POST'])
def like():

    # data is the post data put in jsonified format
    data = request.get_json(force=True)

    # making dict object for post data
    item = {
        'postId': data.get('postId'),
        'postLikes': data.get('postLikes')
    }
    postId = item['postId']
    post = Posts.query.filter_by(postId = postId).first()
    post.postLikes += 1
    db.session.add(post)
    db.session.commit()

    #print(item)
    return item

@app.route("/delete_post", methods=['GET','POST'])
def delete():
    info = request.get_json(force=True)
    postId = info['postId']

    conn = db_connection()
    sql = 'DELETE FROM Posts WHERE postId=?'
    cursor = conn.cursor()
    cursor.execute(sql, (postId,))
    conn.commit()
    return info


@app.route("/groups", methods=['GET', 'POST'])
def groupPage():
    userId=1
    groupList = Groups.query.filter_by(groupId=1).first()
    if groupList is None:
        return ""
    return jsonify(groupList.groupName)

@app.route("/create_group", methods=['GET', 'POST'])
def createGroup():
    info = request.get_json(silent=True)
    userId = 1
    gName = info['groupName']
    group = Groups(groupName=gName, groupOwner=userId)
    db.session.add(group)
    db.session.commit()
    gId = Groups.query.filter_by(groupName = gName).first()
    groupMem = GroupMembers(member=userId, group=gId.groupId)
    db.session.add(groupMem)
    db.session.commit()


    # print(f"\nGroup: {gName}\nCreator: {userId}")

@app.route("/group_post", methods=['GET', 'POST'])
def groupPost():
    info = request.get_json(silent=True)
    userId=1
    groupId=info.get('groupId')
    desc=info.get('description')
    img=info.get('image')
    newPost = Posts(groupAssociation=groupId, poster=userId, description=desc, postImage=img, postLikes=0)
    db.session.add(newPost)
    db.session.commit(newPost)