#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌约牌测试
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from appiumcenter.luadriver import LuaDriver
from uilib.personinfo_page import Personinfo_Page
from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page
from uilib.safebox_page import Safebox_Page
from common.common import Common
from common import Interface as PHPInterface
import re
import json
import test_datas
from datacenter import dataprovider


class C31193_DFQP_Yuepai_CreateRoom_EnoughCrystal(TestCase):
    '''
    破产有金条时，创建金条约牌房
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid=mid, value='0')
        self.common.set_crystal(mid=mid,value="1000")
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(4)
        self.start_step('点击金条单选按钮')
        self.yuepai_page.wait_element('金条单选按钮').click()
        time.sleep(4)
        self.start_step('点击开房按钮')
        self.yuepai_page.wait_element('开房').click()
        try:
            if (self.yuepai_page.element_is_exist("立即升级") == True):
                self.yuepai_page.wait_element("关闭").click()
        except:
            print "无立即升级按钮"
        time.sleep(4)
        self.start_step('点击确定')
        try:
            self.yuepai_page.wait_element('确定').click()
            time.sleep(20)
        except:
            print '未找到确定按钮'
        Flag = True
        while Flag:
            try:
                self.yuepai_page.wait_element('开房').click()
            except:
                Flag = False
        try:
            self.yuepai_page.wait_element('准备ok')
            self.yuepai_page.screenshot('.png')
            print '成功创建房间'
        except:
            print '创建房间失败'
        time.sleep(10)
        self.start_step("退出约牌房")
        self.yuepai_page.wait_element("菜单键").click()
        time.sleep(3)
        self.yuepai_page.wait_element("退出键").click()
        time.sleep(4)
        self.yuepai_page.screenshot('exit.png')
        self.yuepai_page.wait_element("返回").click()
        time.sleep(3)
        self.hall_page.wait_element("同步标志")


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.recover_user(mid)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")


class C31194_DFQP_Yuepai_CreateRoom_NotEnoughCrystal(TestCase):
    '''
    破产金条不够，创建金条约牌房
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid=mid, value='0')
        self.common.set_crystal(mid=mid,value="0")
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(2)
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        self.start_step('点击金条单选按钮')
        self.yuepai_page.wait_element('金条单选按钮').click()
        self.start_step('点击开房按钮')
        self.yuepai_page.wait_element('开房').click()
        try:
            if (self.yuepai_page.element_is_exist("立即升级") == True):
                self.yuepai_page.wait_element("关闭").click()
        except:
            print "无立即升级按钮"
        self.start_step('点击确定')
        try:
            self.yuepai_page.wait_element('确定').click()
        except:
            print '未找到确定按钮'
        Flag = True
        while Flag:
            self.yuepai_page.wait_element('开房').click()
            try:
                self.yuepai_page.wait_element('支付')
                self.yuepai_page.screenshot('.png')
                Flag = False
            except:
                print '游戏下载中'

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.recover_user(mid)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")

class C31195_DFQP_Yuepai_CreateScoreRoom_Broke(TestCase):
    '''
    破产玩家创建积分约牌房
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid=mid, value='0')
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        self.start_step('进入积分房界面')
        self.yuepai_page.wait_element('积分房').click()
        self.start_step('点击开房按钮')
        self.yuepai_page.wait_element('开房').click()
        self.start_step('点击确定')
        try:
            self.yuepai_page.wait_element('确定').click()
        except:
            print '未找到确定按钮'
        Flag = True
        while Flag:
            try:
                self.yuepai_page.wait_element('开房').click()
            except:
                Flag = False
        try:
            self.yuepai_page.wait_element('准备')
            self.yuepai_page.screenshot('3.png')
            print '成功创建房间'
        except:
            print '创建房间失败'
        time.sleep(10)
        self.start_step("退出约牌房")
        self.yuepai_page.wait_element("菜单键").click()
        time.sleep(3)
        self.yuepai_page.wait_element("退出键").click()
        time.sleep(4)
        self.yuepai_page.screenshot('exit.png')
        self.yuepai_page.wait_element("返回").click()
        time.sleep(3)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.recover_user(mid)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")


class C31196_DFQP_Yuepai_CreateCoinRoom_Broke(TestCase):
    '''
    破产玩家创建银币约牌房
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid=mid, value='0')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        self.start_step('点击银币单选按钮')
        self.yuepai_page.wait_element('银币单选按钮').click()
        self.start_step('点击开房按钮')
        self.yuepai_page.wait_element('开房').click()
        self.start_step('点击确定')
        try:
            self.yuepai_page.wait_element('确定').click()
        except:
            print '未找到确定按钮'
        Flag = True
        while Flag:
            self.yuepai_page.wait_element('开房').click()
            try:
                self.yuepai_page.wait_element('支付1')
                self.yuepai_page.screenshot('.png')
                Flag = False
            except:
                print '游戏下载中'
            # self.start_step("退出约牌房")
            # self.yuepai_page.wait_element("菜单键").click()
            # time.sleep(3)
            # self.yuepai_page.wait_element("退出键").click()
            # time.sleep(4)
            # self.yuepai_page.screenshot('exit.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.recover_user(mid)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")


