from flask import Flask
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_envvar('VK_AUDIO_LIST_SETTINGS')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

VK_APP_ID = app.config['VK_APP_ID']
VK_AUTHORIZE_URL = app.config['VK_AUTHORIZE_URL']
VK_APP_SECRET = app.config['VK_APP_SECRET']
VK_API_AUDIO_URL = app.config['VK_API_AUDIO_URL']
UPDATE_TIME = app.config['UPDATE_TIME']
VK_CALLBACK_URL = app.config['VK_CALLBACK_URL']

db = SQLAlchemy(app)

oauth = OAuth()

import app.views

