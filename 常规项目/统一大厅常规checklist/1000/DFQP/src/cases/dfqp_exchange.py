#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Author: MindyZhang
'''
大厅兑换
'''
import time
from runcenter.enums import EnumStatus,EnumPriority
from runcenter.testcase import debug_run_all,TestCase
from common.common import Common
from uilib.hall_page import Hall_Page
from uilib.exchange_page import Exchange_Page

class C100_DFQP_ExChange(TestCase):
    '''
    大厅兑换---兑奖页面显示
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        # 关闭活动弹框
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.exchange_page = Exchange_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("点击更多按钮")
        self.exchange_page.wait_element("更多").click()
        self.start_step("点击兑换")
        self.exchange_page.wait_element("兑换").click()
        time.sleep(3)
        self.exchange_page.screenshot("C100_DFQP_Exchange1.png")
        self.exchange_page.wait_element("手机流量包").click()
        time.sleep(3)
        self.exchange_page.screenshot("C100_DFQP_Exchange2.png")
        self.exchange_page.wait_element("数码家电").click()
        time.sleep(3)
        self.exchange_page.screenshot("C100_DFQP_Exchange3.png")

        self.exchange_page.wait_element("手机充值卡").click()
        time.sleep(3)
        self.exchange_page.screenshot("C100_DFQP_Exchange4.png")
        self.exchange_page.wait_element("返回").click()
        time.sleep(3)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C101_DFQP_ExChange_Record(TestCase):
    '''
    大厅兑换---兑奖记录---无兑奖记录
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        # 关闭活动弹框
        self.common.closeactivity(self.luadriver)

        self.hall_page = Hall_Page()
        self.exchange_page = Exchange_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("点击更多按钮")
        self.exchange_page.wait_element("更多").click()
        self.start_step("点击兑换")
        self.exchange_page.wait_element("兑换").click()
        time.sleep(3)
        self.exchange_page.wait_element("兑换-兑奖记录").click()
        self.exchange_page.screenshot("Exchange_record.png")
        print("无兑奖记录")
        self.exchange_page.wait_element("兑换商品").click()
        time.sleep(2)
        self.exchange_page.wait_element("返回").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C102_DFQP_ExChange_Diamond(TestCase):
    '''
    大厅兑换---兑奖---钻石不足
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        # 关闭活动弹框
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.exchange_page = Exchange_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        self.start_step("点击更多按钮")
        self.exchange_page.wait_element("更多").click()

        self.start_step("点击兑换")
        self.exchange_page.wait_element("兑换").click()
        time.sleep(3)
        self.exchange_page.wait_element("手机流量包").click()
        time.sleep(3)
        self.exchange_page.wait_element("兑换按钮").click()
        time.sleep(3)
        self.exchange_page.screenshot('Exchange_Diamond1.png')
        self.exchange_page.wait_element("钻石余额不足-确定").click()
        time.sleep(3)
        print ("钻石余额不足")
        self.exchange_page.wait_element("数码家电").click()
        time.sleep(3)
        self.exchange_page.wait_element("兑换按钮").click()
        time.sleep(3)
        self.exchange_page.screenshot("Exchange_Diamond2.png")
        self.exchange_page.wait_element("钻石余额不足-确定").click()
        time.sleep(3)
        self.exchange_page.wait_element("手机充值卡").click()
        time.sleep(3)
        self.exchange_page.wait_element("手机充值卡-兑换2").click()
        time.sleep(3)
        self.exchange_page.wait_element("钻石余额不足-确定").click()
        time.sleep(3)
        self.exchange_page.wait_element("手机充值卡-兑换3").click()
        time.sleep(3)
        self.exchange_page.wait_element("钻石余额不足-确定").click()
        time.sleep(3)
        self.exchange_page.wait_element("返回").click()
        time.sleep(3)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

if __name__ == "__main__":
    # C100_DFQP_ExChange = C100_DFQP_ExChange()
    # C100_DFQP_ExChange.debug_run()
    debug_run_all()