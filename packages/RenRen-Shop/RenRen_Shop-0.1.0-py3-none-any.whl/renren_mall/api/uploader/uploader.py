# -*- coding: utf-8 -*-
"""
@Time : 2022/3/30 11:05 
@Author : YarnBlue 
@description : 
@File : uploader.py 
"""
from abc import ABC

from renren_mall.api.RenRen_api import RenRenApi


class Uploader(ABC, RenRenApi):

    def upload(self, file, from_web=False, **kwargs):
        pass
