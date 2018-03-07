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

class C31190_DFQP_Yuepai_UI_Display(TestCase):
    '''
    约牌房界面显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver,'预发布')

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(2)
        self.yuepai_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()


class C31191_DFQP_Yuepai_Tournament(TestCase):
    '''
    约牌房跳转邀请赛
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(3)
        self.yuepai_page.wait_element('+按钮').click()
        time.sleep(3)
        self.yuepai_page.screenshot('1.png')
        self.start_step('跳转至邀请赛界面')
        try:
            self.yuepai_page.wait_element('邀请赛-正式服/预发布').click()
            time.sleep(5)
        except:
            self.yuepai_page.wait_element('+按钮').click()
            time.sleep(3)
            self.yuepai_page.wait_element('邀请赛-正式服/预发布').click()
            time.sleep(3)
        self.yuepai_page.screenshot('2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31192_DFQP_Yuepai_CreateRoom_GameUninstalled(TestCase):
    '''
    未下载游戏创建约牌房
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        capabilities = {}
        capabilities['noReset'] = False
        capabilities['resetKeyboard'] = False
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(1)
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入积分房界面')
        self.yuepai_page.wait_element('积分房').click()
        time.sleep(4)
        self.start_step('点击开房')
        self.yuepai_page.wait_element('开房').click()
        time.sleep(4)
        self.yuepai_page.screenshot('1.png')
        self.start_step('点击确定')
        try:
            self.yuepai_page.wait_element('确定').click()
            time.sleep(40)
        except:
            print '未找到确定按钮'
        time.sleep(4)
        Flag = True
        while Flag:
            try:
                self.yuepai_page.wait_element('开房')
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
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()


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
        global user_info,UserID
        user_info = self.common.get_user()
        print user_info
        UserID = user_info.get('mid')
        print 'UserID:%s' % UserID
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = - coin
        PHPInterface.add_money(UserID, AddMoney)  # 将银币值设为0
        crystal = json.loads(user_info1).get('result', {'crystal': None}).get('crystal')  # 获取当前金条值
        AddCrystal = 1000 - crystal
        PHPInterface.add_crystal(UserID, AddCrystal)  # 将金条数目置1000
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        time.sleep(5)
        self.common.closeActivityBtn()
        # i =0
        # while i < 3:
        #     i += 1
        #     try:
        #         self.personinfo_page.wait_element("关闭").click()
        #     except:
        #         print "已关闭窗口"

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
            if (self.yuepai_page.is_exist("立即升级") == True):
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
            PHPInterface.add_money(UserID, 20000)
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(UserID)


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
        global user_info,UserID
        user_info = self.common.get_user()
        print user_info
        UserID = user_info.get('mid')
        print 'UserID:%s' % UserID
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = - coin
        PHPInterface.add_money(UserID, AddMoney)  # 将银币值设为0
        crystal = json.loads(user_info1).get('result', {'crystal': None}).get('crystal')  # 获取当前金条值
        AddCrystal = - crystal
        PHPInterface.add_crystal(UserID, AddCrystal)  # 将金条数目置0
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        time.sleep(5)
        self.common.closeActivityBtn()

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
            if (self.yuepai_page.is_exist("立即升级") == True):
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
            PHPInterface.add_money(UserID, 10000)
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(UserID)


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
        global user_info,UserID
        user_info = self.common.get_user()
        print user_info
        UserID = user_info.get('mid')
        print 'UserID:%s' % UserID
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = - coin
        PHPInterface.add_money(UserID, AddMoney)  # 将银币值设为0
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

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
            PHPInterface.add_money(UserID, 20000)
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(UserID)


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
        global user_info,UserID
        user_info = self.common.get_user()
        print user_info
        UserID = user_info.get('mid')
        print 'UserID:%s' % UserID
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        print user_info1
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = - coin
        PHPInterface.add_money(UserID, AddMoney)  # 将银币值设为0
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

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
            PHPInterface.add_money(UserID, 20000)
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(UserID)


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
        global user_info,UserID
        user_info = self.common.get_user()
        print user_info
        UserID = user_info.get('mid')
        print 'UserID:%s' % UserID
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 60000 - coin
        PHPInterface.add_money(UserID, AddMoney)  # 将银币值设为60000
        crystal = json.loads(user_info1).get('result', {'crystal': None}).get('crystal')  # 获取当前金条值
        AddCrystal = 1000 - crystal
        PHPInterface.add_crystal(UserID, AddCrystal)  # 将金条数目置1000
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

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
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(UserID)

class C31198_DFQP_Yuepai_ScoreRoom_Display(TestCase):
    '''
    积分约牌房房间展示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        global user_info,UserID
        user_info = self.common.get_user()
        print user_info
        UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

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
            print '成功创建积分房'
        except:
            print '创建积分房失败'
        time.sleep(3)
        self.start_step('点击菜单键')
        self.yuepai_page.wait_element('菜单键').click()
        time.sleep(3)
        self.yuepai_page.screenshot('1.png')
        self.yuepai_page.wait_element('斗地主icon').click()
        time.sleep(3)
        self.start_step('点击二维码按钮')
        self.yuepai_page.wait_element('二维码').click()
        time.sleep(3)
        self.yuepai_page.screenshot('2.png')
        self.yuepai_page.wait_element('斗地主icon').click()
        time.sleep(3)
        self.start_step('点击更多按钮')
        self.yuepai_page.wait_element('更多').click()
        time.sleep(3)
        self.yuepai_page.screenshot('3.png')
        self.yuepai_page.wait_element('斗地主icon').click()
        time.sleep(3)
        self.start_step('点击邀请按钮')
        self.yuepai_page.wait_element('邀请-积分房').click()
        time.sleep(3)
        self.yuepai_page.screenshot('4.png')
        self.yuepai_page.wait_element('斗地主icon').click()
        time.sleep(3)
        self.start_step('点击详情按钮')
        self.yuepai_page.wait_element('详情').click()
        time.sleep(3)
        self.yuepai_page.screenshot('5.png')
        self.yuepai_page.wait_element('斗地主icon').click()
        time.sleep(3)
        self.start_step('点击聊天按钮')
        self.yuepai_page.wait_element('聊天').click()
        time.sleep(3)
        self.yuepai_page.screenshot('6.png')
        self.yuepai_page.wait_element('斗地主icon').click()
        time.sleep(3)
        self.start_step('点击准备按钮')
        self.yuepai_page.wait_element('准备').click()
        time.sleep(3)
        self.yuepai_page.screenshot('7.png')
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
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(UserID)


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
        global user_info
        user_info = self.common.get_user()
        print user_info
        user_info1 = PHPInterface.get_user_info(user_info['mid'])  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 60000 - coin
        PHPInterface.add_money(user_info['mid'], AddMoney)  # 将银币值设为60000
        crystal = json.loads(user_info1).get('result', {'crystal': None}).get('crystal')  # 获取当前金条值
        AddCrystal = 1000 - crystal
        PHPInterface.add_crystal(user_info['mid'], AddCrystal)  # 将金条数目置1000
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver, '预发布')
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

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
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['mid'])

__qtaf_seq_tests__ = [C31196_DFQP_Yuepai_CreateCoinRoom_Broke]
if __name__ == '__main__':
    debug_run_all()

