from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

from twitter.config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login' # no login, will direct user to login.html
# http://localhost:5000/login?next=%2F # if log out, and click home will visit the site, ?next=%2F last page
mail = Mail()


from twitter.route import index, login, logout, register, user, page_not_found, edit_profile, reset_password, explore, delete_tweet # methods


def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	migrate.init_app(app, db)
	login_manager.init_app(app)
	mail.init_app(app)
	app.add_url_rule('/', 'index', index, methods=['GET', 'POST'])
	app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
	app.add_url_rule('/logout', 'logout', logout)
	app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
	app.add_url_rule('/<username>', 'profile', user, methods=['GET', 'POST']) # Method Not Allowed --> methods=['GET', 'POST']
	app.add_url_rule('/editprofile','editprofile', edit_profile, methods=['GET', 'POST'])
	app.add_url_rule('/reset_password','reset_password', reset_password, methods=['GET', 'POST'])
	app.add_url_rule('/explore','explore', explore)
	app.add_url_rule('/delete/<int:id>','delete_tweet', delete_tweet, methods=['GET', 'POST'])
	app.register_error_handler(404, page_not_found)
	
	# line 20
	# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitter.db' # use SQLite database
	# # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:00000000@localhost:3306/twitter' # mysql://scott:tiger@localhost/mydatabase # dialect+driver://username:password@host:port/database
	# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
	# rebuild to config.py, and the twitter.db will move to twiiter folder(original folder: test)

	# =====
	# app.config["SECRET_KEY"] = '7797bacd231b4753b54ec929d2569695' # RuntimeError: A secret key is required to use CSRF.
	# import uuid
	# uuid.uuid4().hex
	# =====

	app.debug = True 
	return app