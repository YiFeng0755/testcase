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
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.hall_page = Hall_Page()
        self.mall_page = Mall_Page()
        self.sign_page = Sign_Page()
        self.backpack_page = Backpack_Page()
        self.personinfo_page = Personinfo_Page()
        time.sleep(1)
        cid = self.common.get_cid()
        global mid
        mid = PHPInterface.get_mid(cid, region=1)
        print "用户mid为：%s" % mid
        PHPInterface.add_money(mid, 53000)
        # self.hall_page.wait_element("头像").click()
        # time.sleep(2)
        # if self.personinfo_page.wait_element("账号ID").get_attribute('text') != user_info['cid']:
        #     self.common.loginuser(user_info['user'], user_info['password'])
        # try:
        #     self.personinfo_page.wait_element("关闭").click()
        # except:
        #     print "已关闭窗口"

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
        # self.common.release_user(user_info['mid'])
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

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
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.mall_page = Mall_Page()
        self.sign_page = Sign_Page()
        self.backpack_page = Backpack_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        # time.sleep(1)
        self.start_step("获取账号mid")
        cid = self.common.get_cid()
        global mid
        mid = PHPInterface.get_mid(cid, region=1)
        print "用户mid为：%s" % mid
        # UserID = user_info.get('mid')
        # print 'UserID:%s' % UserID
        dict = PHPInterface.get_user_info(mid)  # 获取玩家信息
        crystal = eval(dict).get('result', {'crystal': None}).get('crystal')  # 获取当前金条值
        #初始化银币
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 20000 - int(coin)
        print AddMoney
        PHPInterface.add_money(mid, AddMoney)  # 将设置银币值

        AddCrystal = 450 - crystal
        PHPInterface.add_crystal(mid, AddCrystal)  # 将金条数目置1400
        # self.hall_page.wait_element("预发布").click()
        # time.sleep(15)
        # self.common.closeActivityBtn()

        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        # self.common.closeactivitytest(self.luadriver)
        # self.hall_page.wait_element("头像").click()
        # time.sleep(2)
        # if self.personinfo_page.wait_element("账号ID").get_attribute('text') != user_info['cid']:
        #     self.common.loginuser(user_info['user'], user_info['password'])
        # try:
        #     self.personinfo_page.wait_element("关闭").click()
        # except:
        #     print "已关闭窗口"

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
        while(self.hall_page.is_exist("立即升级绑定账号")):
            self.sign_page.wait_element("关闭1").click()
        while(self.mall_page.is_exist("银币页面购买")==False):
            self.mall_page.wait_element("银币购买1").click()
        self.mall_page.wait_element("银币页面购买").click()
        time.sleep(5)
        self.hall_page.screenshot('buy.png')

    def post_test(self):
        try:
            dict = PHPInterface.get_user_info(mid)  # 获取玩家信息
            crystal = eval(dict).get('result', {'crystal': None}).get('crystal')  # 获取当前金条值
            coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
            AddCrystal = 100 - crystal
            AddMoney = 20000 - int(coin)
            PHPInterface.add_money(mid, AddMoney)  # 将设置银币值
            PHPInterface.add_crystal(mid, AddCrystal)  # 将金条数目置1000
        except:
            self.log_info("初始化银币金条报错")
        try:
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(mid)

__qtaf_seq_tests__ = [C31053_DFCP_Mall_Interface_GetPro]
if __name__ == '__main__':
    # C002_DFQP_Login_GuestLogin = C002_DFQP_Login_GuestLogin()
    # C002_DFQP_Login_GuestLogin.debug_run()
    debug_run_all()
