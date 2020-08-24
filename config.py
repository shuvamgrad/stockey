import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	SECRET_KEY = 'you-will-can-guess'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	FUNDAMENTAL_ANALYSIS_API_KEY = 'd24e7e69227c6a1966fb4561d996fe88'
	CELERY_BROKER_URL = 'redis://localhost:6379/0'
	CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
	