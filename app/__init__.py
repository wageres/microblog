# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from elasticsearch import Elasticsearch
from config import Config


db = SQLAlchemy()
migrate = Migrate()#Механизм миграции

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = "Пожалуйста, войдите, чтобы открыть эту страницу."



mail = Mail()

bootstrap = Bootstrap()

moment = Moment()




#перенаправляет на эту функцию если неавторизированнный пользователь пытается получить доступ
#к странице, где нужна авторизация



def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	app.elasticsearch = (Elasticsearch(app.config['ELASTICSEARCH_URL'])
		if app.config['ELASTICSEARCH_URL'] else None)

	db.init_app(app)
	migrate.init_app(app,db)
	login.init_app(app)
	mail.init_app(app)
	bootstrap.init_app(app)
	moment.init_app(app)

	from app.errors import bp as errors_bp
	app.register_blueprint(errors_bp)

	from app.auth import bp as auth_bp
	app.register_blueprint(auth_bp, url_prefix='/auth')

	from app.main import bp as main_bp
	app.register_blueprint(main_bp)

	if not app.debug and not app.testing:
		if app.config['LOG_TO_STDOUT']:
			stream_handler = logging.StreamHandler()
			stream_handler.setLevel(logging.INFO)
			app.logger.addHandler(stream_handler)
		else:
			if not os.path.exists('logs'):
				os.mkdir('logs')
			file_handler = RotatingFileHandler('logs/flask2.log',maxBytes=10240,
												backupCount=10)
			#Не более 10кб и хранить резервные копии последних 10 копий журнала
			file_handler.setFormatter(logging.Formatter(
				'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
			#Формат сообщений журнала
			file_handler.setLevel(logging.INFO)
			app.logger.addHandler(file_handler)

			app.logger.setLevel(logging.INFO)
			app.logger.info('Microblog startup')	
	return app


from app import models