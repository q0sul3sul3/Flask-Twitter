from flask import render_template, redirect, url_for, request, abort, flash
from flask_login import login_user, current_user, logout_user, login_required

from twitter.forms import LoginForm, SignupForm, EditProfileForm, TweetForm, ResetPasswordForm
from twitter.models import User, Tweet
from twitter.email import send_email

from twitter import db


@login_required
def index():
	tweets = current_user.own_and_followed_tweets()
	# name = {'username': current_user.username}
	# posts = [
	# 	{
	# 		'author': {'username': 'root'}, 
	# 		'body': "Hi, I'm root", 
	# 	}, 
	# 	{
	# 		'author': {'username': 'root'}, 
	# 		'body': "I am boring", 
	# 	}
	# ]
	form = TweetForm()
	if form.validate_on_submit():
		t = Tweet(body=form.tweet.data, author=current_user)
		db.session.add(t)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('index.html', tweets=tweets, form=form)


def delete_tweet(id):
	tweet = Tweet.query.filter_by(id=id).first()
	# tweet = Tweet.query.get_or_404(id)
	db.session.delete(tweet)
	db.session.commit()
	return redirect(request.referrer) # redirect to previous page


def login():
	if current_user.is_authenticated:
		return redirect('/')
	form = LoginForm(meta={'csrf': False}) # csrf_enabled=False # 它還預設有避免CSRF攻擊的功能，這對資訊安全上有絕對的幫助
	# https://flask-wtf.readthedocs.io/en/1.0.x/form/?highlight=secret
	if form.validate_on_submit(): # 點擊submit則跳轉到index.html
		u = User.query.filter_by(username=form.username.data).first()
		if u is None or not u.check_password(form.password.data):
			# print('invalid username or password') # print in the terminal
			flash('Invalid Username or Password', 'error')
			return redirect('/login')
		login_user(u, remember=form.remember_me.data)
		next_page = request.args.get('next') # logout situation, when log in,it turns to previous page
		# print(next_page)
		if next_page:
			return redirect(next_page)
		return redirect('/')
		# msg = "username={}, password={}, remember_me{}".format(
		# 	form.username.data, form.password.data, form.remember_me.data
		# 	)
		# print(msg)
		# return redirect('/') # redirect() 內建方法
		# return redirect(url_for('index')) # url_for: redirect to index()
	# =====?=====
	# if request.method == 'POST':
		# return render_template('home.html')
	# =====?=====
	return render_template('login.html', title="Sign In", form=form) # title 網頁標題


def logout():
	logout_user()
	return redirect('/login')


def register():
	if current_user.is_authenticated:
		return redirect('/')
	form = SignupForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect('/login')
	return render_template('register.html', title='Sign Up', form=form)


@login_required
def user(username): # different user has different page
	u = User.query.filter_by(username=username).first() # filter_by current user
	if u is None:
		abort(404) # Not Found page

	tweets = u.tweets.order_by(Tweet.create_time.desc())
	# tweets = Tweet.query.filter_by(author=u)
	# posts = [
	# 	{
	# 		'author': {'username': u.username}, 
	# 		'body': "Hi, I'm {}".format(u.username), 
	# 	}
	# ]

	if request.method=='POST':
		# print(request.form.to_dict()) # print in the terminal: {"request_botton": "Follow"}
		if request.form['request_botton']=='Follow':
			current_user.follow(u)
			db.session.commit()
		else:
			current_user.unfollow(u)
			db.session.commit()

	return render_template('user.html', title='Profile', tweets=tweets, user=u)


def page_not_found(e):
	return render_template('404.html'), 404


@login_required # someone who login can reach this page
def edit_profile():
	form = EditProfileForm()
	if request.method == 'GET':
		form.bio.data = current_user.bio
	if request.method == 'POST':
		current_user.bio = form.bio.data
		db.session.commit()
		return redirect(url_for('profile', username=current_user.username))
	return render_template('editprofile.html', form=form) # parameter depends on editprofile.html need


def reset_password():
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			flash(
				"You should soon receive an email allowing you to reset your password. \
				Please make sure to check your spam and trash if you don't find the email."
				,'success')
			send_email(
				subject='Reset Password',
				recipients=['q0sul3sul3@gmail.com'],
				text_body='It seems like you forgot your password for Twitter. \
				If this is true, click the link below to reset your password. \
				Reset my password [link] \
				If you did not forget your password, please disregard this email.',
				html_body='It seems like you forgot your password for Twitter. \
				If this is true, click the link below to reset your password.<br> \
				Reset my password [link]<br> \
				If you did not forget your password, please disregard this email.'
				)
		return redirect('/login')
	return render_template('reset.html', form=form)

@login_required # the one who login can reach this page
def explore():
	tweets = Tweet.query.order_by(Tweet.create_time.desc())
	return render_template('explore.html', tweets=tweets)