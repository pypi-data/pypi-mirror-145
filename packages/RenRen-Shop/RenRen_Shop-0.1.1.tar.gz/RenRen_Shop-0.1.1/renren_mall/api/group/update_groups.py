# -*- coding: utf-8 -*-
"""
@Time : 2022/4/1 20:29 
@Author : YarnBlue 
@description : 
@File : update_groups.py
"""
from renren_mall.api.RenRen_api import RenRenApi
from renren_mall.api.group.groups_info import GroupsInfo
from renren_mall.api.group.fetch_groups_list import FetchGroupsList


class UpdateGroups(RenRenApi):
    def __init__(self, session, shop_id, **kwargs):
        super().__init__(session, **kwargs)
        self.shop_id = shop_id

    def update_groups(self, id=None, name=None, *goods_ids, **kwargs):
        """
        更新商品组信息

        :param id: 商品组id
        :param goods_ids: 内含商品id列表
        :param kwargs: 根据需求传入对应属性值
        :return:
        """
        if id:
            groupsInfo = GroupsInfo(self.session, **self.kwargs)
            name = groupsInfo.groups_info(id)['data']['name']
        if name:
            groupsList = FetchGroupsList(self.session, **self.kwargs)
            groupsList.next(name=name)
            id = groupsList.result()[0]['id']
        data = {
            'id': id,
            'shop_id': 480,
            'status': 1,
            'name': name,
            'desc': '',
            'sort_type': 0,
        }
        for index, value in enumerate(goods_ids):
            data[f'goods_id[{index}]'] = value
        for index, (key, value) in enumerate(kwargs.items()):
            data[key] = value
        rep = self.session.post(self.URL.update_groups(), data=data)
        if rep.json()['error'] == 0:
            return True
        else:
            return False

    def add_goods_to_groups(self, group_id, *goods_id):
        InfoGetter = GroupsInfo(self.session, **self.kwargs)
        inofs = InfoGetter.groups_info(group_id)


