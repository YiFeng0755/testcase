#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌广播测试
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
testdata=test_datas.logindata4

@dataprovider.DataDrive(testdata)
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
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.broadcast_page = Broadcast_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')

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
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C31135_DFQP_Broadcast_RegisterUnderLevel15(TestCase):
    '''
    注册玩家等级不足15级,点击广播输入文字点击发送，查看
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        UserID = self.casedata.get('mid2')
        print 'UserID:%s' % UserID
        PHPInterface.set_level(UserID, 1) #将玩家等级设为1级
        user_info = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 30000 - coin
        PHPInterface.add_money(UserID, AddMoney)  # 将银币值设为30000
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.game_page = Game_Page()
        self.setting_page = Setting_Page()
        self.personinfo_page = Personinfo_Page()
        self.broadcast_page = Broadcast_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
        i = 0
        while i < 3:
            i += 1
            try:
                self.personinfo_page.wait_element("关闭").click()
            except:
                print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入广播界面')
        self.broadcast_page.wait_element('广播').click()
        self.broadcast_page.wait_element('输入文字').send_keys('11')
        self.start_step('点击发送')
        self.broadcast_page.wait_element('发送').click()
        time.sleep(1)
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C31136_DFQP_Broadcast_NotEnoughMoney(TestCase):
    '''
    注册15级玩家银币不足23000,点击广播输入文字点击发送，查看
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        UserID = self.casedata.get('mid2')
        print 'UserID:%s' % UserID
        PHPInterface.set_level(UserID,15)
        user_info = PHPInterface.get_user_info(UserID) #获取玩家信息
        coin = json.loads(user_info).get('result',{'coin':None}).get('coin') #获取当前银币值
        AddMoney = 10000 - coin
        PHPInterface.add_money(UserID,AddMoney) #将银币值设为10000
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.game_page = Game_Page()
        self.setting_page = Setting_Page()
        self.personinfo_page = Personinfo_Page()
        self.broadcast_page = Broadcast_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
        i = 0
        while i < 3:
            i += 1
            try:
                self.personinfo_page.wait_element("关闭").click()
            except:
                print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入广播界面')
        self.broadcast_page.wait_element('广播').click()
        self.broadcast_page.wait_element('输入文字').send_keys('11')
        self.start_step('点击发送')
        self.broadcast_page.wait_element('发送').click()
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C31137_DFQP_Broadcast_EnoughMoney(TestCase):
    '''
    注册15级玩家银币足够,点击广播输入文字点击发送，查看
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        UserID = self.casedata.get('mid2')
        print 'UserID:%s' % UserID
        PHPInterface.set_level(UserID,16)
        user_info = PHPInterface.get_user_info(UserID) #获取玩家信息
        coin = json.loads(user_info).get('result',{'coin':None}).get('coin') #获取当前银币值
        AddMoney = 40000 - coin
        PHPInterface.add_money(UserID,AddMoney) #将银币值设为40000
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.game_page = Game_Page()
        self.setting_page = Setting_Page()
        self.personinfo_page = Personinfo_Page()
        self.broadcast_page = Broadcast_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
        i = 0
        while i < 3:
            i += 1
            try:
                self.personinfo_page.wait_element("关闭").click()
            except:
                print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入广播界面')
        self.broadcast_page.wait_element('广播').click()
        self.broadcast_page.wait_element('输入文字').send_keys('11')
        self.start_step('点击发送')
        self.broadcast_page.wait_element('发送').click()
        time.sleep(1)
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
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
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.game_page = Game_Page()
        self.setting_page = Setting_Page()
        self.personinfo_page = Personinfo_Page()
        self.broadcast_page = Broadcast_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
        i = 0
        while i < 3:
            i += 1
            try:
                self.personinfo_page.wait_element("关闭").click()
            except:
                print "已关闭窗口"

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
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C31139_DFQP_Broadcast_BroadcastSeveralMessages(TestCase):
    '''
    接收多条广播消息
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        global UserID
        UserID = self.casedata.get('mid2')
        print 'UserID:%s' % UserID
        PHPInterface.set_level(UserID, 16)
        user_info = PHPInterface.get_user_info(UserID) #获取玩家信息
        coin = json.loads(user_info).get('result',{'coin':None}).get('coin') #获取当前银币值
        AddMoney = 300000 - coin
        PHPInterface.add_money(UserID,AddMoney) #将银币值设为300000
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.game_page = Game_Page()
        self.setting_page = Setting_Page()
        self.personinfo_page = Personinfo_Page()
        self.broadcast_page = Broadcast_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
        i = 0
        while i < 3:
            i += 1
            try:
                self.personinfo_page.wait_element("关闭").click()
            except:
                print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入广播界面')
        self.broadcast_page.wait_element('广播').click()
        # PHPInterface.broadcast(UserID, content='第一条')后台发送不会显示‘广播正在冷却中，请稍后再发’的提示
        self.broadcast_page.wait_element('输入文字').send_keys('11')
        self.start_step('点击发送')
        self.broadcast_page.wait_element('发送').click()
        time.sleep(1)
        self.broadcast_page.wait_element('广播').click()
        self.personinfo_page.screenshot('1.png')
        self.broadcast_page.wait_element('输入文字').send_keys('22')
        self.start_step('点击发送')
        self.broadcast_page.wait_element('发送').click()
        time.sleep(1)
        self.personinfo_page.screenshot('2.png')
        self.broadcast_page.wait_element('广播').click()
        time.sleep(305)#5分多钟后再发广播
        self.broadcast_page.wait_element('输入文字').send_keys('22')
        self.broadcast_page.wait_element('广播').click()
        self.personinfo_page.screenshot('3.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
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
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.game_page = Game_Page()
        self.setting_page = Setting_Page()
        self.personinfo_page = Personinfo_Page()
        self.broadcast_page = Broadcast_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
        i = 0
        while i < 3:
            i += 1
            try:
                self.personinfo_page.wait_element("关闭").click()
            except:
                print "已关闭窗口"

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
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C31141_DFQP_Broadcast_ReceiveMessageInHall(TestCase):
    '''
    在大厅界面接收玩家广播消息
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.game_page = Game_Page()
        self.setting_page = Setting_Page()
        self.personinfo_page = Personinfo_Page()
        self.broadcast_page = Broadcast_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
        i = 0
        while i < 3:
            i += 1
            try:
                self.personinfo_page.wait_element("关闭").click()
            except:
                print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        UserID = self.casedata.get('mid2')
        print 'UserID:%s' % UserID
        PHPInterface.broadcast(UserID,content='地方棋牌测试专用')
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()


if __name__ == '__main__':
    #C31138_DFQP_Exchange = C31138_DFQP_Broadcast()
    #C31138_DFQP_Exchange.debug_run()
    debug_run_all()