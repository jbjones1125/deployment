from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from sqlalchemy import desc
import os


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    posts = db.session.query(User, Posts).join(User).order_by(desc(Posts.postId))
    return render_template("home.html", title='Home', posts=posts)

@app.route('/post/<string:previousPage>', methods=['GET', 'POST'])
@login_required
def post(previousPage):
    form = PostForm()
    if form.validate_on_submit():
        if form.img.data:   # post with image
            filename = secure_filename(form.img.data.filename)
            destination = f'app/static/uploads/{current_user.id}/'
            filepath = destination + filename
            try:
                os.makedirs(destination)
            except FileExistsError:
                pass
            form.img.data.save(filepath)
            newPost = Posts(poster=current_user.id, postDateTime=datetime.today().strftime('%Y-%m-%d'),
                postTitle=form.title.data, description=form.description.data, postTags=form.tag.data, postImage=f'/static/uploads/{current_user.id}/{filename}')
        else:             # post without image
            newPost = Posts(poster=current_user.id, postDateTime=datetime.today().strftime('%Y-%m-%d'),
                postTitle=form.title.data, description=form.description.data, postTags=form.tag.data)
        db.session.add(newPost)
        db.session.commit()
        if previousPage[0] == 'p':
            previousPage = previousPage.split('-')
            return redirect(url_for(previousPage[0], userId = int(previousPage[1])))
        return redirect(url_for(previousPage))
    return render_template('post.html', title='new post', form=form)

