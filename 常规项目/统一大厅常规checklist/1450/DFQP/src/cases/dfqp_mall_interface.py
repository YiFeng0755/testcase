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


testdata=test_datas.logindata2
@dataprovider.DataDrive(testdata)
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
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.mall_page = Mall_Page()
        self.sign_page = Sign_Page()
        self.backpack_page = Backpack_Page()
        self.personinfo_page = Personinfo_Page()
        time.sleep(1)
        PHPInterface.add_money(self.casedata['mid'], 53000)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(2)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.start_step("进入商城页面")
        self.hall_page.wait_element("商城").click()
        time.sleep(2)
        self.mall_page.wait_element("道具页签").click()
        time.sleep(2)
        self.start_step("购买道具")
        self.mall_page.wait_element("提示卡").click()
        time.sleep(5)
        self.sign_page.wait_element("购买").click()
        time.sleep(2)
        self.hall_page.screenshot('bug.png')

    def post_test(self):
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata = test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C31053_DFCP_Mall_Interface_GetPro(TestCase):
    '''
    金条购买银币
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.mall_page = Mall_Page()
        self.sign_page = Sign_Page()
        self.backpack_page = Backpack_Page()
        self.personinfo_page = Personinfo_Page()
        time.sleep(1)
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        crystal = eval(dict).get('result', {'crystal': None}).get('crystal')  # 获取当前金条值
        AddCrystal = 1000 - crystal
        PHPInterface.add_crystal(UserID, AddCrystal)  # 将金条数目置1000
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(2)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.start_step("进入商城页面")
        self.hall_page.wait_element("商城").click()
        time.sleep(2)
        self.mall_page.wait_element("银币页签").click()
        time.sleep(2)
        self.start_step("购买道具")
        self.mall_page.wait_element("提示卡").click()
        time.sleep(5)
        self.sign_page.wait_element("购买").click()
        time.sleep(2)
        self.hall_page.screenshot('bug.png')

    def post_test(self):
        self.common.deletefile(self.luadriver)
        self.common.closedriver()
# __qtaf_seq_tests__ = [C31056_DFQP_Mall]
if __name__ == '__main__':
    # C002_DFQP_Login_GuestLogin = C002_DFQP_Login_GuestLogin()
    # C002_DFQP_Login_GuestLogin.debug_run()
    debug_run_all()
