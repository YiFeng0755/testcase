#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
准备与换桌
'''
import time,sys
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.broadcast_page import Broadcast_Page
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common
import common.Interface as PHPInterface
import test_datas,json
from utils.confighelper import ConfigHelper
from utils.constant import user_cfg

class C27021_ReadyCountdown(TestCase):
    '''
    准备成功倒计时，换桌按钮点击无效
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.personinfo_page = Personinfo_Page()
        self.start_step("初始化环境")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

    def enter_room(self,is_next=False):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('遍历子游戏')
        # elements = self.hall_page.get_elements('子游戏')
        game_list = self.game_page.get_game_list()
        print len(game_list)
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if (self.game_page.game_is_download() == False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i].get_attribute("name"))
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            self.start_step('进入初级场')
            self.game_page.wait_element("房间场次").click()
            while self.hall_page.element_is_exist("换桌"):
                self.hall_page.wait_element("准备").click()
                time.sleep(2)
                self.hall_page.screenshot("%s_huanzuo.png"% game_list[i].get_attribute("name"))
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
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("获取首屏子游戏列表")
        self.enter_room()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("获取第二页的子游戏")
        self.enter_room(is_next=True)


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(self.common.get_config_value("casecfg", "mid"))
        self.common.closedriver()

class C27022_ChangetableCountdown(TestCase):
    '''
    换桌成功倒计时，准备按钮点击无效
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.personinfo_page = Personinfo_Page()
        self.start_step("初始化环境")
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

    def enter_room(self,is_next = False):
        self.start_step('遍历子游戏')
        # elements = self.hall_page.get_elements('子游戏')
        game_list = self.game_page.get_game_list()
        print len(game_list)
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if (self.game_page.game_is_download() == False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i].get_attribute("name"))
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            self.start_step('进入初级场')
            self.game_page.wait_element("房间场次").click()
            while self.hall_page.element_is_exist("换桌"):
                self.hall_page.wait_element("换桌").click()
                self.hall_page.screenshot("%s_huanzuo.png"% game_list[i].get_attribute("name"))
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
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("获取首屏子游戏列表")
        self.enter_room()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("获取第二页的子游戏")
        self.enter_room(is_next=True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(self.common.get_config_value("casecfg","mid"))
        self.common.closedriver()

class C27023_ReadybuttonDisappear(TestCase):
    '''
    准备成功后准备按钮消失
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.start_step("初始化环境")
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.personinfo_page = Personinfo_Page()
        self.game_page = Game_Page()
        self.common.closeactivity(self.luadriver)

    def enter_room(self,is_next = False):
        self.start_step('遍历子游戏')
        # elements = self.hall_page.get_elements('子游戏')
        game_list = self.game_page.get_game_list()
        print len(game_list)
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if (self.game_page.game_is_download() == False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i].get_attribute("name"))
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            self.start_step('进入初级场')
            self.game_page.wait_element("房间场次").click()
            while self.hall_page.element_is_exist("准备"):
                self.hall_page.wait_element("准备").click()
                self.hall_page.screenshot("%s_huanzuo.png"% game_list[i].get_attribute("name"))
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
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("获取首屏子游戏列表")
        self.enter_room()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("获取第二页的子游戏")
        self.enter_room(is_next=True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(self.common.get_config_value("casecfg", "mid"))
        self.common.closedriver()

# __qtaf_seq_tests__=[C27021_ReadyCountdown]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()