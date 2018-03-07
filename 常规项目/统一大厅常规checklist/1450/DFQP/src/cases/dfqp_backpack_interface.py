#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
物品箱_接口
'''
import time
import datetime
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.sign_page import Sign_Page
from uilib.hall_page import Hall_Page
from uilib.setting_page import Setting_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.mall_page import Mall_Page
from uilib.backpack_page import Backpack_Page
from uilib.message_page import Message_Page
from common.common import Common
import test_datas
from datacenter import dataprovider
import common.Interface as PHPInterface

testdata=test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C31034_DFCP_Backpack_Interface_GetPro(TestCase):
    '''
    购买道具，商城购买道具，查看物品箱
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.mall_page = Mall_Page()
        self.sign_page = Sign_Page()
        self.backpack_page = Backpack_Page()
        self.personinfo_page = Personinfo_Page()
        time.sleep(1)
        PHPInterface.add_money(self.casedata['mid'], 53000)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivityprepublish(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(2)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入物品箱页面")
        time.sleep(2)
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack1.png')
        self.luadriver.keyevent(4)
        self.start_step("进入商城页面")
        self.hall_page.wait_element("商城").click()
        time.sleep(2)
        self.mall_page.wait_element("道具页签").click()
        time.sleep(2)
        self.start_step("购买道具")
        self.mall_page.wait_element("提示卡").click()
        time.sleep(5)
        self.sign_page.wait_element("购买").click()
        time.sleep(3)
        self.mall_page.wait_element("返回").click()
        time.sleep(3)
        self.start_step("进入物品箱页面")
        time.sleep(2)
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack2.png')

    def post_test(self):
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata = test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C31036_DFQP_Backpack_Sendpro(TestCase):
    '''
    私信发送道具,鲜花
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("接口交互道具私信")
        # 每个用例都需要关闭活动，并切换到测试服
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        print self.casedata['mid']
        return1 = PHPInterface.send_message(int(self.casedata['mid']), "接口交互道具私信","接口交互道具私信",200,1,0)
        print return1
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivity_switchserver(self.luadriver, "预发布")
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
                self.common.loginuser(self.casedata['user'], self.casedata['password'])
                self.common.closeactivity_switchserver(self.luadriver, "预发布")
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入物品箱页面")
        time.sleep(2)
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack2.png')
        self.luadriver.keyevent(4)
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看消息")
        try:
            try:
                element = self.message_page.get_elements("小琪妹")
                element[1].click()
            except:
                self.message_page.wait_element("小琪妹").click()
            time.sleep(3)

            self.message_page.screenshot('getcalls1.png')
            self.message_page.wait_element("立即领取").click()
            time.sleep(3)
            self.message_page.screenshot('getcalls2.png')
            self.message_page.wait_element("知道了").click()
            time.sleep(2)
            self.message_page.wait_element('已领取').get_attribute('text') == "已领取"
        except:
            print ("没有消息")
        time.sleep(3)
        self.hall_page.wait_element("头像").click()
        time.sleep(3)
        self.hall_page.wait_element("头像").click()
        self.hall_page.wait_element("同步标志")
        self.start_step("进入物品箱页面")
        time.sleep(2)
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata = test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C31035_DFQP_Backpack_Givepro(TestCase):
    '''
    丢弃道具，鲜花
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("接口交互道具私信")
        # 每个用例都需要关闭活动，并切换到测试服
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        print self.casedata['mid']
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        return1 = PHPInterface.send_message(int(self.casedata['mid']), "接口交互道具私信","接口交互道具私信",200,1,0)
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivity_switchserver(self.luadriver, "预发布")
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
                self.common.loginuser(self.casedata['user'], self.casedata['password'])
                self.common.closeactivity_switchserver(self.luadriver, "预发布")
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看消息")
        try:
            try:
                element = self.message_page.get_elements("小琪妹")
                element[1].click()
            except:
                self.message_page.wait_element("小琪妹").click()
            time.sleep(3)

            self.message_page.screenshot('getcalls1.png')
            self.message_page.wait_element("立即领取").click()
            time.sleep(3)
            self.message_page.screenshot('getcalls2.png')
            self.message_page.wait_element("知道了").click()
            time.sleep(2)
            self.message_page.wait_element('已领取').get_attribute('text') == "已领取"
        except:
            print ("没有消息")
        time.sleep(3)
        # self.message_page.wait_element("返回").click()
        self.hall_page.wait_element("头像").click()
        time.sleep(3)
        self.hall_page.wait_element("头像").click()
        self.hall_page.wait_element("同步标志")
        self.start_step("进入物品箱页面")
        time.sleep(2)
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack2.png')
        self.backpack_page.wait_element("物品名称").click()
        time.sleep(2)
        self.backpack_page.wait_element("丢弃").click()
        time.sleep(2)
        self.backpack_page.wait_element("丢弃").click()
        time.sleep(2)
        self.backpack_page.screenshot('Backpack_Enterpack2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata = test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C31037_DFQP_Backpack_Compose(TestCase):
    '''
    合成话费碎片
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("接口交互道具私信")
        # 每个用例都需要关闭活动，并切换到测试服
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        print self.casedata['mid']
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        return1 = PHPInterface.send_message(int(self.casedata['mid']), "接口交互道具私信","接口交互道具私信",400002,10,0)
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivity_switchserver(self.luadriver, "预发布")
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
                self.common.loginuser(self.casedata['user'], self.casedata['password'])
                self.common.closeactivity_switchserver(self.luadriver, "预发布")
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看消息")
        try:
            try:
                element = self.message_page.get_elements("小琪妹")
                element[1].click()
            except:
                self.message_page.wait_element("小琪妹").click()
            time.sleep(3)

            self.message_page.screenshot('getcalls1.png')
            self.message_page.wait_element("立即领取").click()
            time.sleep(3)
            self.message_page.screenshot('getcalls2.png')
            self.message_page.wait_element("知道了").click()
            time.sleep(2)
            self.message_page.wait_element('已领取').get_attribute('text') == "已领取"
        except:
            print ("没有消息")
        time.sleep(3)
        self.hall_page.wait_element("头像").click()
        time.sleep(3)
        self.hall_page.wait_element("头像").click()
        self.hall_page.wait_element("同步标志")
        self.start_step("进入物品箱页面")
        time.sleep(2)
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack2.png')
        self.backpack_page.wait_element("物品名称").click()
        time.sleep(2)
        self.start_step("合成话费")
        self.backpack_page.wait_element("合成").click()
        time.sleep(2)
        self.backpack_page.screenshot('Backpack_Enterpack2.png')
        self.backpack_page.wait_element("返回").click()
        time.sleep(2)
        self.backpack_page.screenshot('Backpack_Enterpack3.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata = test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C31038_DFQP_Backpack_Compose(TestCase):
    '''
    话费碎片回兑银币
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("接口交互道具私信")
        # 每个用例都需要关闭活动，并切换到测试服
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        print self.casedata['mid']
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        return1 = PHPInterface.send_message(int(self.casedata['mid']), "接口交互道具私信","接口交互道具私信",400002,10,0)
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivity_switchserver(self.luadriver, "预发布")
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
                self.common.loginuser(self.casedata['user'], self.casedata['password'])
                self.common.closeactivity_switchserver(self.luadriver, "预发布")
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看消息")
        try:
            try:
                element = self.message_page.get_elements("小琪妹")
                element[1].click()
            except:
                self.message_page.wait_element("小琪妹").click()
            time.sleep(3)

            self.message_page.screenshot('getcalls1.png')
            self.message_page.wait_element("立即领取").click()
            time.sleep(3)
            self.message_page.screenshot('getcalls2.png')
            self.message_page.wait_element("知道了").click()
            time.sleep(2)
            self.message_page.wait_element('已领取').get_attribute('text') == "已领取"
        except:
            print ("没有消息")
        time.sleep(3)
        self.hall_page.wait_element("头像").click()
        time.sleep(3)
        self.hall_page.wait_element("头像").click()
        self.hall_page.wait_element("同步标志")
        self.start_step("进入物品箱页面")
        time.sleep(2)
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack2.png')
        try:
            self.backpack_page.wait_element("物品名称").click()
            time.sleep(2)
            self.start_step("出售话费碎片")
            self.backpack_page.wait_element("出售").click()
            time.sleep(2)
            self.backpack_page.wait_element("出售").click()
            time.sleep(2)
            self.backpack_page.screenshot('Backpack_Enterpack2.png')
        except:
            print "未找到物品箱"
        # self.backpack_page.wait_element("返回").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata = test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C31040_DFQP_Backpack_Compose(TestCase):
    '''
    兑换实物及话费
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("接口交互道具私信")
        # 每个用例都需要关闭活动，并切换到测试服
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        print self.casedata['mid']
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        return1 = PHPInterface.send_message(int(self.casedata['mid']), "接口交互道具私信","接口交互道具私信",200005,1,0)
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivity_switchserver(self.luadriver, "预发布")
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
                self.common.loginuser(self.casedata['user'], self.casedata['password'])
                self.common.closeactivity_switchserver(self.luadriver, "预发布")
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看消息")
        try:
            try:
                element = self.message_page.get_elements("小琪妹")
                element[1].click()
            except:
                self.message_page.wait_element("小琪妹").click()
            time.sleep(3)

            self.message_page.screenshot('getcalls1.png')
            self.message_page.wait_element("立即领取").click()
            time.sleep(3)
            self.message_page.screenshot('getcalls2.png')
            self.message_page.wait_element("知道了").click()
            time.sleep(2)
            self.message_page.wait_element('已领取').get_attribute('text') == "已领取"
        except:
            print ("没有消息")
        time.sleep(3)
        self.message_page.wait_element("返回").click()
        time.sleep(3)
        self.hall_page.wait_element("头像").click()
        self.hall_page.wait_element("同步标志")
        self.start_step("进入物品箱页面")
        time.sleep(2)
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack2.png')
        self.backpack_page.wait_element("物品名称").click()
        time.sleep(2)
        self.start_step("兑换金币/金币")
        self.backpack_page.wait_element("使用").click()
        time.sleep(2)
        self.backpack_page.wait_element("手机号码").send_keys(self.casedata['user'])
        time.sleep(2)
        self.backpack_page.wait_element("确认手机号码").send_keys(self.casedata['user'])
        time.sleep(2)
        self.backpack_page.wait_element("使用").click()
        time.sleep(9)
        self.backpack_page.screenshot('use.png')
        self.start_step("分享好友")
        self.backpack_page.wait_element("分享好友").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata = test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C31042_DFQP_Backpack_share(TestCase):
    '''
    安装了微信分享兑换记录
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("接口交互道具私信")
        # 每个用例都需要关闭活动，并切换到测试服
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        print self.casedata['mid']
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        return1 = PHPInterface.send_message(int(self.casedata['mid']), "接口交互道具私信","接口交互道具私信",200005,1,0)
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivity_switchserver(self.luadriver, "预发布")
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
                self.common.loginuser(self.casedata['user'], self.casedata['password'])
                self.common.closeactivity_switchserver(self.luadriver, "预发布")
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看消息")
        try:
            try:
                element = self.message_page.get_elements("小琪妹")
                element[1].click()
            except:
                self.message_page.wait_element("小琪妹").click()
            time.sleep(3)

            self.message_page.screenshot('getcalls1.png')
            self.message_page.wait_element("立即领取").click()
            time.sleep(3)
            self.message_page.screenshot('getcalls2.png')
            self.message_page.wait_element("知道了").click()
            time.sleep(2)
            self.message_page.wait_element('已领取').get_attribute('text') == "已领取"
        except:
            print ("没有消息")
        time.sleep(3)
        self.hall_page.wait_element("头像").click()
        time.sleep(3)
        self.hall_page.wait_element("头像").click()
        self.hall_page.wait_element("同步标志")
        self.start_step("进入物品箱页面")
        time.sleep(2)
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack2.png')
        self.backpack_page.wait_element("物品名称").click()
        time.sleep(2)
        self.backpack_page.wait_element("使用").click()
        time.sleep(2)
        self.backpack_page.wait_element("手机号码").send_keys(self.casedata['user'])
        time.sleep(2)
        self.backpack_page.wait_element("确认手机号码").send_keys(self.casedata['user'])
        time.sleep(2)
        self.backpack_page.wait_element("使用").click()
        time.sleep(9)
        self.backpack_page.screenshot('use.png')
        self.backpack_page.wait_element("返回").click()
        time.sleep(3)
        self.backpack_page.wait_element("兑换记录").click()
        time.sleep(3)
        self.backpack_page.wait_element("兑换记录1").click()
        time.sleep(2)
        self.backpack_page.wait_element("分享好友").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_Enterpack2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

__qtaf_seq_tests__ = [C31035_DFQP_Backpack_Givepro]
if __name__ == '__main__':
    # C002_DFQP_Login_GuestLogin = C002_DFQP_Login_GuestLogin()
    # C002_DFQP_Login_GuestLogin.debug_run()
    debug_run_all()
