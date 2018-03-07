#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
双癞子场-双癞子场界面(测试)
'''
import time
from runcenter.enums import EnumStatus, EnumPriority
from runcenter.testcase import TestCase, debug_run_all
from common.common import Common
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from common import Interface
from uilib.level_page import Level_Page

class D25708_DoubleLaizi_Quickstart(TestCase):
    '''
    金币不足,快速开始
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 20

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_money(mid, 999)
        self.hall_page = Hall_Page()
        self.level_page = Level_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            print len(elments1)
            elments1[1].click()
        self.level_page.wait_element("快速开始").click()
        try:
            self.level_page.wait_element("关闭2").click()
        except:
            self.log_info("未出现此按钮")
        self.game_page.element_is_exist("立即购买")
        self.assert_equal("检查是否出现立即购买", self.level_page.wait_element("立即购买文本").get_attribute("text") == "立即购买")
        self.game_page.screenshot("快速开始界面.png")
        self.hall_page.wait_element("关闭1").click()
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
            self.common.set_money(mid, 5000)
        finally:
            self.common.closedriver()

class D25708_DoubleLaizi_Enter(TestCase):
    '''
    金币不足进入房间
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 20

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_money(mid, 999)
        self.hall_page = Hall_Page()
        self.level_page = Level_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去癞子场")
        elments1 = self.hall_page.get_elements("游戏列表")
        print len(elments1)
        elments1[1].click()
        self.start_step("进入房间")
        elments = self.level_page.get_elements("房间列表")
        for j in range(len(elments)/2):
            self.start_step("点击第%s个房间" %(j+1))
            elments[j].click()
            try:
                self.level_page.wait_element("关闭2").click()
            except:
                self.log_info("未出现此按钮")
            self.game_page.element_is_exist("立即购买")
            self.assert_equal("检查是否出现立即购买", self.level_page.wait_element("立即购买文本").get_attribute("text") == "立即购买")
            self.game_page.screenshot("点击第%s个房间界面.png" %(j+1))
            self.hall_page.wait_element("关闭1").click()
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
            self.common.set_money(mid, 5000)
        finally:
            self.common.closedriver()

__qtaf_seq_tests__ = [D25708_DoubleLaizi_Enter]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()


