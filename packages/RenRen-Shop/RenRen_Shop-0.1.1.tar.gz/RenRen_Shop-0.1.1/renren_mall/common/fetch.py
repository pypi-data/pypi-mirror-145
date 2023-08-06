# -*- coding: utf-8 -*-
"""
@Time : 2022/4/1 18:35 
@Author : YarnBlue 
@description : 
@File : fetch.py 
"""
from abc import ABC

from renren_mall.api.RenRen_api import RenRenApi


class Fetch(ABC, RenRenApi):
    def __init__(self, session, **kwargs):
        RenRenApi.__init__(self, session, **kwargs)
        self.data = None
        self.is_end = None
        self.is_start = None
        self.next_page = None
        self.previous_page = None
        self.Temp = None
        self.first = None

    def fetch(self, url, **kwargs):
        pass

    def result(self, **kwargs):
        pass

    def next(self, **kwargs):
        pass

    def start(self, **kwargs):
        pass

    def previous(self, **kwargs):
        pass
