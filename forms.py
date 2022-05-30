from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from twitter.models import User


class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()]) # html label: Username
	password = PasswordField("Password", validators=[DataRequired()])
	remember_me = BooleanField("Remember Me")
	submit = SubmitField("Log in")


class SignupForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	email = StringField("Email Address", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	password2 = PasswordField("Comfirm Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
	submit = SubmitField("Sign up")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use different username')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use different email')


class EditProfileForm(FlaskForm):
	bio = TextAreaField("bio", [validators.Length(min=4, max=25)])
	submit = SubmitField("Save")


class TweetForm(FlaskForm):
	tweet = TextAreaField("Tweet", validators=[DataRequired(), validators.Length(min=0, max=140)], render_kw={"placeholder": "What's happening?"})
	submit = SubmitField("Tweet")


class ResetPasswordForm(FlaskForm):
	email = StringField('Email Address', validators=[DataRequired(), Email()])
	submit = SubmitField('Reset Password')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if not user:
			raise ValidationError('You do not have an account for this email')
