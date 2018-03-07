#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
战绩
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common

class C70524_Record_display(TestCase):
    '''
    约牌房战绩显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.screenshot("hall.png")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("查看战绩")
        time.sleep(10)
        self.yuepai_page.wait_element("战绩",30).click()
        # self.yuepai_page.wait_element("约牌战绩提示框",120).get_attribute("text")==u"您目前还没有约过牌，快来创建房间邀请好友一起玩吧~"
        self.yuepai_page.wait_element("约牌战绩提示框")
        self.start_step("进入免费记分房创建页面")
        self.yuepai_page.wait_element("免费记分房",30).click()
        self.yuepai_page.wait_element("记分房提示语").get_attribute("text")==u"提示：免费房结算积分，不收取任何费用，仅作娱乐或切磋牌技使用 。"
        self.yuepai_page.wait_element("建房页面关闭").click()
        # self.luadriver.keyevent(4)
        self.start_step("进入银币/金条房页面")
        self.yuepai_page.wait_element("战绩",30).click()
        self.yuepai_page.wait_element("银币金条房",30).click()
        self.yuepai_page.wait_element("开房限制")
        self.yuepai_page.wait_element("建房页面关闭").click()
        # self.luadriver.keyevent(4)
        self.start_step("约牌页面返回")
        self.yuepai_page.wait_element("返回")
        time.sleep(3)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70558_Yuepaipage_return(TestCase):
    '''
    点击物理返回键返回大厅
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.screenshot("hall.png")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        time.sleep(4)
        self.luadriver.keyevent(4)
        time.sleep(2)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

__qtaf_seq_tests__ = [C70524_Record_display]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
