#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
三人场-初级场-正常玩牌1小时(正式/测试)
'''
import time
from runcenter.enums import EnumStatus, EnumPriority
from runcenter.testcase import TestCase, debug_run_all

from common.common import Common
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from common import Interface
from uilib.level_page import Level_Page

class D0004_ThreeRoom_PlayGame(TestCase):
    '''
    三人场玩牌
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 70
    # pending = True

    def pre_test(self):
        global starttime,endtime
        starttime=time.time()
        self.common = Common()
        self.hall_page = Hall_Page()
        self.level_page = Level_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()
        self.common.user_money(money=1000)

    def gameplay(self):
        i = 1
        self.game_page.wait_element("开始").click()
        # while self.game_page.element_is_exist("立即领取"):
        #     self.game_page.wait_element("关闭1").click()
        while self.game_page.element_is_exist("破产对话框",1)==False:
            self.start_step("开始玩第%s场牌" %i)
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
            while self.game_page.element_is_exist("出牌",1)==False:
                list1 = ["叫地主","不叫"]
                self.log_info("叫地主中")
                from random import choice
                print choice(list1)
                try:
                    self.game_page.wait_element(choice(list1), 1).click()
                except:
                    self.log_info("未出现抢地主按钮")
                list = ["叫地主", "不叫", "抢地主"]
                for name in list:
                    try:
                        self.game_page.wait_element(name, 1).click()
                    except:
                        self.log_info("未出现抢地主按钮")
                # if self.game_page.element_is_exist("不出",1):
                #     break
                if self.game_page.element_is_exist("继续游戏", 1):
                    break
            if self.game_page.element_is_exist("机器人") == False:
                self.game_page.wait_element("托管").click()
            while (self.game_page.element_is_exist("提示",1) or self.game_page.element_is_exist("出牌",1)):
                try:
                    self.game_page.wait_element("提示").click()
                    self.game_page.element_is_exist("出牌").click()
                except:
                    self.log_info("未出现提示按钮")
            self.game_page.screenshot("第%s次托管玩牌.png" %i)
            while self.game_page.element_is_exist("继续游戏",1)==False:
                time.sleep(1)
                self.log_info("正在游戏中")
                endtime = time.time()
                if (endtime - starttime)/60 > self.timeout - 10:
                    self.game_page.is_in_gameroom(self.luadriver)
                    return
            self.game_page.screenshot("第%s次玩牌结算.png" %i)
            while self.game_page.element_is_exist("继续游戏", 1):
                while self.game_page.element_is_exist("QQ分享",3):
                    self.game_page.screenshot("第%s次玩牌出现分享页面.png" % i)
                    self.luadriver.keyevent(4)
                self.game_page.wait_element("继续游戏").click()
            while self.game_page.element_is_exist("去底倍场",1):
                self.game_page.screenshot("第%s次玩牌提示去底倍场.png" %i)
                self.game_page.wait_element("去底倍场").click()
            while (self.game_page.element_is_exist("立即领取",1) or self.game_page.element_is_exist("立即购买",1)):
                try:
                    self.game_page.wait_element("关闭1").click()
                except:
                    self.log_info("未出现关闭按钮")
                try:
                    self.game_page.wait_element("关闭2").click()
                except:
                    self.log_info("未出现关闭按钮")
                self.game_page.exit_game(self.luadriver)
                self.common.user_money(money=1000)
                self.start_step("进入三人场")
                while self.hall_page.element_is_exist("游戏列表"):
                    elments = self.hall_page.get_elements("游戏列表")
                    elments[2].click()
                while self.level_page.element_is_exist("房间列表"):
                    self.level_page.wait_element("房间列表").click()
            while self.game_page.element_is_exist("开始"):
                self.game_page.wait_element("开始").click()
            i += 1


    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.hall_page.screenshot("进入三人场游戏.png")
        self.start_step("进入三人场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments = self.hall_page.get_elements("游戏列表")
            elments[2].click()
        self.start_step("点击初级场房间")
        while self.level_page.element_is_exist("房间列表",3):
            self.level_page.wait_element("房间列表").click()
        self.game_page.wait_element("同步标志")
        self.gameplay()

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
        finally:
            self.common.closedriver()

# __qtaf_seq_tests__ = [D25734_ThreeRoom_PlayGame]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()


