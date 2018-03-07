#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
物品箱
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.backpack_page import Backpack_Page
from uilib.hall_page import Hall_Page
from common.common import Common

class C31033_DFQP_Backpack_Enterpack(TestCase):
    '''
    物品箱没有道具，也没有对讲纪录,点击物品箱以及兑奖记录
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.backpack_page = Backpack_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入物品箱页面")
        self.hall_page.wait_element("物品箱").click()
        self.hall_page.screenshot('1.png')
        self.hall_page.wait_element("兑奖记录").click()
        self.hall_page.screenshot('2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

# __qtaf_seq_tests__ = [C032_DFQP_Backpack_Enterpack]
if __name__ == '__main__':
    # C002_DFQP_Login_GuestLogin = C002_DFQP_Login_GuestLogin()
    # C002_DFQP_Login_GuestLogin.debug_run()
    debug_run_all()
