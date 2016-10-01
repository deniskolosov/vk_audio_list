from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean

from app.application import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(80))
    vk_access_token = db.Column(String(100))
    external_id = db.Column(Integer, unique=True)
    audios = db.relationship('Audio', back_populates='user')

    def __init__(self, username, external_id, vk_access_token):
        self.username = username
        self.external_id = external_id
        self.vk_access_token = vk_access_token

    def __repr__(self):
        return '<User %r>' % self.username


class Audio(db.Model):
    __tablename__ = 'audios'
    id = db.Column(Integer, primary_key=True)
    artist = db.Column(String(80))
    title = db.Column(String(80))
    url = db.Column(String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='audios')

    def __init__(self, title, url, user_id, artist):
        self.artist = artist
        self.title = title
        self.url = url
        self.user_id = user_id

