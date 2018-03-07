#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
签到
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.sign_page import Sign_Page
from uilib.hall_page import Hall_Page
from common.common import Common

class C30960_DFQP_Sign(TestCase):
    '''
    每日签到--签到默认页面显示
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
        time.sleep(4)
        try:
            self.luadriver.find_element_by_xpath('//*[contains(@text, "允许")]').click()
        except:
            "未出现按钮"
        self.start_step("等待页面加载完成")
        time.sleep(10)
        self.start_step("签到页面")
        try:
            self.hall_page.wait_element("确认登陆").click()
        except:
            "未出现登陆按钮"
        self.hall_page.screenshot("sign1.png")
        try:
            if (self.sign_page.wait_element("每日签到页面")):
                self.sign_page.screenshot('sign2.png')
                time.sleep(2)
        except:
            print "没有签到"

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C30961_DFQP_Sign(TestCase):
    '''
    每日签到--非VIP账号
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
        time.sleep(4)
        try:
            self.luadriver.find_element_by_xpath('//*[contains(@text, "允许")]').click()
        except:
            "未出现按钮"
        self.start_step("等待页面加载完成")
        time.sleep(10)
        self.start_step("开始签到")
        try:
            self.hall_page.wait_element("确认登陆").click()
        except:
            "未出现登陆按钮"
        self.hall_page.screenshot("sign1.png")
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
        self.sign_page.get_element("每日签到tag").click()
        time.sleep(3)
        self.sign_page.wait_element("获取")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()


class C30962_DFQP_Sign_VIPtab(TestCase):
    '''
    签到界面vip购买
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
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
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
        self.sign_page.screenshot('VIPtab.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C30969_DFQP_SignShare1(TestCase):
    '''
    点击签到界面右侧广告
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
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入任务页面")
        self.hall_page.wait_element("任务").click()
        time.sleep(3)
        self.sign_page.wait_element("每日签到tag").click()
        time.sleep(5)
        self.start_step("微信邀请好友")
        try:
            self.sign_page.wait_element("微信邀请好友").click()
            time.sleep(3)
            self.sign_page.screenshot('SignShare.png')
        except:
            print("暂未此任务")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C30964_DFQP_BuSign(TestCase):
    '''
    无补签卡补签
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入任务页面")
        self.hall_page.wait_element("任务").click()
        time.sleep(3)
        self.sign_page.wait_element("每日签到tag").click()
        time.sleep(5)
        try:
            self.sign_page.wait_element('补签').click()
            self.start_step('进入补签页面')
        except:
            print '已签过到'
        self.start_step('第一次点击[补]开始补签')
        for i in range(1, 37):  # 轮询查找[补]按钮，找到便break循环
            element = self.luadriver.find_lua_element_by_xpath( '//element/element/taskRewardLayout/content/dayRewardView/buSignupView/calendarView/element/element/dayCalendarItem/bu[%d]' % i)
            element_name = element.get_attribute('name')
            if element_name =='bu':
                element.click()
                print '找到并点击了[补]按钮'
                try:
                    self.luadriver.find_element_by_name('okBtn').click()
                except:
                    print '已补签过'
                break
            else:
                print '继续查找[补]按钮'
        # try:
        #     elements = self.sign_page.get_elements("补")
        #     print elements
        #     print elements.len()
        #     if (elements.len() >0):
        #         elements[1].click()
        # except:
        #     print "补签失败"
        self.hall_page.screenshot("buqian.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()


__qtaf_seq_tests__ = [C30964_DFQP_BuSign]
if __name__ == '__main__':
    # C012_DFQP_Sign_Resign = C012_DFQP_Sign_Resign()
    # C012_DFQP_Sign_Resign.debug_run()
    debug_run_all()
