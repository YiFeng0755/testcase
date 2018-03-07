#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
三人场界面，涉及到金币接口相关(测试)
'''
import time
from runcenter.enums import EnumStatus, EnumPriority
from runcenter.testcase import TestCase, debug_run_all
from utils import util
from common.common import Common
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from common import Interface
from uilib.level_page import Level_Page
class D25734_ThreeRoom_Displays(TestCase):
    '''
    三人场界面
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg","mid")
        self.common.set_money(mid,999)
        self.hall_page = Hall_Page()
        self.level_page = Level_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去三人场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[2].click()
        self.start_step("查看房间列表")
        self.start_step("点击快速开始")
        self.level_page.wait_element("快速开始").click()
        self.level_page.screenshot("破产点击快速开始出现的界面.png")
        try:
            self.level_page.wait_element("关闭2").click()
        except:
            self.log_info("未出现此按钮")
        self.level_page.element_is_exist("立即购买")
        self.assert_equal("检查是否出现立即购买",self.level_page.wait_element("立即购买文本").get_attribute("text")=="立即购买")
        self.level_page.screenshot("立即购买.png")

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
            self.common.set_money(mid, 3000)
        finally:
            self.common.closedriver()

class D25735_ThreeRoom_Enter(TestCase):
    '''
    玩家金币不足
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    # pending = True

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
        self.start_step("进去三人场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            print len(elments1)
            elments1[2].click()
        self.start_step("查看房间列表")
        self.hall_page.screenshot("查看房间列表.png")
        elments = self.level_page.get_elements("房间列表")
        print len(elments)
        for j in range(len(elments)/2):
            if j<4:
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
            elif j<5:
                elments = self.level_page.get_elements("房间列表")
                self.common.swipeelement(elments[3], elments[1])
                self.common.swipeelement(elments[3], elments[1])
                self.start_step("点击第%s个房间" %(j+1))
                elments = self.level_page.get_elements("房间列表")
                elments[len(elments)-1].click()
                try:
                    self.level_page.wait_element("关闭2").click()
                except:
                    self.log_info("未出现此按钮")
                try:
                    self.game_page.element_is_exist("立即购买")
                    self.assert_equal("检查是否出现立即购买", self.level_page.wait_element("立即购买文本").get_attribute("text") == "立即购买")
                    self.game_page.screenshot("点击第%s个房间界面.png" %(j+1))
                    self.hall_page.wait_element("关闭1").click()
                except:
                    self.log_info("滑动失败，未找到第五个房间")
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
            self.common.set_money(mid, 3000)
        finally:
            self.common.closedriver()

class D25736_ThreeRoom_Enter_ToomuchMoney(TestCase):
    '''
    三人场进场
    金币过多
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    # pending = True

    def pre_test(self):
        self.common = Common()
        global mid,money
        money = 30000
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_money(mid, money)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去三人场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            print len(elments1)
            elments1[2].click()
        self.start_step("查看房间列表")
        self.hall_page.screenshot("查看房间列表.png")
        elments = self.level_page.get_elements("房间列表")
        self.start_step("获取初级场底分")
        image_element = self.game_page.wait_element("场次底分")
        chujichangdifen = self.common.image_text(image_element)
        if chujichangdifen == '':
            chujichangdifen = '50'
        self.log_info("初级场底分:"+chujichangdifen)
        self.start_step("点击初级场房间")
        self.level_page.wait_element("房间列表").click()
        string = self.level_page.wait_element("金币超出文本").get_attribute("text")
        self.assert_equal("检查是否出现金币超出弹框",string.find("您的金币已超过本房间上限")!= -1)
        self.level_page.screenshot("金币超出.png")
        self.level_page.wait_element("去高级场").click()
        self.level_page.screenshot("高级场房间.png")
        elments1 = self.game_page.wait_element("房间底分")
        room = self.common.image_text(elments1)
        if room.isdigit():
            self.start_step("初级场底：%s，房间底分：%s，核对是否是高级场" %(chujichangdifen,room))
            self.assert_equal("进入了高级场",actual= int(room)>int(chujichangdifen))
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
            self.common.set_money(mid, 3000)
        finally:
            self.common.closedriver()

class D25749_ThreeRoom_Talkfor1000_Display(TestCase):
    '''
    1000、5000底注场
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    # pending = True

    def pre_test(self):
        self.common = Common()
        self.start_step("设置金币数为100000")
        global mid,money
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_money(mid,100000)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去三人场")
        elments1 = self.hall_page.get_elements("游戏列表")
        print len(elments1)
        elments1[2].click()
        self.start_step("查看房间列表")
        self.hall_page.screenshot("查看房间列表.png")
        elments = self.level_page.get_elements("房间列表")
        self.common.swipeelement(elments[3], elments[1])
        elments = self.level_page.get_elements("房间列表")
        print len(elments)
        self.start_step("进入房间")
        elments[len(elments)*1/2-2].click()
        self.game_page.wait_element("聊天").click()
        self.hall_page.screenshot("聊天.png",sleeptime=0)
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
            self.common.set_money(mid, 3000)
        finally:
            self.common.closedriver()

# __qtaf_seq_tests__ = [D25735_ThreeRoom_Enter]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()


