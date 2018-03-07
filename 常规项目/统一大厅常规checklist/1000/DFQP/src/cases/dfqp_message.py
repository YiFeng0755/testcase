#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌消息页面
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.message_page import Message_Page
from uilib.hall_page import Hall_Page
from common.common import Common

class C080_DFQP_Message_Enter(TestCase):
    '''
    大厅进入消息页面
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
        self.common.closeactivity(self.luadriver)
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看消息")
        try:
            self.message_page.wait_element("查看消息").click()
            self.message_page.wait_element("关闭对话框").click()
        except:
            print ("没有消息")

        self.message_page.wait_element("返回").click()
#        self.luadriver.keyevent(4)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()


# __qtaf_seq_tests__ = [C080_DFQP_Message_Enter]
if __name__ == '__main__':
    # C002_DFQP_Login_GuestLogin = C002_DFQP_Login_GuestLogin()
    # C002_DFQP_Login_GuestLogin.debug_run()
    debug_run_all()