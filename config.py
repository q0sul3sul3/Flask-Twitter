import os


config_path = os.path.abspath(os.path.dirname(__file__))

class Config:
	# SQLALCHEMY_DATABASE_URI = 'sqlite:///twitter.db' # relative path
	SQLALCHEMY_DATABASE_URI = "sqlite:///"+ os.path.join(config_path, 'twitter.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = '7797bacd231b4753b54ec929d2569695'

	MAIL_DEFAULT_SENDER = 'noreply@twitter.com'
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = 1
	MAIL_USERNAME = 'q0sul3sul3'
	MAIL_PASSWORD = 'pjpsizyykxhwphmt'