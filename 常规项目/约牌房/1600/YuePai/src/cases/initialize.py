#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
用例初始化
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase

from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from common.common import Common

class Initialize(TestCase):
    '''
    用例初始化
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.hall_page.screenshot(".png")
        self.start_step("获取mid")
        mid = self.common.get_mid()
        self.common.set_config_value("casecfg","mid",str(mid))
        env = self.common.get_config_value('casecfg', 'env')
        if env != "0":
            self.log_info("游戏机器人开关设置为关闭")
            self.start_step("设置第一页的游戏开关")
            gamelist = self.game_page.get_game_list()
            print gamelist
            for i in range(len(gamelist)):
                gamename = gamelist[i].get_attribute("name")
                gameid = filter(lambda ch: ch in '0123456789', gamename)
                print gameid
                self.game_page.set_robot(gameid=gameid)
            self.start_step("点击大厅第二页")
            if (self.game_page.element_is_exist("右三角标") == True):
                self.game_page.wait_element("右三角标").click()
            else:
                self.game_page.wait_element("左三角标").click()
            self.start_step("查看第二屏子游戏列表")
            gamelist = self.game_page.get_game_list()
            print gamelist
            for i in range(len(gamelist)):
                gamename = gamelist[i].get_attribute("name")
                gameid = filter(lambda ch: ch in '0123456789', gamename)
                print gameid
                self.game_page.set_robot(gameid=gameid)
            self.common.recover_user(mid)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

# __qtaf_seq_tests__ = [C039_DFQP_Activity]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
