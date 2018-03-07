#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
防作弊场次显示
'''
import re
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.game_page import Game_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common
from common import Interface


class C27467_Gameroom_Cheat_Display(TestCase):
    '''
    防作弊房间外UI显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 20

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

    def room_cheat(self,game_list,is_next=False,switch=1):
        for i in range(len(game_list)):
            self.start_step("进入 %s 标准场_作弊场" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i].get_attribute("name"))
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            if switch==1:
                self.game_page.wait_element("反作弊icon")
                self.game_page.screenshot("_%s_cheat.png" % game_list[i].get_attribute("name"))
            else:
                self.game_page.element_is_exist("反作弊icon") ==False
                self.game_page.screenshot("_%s_nocheat.png" % game_list[i].get_attribute("name"))
            try:
                self.game_page.wait_element("返回1").click()
            except:
                self.log_info("从 %s 标准场返回大厅失败" % game_list[i].get_attribute("name"))
            if is_next == True:
                self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                try:
                    self.game_page.wait_element("右三角标").click()
                except:
                    self.log_info("当前为第二页")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("获取首屏子游戏列表,并设置为作弊场")
        game_list = self.game_page.get_game_list()
        self.common.room_set_cheat(game_list,switch=1)
        self.room_cheat(game_list,switch=1)
        self.start_step("首屏子游戏列表设置为非作弊场")
        self.common.room_set_cheat(game_list,switch=0)
        self.start_step("获取第二页的子游戏")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("获取第二页子游戏列表,并设置为作弊场")
        game_list1 = self.game_page.get_game_list()
        self.common.room_set_cheat(game_list1,switch=1)
        self.room_cheat(game_list1,is_next=True,switch=1)
        self.start_step("第二页子游戏列表设置为非作弊场")
        self.common.room_set_cheat(game_list1,switch=0)
        self.start_step("查看非作弊场的游戏")
        self.common.switchserver()
        self.common.closeActivityBtn()
        self.room_cheat(game_list, switch=0)
        self.room_cheat(game_list1,is_next=True,switch=0)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27468_Gameroom_Cheat_Room(TestCase):
    '''
    进入防作弊房间查看房间内UI显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 20

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        global mid
        mid = self.common.get_config_value("casecfg","mid")
        self.common.set_coin(mid,value=50000)
        self.common.closeactivity(self.luadriver)

    def room_cheat(self, game_list, is_next=False, switch=1):
        self.common.room_set_cheat(game_list, switch)
        for i in range(len(game_list)):
            self.start_step("进入 %s 中级场_作弊场" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if (self.game_page.game_is_download() == False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i].get_attribute("name"))
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            self.game_page.wait_element("反作弊icon")
            self.game_page.screenshot("_%s_cheat.png" % game_list[i].get_attribute("name"))
            elements = self.game_page.get_elements("房间场次")
            print elements
            elements[1].click()
            self.game_page.screenshot("_%s_cheat_room.png" % game_list[i].get_attribute("name"))
            if(self.game_page.element_is_exist("房间内聊天")==False):
                self.log_info("%s防作弊场无聊天按钮" % game_list[i].get_attribute("name"))
            else:
                raise "%s防作弊场出现聊天按钮" % game_list[i].get_attribute("name")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("获取首屏子游戏列表,并设置为作弊场")
        game_list = self.game_page.get_game_list()
        self.room_cheat(game_list, switch=1)
        self.common.room_set_cheat(game_list, switch=0)
        self.start_step("获取第二页的子游戏")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("获取第二页子游戏列表,并设置为作弊场")
        game_list1 = self.game_page.get_game_list()
        self.room_cheat(game_list1, is_next=True, switch=1)
        self.common.room_set_cheat(game_list1, switch=0)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27470_Gameroom_Cheat_Quickly(TestCase):
    '''
    点击快速开始进入防作弊场次
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 20

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        global mid
        mid = self.common.get_config_value("casecfg","mid")
        self.common.set_coin(mid,value=50000)
        self.common.closeactivity(self.luadriver)

    def room_cheat(self, game_list, is_next=False, switch=1):
        self.common.room_set_cheat(game_list, switch)
        for i in range(len(game_list)):
            self.start_step("进入 %s 中级场_作弊场" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if (self.game_page.game_is_download() == False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i].get_attribute("name"))
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            self.game_page.wait_element("反作弊icon")
            self.game_page.screenshot("_%s_cheat.png" % game_list[i].get_attribute("name"))
            self.game_page.wait_element("快速开始").click()
            time.sleep(4)
            self.game_page.screenshot("_%s_cheat_room.png" % game_list[i].get_attribute("name"))
            if(self.game_page.element_is_exist("房间内聊天")==False):
                self.log_info("%s防作弊场无聊天按钮" % game_list[i].get_attribute("name"))
            else:
                raise "%s防作弊场出现聊天按钮" % game_list[i].get_attribute("name")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("获取首屏子游戏列表,并设置为作弊场")
        game_list = self.game_page.get_game_list()
        self.room_cheat(game_list, switch=1)
        self.common.room_set_cheat(game_list, switch=0)
        self.start_step("获取第二页的子游戏")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("获取第二页子游戏列表,并设置为作弊场")
        game_list1 = self.game_page.get_game_list()
        self.room_cheat(game_list1, is_next=True, switch=1)
        self.common.room_set_cheat(game_list1, switch=0)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27471_Gameroom_Cheat_Useinfo_NoVIP(TestCase):
    '''
    防作弊房间中查看自己的信息
    防作弊场玩家A非vip
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 20

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        global mid
        mid = self.common.get_config_value("casecfg","mid")
        # self.common.set_coin(mid,value=50000)
        self.common.closeactivity(self.luadriver)

    def room_cheat(self, game_list, is_next=False, switch=1):
        self.common.room_set_cheat(game_list, switch)
        for i in range(len(game_list)):
            self.start_step("进入 %s 中级场_作弊场" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if (self.game_page.game_is_download() == False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i].get_attribute("name"))
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            self.game_page.wait_element("反作弊icon")
            self.game_page.screenshot("_%s_cheat.png" % game_list[i].get_attribute("name"))
            elements = self.game_page.get_elements("房间场次")
            elements[1].click()
            self.game_page.screenshot("_%s_cheat_room.png" % game_list[i].get_attribute("name"))
            if(self.game_page.element_is_exist("房间内聊天")==False):
                self.log_info("%s防作弊场无聊天按钮" % game_list[i].get_attribute("name"))
            else:
                raise "%s防作弊场出现聊天按钮" % game_list[i].get_attribute("name")
            self.start_step("%s防作弊场查看头像" % game_list[i].get_attribute("name"))
            try:
                self.game_page.wait_element("头像frame").click()
                self.game_page.screenshot("_%s_cheat_room_user.png" % game_list[i].get_attribute("name"))
                self.game_page.wait_element("头像frame").click()
            except:
                self.log_info("%s防作弊场查看头像失败" % game_list[i].get_attribute("name"))
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("获取首屏子游戏列表,并设置为作弊场")
        game_list = self.game_page.get_game_list()
        self.room_cheat(game_list, switch=1)
        self.common.room_set_cheat(game_list, switch=0)
        self.start_step("获取第二页的子游戏")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("获取第二页子游戏列表,并设置为作弊场")
        game_list1 = self.game_page.get_game_list()
        self.room_cheat(game_list1, is_next=True, switch=1)
        self.common.room_set_cheat(game_list1, switch=0)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27472_Gameroom_Cheat_Useinfo_VIP(TestCase):
    '''
    防作弊房间中查看自己的信息
    防作弊场玩家Avip
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 20

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        global mid
        mid = self.common.get_config_value("casecfg","mid")
        # self.common.set_coin(mid,value=50000)
        Interface.set_vip(mid,5)
        self.common.closeactivity(self.luadriver)

    def room_cheat(self, game_list, is_next=False, switch=1):
        self.common.room_set_cheat(game_list, switch)
        for i in range(len(game_list)):
            self.start_step("进入 %s 中级场_作弊场" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if (self.game_page.game_is_download() == False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i].get_attribute("name"))
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            self.game_page.wait_element("反作弊icon")
            self.game_page.screenshot("_%s_cheat.png" % game_list[i].get_attribute("name"))
            self.game_page.get_elements("房间场次")[1].click()
            self.game_page.screenshot("_%s_cheat_room.png" % game_list[i].get_attribute("name"))
            if(self.game_page.element_is_exist("房间内聊天")==False):
                self.log_info("%s防作弊场无聊天按钮" % game_list[i].get_attribute("name"))
            else:
                raise "%s防作弊场出现聊天按钮" % game_list[i].get_attribute("name")
            self.start_step("%s防作弊场查看头像" % game_list[i].get_attribute("name"))
            try:
                self.game_page.wait_element("头像frame").click()
                self.game_page.screenshot("_%s_cheat_room_user.png" % game_list[i].get_attribute("name"))
                self.game_page.wait_element("头像frame").click()
            except:
                self.log_info("%s防作弊场查看头像失败" % game_list[i].get_attribute("name"))
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("获取首屏子游戏列表,并设置为作弊场")
        game_list = self.game_page.get_game_list()
        self.room_cheat(game_list, switch=1)
        self.common.room_set_cheat(game_list, switch=0)
        self.start_step("获取第二页的子游戏")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("获取第二页子游戏列表,并设置为作弊场")
        game_list1 = self.game_page.get_game_list()
        self.room_cheat(game_list1, is_next=True, switch=1)
        self.common.room_set_cheat(game_list1, switch=0)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

# __qtaf_seq_tests__ = [C27470_Gameroom_Cheat_Quickly]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
