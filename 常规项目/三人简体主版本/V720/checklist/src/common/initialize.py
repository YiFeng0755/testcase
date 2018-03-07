#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
用例初始化
'''
import re
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from common import Common
from uilib.hall_page import Hall_Page

class TestCase_Initialize(TestCase):
    '''
    用例初始化
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()
        # self.common.user_money(money=5000)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        # env = self.common.get_config_value('casecfg', 'env')
        self.start_step("获取mid")
        mid = self.common.get_mid()
        self.common.set_config_value("casecfg","mid",str(mid))
        print self.common.get_config_value("casecfg","mid")
        # if env == '1':
        #     self.common.recover_user(str(mid))
        # else:
        #     self.log_info("当前环境非测试环境")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

# __qtaf_seq_tests__ = [C039_DFQP_Activity]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
