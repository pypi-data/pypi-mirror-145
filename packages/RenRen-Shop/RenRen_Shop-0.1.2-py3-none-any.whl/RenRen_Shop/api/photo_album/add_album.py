# -*- coding: utf-8 -*-
"""
@Time : 2022/3/30 14:26 
@Author : YarnBlue 
@description : 
@File : add_album.py
"""

from RenRen_Shop.api.RenRen_api import RenRenApi


class AddAlbum(RenRenApi):
    def add_album(self, name):
        """
        新增相册
        返回数据格式：
        ================
        {'error': 0, 'id': 496}
        ================

        :param name:
        :return:
        """
        data = {
            'name': name,
            'type': 10
        }
        rep = self.session.post(self.URL.add_album(), data=data)
        return rep.json()
