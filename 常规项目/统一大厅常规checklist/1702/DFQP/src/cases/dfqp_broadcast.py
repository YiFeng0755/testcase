#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
广播
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from appiumcenter.luadriver import LuaDriver
from uilib.personinfo_page import Personinfo_Page
from uilib.hall_page import Hall_Page
from uilib.sign_page import Sign_Page
from uilib.game_page import Game_Page
from uilib.setting_page import Setting_Page
from uilib.broadcast_page import Broadcast_Page
from common.common import Common
from common import Interface as PHPInterface
import json
import test_datas
from datacenter import dataprovider
from common import user_util

class C31134_DFQP_Broadcast_Visitors(TestCase):
    '''
    游客账号点击广播输入文字发送，查看
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.broadcast_page = Broadcast_Page()
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动页面")
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入广播界面')
        self.broadcast_page.wait_element('广播').click()
        self.personinfo_page.screenshot('.png')
        self.start_step('点击立即绑定')
        self.broadcast_page.wait_element('发送').click()
        try:
            self.broadcast_page.wait_element('确定')
            print '点击立即绑定可以成功绑定手机'
        except:
            print '点击立即绑定没有出现绑定手机操作'

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()


class C31138_DFQP_Broadcast_NoBroadcast(TestCase):
    '''
    无广播消息时，广播界面消息列表显示空白
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.game_page = Game_Page()
        self.setting_page = Setting_Page()
        self.personinfo_page = Personinfo_Page()
        self.broadcast_page = Broadcast_Page()
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动页面")
        self.common.closeactivity(self.luadriver)
        # self.start_step("判断是否登陆")
        # self.hall_page.wait_element("头像").click()
        # time.sleep(5)
        # self.common.loginuser(user_info['user'], user_info['password'])
        # self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入广播界面')
        self.broadcast_page.wait_element('广播').click()
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        # finally:
        #     self.common.release_user(user_info['mid'])


class C31140_DFQP_Broadcast_ReceiveSystemMessages(TestCase):
    '''
    接收系统消息,查看广播消息界面显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.game_page = Game_Page()
        self.setting_page = Setting_Page()
        self.personinfo_page = Personinfo_Page()
        self.broadcast_page = Broadcast_Page()
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动页面")
        self.common.closeactivity(self.luadriver)
        # self.start_step("判断是否登陆")
        # self.hall_page.wait_element("头像").click()
        # time.sleep(5)
        # self.common.loginuser(user_info['user'], user_info['password'])
        # self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入广播界面')
        self.broadcast_page.wait_element('广播').click()
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()


if __name__ == '__main__':
    # C31139_DFQP_Broadcast_SeveralMessages = C31139_DFQP_Broadcast_SeveralMessages()
    # C31139_DFQP_Broadcast_SeveralMessages.debug_run()
    debug_run_all()