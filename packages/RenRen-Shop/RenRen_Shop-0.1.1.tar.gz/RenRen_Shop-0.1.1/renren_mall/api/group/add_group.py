# -*- coding: utf-8 -*-
"""
@Time : 2022/4/1 20:04 
@Author : YarnBlue 
@description : 
@File : add_group.py 
"""
from renren_mall.api.RenRen_api import RenRenApi


class AddGroup(RenRenApi):
    def add_group(self, name, status, *goods_ids):
        data = {
            'name': name,
            'status': status
        }
        for index, each in enumerate(goods_ids):
            data[f'goods_id[{index}]'] = each
        self.session.post(self.URL.add_group(), data=data)
