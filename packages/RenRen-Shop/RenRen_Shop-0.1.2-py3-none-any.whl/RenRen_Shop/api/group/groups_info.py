# -*- coding: utf-8 -*-
"""
@Time : 2022/4/1 20:25 
@Author : YarnBlue 
@description : 
@File : groups_info.py 
"""
from RenRen_Shop.api.RenRen_api import RenRenApi


class GroupsInfo(RenRenApi):
    def groups_info(self, id):
        rep = self.session.get(self.URL.groups_info(), params={'id': id}, **self.kwargs)
        return rep.json()
