#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
游戏币房（广播邀请）
'''
import time,sys
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.broadcast_page import Broadcast_Page
from uilib.hall_page import Hall_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common
import common.Interface as PHPInterface
import test_datas,json
from utils.confighelper import ConfigHelper
from utils.constant import user_cfg

class C70600_DFQP_BroadcastEnoughMoney(TestCase):
    '''
    银币充足，查看广播邀请显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        global user_info, UserID
        userinfo_and_mid = self.common.get_idle_userinfo_and_mid()
        user_info = userinfo_and_mid.get('userinfo')
        print user_info
        UserID = userinfo_and_mid.get('mid')
        print 'UserID:%s' % UserID
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        AddMoney = 60000 - coin
        PHPInterface.add_money(UserID, AddMoney)  # 将银币值设为60000
        PHPInterface.set_level(UserID,16)
        self.start_step("初始化环境")
        # 初始化Luadriver
        args = {}
        args['newCommandTimeout'] = 305
        self.luadriver = self.common.setupdriver(args)
        self.broadcast_page = Broadcast_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        time.sleep(5)
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入广播界面')
        self.broadcast_page.wait_element('广播').click()
        self.broadcast_page.wait_element('输入文字').send_keys('11')
        time.sleep(300)
        self.broadcast_page.wait_element('发送').click()
        time.sleep(4)
        self.broadcast_page.screenshot('1.png')
        self.start_step('重新进入广播界面')
        self.broadcast_page.wait_element('广播').click()
        self.broadcast_page.wait_element('输入文字').send_keys('11')
        self.broadcast_page.wait_element('发送').click()
        self.broadcast_page.screenshot('2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        try:
            PHPInterface.set_level(UserID, 0)
            PHPInterface.add_money(UserID, 10000-coin)
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C70601_DFQP_BroadcastNotEnoughMoney(TestCase):
    '''
    银币不足，查看广播邀请显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global user_info,UserID
        user_info = self.common.get_user()
        UserID = user_info.get('mid')
        print 'UserID:%s' % UserID
        self.start_step("初始化环境")
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.broadcast_page = Broadcast_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        time.sleep(5)
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入广播界面')
        self.broadcast_page.wait_element('广播').click()
        self.broadcast_page.wait_element('输入文字').send_keys('11')
        self.broadcast_page.wait_element('发送').click()
        self.broadcast_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C70583_DFQP_TableDisplay(TestCase):
    '''
    查看牌桌信息显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global user_info, UserID,coin
        userinfo_and_mid = self.common.get_idle_userinfo_and_mid()
        user_info = userinfo_and_mid.get('userinfo')
        print user_info
        UserID = userinfo_and_mid.get('mid')
        print 'UserID:%s' % UserID
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 20000 - coin
        PHPInterface.add_money(UserID, AddMoney)  # 将银币值设为20000
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        self.start_step("初始化环境")
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)
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
        time.sleep(4)
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(4)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('银币/金条房').click()
                time.sleep(2)
            text = element.get_attribute('text')
            if not text.isdigit():
                element.click()
            else:
                Tag = False
                continue
            try:
                self.yuepai_page.wait_element('确定').click()
            except:
                print '未找到确定按钮'
            Flag = True
            while Flag:
                try:
                    percent = self.yuepai_page.wait_element('百分比').get_attribute('text')
                    print percent
                    time.sleep(1)
                except:
                    Flag = False
            self.yuepai_page.wait_element('开房').click()
            time.sleep(5)
            try:
                self.yuepai_page.wait_element('准备')
                Tag = True
                print '创建房间成功'
            except:
                print '创建房间失败'
            print 'i = %s' % i
            self.yuepai_page.screenshot('{index}.png'.format(index=i))
            i += 1
            self.luadriver.keyevent(4)
            time.sleep(5)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        print coin
        try:
            PHPInterface.add_money(UserID, 10000-coin)
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C70575_DFQP_CreateCoinRoom(TestCase):
    '''
    创建麻将银币/金条房
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global user_info, UserID,coin
        userinfo_and_mid = self.common.get_idle_userinfo_and_mid()
        user_info = userinfo_and_mid.get('userinfo')
        print user_info
        UserID = userinfo_and_mid.get('mid')
        print 'UserID:%s' % UserID
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        AddMoney = 20000 - coin
        PHPInterface.add_money(UserID, AddMoney)  # 将银币值设为20000
        time.sleep(2)
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        self.start_step("初始化环境")
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)
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
        time.sleep(4)
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(4)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('银币/金条房').click()
                time.sleep(2)
            text = element.get_attribute('text')
            if not text.isdigit():
                element.click()
            else:
                Tag = False
                continue
            try:
                self.yuepai_page.wait_element('确定').click()
            except:
                print '未找到确定按钮'
            Flag = True
            while Flag:
                try:
                    percent = self.yuepai_page.wait_element('百分比').get_attribute('text')
                    print percent
                    time.sleep(1)
                except:
                    Flag = False
            self.yuepai_page.wait_element('开房').click()
            time.sleep(5)
            try:
                self.yuepai_page.wait_element('准备')
                Tag = True
                print '创建房间成功'
            except:
                print '创建房间失败'
            print 'i = %s' % i
            self.yuepai_page.screenshot('{index}.png'.format(index=i))
            i += 1
            self.luadriver.keyevent(4)
            time.sleep(5)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        print coin
        try:
            PHPInterface.add_money(UserID, 10000-coin)
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C70588_DFQP_MoneyRoomComboBox(TestCase):
    '''
    游戏币房菜单下拉框按钮
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        global user_info, UserID, coin
        userinfo_and_mid = self.common.get_idle_userinfo_and_mid()
        user_info = userinfo_and_mid.get('userinfo')
        print user_info
        UserID = userinfo_and_mid.get('mid')
        print 'UserID:%s' % UserID
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 20000 - coin
        PHPInterface.add_money(UserID, AddMoney)  # 将银币值设为20000
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        self.start_step("初始化环境")
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)
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
        time.sleep(4)
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(4)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('银币/金条房').click()
                time.sleep(2)
            text = element.get_attribute('text')
            if not text.isdigit():
                element.click()
            else:
                Tag = False
                continue
            try:
                self.yuepai_page.wait_element('确定').click()
            except:
                print '未找到确定按钮'
            Flag = True
            while Flag:
                try:
                    percent = self.yuepai_page.wait_element('百分比').get_attribute('text')
                    print percent
                    time.sleep(1)
                except:
                    Flag = False
            self.yuepai_page.wait_element('开房').click()
            time.sleep(5)
            try:
                self.yuepai_page.wait_element('准备')
                Tag = True
                print '创建房间成功'
            except:
                print '创建房间失败'
            self.yuepai_page.wait_element('菜单键').click()
            self.yuepai_page.wait_element('设置键').click()
            time.sleep(1)
            print 'i = %s' % i
            self.yuepai_page.screenshot('setting_button{index}.png'.format(index=i))
            self.luadriver.keyevent(4)
            self.yuepai_page.wait_element('菜单键').click()
            self.yuepai_page.wait_element('退出键').click()
            time.sleep(4)
            self.yuepai_page.screenshot('exit_button{index}.png'.format(index=i))
            i += 1

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        print coin
        try:
            PHPInterface.add_money(UserID, 10000-coin)
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C70573_DFQP_99999999CreateCoinRoom(TestCase):
    '''
    查看携带99999999创建银币房
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global user_info,UserID,coin
        userinfo_and_mid = self.common.get_idle_userinfo_and_mid()
        user_info = userinfo_and_mid.get('userinfo')
        print user_info
        UserID = userinfo_and_mid.get('mid')
        print 'UserID:%s' % UserID
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        AddMoney = 99999999 - coin
        PHPInterface.add_money(UserID, AddMoney)  # 将银币值设为99999999
        time.sleep(2)
        user_info1 = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        self.start_step("初始化环境")
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)
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
        time.sleep(4)
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(4)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('银币/金条房').click()
                time.sleep(2)
            text = element.get_attribute('text')
            if not text.isdigit():
                element.click()
            else:
                Tag = False
                continue
            try:
                self.yuepai_page.wait_element('确定').click()
            except:
                print '未找到确定按钮'
            Flag = True
            while Flag:
                try:
                    percent = self.yuepai_page.wait_element('百分比').get_attribute('text')
                    print percent
                    time.sleep(1)
                except:
                    Flag = False
            self.yuepai_page.wait_element('开房').click()
            time.sleep(5)
            try:
                self.yuepai_page.wait_element('准备')
                Tag = True
                print '创建房间成功'
            except:
                print '创建房间失败'
            self.yuepai_page.wait_element('头像').click()
            time.sleep(2)
            print 'i = %s' % i
            self.yuepai_page.screenshot('{index}.png'.format(index=i))
            total_money_value = self.yuepai_page.wait_element('银币值').get_attribute('text')
            i += 1
            #money_value = total_money_value.replace(',','')
            print total_money_value
            print type(total_money_value)
            self.luadriver.keyevent(4)
            time.sleep(1)
            self.luadriver.keyevent(4)
            time.sleep(5)
            if total_money_value == u'9999.9万':
                print '玩家银币数正常显示9999.9万'
            else:
                print '玩家银币数显示不正常'
                sys.exit()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        print coin
        try:
            PHPInterface.add_money(UserID, 10000-coin)
            self.common.deletefile(self.luadriver)
            time.sleep(1)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

if __name__ == '__main__':
    C70600_DFQP_BroadcastEnoughMoney = C70600_DFQP_BroadcastEnoughMoney()
    C70600_DFQP_BroadcastEnoughMoney.debug_run()