#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
启动/闪屏
'''
import time,test_datas
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
import os
import utils.util as util
from utils.confighelper import ConfigHelper
from uilib.login_page import Login_Page
from uilib.setting_page import Setting_Page
from uilib.hall_page import Hall_Page
from uilib.personinfo_page import Personinfo_Page
from common.common import Common
from datacenter import dataprovider

class C30957_DFQP_Start_Nonetwork(TestCase):
    '''
    无网络,点击启动游戏,首次无网络时启动游戏
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.Normal
    timeout = 5
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        # 初始化Luadriver
        capabilities = {}
        capabilities['noReset'] = False    #清除应用缓存
        self.luadriver = self.common.setupdriver(capabilities)
        self.common.deletefile(self.luadriver)
        self.common.switchnetwork(self.luadriver, u"无网络")
        # 声明方法
        self.login_page = Login_Page()
        #关闭活动页面
        self.common.closeactivity_switchserver(self.luadriver,"环境切换")

    def run_test(self):
        #测试用例
        self.start_step("启动游戏")
        self.login_page.screenshot('GuestLogin1.png')

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        #设置网络
        self.common.switchnetwork(self.luadriver, u"WIFI模式")
        self.common.closedriver()

class C30958_DFQP_Start(TestCase):
    '''
    有网络时启动游戏
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.Normal
    timeout = 5
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 声明方法
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()
        self.common.switchnetwork(self.luadriver, u"WIFI模式")
        #关闭活动页面
        self.common.closeactivity_switchserver(self.luadriver,"环境切换")

    def run_test(self):
        # 测试用例
        self.hall_page.wait_element("同步标志")
        self.start_step("启动游戏")
        self.login_page.screenshot('Login.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C30959_DFQP_Load(TestCase):
    '''
    后台不配置节日闪屏图片
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 声明方法
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver, "环境切换")

    def run_test(self):
        # 测试用例
        self.hall_page.screenshot('Load_0.png')
        time.sleep(0.5)
        self.hall_page.screenshot('Load_1.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

# __qtaf_seq_tests__ = [C30957_DFQP_Login_GuestLogin]
if __name__ == '__main__':
    # C008_DFQP_Bandding = C008_DFQP_Bandding()
    # C008_DFQP_Bandding.debug_run()
    debug_run_all()