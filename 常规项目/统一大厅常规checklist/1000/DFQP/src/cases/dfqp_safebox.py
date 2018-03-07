#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
地方棋牌保险箱页面
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.safebox_page import Safebox_Page
from uilib.hall_page import Hall_Page
from common.common import Common

class C033_DFQP_safebox1(TestCase):
    '''
    大厅进入保险箱-银币界面
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
        self.hall_page = Hall_Page()
        self.safebox_page = Safebox_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入保险箱页面")
        self.hall_page.wait_element("保险箱").click()
        time.sleep(2)
        self.safebox_page.wait_element("金条-老")
        self.safebox_page.screenshot( 'safebox1.png')
        self.safebox_page.wait_element("关闭对话框").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C034_DFQP_safebox2(TestCase):
    '''
    大厅进入保险箱-金币界面
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

        self.hall_page = Hall_Page()
        self.safebox_page = Safebox_Page()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进入保险箱页面")
        self.hall_page.wait_element("保险箱").click()
        time.sleep(1)
        self.safebox_page.wait_element("银币—老")
        self.start_step("切换到金条页面")
        time.sleep(2)
        self.safebox_page.get_element("金条-老").click()
        self.safebox_page.screenshot('safebox2.png')
        self.safebox_page.wait_element("关闭对话框").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C035_DFQP_Safebox_SilverReset(TestCase):
    '''
    大厅进入保险箱-银币界面
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

        self.hall_page = Hall_Page()
        self.safebox_page = Safebox_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入保险箱页面")
        # self.luadriver.find_element_by_xpath("//element/element/hall/bottomBtnsView/element/hall_bottom_btns/setting").click()
        self.hall_page.wait_element("保险箱").click()
        time.sleep(1)
        self.safebox_page.wait_element("金条-老")
        self.safebox_page.screenshot('SilverReset1.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C036_DFQP_Safebox_GoldReset(TestCase):
    '''
    大厅进入保险箱-银币界面
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
        self.hall_page = Hall_Page()
        self.safebox_page = Safebox_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入保险箱页面")
        # self.luadriver.find_element_by_xpath("//element/element/hall/bottomBtnsView/element/hall_bottom_btns/setting").click()
        self.hall_page.wait_element("保险箱").click()
        time.sleep(1)
        self.safebox_page.wait_element("金条-老")
        self.start_step("切换到金条页面")
        time.sleep(2)
        # self.luadriver.find_element_by_name("bullionRadioButton").click()
        self.safebox_page.get_element("金条-老").click()
        self.safebox_page.screenshot('GoldReset1.png')
        self.safebox_page.wait_element("关闭对话框").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C037_DFQP_Safebox_SilverReset1(TestCase):
    '''
    大厅进入保险箱-银币界面
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

        self.hall_page = Hall_Page()
        self.safebox_page = Safebox_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入保险箱页面")
        # self.luadriver.find_element_by_xpath("//element/element/hall/bottomBtnsView/element/hall_bottom_btns/setting").click()
        self.hall_page.wait_element("保险箱").click()
        time.sleep(1)
        self.safebox_page.wait_element("金条-老")
        self.safebox_page.wait_element("减少金条/银条数目").click()
        self.safebox_page.wait_element("减少金条/银条数目").click()
        self.safebox_page.wait_element("增加金条/银条数目").click()
        self.safebox_page.screenshot('SilverReset11.png')
        self.safebox_page.wait_element("重置").click()
        self.safebox_page.screenshot('SilverReset12.png')
        self.safebox_page.wait_element("关闭对话框").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C038_DFQP_Safebox_GoldReset1(TestCase):
    '''
    大厅进入保险箱-银币界面
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
        self.hall_page = Hall_Page()
        self.safebox_page = Safebox_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入保险箱页面")
        # self.luadriver.find_element_by_xpath("//element/element/hall/bottomBtnsView/element/hall_bottom_btns/setting").click()
        self.hall_page.wait_element("保险箱").click()
        time.sleep(1)
        self.safebox_page.wait_element("银币—老")
        self.start_step("切换到金条页面")
        time.sleep(2)
        # self.luadriver.find_element_by_name("bullionRadioButton").click()
        self.safebox_page.get_element("金条-老").click()
        time.sleep(2)
        self.safebox_page.wait_element("减少金条/银条数目").click()
        self.safebox_page.wait_element("减少金条/银条数目").click()
        self.safebox_page.wait_element("增加金条/银条数目").click()
        self.safebox_page.screenshot('GoldReset11.png')
        self.safebox_page.wait_element("重置").click()
        self.safebox_page.screenshot('GoldReset12.png')
        self.safebox_page.wait_element("关闭对话框").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

# __qtaf_seq_tests__ = [C033_DFQP_safebox1,C034_DFQP_safebox2,C035_DFQP_Safebox_SilverReset,C036_DFQP_Safebox_GoldReset,C037_DFQP_Safebox_SilverReset1,C038_DFQP_Safebox_GoldReset1]
if __name__ == '__main__':
    # C034_DFQP_safebox2 = C034_DFQP_safebox2()
    # C034_DFQP_safebox2.debug_run()
    debug_run_all()
