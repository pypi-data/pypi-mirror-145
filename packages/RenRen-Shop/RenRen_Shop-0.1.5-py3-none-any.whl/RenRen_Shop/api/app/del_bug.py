# -*- coding: utf-8 -*-
"""
@Time : 2022/4/2 14:43 
@Author : YarnBlue 
@description : 
@File : del_bug.py 
"""
import json
import random
import sys
import time

import requests

from RenRen_Shop.api.app.mass_update_goods import MassUpdateGoods
from RenRen_Shop.api.goods.goods_info import GoodsInfo
from RenRen_Shop.api.goods.edit_goods import EditGoods
from RenRen_Shop.api.app.goods_to_csv import GoodsToCsv


def build_spec_data(dict):
    """
    根据规格及名称对，自动生成符合格式的spec_data

    :param spec_item:
    :return:
    """
    datas = []
    for index, (key, value) in enumerate(dict.items()):
        time.sleep(0.1)
        data = {
            'id': f'spec{int(time.time() * 1000)}',
            'title': key,
            'image_checked': 0
        }
        items = []
        for index, each in enumerate(value):
            items_data = {
                'id': f'childSpec{int(time.time() * 1000) + index + 1}',
                'title': each,
                '_sortId': f'{int(time.time() * 1000) + index + 1}_{random.random()}',
                'specId': data['id'],
                'display_order': index
            }
            items.append(items_data)
        data['items'] = items
        datas.append(data)
    return datas

if __name__ == '__main__':
    client = MassUpdateGoods(COOKIE, requests.Session(), SESSION_ID, SHOP_ID)
    ids = client.fetcha_goods()
    for goods_id in ids:
        print(f'当前goods_id:{goods_id}')
        session = requests.Session()
        Info = GoodsInfo(COOKIE, session, SESSION_ID, SHOP_ID)
        Edit = EditGoods(COOKIE, session, SESSION_ID, SHOP_ID)
        infos = Info.goods_info(goods_id)['data']
        print(f'商品名称为：{infos["title"]}')
        try:
            spec = infos['spec']
        except:
            continue
        if not spec:
            print('需要修改')
        else:
            print('不需要修改')
            continue
        options = infos['options']
        # for option in options:
        #     print(option['title'])
        Spec = {}
        items = []
        for option in options:
            items.append(option['title'])
        Spec['规格'] = items
        data = GoodsToCsv.build_spec_data(Spec)
        # print(json.dumps(data))
        spec_for_options = []
        for item in data[0]['items']:
            spec_for_options.append(item['id'])
        # print(spec_for_options)
        data_source = Edit.form_data(infos)
        data_source['spec'] = data
        for index, option in enumerate(data_source['options']):
            option['specs'] = [spec_for_options[index]]
        if Edit.edit_goods(data_source['goods'],
                           data_source['spec'],
                           data_source['options'],
                           data_source['goods_commission'],
                           data_source['member_level_discount']):
            print('成功')
        else:
            print('失败')
