#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
重连_游戏币房
'''
import json
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from utils import constant
from utils.confighelper import ConfigHelper

from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common
import test_datas
from datacenter import dataprovider
import common.Interface as PHPInterface

class C70621_Moneyroom_Noready_Back(TestCase):
    '''
    玩家进入银币/金条房间未准备，短时间切换后台
    '''
    owner = "LucyLiu"
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
        self.start_step("获取mid")
        mid = self.common.get_mid()
        self.start_step("设置为20000银币")
        self.common.set_coin(mid=mid,value='20000')
        self.common.switchserver()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建银币/金条房")
        self.yuepai_page.create_room("创建银币金条房")
        time.sleep(5)
        if (self.yuepai_page.element_is_exist("准备") or self.yuepai_page.element_is_exist("已准备")):
            self.yuepai_page.screenshot("before.png")
            self.start_step("home键")
            self.luadriver.keyevent(3)  # home
            time.sleep(2)
            self.yuepai_page.screenshot("being.png")
            # self.yuepai_page.wait_element("准备")
            self.start_step("拉起游戏")
            config=ConfigHelper(constant.cfg_path)
            self.luadriver.start_activity(config.getValue('appium','apppackage'), config.getValue('appium','appactivity'))
            time.sleep(1)
            self.yuepai_page.screenshot("after.png")
            if (self.yuepai_page.element_is_exist("准备") or self.yuepai_page.element_is_exist("已准备")):
                pass
            else:
                self.log_info("当前页面未展示准备按钮")
            self.start_step("退出约牌房")
            self.yuepai_page.exit_yuepai_page()
            self.hall_page.wait_element("同步标志")
        else:
            self.yuepai_page.screenshot("error.png")
            raise Exception("未出现所需要的准备按钮")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70621_Moneyroom_Noready_Lock(TestCase):
    '''
    玩家进入银币/金条房间未准备，短时间锁屏
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
        self.start_step("获取mid")
        mid = self.common.get_mid()
        self.start_step("设置为20000银币")
        self.common.set_coin(mid=mid,value='20000')
        self.common.switchserver()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建银币/金条房")
        self.yuepai_page.create_room("创建银币金条房")
        if (self.yuepai_page.element_is_exist("准备") or self.yuepai_page.element_is_exist("已准备")):
            time.sleep(10)
            self.yuepai_page.screenshot("before.png")
            self.start_step("锁屏")
            self.luadriver.keyevent(26)  # 锁屏
            time.sleep(2)
            self.yuepai_page.screenshot("being.png")
            self.start_step("解锁")
            self.common.unlock()
            time.sleep(6)
            self.yuepai_page.screenshot("after.png")
            if (self.yuepai_page.element_is_exist("准备") or self.yuepai_page.element_is_exist("已准备")):
                pass
            else:
                self.log_info("当前页面未展示准备按钮")
            self.start_step("退出约牌房")
            self.yuepai_page.exit_yuepai_page()
            self.hall_page.wait_element("同步标志")
        else:
            self.yuepai_page.screenshot("error.png")
            raise Exception("未出现所需要的准备按钮")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70622_Moneyroom_Noready_Back_Longtime(TestCase):
    '''
    玩家进入银币/金条房间未准备 长时间切换后台
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 12

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        capabilities = {}
        capabilities['newCommandTimeout'] = 60*3
        self.luadriver = self.common.setupdriver(capabilities)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.start_step("获取mid")
        mid = self.common.get_mid()
        self.start_step("设置为20000银币")
        self.common.set_coin(mid=mid,value='20000')
        self.common.switchserver()
        self.common.closeactivity(self.luadriver)


    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建银币/金条房")
        self.yuepai_page.create_room("创建银币金条房")
        if (self.yuepai_page.element_is_exist("准备") or self.yuepai_page.element_is_exist("已准备")):
            time.sleep(10)
            self.yuepai_page.screenshot("before.png")
            self.start_step("切换到后台")
            self.luadriver.keyevent(3)  # home
            time.sleep(2*60)
            self.yuepai_page.screenshot("being.png")
            self.common.unlock()
            time.sleep(4)
            self.yuepai_page.screenshot("agfter.png")
            if (self.yuepai_page.element_is_exist("准备") or self.yuepai_page.element_is_exist("已准备")):
                pass
            else:
                self.log_info("当前页面未展示准备按钮")
            self.start_step("退出约牌房")
            self.yuepai_page.exit_yuepai_page()
            self.hall_page.wait_element("同步标志")
        else:
            self.log_info("未出现准备按钮")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70622_Moneyroom_Noready_Lock_Longtime(TestCase):
    '''
    玩家进入金银币房间，长时间锁屏
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 12

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        capabilities = {}
        capabilities['newCommandTimeout'] = 60*3
        self.luadriver = self.common.setupdriver(capabilities)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.start_step("获取mid")
        mid = self.common.get_mid()
        self.start_step("设置为20000银币")
        self.common.set_coin(mid=mid,value='20000')
        self.common.switchserver()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建银币/金条房")
        self.yuepai_page.create_room("创建银币金条房")
        if (self.yuepai_page.element_is_exist("准备") or self.yuepai_page.element_is_exist("已准备")):
            time.sleep(10)
            self.yuepai_page.screenshot("before.png")
            self.start_step("锁屏")
            self.luadriver.keyevent(26)  # 锁屏
            time.sleep(2*60)
            self.yuepai_page.screenshot("being.png")
            self.start_step("解锁")
            self.common.unlock()
            time.sleep(10)
            self.yuepai_page.screenshot("after.png")
            if (self.yuepai_page.element_is_exist("准备") or self.yuepai_page.element_is_exist("已准备")):
                pass
            else:
                self.log_info("当前页面未展示准备按钮")
            self.start_step("退出约牌房")
            self.yuepai_page.exit_yuepai_page()
            self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70627_Moneyroom_Ready_Back(TestCase):
    '''
    玩家进入银币/金条房间已准备，短时间切换后台
    '''
    owner = "LucyLiu"
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
        self.start_step("获取mid")
        mid = self.common.get_mid()
        self.start_step("设置为20000银币")
        self.common.set_coin(mid=mid,value='20000')
        self.common.switchserver()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建银币/金条房")
        self.yuepai_page.create_room("创建银币金条房")
        try:
            self.yuepai_page.wait_element("准备",120).click()
        except:
            self.log_info("当前页面未展示准备按钮")
        self.yuepai_page.element_is_exist("已准备")
        self.yuepai_page.screenshot("before.png")
        self.start_step("home键")
        self.luadriver.keyevent(3)  # home
        time.sleep(2)
        self.yuepai_page.screenshot("being.png")
        # self.yuepai_page.wait_element("准备")
        self.start_step("拉起游戏")
        config=ConfigHelper(constant.cfg_path)
        self.luadriver.start_activity(config.getValue('appium','apppackage'), config.getValue('appium','appactivity'))
        time.sleep(1)
        self.yuepai_page.screenshot("after.png")
        self.yuepai_page.element_is_exist("已准备")
        self.start_step("退出约牌房")
        self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70627_Moneyroom_Ready_Lock(TestCase):
    '''
    玩家进入银币/金条房间已准备，短时间锁屏
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
        self.start_step("获取mid")
        mid = self.common.get_mid()
        self.start_step("设置为20000银币")
        self.common.set_coin(mid=mid,value='20000')
        self.common.switchserver()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建银币/金条房")
        self.yuepai_page.create_room("创建银币金条房")
        try:
            self.yuepai_page.wait_element("准备",30).click()
        except:
            self.log_info("当前页面未展示准备按钮")
        self.yuepai_page.element_is_exist("已准备")
        time.sleep(10)
        self.yuepai_page.screenshot("before.png")
        self.start_step("锁屏")
        self.luadriver.keyevent(26)  # 锁屏
        time.sleep(2)
        self.yuepai_page.screenshot("being.png")
        self.start_step("解锁")
        self.common.unlock()
        time.sleep(6)
        self.yuepai_page.screenshot("after.png")
        self.yuepai_page.element_is_exist("已准备")
        self.start_step("退出约牌房")
        self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70628_Moneyroom_Ready_Back_Longtime(TestCase):
    '''
    玩家进入银币/金条房间已准备 长时间切换后台
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        capabilities = {}
        capabilities['newCommandTimeout'] = 60*3
        self.luadriver = self.common.setupdriver(capabilities)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.start_step("获取mid")
        mid = self.common.get_mid()
        self.start_step("设置为20000银币")
        self.common.set_coin(mid=mid,value='20000')
        self.common.switchserver()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建银币/金条房")
        self.yuepai_page.create_room("创建银币金条房")
        try:
            self.yuepai_page.wait_element("准备",30).click()
        except:
            self.log_info("当前页面未展示准备按钮")
        self.yuepai_page.element_is_exist("已准备")
        time.sleep(10)
        self.yuepai_page.screenshot("before.png")
        self.start_step("切换到后台")
        self.luadriver.keyevent(3)  # home
        time.sleep(2*60)
        self.yuepai_page.screenshot("being.png")
        self.common.unlock()
        time.sleep(4)
        self.yuepai_page.screenshot("agfter.png")
        self.yuepai_page.element_is_exist("已准备")
        self.start_step("退出约牌房")
        self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70628_Moneyroom_Ready_Lock_Longtime(TestCase):
    '''
    玩家进入金银币房间已准备，长时间锁屏
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 12

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        capabilities = {}
        capabilities['newCommandTimeout'] = 60*3
        self.luadriver = self.common.setupdriver(capabilities)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.start_step("获取mid")
        mid = self.common.get_mid()
        self.start_step("设置为20000银币")
        self.common.set_coin(mid=mid,value='20000')
        self.common.switchserver()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建银币/金条房")
        self.yuepai_page.create_room("创建银币金条房")
        try:
            self.yuepai_page.wait_element("准备",30).click()
        except:
            self.log_info("当前页面未展示准备按钮")
        self.yuepai_page.element_is_exist("已准备")
        time.sleep(10)
        self.yuepai_page.screenshot("before.png")
        self.start_step("锁屏")
        self.luadriver.keyevent(26)  # 锁屏
        time.sleep(2*60)
        self.yuepai_page.screenshot("being.png")
        self.start_step("解锁")
        self.common.unlock()
        time.sleep(10)
        self.yuepai_page.screenshot("after.png")
        self.yuepai_page.element_is_exist("已准备")
        self.start_step("退出约牌房")
        self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

__qtaf_seq_tests__ = [C70628_Moneyroom_Ready_Back_Longtime]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
