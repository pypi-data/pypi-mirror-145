# -*- coding: utf-8 -*-
"""
@Time : 2022/3/30 19:11 
@Author : YarnBlue 
@description : 
@File : category_list.py 
"""
from RenRen_Shop.api.RenRen_api import RenRenApi


class Category(RenRenApi):
    def category_list(self):
        rep = self.session.get(self.URL.category_list())
        return rep.json()
