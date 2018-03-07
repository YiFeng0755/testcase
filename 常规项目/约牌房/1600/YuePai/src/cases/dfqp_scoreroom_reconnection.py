#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
重连
'''
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

class C70527_Scoreroom_Enterroom(TestCase):
    '''
    玩家进入积分房间未准备，掉线重连
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
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.create_room('记分房')
        self.common.switchnetwork(self.luadriver, u"无网络")
        self.common.switchnetwork(self.luadriver, u"WIFI模式")
        self.common.network_connect()
        self.yuepai_page.screenshot("reconnect.png")
        # self.yuepai_page.wait_element("准备").click()
        # self.start_step("退出约牌房")
        # self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70531_Scoreroom_Noready_Back(TestCase):
    '''
    玩家进入积分房间未准备，短时间切换后台
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
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.create_room('记分房')
        time.sleep(10)
        self.yuepai_page.screenshot("before.png")
        self.luadriver.keyevent(3)  # home
        self.yuepai_page.screenshot("being.png")
        time.sleep(2)
        self.start_step("解锁")
        self.common.unlock()
        time.sleep(4)
        self.yuepai_page.screenshot("after.png")
        self.start_step("读配置,拉起游戏")
        self.yuepai_page.wait_element("准备")
        self.start_step("退出约牌房")
        self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70531_Scoreroom_Noready_Lock(TestCase):
    '''
    玩家进入积分房间未准备，短时间锁屏
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
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.create_room('记分房')
        time.sleep(10)
        self.yuepai_page.screenshot("before.png")
        self.start_step("锁屏")
        self.luadriver.keyevent(26)  # 锁屏
        time.sleep(2)
        self.yuepai_page.screenshot("being.png")
        # self.yuepai_page.wait_element("准备")
        self.start_step("解锁")
        self.common.unlock()
        time.sleep(10)
        self.yuepai_page.screenshot("after.png")
        self.yuepai_page.wait_element("准备",30)
        self.start_step("退出约牌房")
        self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70532_Scoreroom_Noready_Back_Longtime(TestCase):
    '''
    玩家进入积分房间未准备，长时间切换后台
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 8

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        # 初始化Luadriver
        self.start_step("初始化driver")
        capabilities = {}
        capabilities['newCommandTimeout'] = 60*3
        self.luadriver = self.common.setupdriver(capabilities)
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
        self.yuepai_page.create_room('记分房')
        time.sleep(10)
        self.yuepai_page.screenshot("before.png")
        self.luadriver.keyevent(3)  # home
        time.sleep(2*60)
        self.yuepai_page.screenshot("being.png")
        self.start_step("解锁")
        self.common.unlock()
        time.sleep(4)
        self.yuepai_page.screenshot("after.png")
        self.yuepai_page.wait_element("准备")
        self.start_step("退出约牌房")
        self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70532_Scoreroom_Noready_Lock_Longtime(TestCase):
    '''
    玩家进入积分房间未准备，长时间锁屏
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
        capabilities = {}
        capabilities['newCommandTimeout'] = 60*3
        self.luadriver = self.common.setupdriver(capabilities)
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
        self.yuepai_page.create_room('记分房')
        self.yuepai_page.screenshot("before.png")
        time.sleep(10)
        self.luadriver.keyevent(26)  # 锁屏
        time.sleep(2*60)
        self.yuepai_page.screenshot("being.png")
        # self.yuepai_page.wait_element("准备")
        self.start_step("解锁")
        self.common.unlock()
        self.yuepai_page.screenshot("after.png")
        self.yuepai_page.wait_element("准备")
        self.start_step("退出约牌房")
        self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70535_Scoreroom_ready_Back(TestCase):
    '''
    玩家进入积分房间已准备，短时间切换后台
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
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.create_room('记分房')
        time.sleep(10)
        self.yuepai_page.wait_element("准备").click()
        time.sleep(5)
        self.yuepai_page.screenshot("before.png")
        self.luadriver.keyevent(3)  # home
        time.sleep(2)
        self.yuepai_page.screenshot("being.png")
        self.start_step("读配置,拉起游戏")
        config = ConfigHelper(constant.cfg_path)
        self.luadriver.start_activity(config.getValue('appium', 'apppackage'), config.getValue('appium', 'appactivity'))
        time.sleep(1)
        self.yuepai_page.screenshot("after.png")
        self.yuepai_page.element_not_exist("准备")
        self.start_step("退出约牌房")
        self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70535_Scoreroom_ready_Lock(TestCase):
    '''
    玩家进入积分房间已准备，短时间锁屏
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
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.create_room('记分房')
        self.yuepai_page.wait_element("准备",30).click()
        time.sleep(5)
        self.yuepai_page.screenshot("before.png")
        self.start_step("锁屏")
        self.luadriver.keyevent(26)  # 锁屏
        time.sleep(2)
        self.yuepai_page.screenshot("being.png")
        # self.yuepai_page.wait_element("准备")
        self.start_step("解锁")
        self.common.unlock()
        time.sleep(10)
        self.yuepai_page.element_not_exist("准备")
        self.yuepai_page.screenshot("after.png")
        self.start_step("退出约牌房")
        self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70537_Scoreroom_Ready_Back_Longtime(TestCase):
    '''
    玩家进入积分房间未准备，长时间切换后台
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 8

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        # 初始化Luadriver
        self.start_step("初始化driver")
        capabilities = {}
        capabilities['newCommandTimeout'] = 60*3
        self.luadriver = self.common.setupdriver(capabilities)
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
        self.yuepai_page.create_room('记分房')
        self.yuepai_page.wait_element("准备",30).click()
        time.sleep(5)
        self.yuepai_page.screenshot("before.png")
        self.luadriver.keyevent(3)  # home
        time.sleep(2 * 60)
        self.yuepai_page.screenshot("being.png")
        self.start_step("解锁")
        self.common.unlock()
        time.sleep(4)
        self.yuepai_page.screenshot("after.png")
        self.yuepai_page.element_not_exist("准备")
        self.start_step("退出约牌房")
        self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70537_Scoreroom_Ready_Lock_Longtime(TestCase):
    '''
    玩家进入积分房间已准备，长时间锁屏
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
        capabilities = {}
        capabilities['newCommandTimeout'] = 60*3
        self.luadriver = self.common.setupdriver(capabilities)
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
        self.yuepai_page.create_room('记分房')
        self.yuepai_page.wait_element("准备",30).click()
        time.sleep(5)
        self.yuepai_page.screenshot("before.png")
        self.start_step("锁屏")
        self.luadriver.keyevent(26)  # 锁屏
        time.sleep(2 * 60)
        self.yuepai_page.screenshot("being.png")
        self.start_step("解锁")
        self.common.unlock()
        time.sleep(10)
        self.yuepai_page.screenshot("after.png")
        self.yuepai_page.element_not_exist("准备")
        self.start_step("退出约牌房")
        self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

__qtaf_seq_tests__ = [C70532_Scoreroom_Noready_Lock_Longtime]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
