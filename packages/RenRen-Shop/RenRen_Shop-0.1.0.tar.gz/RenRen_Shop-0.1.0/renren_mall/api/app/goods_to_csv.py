# -*- coding: utf-8 -*-
"""
@Time : 2022/3/30 16:50 
@Author : YarnBlue 
@description : 
@File : goods_to_csv.py 
"""
import json
import random
import re
import time

import pandas as pd
from itertools import product

from pymysql import escape_string

from renren_mall.common.conDB import connection_db
from renren_mall.api.goods.add_goods import AddGoods
from renren_mall.api.uploader.img_uploader import ImgUploader
from renren_mall.api.photo_album.add_album import AddAlbum


class GoodsToCsv:
    def __init__(self):
        self.host = ''
        self.database = ''
        self.user = ''
        self.password = ''
        self.db = connection_db(self.host, self.database, self.user, self.password)

    def goods_to_csv(self):
        """
        数据库商品数据导出到csv

        :return:
        """
        db = self.db.db()
        cursor = db.cursor()
        sql = '''SELECT id,title,type,subtitle as sub_title, shorttitle as short_title, thumb,thumb_url as thumb_all, 
        pcate as category_id,content 
        FROM ims_ewei_shop_goods 
        WHERE uniacid=6'''
        cursor.execute(sql)
        raws = cursor.fetchall()
        return pd.DataFrame(raws, columns=['id', 'title', 'type', 'sub_title', 'short_title', 'thumb', 'thumb_all',
                                           'category_id', 'content'])

    def get_spec(self, goods_id) -> dict:
        """
        根据商品id 获取规格及对应规格名称

        :param goods_id:
        :return:
        """
        db = self.db.db()
        cursor = db.cursor()
        sql = f'select title, content from ims_ewei_shop_goods_spec where goodsid="{goods_id}" order by displayorder'
        try:
            cursor.execute(sql)
            raws = cursor.fetchall()
        finally:
            db.close()
        Dict = {}
        for i in range(len(raws)):
            title = raws[i][0]
            spec_ids = re.findall('"(\d+)"', raws[i][1])
            item = self.get_spec_item(spec_ids)
            Dict[title] = item
        return Dict

    @staticmethod
    def build_spec_data(spec_item: get_spec):
        """
        根据规格及名称对，自动生成符合格式的spec_data

        :param spec_item:
        :return:
        """
        datas = []
        for index, (key, value) in enumerate(spec_item.items()):
            time.sleep(0.1)
            data = {
                'id': f'spec{int(time.time()*1000)}',
                'title': key,
                'image_checked': 0
            }
            items = []
            for index, each in enumerate(value):
                items_data = {
                    'id': f'childSpec{int(time.time()*1000) + index + 1}',
                    'title': each,
                    '_sortId': f'{int(time.time()*1000)+ index + 1}_{random.random()}',
                    'specId': data['id'],
                    'display_order': index
                }
                items.append(items_data)
            data['items'] = items
            datas.append(data)
        return datas

    def get_spec_item(self, ids: list) -> list:
        """
        根据规格id,获取下属的名称列表

        :param ids:
        :return:
        """
        db = self.db.db()
        try:
            cursor = db.cursor()
            raws = []
            for id in ids:
                sql = f'select id,title from ims_ewei_shop_goods_spec_item where id="{id}"'
                cursor.execute(sql)
                raw = cursor.fetchone()
                raws.append(raw[1])
        finally:
            db.close()
        return raws

    def get_options(self, spec_data: build_spec_data):
        """
        获取规格组合后的sku列表，返回迭代器

        :param spec_data:
        :return:
        """
        datas = []
        for data in spec_data:
            items = data['items']
            childspecs = []
            for item in items:
                childspecs.append({item['id']: item['title']})
            if childspecs:
                datas.append(childspecs)
            datas = sorted(datas, key=lambda Len: len(Len))
        return self.Iter(*datas)

    def fetch_options_infos(self, title) -> dict:
        """
        获取sku信息

        :param title:
        :return:
        """

        # print(title)
        db = self.db.db()
        cursor = db.cursor()
        sql = 'select productprice as original_price,marketprice as price,costprice as cost_price,stock,' \
              f'`virtual` as virtual_account_id,weight from ims_ewei_shop_goods_option where title="{escape_string(title)}"'
        try:
            cursor.execute(sql)
            raw = cursor.fetchone()
        finally:
            db.close()
        return {
            'original_price': float(raw[0]),
            'price': float(raw[1]),
            'cost_price': float(raw[2]),
            'stock': raw[3],
            'virtual_account_id': raw[4],
            'weight': raw[5]
        }

    def buidl_options_data(self, options: get_options):
        datas = []
        for index, sku in enumerate(options):
            title = ''
            specs = []
            for i in range(len(sku)):
                title = title + list(sku[i].values())[0] + '+'
                specs.append(list(sku[i].keys())[0])
            title = title.strip('+')
            # if len(sku) > 1:
            #     title = f'{list(sku[0].values())[0]}+{list(sku[1].values())[0]}'
            #     specs = [list(sku[0].keys())[0], list(sku[1].keys())[0]]
            # else:
            #     title = list(sku[0].values())[0]
            #     specs = [list(sku[0].keys())[0]]

            option_infos = self.fetch_options_infos(title)
            data = {
                'thumb': '',
                'price': option_infos['price'],
                'original_price': option_infos['original_price'],
                'cost_price': option_infos['cost_price'],
                'stock': option_infos['stock'],
                'virtual_account_id': option_infos['virtual_account_id'],
                'goods_code': '',
                'bar_code': '0',
                'weight': float(option_infos['weight']),
                'tmpid': f'_tmpID_{index}',
                'title': title,
                'specs': specs
            }
            datas.append(data)
        return datas

    @staticmethod
    def Iter(*params):
        for each in product(*params):
            yield each

    def get_params(self, goods_id):
        """
        根据原数据库商品id返回参数列表

        :param goods_id:
        :return:
        """
        db = self.db.db()
        cursor = db.cursor()
        sql = f'select title,value from ims_ewei_shop_goods_param where goodsid="{goods_id}"'
        try:
            cursor.execute(sql)
            raws = cursor.fetchall()
        finally:
            db.close()
        params = dict(raws)
        datas = []
        for index, (key, value) in enumerate(params.items()):
            data = {
                'key': key,
                'value': value
            }
            datas.append(data)
        return datas

    @staticmethod
    def get_thumb_all(thumb_all_source: str, uploader: ImgUploader, group_id):
        imgs = re.findall('"(.*?)"', thumb_all_source)
        thumb_all = []
        for index, img in enumerate(imgs):
            path = uploader.upload(f'https://wx.hi-bro.club/attachment/{img}',
                                   from_web=True,
                                   type=10,
                                   group_id=group_id,
                                   filename=f'轮播图_{index + 1}')['path']
            thumb_all.append(path)
        return thumb_all

    @staticmethod
    def get_content(content_source: str, uploader: ImgUploader, group_id):
        imgs = re.findall('src="(.*?)"', content_source)
        content = ''
        for index, img in enumerate(imgs):
            path = uploader.upload(f'https://wx.hi-bro.club/attachment/{img}',
                                   from_web=True,
                                   type=10,
                                   group_id=group_id,
                                   filename=f'详情图{index + 1}')['path']
            content = content + f'<img style="width: 100% !important; vertical-align: top;" src="{path}" />'
        content = f'<p>{content}</p>'
        return content



