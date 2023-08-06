# -*- coding: utf-8 -*-
"""
@Time : 2022/4/1 18:39 
@Author : YarnBlue 
@description : 
@File : fetch_goods_list.py 
"""
import time

from RenRen_Shop.common.fetch import Fetch


class FetchGoodsList(Fetch):
    def __init__(self, session, **kwargs):
        """
        start() 启动时可以输入属性值，
        type:商品类型，可以为all, 0, 1, 2, 3, 4


        :param cookie:
        :param session:
        :param session_id:
        :param shop_id:
        :param kwargs:
        """
        super().__init__(session, **kwargs)
        self.first = self.URL.goods_list()
        self.Temp = {
            'type': 'all',
            'status': 1,
            'page': 1,
            'pagesize': 10,
        }
        self.is_end = False
        self.next_page = 1

    def fetch(self, url, **kwargs):
        params = {
            'timestamp': int(time.time() * 1000),
        }
        for index, (key, value) in enumerate(kwargs.items()):
            params[key] = value
        rep = self.session.get(url, params=params).json()
        self.data = rep['list']
        self.next_page = rep['page'] + 1
        self.previous_page = rep['page'] - 1
        if rep['total'] < rep['page_size'] or len(self.data) == 0:
            self.is_end = True
        else:
            self.is_end = False
        if rep['page'] == 1:
            self.is_start = True
        else:
            self.is_start = False

    def start(self, **kwargs):
        """

        :param kwargs: 可接受参数如下：

        =========================
        status: 上下架商品，值为0或1

        keywords: 关键词搜索，接受名称，编码，条码

        label_field: 营销标签，值为 is_hot, is_new, is_recommand

        create_time[]: 开始时间， 时间格式2022-03-28+00:00

        create_time[]: 结束时间， 时间格式2022-03-28+00:00

        category_id[]: 分类搜索，多个分类传入多个category_id[],值为分类id

        type: 类型，值为 all, 0, 1, 2, 3, 4, 5

        audit_status: 审核状态

        sub_shop_name: 子店铺名

        page: 页数

        pagesize: 每页数量大小

        =========================

        :return:
        """
        if kwargs:
            for index, (key, value) in enumerate(kwargs.items()):
                self.Temp[key] = value
        self.fetch(self.first, **kwargs)

    def next(self, **kwargs):
        """

        :param kwargs: 可接受参数如下：

        =========================
        status: 上下架商品，值为0或1

        keywords: 关键词搜索，接受名称，编码，条码

        label_field: 营销标签，值为 is_hot, is_new, is_recommand

        create_time[]: 时间范围，按列表传入 时间格式[2022-03-28+00:00,2022-03-28+00:00],因key包含[],以**kwargs传入

        category_id[]: 分类搜索，多个分类按表格传入，单个分类可以使用参数category_id,因key包含[],以**kwargs传入

        type: 类型，值为 all, 0, 1, 2, 3, 4, 5

        audit_status: 审核状态

        sub_shop_name: 子店铺名

        page: 页数

        pagesize: 每页数量大小

        =========================

        :return:
        """
        if self.is_end:
            return False
        else:
            if kwargs:
                for index, (key, value) in enumerate(kwargs.items()):
                    self.Temp[key] = value
            self.Temp['page'] = self.next_page
            self.fetch(self.first, **self.Temp)
            return True

    def previous(self) -> bool:

        if self.is_start:
            return False
        else:
            self.Temp['page'] = self.previous_page
            self.fetch(self.first, **self.Temp)
            return True

    def result(self):
        return self.data


