#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/3 18:14
# @Author  : YarnBlue
# @Site    : 
# @File    : login.py
# @Software: PyCharm

import requests
from RenRen_Shop.api.url.url import URL


class Login:
    def __init__(self, username, password, **kwargs):
        self.username = username
        self.password = password
        self.kwargs = kwargs
        self.session = requests.Session()
        self.URL = URL()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/100.0.4896.60 Safari/537.36',
            'client-type': '50'
        }
        self.session_id = None
        self.cookie = None
        self.shop_id = None
        self.session.headers = self.headers
        self.request_session_id()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    def __enter__(self):
        self.login()
        return self

    def request_session_id(self):
        rep = self.session.get(self.URL.get_session_id(), **self.kwargs)
        self.session_id = rep.json()['session_id']
        self.headers['session-id'] = self.session_id
        self.session.headers = self.headers

    def login(self):
        data = {
            'username': self.username,
            'password': self.password
        }
        rep = self.session.post(self.URL.login(), data=data, **self.kwargs)
        if rep.json()['error'] == 0:
            return True

    def logout(self):
        rep = requests.post(self.URL.logout(), headers=self.headers, **self.kwargs)
        if rep.json()['error'] == 0:
            return True
        else:
            return False

