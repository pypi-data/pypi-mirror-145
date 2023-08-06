# -*- coding: utf-8 -*-
"""
@Time : 2022/3/30 14:27 
@Author : YarnBlue 
@description : 
@File : RenRen_api.py
"""

from renren_mall.api.url.url import URL


class RenRenApi:
    def __init__(self, session, **kwargs):
        self.session = session
        self.URL = URL()
        self.kwargs = kwargs
