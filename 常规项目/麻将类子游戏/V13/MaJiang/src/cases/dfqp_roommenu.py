#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
子游戏房间菜单
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.game_page import Game_Page
from uilib.safebox_page import Safebox_Page
from common.common import Common
import common.Interface as PHPInterface

class C27546_RoomMenu_NoAlready(TestCase):
    '''
    未准备，查看房间内菜单按钮显示
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("获取用户mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("设置银币数为10000")
        self.common.set_coin(mid = mid, value = "10000")

        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange=False):
            game_list = self.game_page.get_game_list()
            for i in range(len(game_list)):
                # 大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()
                self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                game_list[i].click()
                if (self.game_page.element_is_exist("重新获取")):
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击重新获取")
                    self.game_page.wait_element("重新获取").click()
                else:
                    self.game_page.game_is_download()
                    print "进入子游戏选场界面"
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    roomlevel = self.game_page.get_elements("房间场次")
                    self.start_step("点击初级场")
                    roomlevel[0].click()
                    self.game_page.screenshot("%s_room.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击房间内菜单按钮")
                    self.game_page.wait_element("房间内菜单").click()
                    self.game_page.screenshot("menu.png")
                    self.start_step("点击退出")
                    self.game_page.wait_element("退出").click()
                    self.start_step("退出子游戏%s到大厅界面" % game_list[i].get_attribute("name"))
                    # while (self.hall_page.element_is_exist("预发布") != True):
                    #     self.luadriver.back()
                    #     time.sleep(10)
                    self.game_page.wait_element("返回1").click()

        self.start_step("大厅第一页子游戏")
        traversal_gameList(self, False)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏")
        traversal_gameList(self, True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class  C27568_RoomMenu_Setting(TestCase):
    '''
    3种方式关闭设置界面
     '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

        self.start_step("获取用户mid")
        mid = self.common.get_config_value("casecfg","mid")
        self.start_step("设置银币数为10000")
        self.common.set_coin(mid=mid, value="10000")
        
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("获取子游戏列表")

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange=False):
            game_list = self.game_page.get_game_list()
            for i in range(len(game_list)):
                # 大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()
                self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                time.sleep(2)
                game_list[i].click()
                if (self.game_page.element_is_exist("重新获取")):
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击重新获取")
                    self.game_page.wait_element("重新获取").click()
                else:
                    self.game_page.game_is_download()
                    print "进入子游戏%s选场界面" % game_list[i].get_attribute("name")
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    roomlevel = self.game_page.get_elements("房间场次")
                    self.start_step("点击初级场")
                    roomlevel[0].click()
                    self.game_page.screenshot("room.png")
                    self.start_step("点击房间内菜单按钮")
                    self.game_page.wait_element("房间内菜单").click()
                    self.game_page.screenshot("menu.png")

                    self.start_step("点击设置")
                    self.game_page.wait_element("设置").click()
                    self.game_page.screenshot("setting.png")
                    self.start_step("关闭设置页面")
                    self.game_page.wait_element("关闭设置页面").click()

                    self.game_page.wait_element("房间内菜单").click()
                    self.start_step("点击设置")
                    self.game_page.wait_element("设置").click()
                    self.game_page.screenshot("setting.png")
                    self.start_step("点击设置界面之外的地方关闭设置页面")
                    self.game_page.wait_element("房间内菜单").click()

                    self.game_page.wait_element("房间内菜单").click()
                    self.start_step("点击设置")
                    self.game_page.wait_element("设置").click()
                    self.game_page.screenshot("setting.png")
                    self.start_step("点击手机物理返回键关闭设置界面")
                    self.luadriver.back()


                    self.start_step("退出子游戏%s房间到选场界面" % game_list[i].get_attribute("name"))
                    # self.game_page.wait_element("房间内菜单").click()
                    # self.game_page.wait_element("退出").click()
                    # self.start_step("退出子游戏%s到大厅界面" % game_list[i].get_attribute("name"))
                    # try:
                    #     self.game_page.wait_element("返回1").click()
                    # except:
                    #     self.log_info()

                    while (self.hall_page.element_is_exist("预发布") != True):
                        self.luadriver.back()
                        time.sleep(10)
                    self.game_page.wait_element("返回1").click()

        self.start_step("大厅第一页子游戏")
        traversal_gameList(self, False)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏")
        traversal_gameList(self, True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C27592_RoomMenu_Recharge(TestCase):
    '''
    牌局未开始，点击菜单栏商城，购买银币，打开购买方式页面，查看显示
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

        self.start_step("获取用户mid")
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("设置银币数为10000")
        self.common.set_coin(mid=mid, value="10000")

        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange = False):
            game_list = self.game_page.get_game_list()
            for i in range(len(game_list)):
                #大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()
                self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                game_list[i].click()
                if (self.game_page.element_is_exist("重新获取")):
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击重新获取")
                    self.game_page.wait_element("重新获取").click()
                else:
                    self.game_page.game_is_download()
                    print "进入子游戏%s选场界面" % game_list[i].get_attribute("name")
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    roomlevel = self.game_page.get_elements("房间场次")
                    self.start_step("点击游戏ID: %s的初级场" % game_list[i].get_attribute("name"))
                    roomlevel[0].click()
                    self.game_page.screenshot("%s_room.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击房间内菜单按钮")
                    self.game_page.wait_element("房间内菜单").click()
                    self.game_page.screenshot("%s_menu.png" % game_list[i].get_attribute("name"))

                    self.start_step("点击商城")
                    self.game_page.wait_element("商城").click()
                    self.game_page.screenshot("%s_shop.png" % game_list[i].get_attribute("name"))
                    goodslist = self.game_page.get_elements("商品列表")
                    if len(goodslist) > 0:
                        self.start_step("点击购买第一个")
                        goodslist[0].click()
                        self.game_page.screenshot("%s_paymethod.png" % game_list[i].get_attribute("name"))
                        self.start_step("关闭购买方式页面")
                        self.game_page.wait_element("关闭购买方式").click()
                    # self.start_step("关闭商城页面")
                    # self.game_page.wait_element("关闭商城页面").click()

                    self.start_step("退出子游戏%s房间到选场界面" % game_list[i].get_attribute("name"))
                    # self.game_page.wait_element("房间内菜单").click()
                    # self.start_step("点击退出")
                    # self.game_page.wait_element("退出").click()
                    # self.start_step("退出子游戏%s到大厅界面" % game_list[i].get_attribute("name"))
                    while (self.hall_page.element_is_exist("预发布") != True):
                        self.luadriver.back()
                        time.sleep(10)
                    self.game_page.wait_element("返回1").click()

        self.start_step("大厅第一页子游戏")
        traversal_gameList(self, False)
        time.sleep(2)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏")
        traversal_gameList(self, True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

__qtaf_seq_tests__ = [C27592_RoomMenu_Recharge]
if __name__ == '__main__':
    # C27546_RoomMenu_NoAlready().debug_run()
    # C27568_RoomMenu_Setting().debug_run()
    C27592_RoomMenu_Recharge().debug_run()
     # debug_run_all()