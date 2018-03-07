#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
注册绑定
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


class C31005_DFQP_Login_UseLogin2(TestCase):
    '''
    老手机账号切换老手机账号
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 8
    def pre_test(self):
        # 初始化nativeDriver
        self.common = Common()
        global user_info1,user_info2,mid1,mid2
        user_info1 = self.common.get_user()
        print user_info1
        user_info2 = self.common.get_user()
        print user_info2
        self.luadriver = self.common.setupdriver()
        # 声明方法
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()
        #关闭活动页面
        self.common.closeactivity_switchserver(self.luadriver)
        self.start_step("判断是否登陆")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(user_info1['user'],user_info1['password'])
            self.common.closeActivityBtn()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.hall_page.wait_element("头像").click()
        time.sleep(8)
        self.hall_page.screenshot('Login_UseLogin1.png')
        self.start_step("登陆")
        self.common.loginuser(user_info2['user'], user_info2['password'])
        #关闭活动页面
        self.common.closeActivityBtn()
        self.hall_page.wait_element("同步标志")
        self.hall_page.wait_element("头像").click()
        time.sleep(3)
        self.hall_page.screenshot('Login_UseLogin2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info1['mid'])
            self.common.release_user(user_info2['mid'])


class C30998_DFQP_Login(TestCase):
    '''
    游客账号第一次登陆
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        capabilities = {}
        capabilities['noReset'] = False    #清除应用缓存
        self.luadriver = self.common.setupdriver(capabilities)
        self.common.deletefile(self.luadriver)
        # 声明方法
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()
        #关闭活动页面
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        #测试用例
        self.hall_page.wait_element("同步标志")
        self.hall_page.wait_element("头像").click()
        time.sleep(1)
        self.hall_page.screenshot('Login1.png')
        self.setting_page.wait_element("注册绑定手机").click()
        time.sleep(2)
        self.common.restart()
        #关闭活动页面
        self.common.closeactivity_switchserver(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(2)
        self.hall_page.screenshot('Login2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # try:
        #     self.common.deletefile(self.luadriver)
        # except:
        #     print "删除失败"
        self.common.closedriver()


class C31001_DFQP_Bandding(TestCase):
    '''
    游客绑定该地区已经登录注册过的手机账号
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)
        # 声明方法
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        # 测试用例
        self.hall_page.wait_element("同步标志")
        self.start_step("注册登录")
        self.hall_page.wait_element("头像").click()
        time.sleep(4)
        self.setting_page.wait_element("切换账号").click()
        time.sleep(4)
        try:
            self.setting_page.wait_element("继续登录").click()
        except:
            print "不需要继续切换"
        time.sleep(4)
        self.start_step("注册新账号")
        self.setting_page.wait_element("注册新账号").click()
        time.sleep(4)
        # print self.setting_page.wait_element("你的手机号码").get_attribute('text')
        self.setting_page.wait_element("你的手机号码").get_attribute('text')=="您的手机号"
        self.setting_page.wait_element("你的手机号码").send_keys(user_info['user'])
        time.sleep(4)
        self.setting_page.wait_element("确认登陆").click()
        time.sleep(2)
        self.start_step("登陆")
        self.setting_page.wait_element("直接登陆").click()
        self.setting_page.screenshot('Bandding.png')
        time.sleep(3)
        self.setting_page.wait_element("密码").send_keys(user_info['password'])
        time.sleep(3)
        self.setting_page.wait_element("注册登录按钮").click()
        time.sleep(10)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['mid'])


class C31004_DFQP_VisitorLogin(TestCase):
    '''
    玩家为游客，并且记录个人信息
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)
        self.common.closeactivity_switchserver(self.luadriver)
        # 声明方法
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        # 测试用例
        self.hall_page.wait_element("同步标志")
        self.start_step("获取游客信息")
        self.hall_page.wait_element("头像").click()
        time.sleep(3)
        # id1 = self.setting_page.wait_element("账号ID").get_attribute('text')
        # print id1
        self.setting_page.wait_element("立即升级")
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeactivity_switchserver(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(3)
        self.personinfo_page.wait_element("账号ID").get_attribute('text') == user_info['cid']
        self.setting_page.screenshot('VisitorLogin.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['mid'])

__qtaf_seq_tests__ = [C31005_DFQP_Login_UseLogin2]
if __name__ == '__main__':
    # C008_DFQP_Bandding = C008_DFQP_Bandding()
    # C008_DFQP_Bandding.debug_run()
    debug_run_all()