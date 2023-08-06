# -*- coding: utf-8 -*-
"""
@Time : 2022/3/30 14:57 
@Author : YarnBlue 
@description : 
@File : add_goods.py 
"""
import json
import os

import numpy as np

from RenRen_Shop.api.RenRen_api import RenRenApi


class AddGoods(RenRenApi):
    @ staticmethod
    def template(type):
        filepath = os.path.dirname(__file__)
        with open(os.path.join(filepath, f'template/{type}_template.json'), 'rb') as f:
            data = json.load(f)
        return data

    def add_goods(self,
                  goods: dict,  # 商品属性
                  spec: list,  # 多规格
                  options: list,  # 多规格定价
                  goods_commission: dict,  # 分销设置
                  member_level_discount: dict  # 会员折扣信息
                  ) -> bool:
        data = {
            'goods': json.dumps(goods),
            'spec': json.dumps(spec),
            'options': json.dumps(options),
            'goods_commission': json.dumps(goods_commission),
            'member_level_discount': json.dumps(member_level_discount)
        }
        rep = self.session.post(self.URL.add_goods(), data=data)
        if rep.json()['error'] == 0:
            return True
        else:
            return False

    def add_goods_data_for_post(self, **kwargs):
        goods_data: dict = self.template('goods')

        # 更新商品详情信息
        goods_data['title'] = kwargs['title']  # 标题
        goods_data['type'] = int(kwargs['type'])  # 商品类型
        goods_data['sub_title'] = kwargs['sub_title']  # 副标题
        goods_data['short_title'] = kwargs['short_title']  # 短标题
        goods_data['thumb'] = kwargs['thumb']  # 首图
        goods_data['thumb_all'] = kwargs['thumb_all']  # 轮播图
        goods_data['category_id'] = kwargs['category_id']  # 分类
        goods_data['content'] = kwargs['content']  # 详情图
        goods_data['params'] = kwargs['params']  # 参数

        return goods_data


    def add_goods_from_csv(self, file):
        pass

    def add_goods_from_sql(self):
        pass


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)



