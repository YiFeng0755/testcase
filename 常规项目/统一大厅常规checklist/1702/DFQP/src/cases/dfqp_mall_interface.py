#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
商城
'''
import time
import datetime
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.sign_page import Sign_Page
from uilib.hall_page import Hall_Page
from uilib.setting_page import Setting_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.mall_page import Mall_Page
from uilib.backpack_page import Backpack_Page
from uilib.message_page import Message_Page
from common.common import Common
import test_datas
from datacenter import dataprovider
import common.Interface as PHPInterface

class C31060_DFCP_Mall_Interface_GetPro(TestCase):
    '''
    商城购买道具
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.mall_page = Mall_Page()
        self.sign_page = Sign_Page()
        self.backpack_page = Backpack_Page()
        self.personinfo_page = Personinfo_Page()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid=mid, value='53000')
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.start_step("进入商城页面")
        self.hall_page.wait_element("商城").click()
        self.mall_page.wait_element("道具页签").click()
        self.start_step("购买道具")
        self.mall_page.wait_element("提示卡").click()
        time.sleep(5)
        self.sign_page.wait_element("购买").click()
        time.sleep(2)
        self.hall_page.screenshot('bug.png')

    def post_test(self):
        # self.common.release_user(user_info['mid'])
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()
        self.common.recover_user(mid)

class C31053_DFCP_Mall_Interface_GetPro(TestCase):
    '''
    金条购买银币
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid=mid, value='20000')
        self.common.set_crystal(mid=mid,value='450')
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.mall_page = Mall_Page()
        self.sign_page = Sign_Page()
        self.backpack_page = Backpack_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.start_step("进入商城页面")
        self.hall_page.wait_element("商城").click()
        time.sleep(4)
        self.mall_page.wait_element("银币页签").click()
        time.sleep(2)
        self.start_step("购买道具")
        time.sleep(4)
        try:
            self.hall_page.wait_element("立即升级绑定账号").click()
            time.sleep(3)
            self.sign_page.wait_element("关闭1").click()
            time.sleep(4)
        except:
            print "未出现立即升级绑定账号按钮"
        self.mall_page.wait_element("银币购买1").click()
        time.sleep(5)
        while(self.hall_page.element_is_exist("立即升级绑定账号")):
            self.sign_page.wait_element("关闭1").click()
        while(self.mall_page.element_is_exist("银币页面购买")==False):
            self.mall_page.wait_element("银币购买1").click()
        self.mall_page.wait_element("银币页面购买").click()
        time.sleep(5)
        self.hall_page.screenshot('buy.png')

    def post_test(self):
        try:
            self.common.recover_user(mid)
        except:
            self.log_info("初始化银币金条报错")
        try:
            self.common.closedriver()
        except:
            self.log_info("close driver fail")

__qtaf_seq_tests__ = [C31053_DFCP_Mall_Interface_GetPro]
if __name__ == '__main__':
    # C002_DFQP_Login_GuestLogin = C002_DFQP_Login_GuestLogin()
    # C002_DFQP_Login_GuestLogin.debug_run()
    debug_run_all()
