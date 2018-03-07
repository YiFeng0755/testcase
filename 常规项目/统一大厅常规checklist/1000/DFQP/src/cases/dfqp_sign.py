#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
地方棋牌签到测试
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.sign_page import Sign_Page
from uilib.hall_page import Hall_Page
from common.common import Common

class C010_DFQP_Sign(TestCase):
    '''
    每日签到
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.sign_page = Sign_Page()
        self.hall_page = Hall_Page()


    def run_test(self):
        '''
        测试用例
        '''
        time.sleep(4)
        try:
            self.luadriver.find_element_by_xpath('//*[contains(@text, "允许")]').click()
        except:
            "未出现按钮"
        self.start_step("等待页面加载完成")
        time.sleep(10)
        #声明方法
        self.start_step("开始签到")
        try:
            self.hall_page.wait_element("确认登陆").click()
        except:
            "未出现登陆按钮"
        try:
            if (self.sign_page.wait_element("每日签到页面")):
                self.sign_page.wait_element("签到").click()
                self.sign_page.screenshot('C010_DFQP_Sign.png')
                print "签到成功"
                time.sleep(2)
        except:
            print "没有签到"
        self.common.closeactivity(self.luadriver)
        self.common.closefloatBall()
        self.start_step("验证签到是否成功")
        self.hall_page.wait_element("任务").click()
        time.sleep(3)
        self.start_step("切换每日签到页面")
        self.sign_page.get_element("每日签到页面").click()
        time.sleep(3)
        self.sign_page.wait_element("获取")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C011_DFQP_Sign_Daytask(TestCase):
    '''
    大厅进入任务页面---签到
    '''
    owner = "Lucyliu"
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
        self.sign_page = Sign_Page()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进入任务页面")
        self.hall_page.wait_element("任务").click()
        time.sleep(3)
        self.start_step("切换每日签到页面")
        self.sign_page.get_element("每日签到tag").click()
        time.sleep(2)
        self.sign_page.wait_element("每日签到页面")
        time.sleep(1)
        self.sign_page.wait_element("关闭1").click()
        time.sleep(2)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C012_DFQP_Sign_Resign(TestCase):
    '''
    大厅进入任务页面---补签
    '''
    owner = "Lucyliu"
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
        self.sign_page = Sign_Page()

    def run_test(self):
        self.start_step("进入任务页面")
        self.hall_page.wait_element("任务").click()
        time.sleep(3)
        self.start_step("切换每日签到页面")
        self.sign_page.get_element("每日签到tag").click()
        time.sleep(2)
        try:
            self.sign_page.wait_element("补签").click()
        except:
            print "当前用户今天已经签过到"
        self.sign_page.wait_element("获取").click()
        time.sleep(10)
        self.start_step("购买补签卡")
        self.sign_page.wait_element("购买").click()
        self.sign_page.screenshot('C012_DFQP_Resign.png')


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C013_DFQP_Sign_VIPtab(TestCase):
    '''
    点击开通vip按钮
    '''
    owner = "Lucyliu"
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
        self.sign_page = Sign_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入任务页面")
        self.hall_page.wait_element("任务").click()
        time.sleep(4)
        self.hall_page.wait_element("每日任务页面")
        time.sleep(1)
        self.start_step("切换每日签到页面")
        self.sign_page.get_element("每日签到tag").click()
        time.sleep(2)
        self.sign_page.wait_element("签到页面返回").click()
        time.sleep(2)
        self.start_step("点击开通vip")
        self.sign_page.wait_element("开通vip").click()
        time.sleep(2)
        self.sign_page.screenshot('C013_DFQP_VIPtab.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

__qtaf_seq_tests__ = [C012_DFQP_Sign_Resign]
if __name__ == '__main__':
    # C012_DFQP_Sign_Resign = C012_DFQP_Sign_Resign()
    # C012_DFQP_Sign_Resign.debug_run()
    debug_run_all()
