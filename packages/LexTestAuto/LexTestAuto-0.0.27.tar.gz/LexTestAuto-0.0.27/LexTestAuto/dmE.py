# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : dmE.py
# Time       ：22/3/10 15:42
# Author     ：Lex
# email      : 2983997560@qq.com
# Description：
"""
import ctypes
import os
import time
from random import uniform
import win32com.client


class DmE:
    """ 对象封装 """

    def __init__(self):
        self.__dm_tmp = None

    def register(self):
        path = os.path.split(os.path.realpath(__file__))[0]
        try:
            dm = ctypes.windll.LoadLibrary(path + r'\DmReg.dll')
            dm.SetDllPathW(path + r'\dm.dll', 0)
            return 1
        except Exception as e:
            print("免注册调用失败")
            return

    # 创建大漠对象
    def Create(self):
        try:
            self.__dm_tmp = win32com.client.DispatchEx('dm.dmsoft')
            return 1
        except Exception as e:
            return

    # 取插件版本
    def Ver(self):
        pass

    # VIP 注册
    def RegisterVip(self, reg_code, ver_info):
        return self.__dm_tmp.Reg(reg_code, ver_info)

    # 设置错误开关
    def SetShowErrorMsg(self, show):
        return self.__dm_tmp.SetShowErrorMsg(show)

    # 设置全局路径
    def SetPath(self, path):
        return self.__dm_tmp.SetPath(path)

    # 设置字库
    def SetDict(self, index, file):
        return self.__dm_tmp.SetDict(index, file)

    # 枚举句柄
    def EnumWindow(self, parent, title, class_name, fil):
        return self.__dm_tmp.EnumWindow(parent, title, class_name, fil)

    # 获取句柄
    def GetWindow(self, hwnd, flag):
        return self.__dm_tmp.GetWindow(hwnd, flag)

    # 移动窗口
    def MoveWindow(self, hwnd, x, y):
        return self.__dm_tmp.MoveWindow(hwnd, x, y)

    # 绑定句柄
    def BindWindow(self, hwnd, display, mouse, keypad, mode):
        return self.__dm_tmp.BindWindow(hwnd, display, mouse, keypad, mode)

    # 绑定句柄Ex
    def BindWindowEx(self, hwnd, display, mouse, keypad, public, mode):
        return self.__dm_tmp.BindWindowEx(hwnd, display, mouse, keypad, public, mode)

    # 大漠盾
    def DmGuard(self, enable, Gtype):
        return self.__dm_tmp.DmGuard(enable, Gtype)

    # 设置窗口状态
    def SetWindowState(self, hwnd, flag):
        return self.__dm_tmp.SetWindowState(hwnd, flag)

    # 解绑
    def UnBindWindow(self):
        return self.__dm_tmp.UnBindWindow()

    # 点阵提取
    def FetchWord(self, x1, y1, x2, y2, color, word):
        return self.__dm_tmp.FetchWord(x1, y1, x2, y2, color, word)

    # 卡屏检测
    def IsDisplayDead(self, x1, y1, x2, y2, t):
        return self.__dm_tmp.IsDisplayDead(x1, y1, x2, y2, t)

    # 找图
    def FindPic(self, x1, y1, x2, y2, pic_name, delta_color="050505", sim=0.9, dirt=0):
        return self.__dm_tmp.FindPic(x1, y1, x2, y2, pic_name, delta_color, sim, dirt)

    # 颜色比较
    def CmpColor(self, x, y, color, sim):
        return self.__dm_tmp.CmpColor(x, y, color, sim)

    # 找色
    def FindColor(self, x1, y1, x2, y2, color, sim=0.9, dirt=0):
        return self.__dm_tmp.FindColor(x1, y1, x2, y2, color, sim, dirt)

    # 多点找色
    def FindMultiColor(self, x1, y1, x2, y2, first_color, offset_color, sim=0.9, dirt=0):
        return self.__dm_tmp.FindMultiColor(x1, y1, x2, y2, first_color, offset_color, sim, dirt)

    # 键盘按键
    def KeyPress(self, vk_code):
        return self.__dm_tmp.KeyPress(vk_code)

    # 移动鼠标
    def MoveTo(self, x, y):
        return self.__dm_tmp.MoveTo(x, y)

    # 左键单击
    def LeftClick(self):
        return self.__dm_tmp.LeftClick()

    # 右键单击
    def RightClick(self):
        return self.__dm_tmp.RightClick()

    # 左鼠标按住
    def LeftDown(self):
        return self.__dm_tmp.LeftDown()

    # 左鼠标弹起
    def LeftUp(self):
        return self.__dm_tmp.LeftUp()

    # 发送文本
    def SendString(self, hwnd, content):
        return self.__dm_tmp.SendString(hwnd, content)

    # 发送文本
    def SendString2(self, hwnd, content):
        return self.__dm_tmp.SendString2(hwnd, content)

    # 找图点击
    def FindPic_and_lclick(self, x1, y1, x2, y2, pic_name, time1=0.5, time2=1):
        ret = self.FindPic(x1, y1, x2, y2, pic_name)
        print("ret", ret)
        if ret[0] > -1:
            self.__dm_tmp.MoveTo(ret[1], ret[2])
            time.sleep(uniform(time1, time2))
            self.__dm_tmp.LeftClick()
            return 1

    # 找字
    def FindStrFast(self, x1, y1, x2, y2, string, color_format, sim=0.9):
        return self.__dm_tmp.FindStrFastE(x1, y1, x2, y2, string, color_format, sim).split('|')

    # 找字并点击
    def FindStr_and_lClick(self, x1, y1, x2, y2, string, color_format, sim=0.9):
        ret = self.__dm_tmp.FindStrFastE(x1, y1, x2, y2, string, color_format, sim).split('|')
        if int(ret[0]) == 0:
            self.Move_and_lclick(int(ret[1]), int(ret[2]))
            return 1

    # 识字
    def Ocr(self, x1, y1, x2, y2, color_format, sim=0.9):
        return self.__dm_tmp.Ocr(x1, y1, x2, y2, color_format, sim)

    # 移动并点击
    def Move_and_lclick(self, x1, y1, time1=0.5, time2=1):
        self.__dm_tmp.MoveTo(x1, y1)
        uniform(time1, time2)
        self.__dm_tmp.LeftClick()

    # 移动并右键
    def Move_and_rclick(self, x1, y1, time1=0.5, time2=1):
        self.__dm_tmp.MoveTo(x1, y1)
        uniform(time1, time2)
        self.__dm_tmp.RightClick()

    # 打开地图
    def OpenMap(self, key_num, pic_name):
        for item in range(5):
            dm_ret = self.FindPic(0, 0, 2000, 2000, pic_name, "030303", 0.9, 2)
            if dm_ret[1] > 0:
                time.sleep(0.5)
                return dm_ret
            else:
                self.KeyPress(int(key_num))
                time.sleep(1)

    # 打开背包
    def OpenBag(self, key_num, pic_name):
        for item in range(5):
            dm_ret = self.FindPic(0, 0, 2000, 2000, pic_name, "030303", 0.9, 2)
            if dm_ret[1] > 0:
                time.sleep(0.5)
                return dm_ret
            else:
                self.KeyPress(int(key_num))
                time.sleep(1)

    # 关闭背包
    def CloseBag(self, key_num, pic_name):
        ret = self.__dm_tmp.FindPic(0, 0, 2000, 2000, pic_name, "030303", 0.9, 2)
        if ret[1] > 0:
            self.KeyPress(int(key_num))
            time.sleep(0.2)
