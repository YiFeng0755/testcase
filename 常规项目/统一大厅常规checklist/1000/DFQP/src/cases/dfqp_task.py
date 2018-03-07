#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
地方棋牌每日任务
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.task_page import Task_Page
from uilib.hall_page import Hall_Page
from common.common import Common

class C014_DFQP_Share1(TestCase):
    '''
    大厅进入任务页面---微信邀请好友
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
        self.task_page = Task_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入任务页面")
        self.hall_page.wait_element("任务").click()
        # time.sleep(1)
        # self.hall_page.wait_element("每日任务tag")
        time.sleep(5)
        self.start_step("微信邀请好友")
        try:
            self.task_page.wait_element("微信邀请好友").click()
            # self.luadriver.find_element_by_xpath("//element/element/taskRewardLayout/content/dayTaskListView/element/dayTaskItem/bg/btn/doTask").click()
            time.sleep(1)
            self.task_page.screenshot('C014_DFQP_Share1.png')
        except:
            print("暂未此任务")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C015_DFQP_Share2(TestCase):
    '''
    大厅进入任务页面---微信分享
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
        self.task_page = Task_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入任务页面")
        self.hall_page.wait_element("任务").click()
        # time.sleep(1)
        # self.hall_page.wait_element("每日任务tag")
        time.sleep(2)
        self.start_step("微信分享")
        self.task_page.wait_element("微信分享").click()
        time.sleep(1)
        self.task_page.screenshot('C015_DFQP_Share2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

# __qtaf_seq_tests__ = [C014_DFQP_Share1,C015_DFQP_Share2]
if __name__ == '__main__':
    # C014_DFQP_Share1 = C014_DFQP_Share1()
    # C014_DFQP_Share1.debug_run()
    debug_run_all()
