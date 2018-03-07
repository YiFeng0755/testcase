#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
商城
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.mall_page import Mall_Page
from uilib.hall_page import Hall_Page
from common.common import Common

class C31049_DFQP_Mall(TestCase):
    '''
    商城界面显示
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver, "切换环境")
        self.hall_page = Hall_Page()
        self.mall_page = Mall_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入商城页面")
        self.hall_page.wait_element("商城").click()
        time.sleep(2)
        self.mall_page.get_element("银币页签").click()
        time.sleep(2)
        self.mall_page.screenshot('Mall1.png')
        self.mall_page.wait_element("金条页签").click()
        time.sleep(2)
        self.mall_page.screenshot('Mall2.png')
        self.mall_page.wait_element("道具页签").click()
        time.sleep(2)
        self.mall_page.screenshot('Mall3.png')
        self.mall_page.wait_element("VIP页签").click()
        time.sleep(2)
        self.mall_page.screenshot('Mall4.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31056_DFQP_Mall_zhifubao(TestCase):
    '''
    安装支付宝支付界面显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver, "切换环境")
        self.hall_page = Hall_Page()
        self.mall_page = Mall_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入商城页面")
        self.hall_page.wait_element("商城").click()
        time.sleep(5)
        self.mall_page.get_element("金条商品").click()
        time.sleep(2)
        self.mall_page.screenshot('zhifu.png')
        time.sleep(2)
        try:
            self.mall_page.get_element("支付宝").click()
            self.mall_page.screenshot('zhifubao.png')
        except:
            print "需升级为手机号码"

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

__qtaf_seq_tests__ = [C31049_DFQP_Mall]
if __name__ == '__main__':
    # C002_DFQP_Login_GuestLogin = C002_DFQP_Login_GuestLogin()
    # C002_DFQP_Login_GuestLogin.debug_run()
    debug_run_all()
