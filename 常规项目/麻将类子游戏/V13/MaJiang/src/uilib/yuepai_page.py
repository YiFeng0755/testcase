#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#Author: Lucyliu
'''
地方棋牌大厅页面
'''
import time
from appiumcenter.element import Element

from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page


class Yuepai_Page(Element):
    # pass
    def create_room(self, room):
        '''
        创建房间
        '''
        self.yuepai_page = Yuepai_Page()
        time.sleep(6)
        self.yuepai_page.wait_element(room,30).click()
        self.yuepai_page.enter_room()

    def exit_yuepai_page(self):
        '''
        退出约牌房
        '''
        self.yuepai_page = Yuepai_Page()
        try:
            self.yuepai_page.wait_element("菜单键",4).click()
        except:
            print "未点击到菜单键"
        if (self.yuepai_page.element_is_exist("退出键")==False):
            try:
                self.yuepai_page.wait_element("菜单键").click()
            except:
                print "未点击到菜单键"
        self.yuepai_page.wait_element("退出键").click()

    def is_exist_yuepairoom(self):
        '''
        判断是否在房间内
        '''
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        try:
            while self.yuepai_page.element_is_exist("菜单键", 1) or self.yuepai_page.element_is_exist("退出键", 1):
                self.yuepai_page.exit_yuepai_page()
            if self.yuepai_page.element_is_exist("关闭", 2):
                self.yuepai_page.wait_element("关闭", 1).click()
        except:
            print "未进入房间"

    def enter_room(self):
        '''
        点击开房，进去房间
        '''
        self.yuepai_page = Yuepai_Page()
        self.yuepai_page.wait_element('开房',30).click()
        try:
            self.yuepai_page.wait_element('确定').click()
        except:
            print '未找到确定按钮'
        while(self.yuepai_page.element_is_exist("开房")):
            self.yuepai_page.wait_element('开房').click()
        time.sleep(10)

    def play_game(self):
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        while (self.yuepai_page.element_is_exist("准备", 3) == False):
            if self.yuepai_page.element_is_exist("菜单键", 1)==False or self.yuepai_page.element_is_exist("退出键", 1)==False \
                    or self.hall_page.element_is_exist("快速开始")==True:
                break
            else:
                try:
                    self.yuepai_page.wait_element("菜单键").click()
                    self.game_page.wait_element("托管").click()
                except:
                    print "托管失败"
                time.sleep(10)
                while self.yuepai_page.wait_element("换桌1",60) or self.yuepai_page.wait_element("换桌",60):
                    try:
                        self.yuepai_page.wait_element("关闭").click()
                    except:
                        print "等待关闭按钮出现失败"
                    break
