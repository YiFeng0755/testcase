#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
性能测试场景3：双癞子场-初级场正常玩牌（正式/测试)
'''
import time
from runcenter.enums import EnumStatus, EnumPriority
from runcenter.testcase import TestCase, debug_run_all

from com.common import Common
from com.constantEnum import EnumSceneName, EnumSceneType
from com.globalVars import singleGlobalVar
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.level_page import Level_Page

class X0003_DoubleLaizi_PlayGame(TestCase):
    '''
    双癞子场玩牌
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout =70
    # pending = True

    def pre_test(self):
        global starttime,endtime
        starttime=time.time()
        self.common = Common()
        self.hall_page = Hall_Page()
        self.level_page = Level_Page()
        self.game_page = Game_Page()
        self.common.user_money(money=1000)

    def gameplay(self):
        i = 1
        self.game_page.wait_element("开始").click()
        self.common.sendTagBroadcast(EnumSceneName.DoublelaiziRoom, EnumSceneType.Start)
        count = 0
        while self.game_page.element_is_exist("破产对话框",1)==False:
            self.start_step("开始玩第%s场牌" % i)
            while self.game_page.element_is_exist("正在配桌中"):
                self.log_info("正在配桌中,等待")
                time.sleep(3)
                try:
                    self.game_page.wait_element("换桌").click()
                except:
                    self.log_info("换桌失败")
                count += 1
                if (count > 10):
                    self.game_page.is_in_gameroom(singleGlobalVar.get("luaDriver"))
                    self.log_info("等待超时")
                    return
            while self.game_page.element_is_exist("出牌",1)==False:
                list = ["叫地主", "抢地主"]
                for name in list:
                    try:
                        self.game_page.wait_element(name, 0).click()
                    except:
                        self.log_info("未出现抢地主按钮")
                if self.game_page.element_is_exist("继续游戏", 1):
                    break
            if self.game_page.element_is_exist("机器人",1) == False:
                self.game_page.wait_element("托管",0).click()
            while (self.game_page.element_is_exist("提示",1) or self.game_page.element_is_exist("出牌",1)):
                try:
                    self.game_page.wait_element("提示").click()
                    self.game_page.element_is_exist("出牌").click()
                except:
                    self.log_info("未出现提示按钮")
            while self.game_page.element_is_exist("继续游戏",1)==False:
                time.sleep(1)
                self.log_info("正在游戏中")
                endtime = time.time()
                if (endtime - starttime)/60 > self.timeout - 10:
                    self.game_page.is_in_gameroom(singleGlobalVar.get("luaDriver"))
                    return
            self.common.taskScreenShot("gameover_%s.jpg" % i)
            while self.game_page.element_is_exist("继续游戏", 1):
                while self.game_page.element_is_exist("QQ分享",1):
                    singleGlobalVar.get("luaDriver").keyevent(4)
                self.game_page.wait_element("继续游戏").click()
            while self.game_page.element_is_exist("去底倍场",1):
                self.game_page.wait_element("去底倍场").click()
            while (self.game_page.element_is_exist("立即购买",1) or self.game_page.element_is_exist("立即领取",1)):
                try:
                    self.game_page.wait_element("关闭1").click()
                except:
                    self.log_info("未出现关闭按钮")
                try:
                    self.game_page.wait_element("关闭2").click()
                except:
                    self.log_info("未出现关闭按钮")
                self.game_page.exit_game(singleGlobalVar.get("luaDriver"))
                self.common.user_money(money=3000)
                self.start_step("进入双癞子场")
                while self.hall_page.element_is_exist("游戏列表"):
                    elments = self.hall_page.get_elements("游戏列表",0)
                    elments[1].click()
                while self.level_page.element_is_exist("房间列表"):
                    self.level_page.wait_element("房间列表",0).click()
            while self.game_page.element_is_exist("开始"):
                self.game_page.wait_element("开始",0).click()
            i += 1

    def run_test(self):
        self.hall_page.screenshot("enter_doubei_laizi.png")
        self.start_step("进入双癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments = self.hall_page.get_elements("游戏列表")
            elments[1].click()
        self.start_step("点击初级场房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.game_page.wait_element("同步标志")
        self.gameplay()
        time.sleep(5)
        self.common.sendTagBroadcast(EnumSceneName.DoublelaiziRoom, EnumSceneType.Stop)

# __qtaf_seq_tests__ = [D25734_DoubleLaizi_PlayGame]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()


