#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
癞子场-玩牌相关(降场)(测试）
'''
import time
from runcenter.enums import EnumStatus, EnumPriority
from runcenter.testcase import TestCase, debug_run_all

from common import Interface
from common.common import Common
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.level_page import Level_Page

class D25705_LaiziRoom_Dropfile_Display(TestCase):
    '''
    房间内降场
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    # pending = True

    def pre_test(self):
        self.common = Common()
        self.start_step("设置金币数为5000")
        global mid, money, starttime, endtime
        starttime = time.time()
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_money(mid, 5000)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()

    def play_game(self):
        self.start_step("开始玩牌")
        while self.game_page.element_is_exist("开始"):
            self.game_page.wait_element("开始").click()
        while self.game_page.element_is_exist("继续游戏"):
            self.game_page.wait_element("继续游戏").click()
        starttime = time.time()
        while self.game_page.element_is_exist("正在配桌中"):
            time.sleep(1)
            self.log_info("正在配桌中,等待")
            endtime = time.time()
            time.sleep(3)
            try:
                self.game_page.wait_element("换桌").click()
            except:
                self.log_info("换桌失败")
            if (endtime - starttime) / 60 > self.timeout - 5:
                self.game_page.is_in_gameroom(self.luadriver)
                self.log_info("等待超时")
                return
        self.start_step("叫地主")
        while self.game_page.element_is_exist("出牌", 1) == False:
            list = ["抢地主", "叫地主", "加倍"]
            self.log_info("叫地主中")
            for name in list:
                try:
                    self.game_page.wait_element(name, 2).click()
                except:
                    self.log_info("未出现抢地主按钮")
            if self.game_page.element_is_exist("继续游戏", 1):
                break
        self.start_step("托管")
        if self.game_page.element_is_exist("机器人") == False:
            self.game_page.wait_element("托管").click()
        while self.game_page.element_is_exist("继续游戏", 3) == False:
            time.sleep(1)
            self.log_info("正在游戏中")

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            print len(elments1)
            elments1[1].click()
        self.game_page.wait_element("切换按钮").click()
        elments = self.game_page.get_elements("切换玩法")
        elments[0].click()
        # self.level_page.wait_element("快速开始").click()
        self.start_step("进入房间")
        while self.level_page.element_is_exist("房间列表"):
            elments = self.level_page.get_elements("房间列表")
            print len(elments)
            elments[1].click()
        self.game_page.screenshot("玩牌的高倍场房间.png")
        while (int(Interface.get_money(mid)) >= 5000 or int(Interface.get_money(mid)<1000)):
            endtime = time.time()
            if (endtime - starttime) / 60 > self.timeout - 5:
                self.game_page.is_in_gameroom(self.luadriver)
                self.log_info("等待超时")
                return
            if int(Interface.get_money(mid)) >= 5000:
                self.common.set_money(mid, 6000)
                self.play_game()
            elif int(Interface.get_money(mid)) < 1000:
                self.common.set_money(mid, 6000)
                self.start_step("重新进场玩牌")
                try:
                    self.game_page.wait_element("关闭2", 3).click()
                except:
                    print "未出现破产页面"
                while self.game_page.element_is_exist("退出"):
                    self.game_page.wait_element("退出", 3).click()
                    try:
                        self.hall_page.wait_element("关闭1", 3).click()
                    except:
                        print "未出现破产页面"
                elments[1].click()
                self.play_game()
        self.game_page.screenshot("结算界面显示破产.png")
        while self.game_page.element_is_exist("继续游戏"):
            self.game_page.wait_element("继续游戏").click()
            while self.game_page.element_is_exist("去底倍场"):
                self.game_page.screenshot("去底倍场.png")
                self.game_page.wait_element("去底倍场").click()
                self.game_page.screenshot("底倍场房间.png")
        # elment1 = self.game_page.wait_element("房间底分1")
        # chujichangdifen = self.common.image_text(elment1)
        # if chujichangdifen.isdigit():
        #     self.log_info("房间底分:" + chujichangdifen)
        #     self.assert_equal("判断进入了底倍场", actual=int(chujichangdifen) < 50)
        self.start_step("退出玩牌房间")
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
            self.common.set_money(mid, 5000)
        finally:
            self.common.closedriver()

# __qtaf_seq_tests__ = [D25704_LaiziRoom_Broke_Display]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()