if __name__ == '__main__':
    df = pd.read_csv('goods.csv', encoding='gbk', encoding_errors='ignore')
    for i in range(len(df)):
        session = requests.Session()
        client = GoodsToCsv()
        goods_id = df['id'][i]
        title = df['title'][i]
        type = df['type'][i]
        sub_title = df['sub_title'][i]
        short_title = df['short_title'][i]
        thumb_source = 'https://wx.hi-bro.club/attachment/' + df['thumb'][i]
        Album = AddAlbum(COOKIE, session, SESSION_ID, SHOP_ID)
        group_id = Album.add_album(short_title)['id']
        Uploader = ImgUploader(cookie=COOKIE, session=session, session_id=SESSION_ID, shop_id=SHOP_ID)
        thumb = Uploader.upload(thumb_source, from_web=True, type=10, group_id=group_id, filename='封面图')['path'] # 首图地址
        thumb_all_source = df['thumb_all'][i]
        thumb_all = client.get_thumb_all(thumb_all_source, Uploader, group_id)
        category_id = [int(df['category_id'][i])]
        content_source = df['content'][i]
        content = client.get_content(content_source, Uploader, group_id)
        spec_titles = client.get_spec(goods_id)
        spec_data = GoodsToCsv().build_spec_data(spec_titles)
        Gen = GoodsToCsv().get_options(spec_data)
        options_data = GoodsToCsv().buidl_options_data(Gen)
        params = GoodsToCsv().get_params(goods_id)
        with open('../goods/template/goods_commission_template.json', 'rb') as f:
            goods_commission_data = json.load(f)

        Adder = AddGoods(COOKIE, session, SESSION_ID, SHOP_ID)
        goods_data = Adder.add_goods_data_for_post(title=title,
                                                   type=type,
                                                   sub_title=sub_title,
                                                   short_title=short_title,
                                                   thumb=thumb,
                                                   thumb_all=thumb_all,
                                                   category_id=category_id,
                                                   content=content,
                                                   params=params)
        res = Adder.add_goods(goods_data, spec_data, options_data, goods_commission_data, {})
        if res:
            print('Done!')
        else:
            print('添加失败...')

