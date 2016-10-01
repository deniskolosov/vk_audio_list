from flask_login import current_user, login_user, login_required, logout_user
from flask import flash, redirect, render_template, url_for

from app import flask_app, VK_CALLBACK_URL
from app.application import db, get_and_save_user_audios, vk
from app.models import User


@flask_app.route('/')
def index():
    print('he')
    audios = None
    if current_user.is_authenticated:
        audios = User.query.get(current_user.id).audios
        if not audios:
            audios = get_and_save_user_audios(current_user.external_id, current_user.vk_access_token)
    return render_template('index.html', audios=audios)


@flask_app.route('/login')
def login():
    return vk.authorize(callback=VK_CALLBACK_URL)


@flask_app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@flask_app.route('/vk')
def vk_authorized():
    next_url = url_for('index')
    resp = vk.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.', category="info")
        return redirect(next_url)
    user = User.query.filter_by(external_id=resp.get('user_id')).scalar()
    if not user:
        username = resp.get('email', 'john@foo.bar').split('@')[0]
        user = User(username=username, external_id=resp.get('user_id', 42), vk_access_token=resp['access_token'])
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(next_url)

