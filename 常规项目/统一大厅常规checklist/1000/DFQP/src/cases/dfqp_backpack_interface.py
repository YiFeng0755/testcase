#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌物品箱接口
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
from common.common import Common
import test_datas
from datacenter import dataprovider
import common.Interface as PHPInterface

testdata=test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C307_DFCP_Backpack_Interface_GetPro(TestCase):
    '''
    购买道具，商城购买道具，查看物品箱
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
        self.hall_page.wait_element("同步标志")
        self.start_step("进入物品箱页面")
        time.sleep(2)
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack1.png')
        self.luadriver.keyevent(4)
        self.start_step("进入商城页面")
        self.hall_page.wait_element("商城").click()
        time.sleep(2)
        self.mall_page.wait_element("道具页签").click()
        time.sleep(2)
        self.start_step("购买道具")
        self.mall_page.wait_element("提示卡").click()
        time.sleep(5)
        self.sign_page.wait_element("购买").click()
        time.sleep(3)
        self.mall_page.wait_element("返回").click()
        time.sleep(3)
        self.start_step("进入物品箱页面")
        time.sleep(2)
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack2.png')

    def post_test(self):
        self.common.closedriver()

testdata = test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C308_DFCP_Backpack_Interface_GivePro(TestCase):
    '''
    物品箱有道具，且有兑奖记录，点击物品箱以及兑奖记录
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
        self.start_step("添加金币，用于购买道具")
        PHPInterface.add_money(self.casedata['mid'], 53000)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivitytest(self.luadriver)
        self.start_step("用户登录")
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
        self.hall_page.wait_element("同步标志")
        self.start_step("进入物品箱页面")
        time.sleep(2)
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack1.png')
        self.luadriver.keyevent(4)
        self.start_step("进入商城页面")
        self.hall_page.wait_element("商城").click()
        time.sleep(2)
        self.mall_page.wait_element("道具页签").click()
        time.sleep(2)
        self.start_step("购买道具")
        i = 0
        while (i < 3):
            i += 1
            try:
                self.sign_page.wait_element("提示卡").click()
                time.sleep(5)
                self.sign_page.wait_element("购买").click()
            except:
                time.sleep(1)
        time.sleep(3)
        self.start_step("进入物品箱页面")
        time.sleep(2)
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack2.png')

    def post_test(self):
        self.common.closedriver()

# __qtaf_seq_tests__ = [C308_DFCP_Backpack_Interface_GivePro]
if __name__ == '__main__':
    # C002_DFQP_Login_GuestLogin = C002_DFQP_Login_GuestLogin()
    # C002_DFQP_Login_GuestLogin.debug_run()
    debug_run_all()
