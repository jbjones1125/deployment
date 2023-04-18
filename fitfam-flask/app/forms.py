from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class PostForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    description = TextAreaField('Description:', validators=[DataRequired()])
    tag = SelectField('Choose a Tag:', choices=[
        (None, ''),
        ('back', 'Back'),
        ('chest', 'Chest'),
        ('arms', 'Arms'),
        ('legs', 'Legs'),
        ('back/bicep', 'Back/Bicep'),
        ('chest/tricep', 'Chest/Tricep'),
        ('full body', 'Full Body')])
    img = FileField('image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    #likes = boolean
    submit = SubmitField('Submit')

class GroupPostForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    description = TextAreaField('Description:', validators=[DataRequired()])
    tag = SelectField('Choose a Tag:', choices=[
        (None, ''),
        ('back', 'Back'),
        ('chest', 'Chest'),
        ('arms', 'Arms'),
        ('legs', 'Legs'),
        ('back/bicep', 'Back/Bicep'),
        ('chest/tricep', 'Chest/Tricep'),
        ('full body', 'Full Body')])
    group = SelectField('Choose a Group:', coerce=int, validators=[DataRequired()])
    img = FileField('image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    #likes = boolean
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SignupForm(FlaskForm):
    firstName = StringField('First Name:', validators=[DataRequired()])
    lastName = StringField('Last Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already in use.')

class SecurityQuestionsForm(FlaskForm):
    secQuestion1 = SelectField('Security Question', choices=[
        ('Q1', 'In what city were you born?'),
        ('Q2', 'What is the name of your favorite pet?'),
        ('Q3', 'What is your mother\'s maiden name?'),
        ('Q4', 'What high school did you attend?'),
        ('Q5', 'What was the name of your elementary school?'),
        ('Q6', 'What was the make of your first car?'),
        ('Q7', 'What was your favorite food as a child?'),
        ('Q8', 'Where did you meet yout spouse?'),
        ('Q9', 'What year was your father born?'),
        ('Q10', 'What year was your mother born?')], validators=[DataRequired()])
    answer1 = StringField('Answer to Question 1:', validators=[DataRequired()])
    secQuestion2 = SelectField('Security Question', choices=[
        ('Q1', 'In what city were you born?'),
        ('Q2', 'What is the name of your favorite pet?'),
        ('Q3', 'What is your mother\'s maiden name?'),
        ('Q4', 'What high school did you attend?'),
        ('Q5', 'What was the name of your elementary school?'),
        ('Q6', 'What was the make of your first car?'),
        ('Q7', 'What was your favorite food as a child?'),
        ('Q8', 'Where did you meet yout spouse?'),
        ('Q9', 'What year was your father born?'),
        ('Q10', 'What year was your mother born?')], validators=[DataRequired()])
    answer2 = StringField('Answer to Question 2:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProfileEditForm(FlaskForm):
    nickname = StringField('WHAT DO YOU WANT YOUR NICKNAME TO BE', validators=[DataRequired()])
    aboutme = StringField('WHAT DO YOU WANT IN YOUR ABOUT ME', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SecurityQuestionsCheckForm(FlaskForm):
    answer1 = StringField('ANSWER TO QUESTION 1:', validators=[DataRequired()])
    answer2 = StringField('ANSWER TO QUESTION 2:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ResetPasswordForm(FlaskForm):
    pass1 = PasswordField('PLEASE ENTER YOUR NEW PASSWORD:', validators=[DataRequired()])
    pass2 = PasswordField('RE-ENTER YOUR NEW PASSWORD:', validators=[DataRequired(), EqualTo('pass1')])
    submit = SubmitField('Submit')

class CreateGroupForm(FlaskForm):
    groupName = StringField('Group name:', validators=[DataRequired()])
    submit = SubmitField('Submit')
