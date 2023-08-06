# -*- coding: utf-8 -*-
"""
@Time : 2022/4/2 13:58 
@Author : YarnBlue 
@description : 
@File : fetch_log_list.py 
"""

from RenRen_Shop.common.fetch import Fetch


class FetchLogList(Fetch):
    def __init__(self, session, **kwargs):
        """
        :param cookie:
        :param session:
        :param session_id:
        :param shop_id:
        :param kwargs:
        """
        super().__init__(session, **kwargs)
        self.first = self.URL.log_list()
        self.Temp = {
            'page': 1,
            'pagesize': 10,
        }
        self.is_end = False
        self.next_page = 1

    def fetch(self, url, **kwargs):
        for index, (key, value) in enumerate(kwargs.items()):
            self.Temp[key] = value
        rep = self.session.get(url, params=self.Temp).json()
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
        if kwargs:
            for index, (key, value) in enumerate(kwargs.items()):
                self.Temp[key] = value
        self.fetch(self.first, **kwargs)

    def next(self, **kwargs):
        """

        :param kwargs: 可接受参数如下：

        =========================
        identify_code: 操作类型，例如 200001: 商品修改

        create_time[1]: 结束时间

        create_time[0]: 开始时间

        name: 关键字，检索操作员用户名

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


