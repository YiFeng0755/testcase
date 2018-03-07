#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
活动
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from common.common import Common

class C31070_DFQP_Activity(TestCase):
    '''
    大厅进入活动页面
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        capabilities = {}
        capabilities['noReset'] = False
        capabilities['resetKeyboard'] = False
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver(capabilities)
        # self.common.deletefile(self.luadriver)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.hall_page = Hall_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入活动页面")
        self.hall_page.wait_element("活动").click()
        time.sleep(9)
        self.hall_page.screenshot('activity.png')
        # element = self.luadriver.find_elements_by_class_name("android.view.View")
        self.luadriver.keyevent(4)
        time.sleep(2)
        self.hall_page.wait_element("同步标志")

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
