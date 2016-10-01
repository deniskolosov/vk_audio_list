from flask import Flask
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__)
flask_app.config.from_envvar('VK_AUDIO_LIST_SETTINGS')

login_manager = LoginManager()
login_manager.init_app(flask_app)
login_manager.login_view = "login"

VK_APP_ID = flask_app.config['VK_APP_ID']
VK_AUTHORIZE_URL = flask_app.config['VK_AUTHORIZE_URL']
VK_APP_SECRET = flask_app.config['VK_APP_SECRET']
VK_API_AUDIO_URL = flask_app.config['VK_API_AUDIO_URL']
UPDATE_TIME = flask_app.config['UPDATE_TIME']
VK_CALLBACK_URL = flask_app.config['VK_CALLBACK_URL']

db = SQLAlchemy(flask_app)

oauth = OAuth()

import app.views

