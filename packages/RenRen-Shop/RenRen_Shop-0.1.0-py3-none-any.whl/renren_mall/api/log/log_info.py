# -*- coding: utf-8 -*-
"""
@Time : 2022/4/2 14:07 
@Author : YarnBlue 
@description : 
@File : log_info.py
"""

from renren_mall.api.RenRen_api import RenRenApi


class LogInfo(RenRenApi):
    def log_info(self, id):
        rep = self.session.get(self.URL.log_info(), params={'id': id})
        return rep.json()