class C31197_DFQP_Yuepai_CreateScoreCoinCrystalRoom(TestCase):
    '''
    玩家成功创建积分、银币、金条约牌房
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid=mid, value='60000')
        self.common.set_crystal(mid=mid,value="1000")
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(3)
        self.start_step('进入积分房界面')
        self.yuepai_page.wait_element('积分房').click()
        time.sleep(4)
        self.start_step('点击开房按钮')
        self.yuepai_page.wait_element('开房').click()
        time.sleep(4)
        self.start_step('点击确定')
        try:
            self.yuepai_page.wait_element('确定').click()
        except:
            print '未找到确定按钮'
        Flag = True
        while Flag:
            try:
                self.yuepai_page.wait_element('开房').click()
            except:
                Flag = False
        try:
            self.yuepai_page.wait_element('准备')
            self.yuepai_page.screenshot('1.png')
            print '成功创建积分房'
        except:
            print '创建积分房失败'
        self.start_step('退出积分房')
        self.yuepai_page.wait_element('菜单键').click()
        time.sleep(2)
        self.yuepai_page.wait_element('退出键').click()
        self.start_step('进入银币房')
        time.sleep(2)
        self.yuepai_page.wait_element('银币/金条房').click()
        self.yuepai_page.wait_element('银币单选按钮').click()
        self.start_step('点击开房按钮')
        self.yuepai_page.wait_element('开房').click()
        time.sleep(3)
        try:
            self.yuepai_page.wait_element('准备ok')
            self.yuepai_page.screenshot('2.png')
            print '成功创建银币房'
        except:
            print '创建银币房失败'
        self.start_step('退出银币房')
        self.yuepai_page.wait_element('菜单键').click()
        self.yuepai_page.wait_element('退出键').click()
        self.start_step('进入金条房')
        time.sleep(2)
        self.yuepai_page.wait_element('银币/金条房').click()
        self.yuepai_page.wait_element('金条单选按钮').click()
        self.start_step('点击开房按钮')
        self.yuepai_page.wait_element('开房').click()
        time.sleep(3)
        try:
            self.yuepai_page.wait_element('准备ok')
            self.yuepai_page.screenshot('3.png')
            print '成功创建金条房'
        except:
            print '创建金条房失败'
        time.sleep(4)
        self.start_step("退出约牌房")
        self.yuepai_page.wait_element("菜单键").click()
        time.sleep(3)
        self.yuepai_page.wait_element("退出键").click()
        time.sleep(4)
        self.yuepai_page.screenshot('exit.png')
        self.yuepai_page.wait_element("返回").click()
        time.sleep(3)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.recover_user(mid)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")



class C199_DFQP_Yuepai_CoinCrystalRoom_Display(TestCase):
    '''
    银币、金条约牌房房间内展示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid=mid, value='60000')
        self.common.set_crystal(mid=mid,value="1000")
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(2)
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(2)
        self.start_step('点击银币单选按钮')
        self.yuepai_page.wait_element('银币单选按钮').click()
        time.sleep(2)
        self.start_step('点击开房按钮')
        self.yuepai_page.wait_element('开房').click()
        time.sleep(2)
        self.start_step('点击确定')
        try:
            self.yuepai_page.wait_element('确定').click()
        except:
            print '未找到确定按钮'
        Flag = True
        while Flag:
            try:
                self.yuepai_page.wait_element('开房').click()
            except:
                Flag = False
        try:
            self.yuepai_page.wait_element('准备')
            print '成功创建银币房'
        except:
            print '创建银币房失败'
        time.sleep(3)
        self.start_step('点击菜单键')
        self.yuepai_page.wait_element('菜单键').click()
        time.sleep(2)
        self.yuepai_page.screenshot('1.png')
        self.yuepai_page.wait_element('银币框').click()
        time.sleep(2)
        self.start_step('点击二维码按钮')
        self.yuepai_page.wait_element('二维码').click()
        time.sleep(2)
        self.yuepai_page.screenshot('2.png')
        self.yuepai_page.wait_element('银币框').click()
        time.sleep(2)
        self.start_step('点击广播邀人按钮')
        self.yuepai_page.wait_element('广播邀人').click()
        time.sleep(2)
        self.yuepai_page.screenshot('3.png')
        self.yuepai_page.wait_element('银币框').click()
        time.sleep(2)
        self.start_step('点击更多按钮')
        self.yuepai_page.wait_element('更多').click()
        time.sleep(2)
        self.yuepai_page.screenshot('4.png')
        self.yuepai_page.wait_element('银币框').click()
        time.sleep(2)
        self.start_step('点击邀请按钮')
        self.yuepai_page.wait_element('邀请-银币/金条房').click()
        time.sleep(2)
        self.yuepai_page.screenshot('5.png')
        self.yuepai_page.wait_element('银币框').click()
        time.sleep(2)
        self.start_step('点击记牌器按钮')
        self.yuepai_page.wait_element('记牌器').click()
        time.sleep(2)
        self.yuepai_page.screenshot('6.png')
        self.yuepai_page.wait_element('银币框').click()
        self.start_step('点击聊天按钮')
        self.yuepai_page.wait_element('聊天').click()
        time.sleep(2)
        self.yuepai_page.screenshot('7.png')
        self.yuepai_page.wait_element('银币框').click()
        time.sleep(2)
        self.start_step('退出银币房，进入金条房')
        self.yuepai_page.wait_element('菜单键').click()
        time.sleep(2)
        self.yuepai_page.wait_element('退出键') .click()
        time.sleep(3)
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(2)
        self.start_step('点击金条单选按钮')
        self.yuepai_page.wait_element('金条单选按钮').click()
        time.sleep(2)
        self.start_step('点击开房按钮')
        self.yuepai_page.wait_element('开房').click()
        time.sleep(3)
        self.yuepai_page.screenshot('8.png')
        self.start_step("退出约牌房")
        self.yuepai_page.wait_element("菜单键").click()
        time.sleep(3)
        self.yuepai_page.wait_element("退出键").click()
        time.sleep(4)
        self.yuepai_page.screenshot('exit.png')
        self.yuepai_page.wait_element("返回").click()
        time.sleep(3)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.recover_user(mid)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")


__qtaf_seq_tests__ = [C31196_DFQP_Yuepai_CreateCoinRoom_Broke]
if __name__ == '__main__':
    debug_run_all()

