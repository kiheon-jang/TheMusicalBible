# -*- coding:utf-8 -*-

import os
import time
from http.cookies import SimpleCookie
from threading import Thread

import requests

from utils import COMMON_HEADERS


class SunoCookie:
    def __init__(self):
        self.cookie = SimpleCookie()
        self.session_id = None
        self.token = None

    def load_cookie(self, cookie_str):
        self.cookie.load(cookie_str)

    def get_cookie(self):
        return ";".join([f"{i}={self.cookie.get(i).value}" for i in self.cookie.keys()])

    def set_session_id(self, session_id):
        self.session_id = session_id

    def get_session_id(self):
        return self.session_id

    def get_token(self):
        return self.token

    def set_token(self, token: str):
        self.token = token


suno_auth = SunoCookie()
_session_id = os.getenv("SESSION_ID")
_cookie = os.getenv("COOKIE")
if _session_id:
    suno_auth.set_session_id(_session_id)
if _cookie and isinstance(_cookie, str) and _cookie.strip():
    try:
        suno_auth.load_cookie(_cookie.strip())
        # PATCH: Use __session cookie as initial token if available
        if "__session" in suno_auth.cookie:
            suno_auth.set_token(suno_auth.cookie["__session"].value)
            print(f"Loaded initial token from __session cookie: {suno_auth.token[:20]}...")
    except Exception as e:
        print(f"Failed to load cookie: {e}")


def update_token(suno_cookie: SunoCookie):
    session_id = suno_cookie.get_session_id()
    if not session_id:
        return
    try:
        cookie_str = suno_cookie.get_cookie()
    except Exception:
        return
    headers = {"cookie": cookie_str}
    headers.update(COMMON_HEADERS)

    resp = requests.post(
        url=f"https://clerk.suno.com/v1/client/sessions/{session_id}/tokens?_clerk_js_version=4.72.0-snapshot.vc141245",
        headers=headers,
    )

    resp_headers = dict(resp.headers)
    set_cookie = resp_headers.get("Set-Cookie")
    suno_cookie.load_cookie(set_cookie)
    token = resp.json().get("jwt")
    suno_cookie.set_token(token)
    # print(set_cookie)
    # print(f"*** token -> {token} ***")


def keep_alive(suno_cookie: SunoCookie):
    while True:
        try:
            update_token(suno_cookie)
        except Exception as e:
            print(e)
        finally:
            time.sleep(5)


def start_keep_alive(suno_cookie: SunoCookie):
    t = Thread(target=keep_alive, args=(suno_cookie,))
    t.start()


start_keep_alive(suno_auth)
