from flask import Flask, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db=SQLAlchemy()
DB_NAME = "database.db"

def creat_app():
	app = Flask(__name__)

	app.config['SECRET_KEY']='sadsdsdsdfsdfdgfdfdfg'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	db.init_app(app)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint,url_prefix='/')

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint,url_prefix='/')

	from .db_models import User

	create_database(app)

	login_manager=LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)


	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

	return app

def create_database(app):
    if not path.exists('website/'+ DB_NAME):
        db.create_all(app=app)
        print('Created database')




