import json
import os
import shutil
import time

import requests

import listener as listener_
from console_tools import clear

url = 'http://127.0.0.1:5000/'
session = requests.session()
screen_now = ''


def update_screen(resp):
    global screen_now
    screen = resp.json()['screen']
    if screen_now != screen:
        clear()
        print(screen)
        screen_now = screen


def on_press(key):
    key_str = str(key)
    columns, rows = shutil.get_terminal_size((80, 20))
    resp = session.post(url, data=json.dumps({'btn': key_str, 'cols': columns, 'rows': rows}))
    update_screen(resp)


def main():
    listener = listener_.get_online_listener(on_press)
    listener.start()
    while True:
        resp = session.get(url)
        update_screen(resp)
        time.sleep(3)


if __name__ == '__main__':
    main()