# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : customVar.py
# Time       ：22/3/10 15:26
# Author     ：Lex
# email      : 2983997560@qq.com
# Description：自定义数据类型
"""
import time
from .dmE import DmE
from random import uniform
import win32com.client


class CustomE:
    def __init__(self):
        super(CustomE, self).__init__()
        self.__dm = DmE()
        self.thread = None
        self.hwnd = None
        self.title = None
        self.account = None
        self.password = None
        self.service = None
        self.task_list = None
        self.progress = None

    @property
    def dm(self):
        return self.__dm