@app.route('/grouppost/<string:previousPage>', methods=['GET', 'POST'])
@login_required
def grouppost(previousPage):
    form = GroupPostForm()
    usr = current_user.id
    form.group.choices = [(g.groupId, g.groupName) for g in db.session.query(Groups).join(GroupMembers, GroupMembers.group == Groups.groupId).filter_by(member = usr).all()]
    if form.validate_on_submit():
        if form.img.data:   # post with image
            filename = secure_filename(form.img.data.filename)
            destination = f'app/static/uploads/{current_user.id}/'
            filepath = destination + filename
            try:
                os.makedirs(destination)
            except FileExistsError:
                pass
            form.img.data.save(filepath)
            newPost = Posts(poster=current_user.id, postDateTime=datetime.today().strftime('%Y-%m-%d'),
                postTitle=form.title.data, groupAssociation=form.group.data, description=form.description.data, postTags=form.tag.data, postImage=f'/static/uploads/{current_user.id}/{filename}')
        else:             # post without image
            newPost = Posts(poster=current_user.id, postDateTime=datetime.today().strftime('%Y-%m-%d'),
                postTitle=form.title.data, groupAssociation=form.group.data, description=form.description.data, postTags=form.tag.data)
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for(previousPage))
    return render_template('grouppost.html', title='new post', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(firstName=form.firstName.data, lastName=form.lastName.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        profile = Profile(userId=current_user.id)
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('securityQuestions'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/security_questions', methods=['GET', 'POST'])
def securityQuestions():
    form = SecurityQuestionsForm(secQuestion2 = "Q2")
    if form.validate_on_submit():
        try:
            securityQuestions = SecurityQuestions(userId=current_user.id, Question1=form.secQuestion1.data,
                                Answer1=form.answer1.data, Question2=form.secQuestion2.data, Answer2=form.answer2.data)
            db.session.add(securityQuestions)
            db.session.commit()
        except:
            db.session.rollback()
            return redirect(url_for('profile', userId=current_user.id))
        return redirect(url_for('home'))
    return render_template('security_questions.html', title='Security Questions', form=form)

@app.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    members = db.session.query(Groups).join(GroupMembers, GroupMembers.group == Groups.groupId).filter_by(member = current_user.id).all()
    if members:
        posts = db.session.query(User, Posts, Groups).join(User, User.id == Posts.poster).join(Groups, Groups.groupId == Posts.groupAssociation).filter(Groups.groupId == members[0].groupId).order_by(desc(Posts.postId)).all()
    else: posts = []
    return render_template("groups.html", title='Groups', posts=posts, members=members)

@app.route('/group', methods=['GET', 'POST'])
@login_required
def group():
    groupId = request.form["groupId"]
    members = db.session.query(Groups).join(GroupMembers, GroupMembers.group == Groups.groupId).filter_by(member = current_user.id).all()
    posts = db.session.query(User, Posts, Groups).join(User, User.id == Posts.poster).join(Groups, Groups.groupId == Posts.groupAssociation).filter(Groups.groupId == groupId).order_by(desc(Posts.postId)).all() 
    return render_template("groupFeed.html", title='Groups', posts=posts, members=members)

@app.route('/createGroup', methods=['GET', 'POST'])
@login_required
def createGroup():
    form = CreateGroupForm()
    if form.validate_on_submit():
        groupName = form.groupName.data
        group = Groups(groupName=groupName, groupOwner=current_user.id)
        db.session.add(group)
        db.session.commit()
        group = Groups.query.filter_by(groupOwner=current_user.id).order_by(desc(Groups.groupId)).first()
        groupMember = GroupMembers(group=group.groupId, member=current_user.id)
        db.session.add(groupMember)
        db.session.commit()
        return redirect(url_for('groups'))
    return render_template("createGroup.html", title='Create Group', form=form)

@app.route('/profile/<int:userId>', methods=['GET', 'POST'])
@login_required
def profile(userId):
    posts = db.session.query(User, Posts).join(User).order_by(desc(Posts.postId))
    profile = User.query.filter_by(id = userId).first()
    bio = Profile.query.filter_by(userId = userId).first()
    return render_template("profile.html", title='Profile', posts=posts, profile = profile, bio = bio.AboutMe)

@app.route('/profileEdit', methods=['GET', 'POST'])
@login_required
def profileEdit():
    form = ProfileEditForm()
    if form.validate_on_submit():
        profile = Profile.query.filter_by(userId = current_user.id).first()
        current_user.nickname = form.nickname.data
        profile.AboutMe = form.aboutme.data
        db.session.commit()
        return redirect(url_for('profile', userId=current_user.id))
    return render_template("profileEdit.html", title='Edit Profile', form=form)

@app.route('/securityQuestionsCheck', methods=['GET', 'POST'])
@login_required
def securityQuestionsCheck():
    form = SecurityQuestionsCheckForm()
    if form.validate_on_submit():
        questions = SecurityQuestions.query.filter_by(userId = current_user.id).first()
        if questions.Answer1 == form.answer1.data and questions.Answer2 == form.answer2.data:
            return redirect(url_for('resetPassword'))
        return redirect(url_for('securityQuestionsCheck'))
    return render_template("securityQuestionsCheck.html", title='Reset Password', form=form)

@app.route('/resetPassword', methods=['GET', 'POST'])
@login_required
def resetPassword():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.password =  form.pass1.data
        db.session.commit()
        return redirect(url_for('profile', userId=current_user.id))
    return render_template("resetPassword.html", title='Reset Password', form=form)

@app.route('/like', methods=['GET', 'POST'])
@login_required
def like():
    postId = request.form["postId"]
    liked = db.session.query(PostLikes).filter_by(postId = postId, userId = current_user.id).first()
    post = Posts.query.filter_by(postId = postId).first()
    
    if not liked:
        post.postLikes += 1
        newLike = PostLikes(postId=postId, userId=current_user.id)
        db.session.add(newLike)
        db.session.commit()
    else:
        db.session.delete(liked)
        post.postLikes -= 1
        db.session.commit()
    # likes might not update if someone else likes unless page is refreshed?
    return f'<p id="post{post.postId}" class="numLikes">{ post.postLikes }</p>'

@app.route('/delete', methods=['POST'])
@login_required
def delete():
    postId = request.form["postId"]
    post = Posts.query.filter_by(postId = postId).first()
    if current_user.id == post.poster:
        db.session.delete(post)
        db.session.commit()
    return ""

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    posts = db.session.query(User, Posts).join(User).order_by(desc(Posts.postId))
    return render_template("search.html", title='Search', posts=posts)

@app.route('/searchFeed', methods=['GET', 'POST'])
@login_required
def searchFeed():
    tags = request.form.getlist('tag')
    posts = db.session.query(User, Posts).join(User).order_by(desc(Posts.postId))
    if tags:
        return render_template("searchFeed.html", title='Search', posts=posts, tags=tags)
    return render_template("searchFeed.html", title='Search', posts=posts, tags=['arms', 'back', 'back/bicep', 'chest', 'chest/tricep', 'legs', 'full body', 'None'])