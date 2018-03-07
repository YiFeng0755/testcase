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
import test_datas
from datacenter import dataprovider
testdata=test_datas.logindata4

@dataprovider.DataDrive(testdata)
class C222_DFQP_Broadcast(TestCase):
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
        self.start_step('删除登录文件')
        self.common.deletefile(self.luadriver)
        self.common.closedriver()
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.broadcast_page = Broadcast_Page()
        self.common.closeactivitytest(self.luadriver)

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

@dataprovider.DataDrive(testdata)
class C223_DFQP_Broadcast(TestCase):
    '''
    注册玩家等级不足15级,点击广播输入文字点击发送，查看
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        PHPInterface.set_level(UserID, 1) #将玩家等级设为1级
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
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
        self.common.closeactivitytest(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入头像界面')
        self.hall_page.wait_element('头像').click()
        self.common.loginuser(self.casedata['user'], self.casedata['password'])
        self.start_step('关闭弹框')
        time.sleep(4)
        i = 0
        while(i<3):
            try:
                self.sign_page.wait_element('关闭1').click()
                i += 1
            except:
                i = 3
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
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C224_DFQP_Broadcast(TestCase):
    '''
    注册15级玩家银币不足23000,点击广播输入文字点击发送，查看
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        PHPInterface.set_level(UserID,15)
        dict = PHPInterface.get_user_info(UserID) #获取玩家信息
        coin = eval(dict).get('result',{'coin':None}).get('coin') #获取当前银币值
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
        self.common.closeactivitytest(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入头像界面')
        self.hall_page.wait_element('头像').click()
        self.common.loginuser(self.casedata['user'], self.casedata['password'])
        self.start_step('关闭弹框')#登录过后也会出现弹框
        time.sleep(4)
        i = 0
        while (i < 3):
            try:
                self.sign_page.wait_element('关闭1').click()
                i += 1
            except:
                i = 3
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
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C225_DFQP_Broadcast(TestCase):
    '''
    注册15级玩家银币足够,点击广播输入文字点击发送，查看
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        PHPInterface.set_level(UserID,16)
        dict = PHPInterface.get_user_info(UserID) #获取玩家信息
        coin = eval(dict).get('result',{'coin':None}).get('coin') #获取当前银币值
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
        self.common.closeactivitytest(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入头像界面')
        self.hall_page.wait_element('头像').click()
        self.common.loginuser(self.casedata['user'], self.casedata['password'])
        self.start_step('关闭弹框')
        time.sleep(4)
        i = 0
        while (i < 3):
            try:
                self.sign_page.wait_element('关闭1').click()
                i += 1
            except:
                i = 3
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
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C226_DFQP_Broadcast(TestCase):
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
        self.common.closeactivitytest(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入头像界面')
        self.hall_page.wait_element('头像').click()
        self.common.loginuser(self.casedata['user'], self.casedata['password'])
        self.start_step('关闭弹框')
        time.sleep(4)
        i = 0
        while (i < 3):
            try:
                self.sign_page.wait_element('关闭1').click()
                i += 1
            except:
                i = 3
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C227_DFQP_Broadcast(TestCase):
    '''
    发送两条广播，查看广播消息界面显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        global UserID
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        dict = PHPInterface.get_user_info(UserID) #获取玩家信息
        coin = eval(dict).get('result',{'coin':None}).get('coin') #获取当前银币值
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
        self.common.closeactivitytest(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入头像界面')
        self.hall_page.wait_element('头像').click()
        self.common.loginuser(self.casedata['user'], self.casedata['password'])
        self.start_step('关闭弹框')
        time.sleep(4)
        i = 0
        while (i < 3):
            try:
                self.sign_page.wait_element('关闭1').click()
                i += 1
            except:
                i = 3
        PHPInterface.broadcast(UserID, content='地方棋牌测试专用1')
        time.sleep(1)
        PHPInterface.broadcast(2188068, content='地方棋牌测试专用2')
        time.sleep(1)
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C228_DFQP_Broadcast(TestCase):
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
        self.common.closeactivitytest(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入头像界面')
        self.hall_page.wait_element('头像').click()
        self.common.loginuser(self.casedata['user'], self.casedata['password'])
        self.start_step('关闭弹框')
        time.sleep(4)
        i = 0
        while (i < 3):
            try:
                self.sign_page.wait_element('关闭1').click()
                i += 1
            except:
                i = 3
        self.start_step('进入广播界面')
        self.broadcast_page.wait_element('广播').click()
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C229_DFQP_Broadcast(TestCase):
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
        self.common.closeactivitytest(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入头像界面')
        self.hall_page.wait_element('头像').click()
        self.common.loginuser(self.casedata['user'], self.casedata['password'])
        self.start_step('关闭弹框')
        time.sleep(4)
        i = 0
        while (i < 3):
            try:
                self.sign_page.wait_element('关闭1').click()
                i += 1
            except:
                i = 3
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        PHPInterface.broadcast(UserID,content='地方棋牌测试专用')
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()


if __name__ == '__main__':
    C222_DFQP_Exchange = C227_DFQP_Broadcast()
    C222_DFQP_Exchange.debug_run()