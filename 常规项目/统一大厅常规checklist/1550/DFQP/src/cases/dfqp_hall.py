#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
大厅主界面
'''
import time,test_datas
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.game_page import Game_Page
from common.common import Common

class C30982_DFQP_Hall(TestCase):
    '''
    查看大厅主界面信息显示
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.Normal
    timeout = 5
    def pre_test(self):
        self.common = Common()
        #初始化luadriver
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver, "切换环境")
        self.hall_page = Hall_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        time.sleep(3)
        self.hall_page.wait_element("同步标志")
        self.hall_page.screenshot('hall.png')

    def post_test(self):
        self.common.closedriver()

class C30983_DFQP_Hall_Gameinfo(TestCase):
    '''
    查看子游戏内置情况
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver, "切换环境")
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        time.sleep(3)
        self.hall_page.wait_element("同步标志")
        self.start_step("查看大厅游戏入口显示")
        self.game_page.screenshot("1.png")
        self.start_step("进入第二页")
        self.game_page.wait_element("右三角标").click()
        time.sleep(2)
        self.game_page.screenshot("2.png")
        self.start_step("查看更多游戏")
        if (self.game_page.is_exist("更多游戏") == True):
            try:
                self.game_page.wait_element("更多游戏").click()
                time.sleep(3)
            except:
                print "无此按钮"
        self.game_page.screenshot("3.png")


    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

# __qtaf_seq_tests__ = [C30983_DFQP_Hall1]
if __name__ == '__main__':
    # C008_DFQP_Bandding = C008_DFQP_Bandding()
    # C008_DFQP_Bandding.debug_run()
    debug_run_all()