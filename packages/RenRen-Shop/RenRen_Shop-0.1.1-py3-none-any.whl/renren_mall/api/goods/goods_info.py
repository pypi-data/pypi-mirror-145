# -*- coding: utf-8 -*-
"""
@Time : 2022/4/1 14:49 
@Author : YarnBlue 
@description : 
@File : goods_info.py 
"""

from renren_mall.api.RenRen_api import RenRenApi


class GoodsInfo(RenRenApi):
    def goods_info(self, id):
        rep = self.session.get(self.URL.goods_info(), params={'id': id})
        return rep.json()


