import sched
import threading
import time

import requests

from flask_login import current_user
from flask.helpers import flash


from app import flask_app, db, VK_API_AUDIO_URL, UPDATE_TIME
from app import oauth, login_manager, VK_APP_ID, VK_APP_SECRET, VK_AUTHORIZE_URL
from app.models import User, Audio

vk = oauth.remote_app('vk',
                      consumer_key=VK_APP_ID,
                      consumer_secret=VK_APP_SECRET,
                      base_url='https://oauth.vk.com/',
                      request_token_url=None,
                      access_token_url='https://oauth.vk.com/access_token',
                      access_token_method='GET',
                      authorize_url=VK_AUTHORIZE_URL,
                      content_type='application/json',
                      request_token_params={'scope': 'audio,email',
                                            'display': 'popup'})

scheduler = sched.scheduler(time.time, time.sleep)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@flask_app.cli.command()
def initdb():
    """Creates the database tables."""
    db.create_all()
    print('Initialized the database.')


@flask_app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


def update_user_audio(external_id, vk_access_token):
    print('updating…')
    audios = get_and_save_user_audios(external_id, vk_access_token, create=False)
    user = User.query.filter_by(external_id=external_id).one()
    user_db_audios = Audio.query.filter_by(user_id=user.id)

    if audios:
        for a in audios:
            # adding only audios that are not yet present
            if not user_db_audios.filter_by(title=a.get('title'), artist=a.get('artist')).scalar():
                audio = Audio(title=a.get('title'), artist=a.get('artist'),
                              url=a.get('url'),
                              vk_audio_id=a.get('vk_audio_id'),
                              user_id=user.id)
                db.session.add(audio)
                flash("updated db with %s-%s" % (a.get('artist'), a.get('title')), category='info')

    db.session.commit()
    scheduler.enter(UPDATE_TIME, 1, update_user_audio, (external_id, vk_access_token))
    scheduler.run()


def get_and_save_user_audios(external_id, vk_access_token, create=True):
    params = {'owner_id': external_id,
              'access_token': vk_access_token,
              'count': 30,
              'v': '5.57'}
    resp = requests.get(VK_API_AUDIO_URL, params=params)
    try:
        resp_json = resp.json()
    except ValueError:
        return None

    if 'error' in resp_json:
        return None

    audios = resp_json.get('response').get('items')

    if audios and create:
        for a in audios:
            audio = Audio(artist=a.get('artist'),
                          title=a.get('title'),
                          url=a.get('url'),
                          vk_audio_id=a.get('id'),
                          user_id=current_user.id)
            db.session.add(audio)

        db.session.commit()
        scheduler.enter(UPDATE_TIME, 1, update_user_audio, (external_id, vk_access_token))
        t = threading.Thread(target=scheduler.run, daemon=True)
        t.start()
    return audios
