#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#Author: Lucyliu
'''
斗地主游戏页面
'''
from appiumcenter.element import Element

from uilib.hall_page import Hall_Page
from uilib.level_page import Level_Page

class Game_Page(Element):

    def exit_game(self,luadriver):
        '''
        退出玩牌房间
        '''
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.hall_page = Hall_Page()
        luadriver.keyevent(4)
        try:
            self.game_page.wait_element("关闭2",1).click()
        except:
            print "未出现破产页面"
        i = 0
        while self.game_page.element_is_exist("退出",1):
            self.game_page.wait_element("退出",2).click()
            try:
                self.hall_page.wait_element("关闭1",2).click()
            except:
                print "未出现破产页面"
            i += 1
            print "点击退出次数：%s" % i
        try:
            i += 1
            self.level_page.wait_element("同步标志",1)
            self.level_page.wait_element("退出场次界面",2).click()
            self.hall_page.wait_element("同步标志",1)
        except:
            print "点击退出次数：%s" % i

    def is_in_gameroom(self,luadriver):
        '''
        玩牌房间内
        '''
        self.game_page = Game_Page()
        while self.game_page.element_is_exist("继续游戏", 1) or self.game_page.element_is_exist("退出",1):
            self.exit_game(luadriver)
