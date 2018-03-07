#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
创建界面
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common
from uilib.broadcast_page import Broadcast_Page
from appiumcenter.element import Element
import test_datas
from datacenter import dataprovider

class C61014_Friendroom_Create(TestCase):
    '''
    约牌房创建界面显示
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        # capabilities = {}
        # capabilities['noReset'] = True
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.yuepai_page.wait_element("创建银币金条房")
        self.yuepai_page.screenshot("create.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C61014_Countscore_Room(TestCase):
    '''
   记分房创建界面显示
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        # capabilities = {}
        # capabilities['noReset'] = True
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房', 20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0,len(elements)):
            self.start_step("查看%s记分房" % elements[i].get_attribute("text"))
            elements[i].click()
            self.yuepai_page.wait_element("开房")
            self.yuepai_page.screenshot("%d.png" % i)
        self.yuepai_page.wait_element("返回").click()
        self.yuepai_page.wait_element("记分房")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C61014_Notdownload_Apk(TestCase):
    '''
   未下载子游戏创建记分房界面显示
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):

        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        # capabilities = {}
        # capabilities['noReset'] = True
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房', 20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0,len(elements)):
            self.start_step("查看%s记分房" % elements[i].get_attribute("text"))
            elements[i].click()
            time.sleep(2)
            self.yuepai_page.screenshot("%d.png" % i)
            try:
                self.yuepai_page.wait_element('取消').click()
            except:
                print '未找到取消按钮'
        self.yuepai_page.wait_element("返回").click()
        self.yuepai_page.wait_element("记分房")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C61014_Diy_Choose(TestCase):
    '''
    DIY全部默认勾选创建积分房
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):

        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        # capabilities = {}
        # capabilities['noReset'] = True
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.common.closefloatBall()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房', 20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0,len(elements)):
            self.start_step("查看%s记分房" % elements[i].get_attribute("text"))
            elements[i].click()
            self.yuepai_page.enter_room()
            self.yuepai_page.screenshot("%d.png" % i)
            try:
                self.yuepai_page.wait_element("规则", 30).click()
                self.yuepai_page.screenshot("%d_rule.png" % i)
                self.yuepai_page.wait_element("规则关闭").click()
            except:
                self.log_info("%s游戏不存在规则按钮" % elements[i].get_attribute("text"))
            self.yuepai_page.exit_yuepai_page()
            try:
                self.yuepai_page.wait_element('记分房').click()
            except:
                self.log_info("未返回到记分房页面")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C61014_Diy_Part(TestCase):
    '''
    DIY部分默认勾选创建积分房
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房', 20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0,len(elements)):
            self.start_step("查看%s记分房" % elements[i].get_attribute("text"))
            elements[i].click()
            ele2 = self.yuepai_page.get_elements("Div控件局数")
            try:
                ele2[3].click()
                ele2[7].click()
                ele2[17].click()
                ele2[30].click()
            except:
                self.log_info("找不到此元素")
            self.yuepai_page.screenshot("%d_div.png" % i)
            self.yuepai_page.enter_room()
            self.yuepai_page.screenshot("%d.png" % i)
            try:
                self.yuepai_page.wait_element("规则", 30).click()
                self.yuepai_page.screenshot("%d_rule.png" % i)
                self.yuepai_page.wait_element("规则关闭").click()
            except:
                self.log_info("当前游戏无规则选项")
            self.yuepai_page.exit_yuepai_page()
            try:
                self.yuepai_page.wait_element('记分房').click()
            except:
                self.log_info("未返回到记分房页面")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C61014_Diy_All(TestCase):
    '''
    DIY全部非默认勾选创建积分房
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房', 20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0, len(elements)):
            self.start_step("查看%s记分房" % elements[i].get_attribute("text"))
            elements[i].click()
            ele2 = self.yuepai_page.get_elements("Div控件局数")
            print len(ele2)
            try:
                ele2[3].click()
                ele2[7].click()
                ele2[12].click()
                ele2[17].click()
                ele2[34].click()
            except:
                self.log_info("不存在此元素")
            self.yuepai_page.enter_room()
            self.yuepai_page.screenshot("%d.png" % i)
            try:
                self.yuepai_page.wait_element("规则", 30).click()
                self.yuepai_page.screenshot("%d_rule.png" % i)
                self.yuepai_page.wait_element("规则关闭").click()
            except:
                self.log_info("当前游戏无规则按钮")
            self.yuepai_page.exit_yuepai_page()
            try:
                self.yuepai_page.wait_element('记分房').click()
            except:
                self.log_info("未返回到记分房页面")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C61014_Fan_Zero(TestCase):
    '''
    记分房封顶番数输入0
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.broadcast_page = Broadcast_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房', 20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0,len(elements)):
            print elements[i].get_attribute("text")
            elements[i].click()
            time.sleep(2)
            ele2 = self.yuepai_page.get_elements('自定义1')
            try:
                ele2[9].click()
            except:
                self.log_info("不存在此元素")
            self.yuepai_page.screenshot("%d.png" % i)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C61014_Jushu_Zero(TestCase):
    '''
    记分房选择局数输入0
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):

        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        # self.broadcast_page = Broadcast_Page()
        self.start_step("初始化driver")
        # capabilities = {}
        # capabilities['noReset'] = True
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房', 20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0,len(elements)):
            print elements[i].get_attribute("text")
            elements[i].click()
            ele2 = self.yuepai_page.get_elements('自定义1')
            try:
                ele2[4].click()
                ele3 = self.yuepai_page.wait_element("输入文字").send_keys("0")
            except:
                self.log_info("当前游戏不存在此元素")
            self.yuepai_page.screenshot("%d.png" % i)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

'''
换座
'''
class C61014_Huanzhuo_Appear(TestCase):
    '''
   查看房间内换座显示
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):

        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.common.closefloatBall()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房',20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0, len(elements)):
            elements[i].click()
            self.start_step("进入%s记分房" % elements[i].get_attribute("text"))
            self.yuepai_page.enter_room()
            try:
                self.yuepai_page.wait_element("换座位").click()
            except:
                self.log_info("无法换座位")
            self.yuepai_page.screenshot("%d.png" %i)
            self.yuepai_page.exit_yuepai_page()
            try:
                self.yuepai_page.wait_element('记分房').click()
            except:
                self.log_info("未返回到记分房页面")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

__qtaf_seq_tests__ = [C61014_Diy_Part]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
