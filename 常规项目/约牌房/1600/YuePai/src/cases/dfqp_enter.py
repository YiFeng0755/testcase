#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
入口
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.game_page import Game_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common

class C70432_Yuepai_display(TestCase):
    '''
    约牌房开启，游戏选场列表正常显示约牌房入口
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("获取子游戏列表")
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            game_list[i].click()
            self.game_page.game_is_download()
            if (self.game_page.element_is_exist("约牌按钮")==True):
                self.game_page.screenshot("%s.png" %game_list[i].get_attribute("name"))
                self.game_page.wait_element("约牌按钮").click()
                self.start_step("进入约牌房")
                self.game_page.wait_element("返回").click()
                time.sleep(3)
            else:
                self.log_info("无约牌房")
            try:
                self.game_page.wait_element("返回1",20).click()
            except:
                self.log_info("返回失败")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70433_Yuepai_display(TestCase):
    '''
    约牌房关闭，游戏选场列表正常隐藏约牌房入口
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("获取子游戏列表")
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            game_list[i].click()
            self.game_page.game_is_download()
            if (self.game_page.element_is_exist("约牌按钮") == False):
                self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
            else:
                self.log_info("有约牌房")
            try:
                self.game_page.wait_element("返回1", 20).click()
            except:
                self.log_info("返回失败")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

# __qtaf_seq_tests__ = [C70524_Recorddisplay]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
