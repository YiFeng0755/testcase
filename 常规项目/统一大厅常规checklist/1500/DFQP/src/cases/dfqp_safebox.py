#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
保险箱
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.safebox_page import Safebox_Page
from uilib.hall_page import Hall_Page
from common.common import Common

class C31043_DFQP_safebox1(TestCase):
    '''
    查看保险箱主界面显示
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
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.hall_page = Hall_Page()
        self.safebox_page = Safebox_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入保险箱页面")
        self.hall_page.wait_element("保险箱").click()
        time.sleep(2)
        self.safebox_page.screenshot( 'coin.png')
        self.safebox_page.wait_element("金条保险箱").click()
        time.sleep(2)
        self.safebox_page.screenshot( 'gold.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

# __qtaf_seq_tests__ = [C30964_DFQP_BuSign]
if __name__ == '__main__':
    # C31043_DFQP_safebox1 = C31043_DFQP_safebox1()
    # C31043_DFQP_safebox1.debug_run()
    debug_run_all()
