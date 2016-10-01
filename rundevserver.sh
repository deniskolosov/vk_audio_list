#!/usr/bin/env bash
DIRECTORY="~/.virtualenvs/vk_audio_list/"
if [ ! -d "$DIRECTORY" ]; then
    echo "Creating virtual environment…"
    pyvenv ~/.virtualenvs/vk_audio_list/
    pip install -r requirements.txt
fi
source "$DIRECTORY""bin/activate"
export VK_AUDIO_LIST_SETTINGS=settings.cfg
export FLASK_APP=app/application.py
rm app/app.db
flask initdb
flask run
