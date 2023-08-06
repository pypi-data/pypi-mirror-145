# -*- coding: utf-8 -*-
"""
@Time : 2022/4/1 15:00 
@Author : YarnBlue 
@description : 
@File : edit_goods.py 
"""
import json
import random
import time


from renren_mall.api.RenRen_api import RenRenApi
from renren_mall.api.goods.add_goods import AddGoods
from renren_mall.api.goods.goods_info import GoodsInfo
from renren_mall.common.log import log
logger = log().logger


class EditGoods(RenRenApi):
    @staticmethod
    def form_data(infos: dict) -> dict:
        """
        获取到的商品数据，重组数据结构，用于编辑用

        :param infos:
        :return:
        """
        goods_commission = AddGoods.template('goods_commission')
        try:
            options = infos.pop('options')
            for option in options:
                # key_list = ['shop_id', 'sub_shop_id', 'goods_id', 'stock_warning', 'sales', 'display_order']
                # for each in key_list:
                #     option.pop(each)
                option['specs'] = option['specs'].split(',')
                option['tmpid'] = option['id']
        except Exception as e:
            logger.error(f'options错误，{e}')
            options = []
        try:
            spec = infos.pop('spec')
            for each in spec:
                items = each['items']
                for item in items:
                    item['specId'] = item['spec_id']
                    item['_sortId'] = f'{int(time.time()*1000)}_{random.random()}'
        except Exception as e:
            logger.error(f'spec错误，{e}')
            spec = []
        data = {
            'options': options,
            'spec': spec,
            'member_level_discount': {} if 'member_level_discount' not in infos.keys() else infos.pop('member_level_discount'),
            'goods': infos,
            'goods_commission': goods_commission
        }
        return data

    def edit_goods(self,
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
        rep = self.session.post(self.URL.edit_goods(), data=data)
        if rep.json()['error'] == 0:
            return True
        else:
            return False

    def edit_goods_by_first_level(self, id, **kwargs):
        """
        仅支持一级属性修改
        常见修改的一级属性如下：
        ====================
        status: 上下架  0:下架; 1:上架;
        title: 标题
        sub_title: 副标题
        short_title: 短标题
        sub_shop_id: 子门店
        type: 商品类型 0：实体 1：虚拟
        thumb: 首图
        thumb_all: 轮播图 list
        stock: 库存
        sales: 虚拟销量
        real_sales: 真实销量
        price: 价格
        has_option: 是否多规格
        content: 详情图
        dispatch_express: 是否开启快递配送
        dispatch_type: 物流方式 0：包邮 1：默认模板 2：统一运费
        dispatch_id: 快递模板ID
        dispatch_price: 邮费， 统一运费时有效
        dispatch_verify: 是否开启核销,开启后需指定核销点
        is_all_verify: 是否选择所有核销点
        dispatch_verify_point_id: 核销点ID,列表
        dispatch_verify_point_list: 核销点信息，与上一条成对存在，列表
        weight: 重量
        is_recommand: 是否推荐 0或1
        is_hot: 是否热卖
        is_new: 是否新品
        params: 参数，list,格式如：[{'key': '产地', 'value': '大陆'},{},...]
        is_commission: 是否分销
        browse_level_perm: 会员查看权限
        browse_tag_perm: 标签组查看权限
        buy_level_perm: 会员购买权限
        buy_tag_perm: 标签组购买权限
        form_status: 是否插入表单
        form_id: 表单ID
        ====================

        :param id:
        :param kwargs:
        :return:
        """
        get_goods_info = GoodsInfo(self.session,
                                   **self.kwargs)
        goods_infos = get_goods_info.goods_info(id)['data']
        for index, (key, value) in enumerate(kwargs.items()):
            goods_infos[key] = value
        data = self.form_data(goods_infos)
        rep = self.edit_goods(data['goods'],
                              data['spec'],
                              data['options'],
                              data['goods_commission'],
                              data['member_level_discount'])
        if rep:
            return True
        else:
            return False



