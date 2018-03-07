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
import utils.constant as constant
import subprocess
import threading

class C74637_DFQP_Start_Nonetwork(TestCase):
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
        config = ConfigHelper(constant.cfg_path)
        global deviceName
        deviceName = config.getValue('appium', 'deviceName')
        self.common.switchnetwork(self.luadriver, u"无网络")
        print self.luadriver.network_connection
        # if self.luadriver.network_connection == 2:
        #     cmd = "adb -s " + deviceName + " shell am broadcast -a io.appium.settings.wifi --es setstatus disable"
        #     print cmd
        #     subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #     try:
        #         self.luadriver.find_element_by_android_uiautomator('new UiSelector().text("允许")').click()
        #     except:
        #         print "未出现按钮1"
        # 声明方法
        self.login_page = Login_Page()
        self.hall_page =  Hall_Page()
        #关闭活动页面
        self.common.closeactivity_switchserver(self.luadriver )
        # time.sleep(10)

    def run_test(self):
        #测试用例
        self.start_step("启动游戏")
        self.hall_page.wait_element("头像")
        self.login_page.screenshot('GuestLogin1.png')
        # self.hall_page.wait_element("头像").click()
        # self.hall_page.element_is_exist("头像")

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        self.common.switchnetwork(self.luadriver, u"WIFI模式")
        print self.luadriver.network_connection
        if self.luadriver.network_connection != 2:
            t1 = threading.Thread(target=self.switchnetwork)
            t2 = threading.Thread(target=self.closebtn)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        self.start_step("close driver")
        self.common.closedriver()
    def switchnetwork(self):
        '''
        测试用例运行过程中切换网络
        '''

        cmd = "shell am start -n com.example.unlock/.Unlock"
        print "adb start:" + str(time.time())
        self.luadriver.adb(cmd)
        print "adb end:"+ str(time.time())
    def closebtn(self):
        time.sleep(1)
        print "closebtn" + str(time.time())
        try:
            self.luadriver.find_element_by_android_uiautomator('new UiSelector().textMatches("确定|允许")').click()
            print "close1" + str(time.time())
        except:
            print "1" + str(time.time())
        try:
            self.luadriver.find_element_by_android_uiautomator('new UiSelector().textMatches("确定|允许")').click()
            print "close2" + str(time.time())
        except:
            print "2" + str(time.time())
        try:
            self.luadriver.find_element_by_android_uiautomator('new UiSelector().textMatches("确定|允许")').click()
            print "close3" + str(time.time())
        except:
            print "3" + str(time.time())

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
        self.common.closeactivity_switchserver(self.luadriver )

    def run_test(self):
        # 测试用例
        self.hall_page.wait_element("同步标志")
        self.start_step("启动游戏")
        self.hall_page.wait_element("头像")
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
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        # 测试用例
        self.hall_page.screenshot('Load_0.png')
        time.sleep(0.5)
        self.hall_page.screenshot('Load_1.png')
        self.hall_page.wait_element("头像")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

__qtaf_seq_tests__ = [C74637_DFQP_Start_Nonetwork]
if __name__ == '__main__':
    # C008_DFQP_Bandding = C008_DFQP_Bandding()
    # C008_DFQP_Bandding.debug_run()
    debug_run_all()