# -*- coding: utf-8 -*-
"""
@Time : 2022/4/1 20:58 
@Author : YarnBlue 
@description : 批量修改商品属性
@File : mass_update_goods.py
"""
from RenRen_Shop.api.RenRen_api import RenRenApi
from RenRen_Shop.api.goods.fetch_goods_list import FetchGoodsList
from RenRen_Shop.api.goods.edit_goods import EditGoods


class MassUpdateGoods(RenRenApi):
    def fetcha_goods(self, **kwargs):
        fetcher = FetchGoodsList(self.session, **self.kwargs)
        ids = []
        while fetcher.next(**kwargs):
            for goods in fetcher.result():
                ids.append(goods['id'])
        return ids

    def mash_update_goods(self, *goods_ids, **kwargs):
        Editor = EditGoods(self.session, **self.kwargs)
        for id in goods_ids:
            if Editor.edit_goods_by_first_level(id, **kwargs):
                print(f'商品:{id}批量修改属性：{kwargs.keys()}完成')
            else:
                print(f'商品:{id}修改属性失败')

