#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
邀请
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

class C70456_Scroeroom_Invitedisplay(TestCase):
    '''
    积分房内查看邀请界面
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
        self.start_step('点击邀请按钮')
        self.yuepai_page.wait_element('+邀请',20).click()
        self.yuepai_page.screenshot("invite.png")
        self.yuepai_page.wait_element("邀请-房号").get_attribute("text").find(u"房号")
        self.yuepai_page.wait_element("微信邀请")
        self.yuepai_page.wait_element("QQ邀请")
        self.yuepai_page.wait_element("在线好友")
        self.luadriver.keyevent(4)
        self.start_step("退出约牌房")
        self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70458_Scroeroom_Invite(TestCase):
    '''
    记分房手机未安装微信/QQ邀请，邀请玩家
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
        self.start_step('点击邀请按钮')
        self.yuepai_page.wait_element('+邀请', 30).click()
        self.yuepai_page.screenshot("invite.png")
        # if (self.yuepai_page.element_is_exist("微信邀请") == True):
        self.start_step("微信邀请好友")
        try:
            self.start_step("微信邀请好友")
            self.yuepai_page.wait_element("微信邀请").click()
            time.sleep(3)
            self.yuepai_page.screenshot("weichat.png")
            time.sleep(2)
            self.luadriver.keyevent(4)
        except:
            print "微信邀请好友失败"
        if (self.yuepai_page.element_is_exist("QQ邀请") == True):
            pass
        else:
            self.yuepai_page.wait_element('+邀请', 30).click()
        self.start_step("QQ邀请")
        self.yuepai_page.wait_element("QQ邀请").click()
        self.yuepai_page.screenshot("5.png")
        self.yuepai_page.wait_element("立即邀请").click()
        self.yuepai_page.screenshot("6.png")
        self.luadriver.keyevent(4)
        self.start_step("退出约牌房")
        self.yuepai_page.exit_yuepai_page()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

__qtaf_seq_tests__ = [C70458_Scroeroom_Invite]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
