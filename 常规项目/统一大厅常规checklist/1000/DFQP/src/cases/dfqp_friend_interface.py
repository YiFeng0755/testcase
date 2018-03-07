#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌好友测试
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from appiumcenter.luadriver import LuaDriver
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.friend_page import Friend_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.feedback_page import Feedback_Page
from common.common import Common
from common import Interface as PHPInterface
import test_datas
from datacenter import dataprovider
testdata=test_datas.logindata4
@dataprovider.DataDrive(testdata)
class C211_DFQP_Friend(TestCase):
    '''
    点击查找好友查看界面显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.game_page =Game_Page()
        self.hall_page = Hall_Page()
        self.friend_page = Friend_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入好友界面')
        self.hall_page.wait_element('好友').click()
        self.start_step("进入查找好友界面")
        self.friend_page.wait_element("查找好友").click()
        self.personinfo_page.screenshot('.png')
        time.sleep(1)
        self.start_step('关闭查找好友界面')
        try:
            self.friend_page.wait_element('关闭按钮').click()

        except:
            print "查找好友界面未找到关闭按钮"

        try:
            self.friend_page.wait_element('输入查找ID')
            print "点击x未能正常关闭弹框"

        except:
            print "点击x能够正常关闭弹框"

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C212_DFQP_Friend(TestCase):
    '''
    查找好友输入的ID不正确，输入后点击查找
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.game_page =Game_Page()
        self.hall_page = Hall_Page()
        self.friend_page = Friend_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入好友界面')
        self.hall_page.wait_element('好友').click()
        self.start_step("进入查找好友界面")
        self.friend_page.wait_element("查找好友").click()
        self.start_step('输入错误ID')
        self.friend_page.wait_element('输入查找ID').send_keys("2187")
        self.start_step("开始查找")
        self.friend_page.wait_element('查看右上图标/查找').click()
        time.sleep(2)
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C213_DFQP_Friend(TestCase):
    '''
    查找好友输入的ID正确,输入后点击查找
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.game_page =Game_Page()
        self.hall_page = Hall_Page()
        self.friend_page = Friend_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入好友界面')
        self.hall_page.wait_element('好友').click()
        self.start_step("进入查找好友界面")
        self.friend_page.wait_element("查找好友").click()
        self.start_step('输入正确ID')
        self.friend_page.wait_element('输入查找ID').send_keys("2188068")
        self.start_step("开始查找")
        self.friend_page.wait_element("查看右上图标/查找").click()
        time.sleep(2)
        self.start_step("开始添加")
        self.friend_page.wait_element('添加').click()
        time.sleep(1)
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C214_DFQP_Friend(TestCase):
    '''
    查看好友消息列表信息展示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.game_page =Game_Page()
        self.hall_page = Hall_Page()
        self.friend_page = Friend_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入好友界面')
        self.hall_page.wait_element('好友').click()
        self.start_step("进入消息界面")
        self.friend_page.wait_element("消息tab").click()
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C215_DFQP_Friend(TestCase):
    '''
    好友排行点击好友聊天，进入聊天界面发送文本消息
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.game_page =Game_Page()
        self.hall_page = Hall_Page()
        self.friend_page = Friend_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入好友界面')
        self.hall_page.wait_element('好友').click()
        self.start_step("进入会话界面")
        #为何这样找元素会报错self.friend_page.wait_element('聊天').click()
        self.luadriver.find_element_by_name('btnWord').click()
        self.start_step("输入聊天文本")
        self.friend_page.wait_element("输入框").send_keys("hello")
        self.friend_page.wait_element("发送").click()
        time.sleep(1)
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C216_DFQP_Friend(TestCase):
    '''
    联系客服，提交问题反馈
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.game_page =Game_Page()
        self.hall_page = Hall_Page()
        self.friend_page = Friend_Page()
        self.personinfo_page = Personinfo_Page()
        self.feedback_page = Feedback_Page()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入意见反馈界面")
        self.feedback_page.wait_element("意见反馈").click()
        list = [['11','11'],['22','22'],['33','33'],['44','44']]
        for i in range(len(list)):
            L = list[i]
            text1 = L[0]
            text2 = L[1]
            self.feedback_page.wait_element('反馈描述').send_keys(text1)
            self.feedback_page.wait_element('联系方式').send_keys(text2)
            self.feedback_page.wait_element('提交').click()
            time.sleep(5)
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()


if __name__ == '__main__':
    C211_DFQP_Friend3 = C216_DFQP_Friend()
    C211_DFQP_Friend3.debug_run()

