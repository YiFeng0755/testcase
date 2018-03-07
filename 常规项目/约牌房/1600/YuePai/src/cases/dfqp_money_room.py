#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
游戏币房（列表）
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.sign_page import Sign_Page
from uilib.hall_page import Hall_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common
import common.Interface as PHPInterface
import test_datas,json
from utils.confighelper import ConfigHelper
from utils.constant import user_cfg

class C70652_DFQP_NoDownloadSubgame(TestCase):
    '''
    子游戏未下载点击创建房间
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入记分房界面')
        self.yuepai_page.wait_element('记分房').click()
        time.sleep(4)
        self.yuepai_page.screenshot('1.png')
        elements = self.yuepai_page.get_elements('子游戏')
        i = 2
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('记分房').click()
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
                print 'i = %s' % i
                self.hall_page.screenshot('{index}.png'.format(index=i))
                i += 1
                print '创建房间成功'
            except:
                print '创建房间失败'
            self.luadriver.keyevent(4)
            time.sleep(5)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70671_DFQP_Exceed_15_Minutes(TestCase):
    '''
    玩家创建房间后超过15分钟未开始，自动解散房间
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 25
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        capabilities = {}
        capabilities['newCommandTimeout'] = 902
        self.luadriver = self.common.setupdriver(capabilities)
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入记分房界面')
        self.yuepai_page.wait_element('记分房').click()
        time.sleep(4)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('记分房').click()
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
                print 'i = %s' % i
                self.hall_page.screenshot('before_dissolution{index}.png'.format(index=i))
                print '创建房间成功'
                time.sleep(900)
                self.hall_page.screenshot('after_dissolution{index}.png'.format(index=i))
                i += 1
            except:
                print '创建房间失败'


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70584_DFQP_CreateScoreRoom(TestCase):
    '''
    玩家进入房间后状态
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入记分房界面')
        self.yuepai_page.wait_element('记分房').click()
        time.sleep(4)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('记分房').click()
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
                print 'i = %s' % i
                self.hall_page.screenshot('{index}.png'.format(index=i))
                i += 1
                print '创建房间成功'
            except:
                print '创建房间失败'
            self.luadriver.keyevent(4)
            time.sleep(5)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70585_DFQP_ReadyExceed15Minutes(TestCase):
    '''
    进入房间内准备15分钟后未开始游戏，查看显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 25

    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        capabilities = {}
        capabilities['newCommandTimeout'] = 902
        self.luadriver = self.common.setupdriver(capabilities)
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入记分房界面')
        self.yuepai_page.wait_element('记分房').click()
        time.sleep(4)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('记分房').click()
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
                self.yuepai_page.wait_element('准备').click()
                Tag = True
                print 'i = %s' % i
                self.hall_page.screenshot('before_dissolution{index}.png'.format(index=i))
                print '创建房间成功'
                time.sleep(900)
                self.hall_page.screenshot('after_dissolution{index}.png'.format(index=i))
                i += 1
            except:
                print '创建房间失败'

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70589_DFQP_RoomQRcode(TestCase):
    '''
    点击查看二维码房间号
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入记分房界面')
        self.yuepai_page.wait_element('记分房').click()
        time.sleep(4)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('记分房').click()
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
            time.sleep(1)
            self.yuepai_page.wait_element('二维码').click()
            time.sleep(1)
            print 'i = %s' % i
            self.yuepai_page.screenshot('{index}.png'.format(index=i))
            i += 1
            self.luadriver.keyevent(4)
            time.sleep(5)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70590_DFQP_Microphone(TestCase):
    '''
    查看游戏币房语音功能开启和关闭情况
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入记分房界面')
        self.yuepai_page.wait_element('记分房').click()
        time.sleep(4)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('记分房').click()
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
            self.yuepai_page.wait_element('语音').click()
            time.sleep(1)
            self.yuepai_page.screenshot('open_microphone{index}.png'.format(index=i))
            time.sleep(3)
            self.yuepai_page.wait_element('语音').click()
            time.sleep(1)
            self.yuepai_page.screenshot('close_microphone{index}.png'.format(index=i))
            i += 1
            self.luadriver.keyevent(4)
            time.sleep(5)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70592_DFQP_CustomChatBeforeGameStart(TestCase):
    '''
    游戏未开始前不能输入自定义聊天
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入记分房界面')
        self.yuepai_page.wait_element('记分房').click()
        time.sleep(4)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('记分房').click()
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
            self.yuepai_page.wait_element('聊天').click()
            time.sleep(1)
            print 'i = %s' % i
            self.yuepai_page.screenshot('{index}.png'.format(index=i))
            i += 1
            self.luadriver.keyevent(4)
            time.sleep(1)
            self.luadriver.keyevent(4)
            time.sleep(5)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70594_DFQP_HeadView(TestCase):
    '''
    查看玩家默认头像显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入记分房界面')
        self.yuepai_page.wait_element('记分房').click()
        time.sleep(4)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('记分房').click()
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
            time.sleep(1)
            print 'i = %s' % i
            self.yuepai_page.screenshot('{index}.png'.format(index=i))
            i += 1
            self.luadriver.keyevent(4)
            time.sleep(5)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70596_DFQP_Invitation(TestCase):
    '''
    查看房间内邀请界面
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入记分房界面')
        self.yuepai_page.wait_element('记分房').click()
        time.sleep(4)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('记分房').click()
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
            self.yuepai_page.wait_element('邀请-积分房').click()
            time.sleep(1)
            print 'i = %s' % i
            self.yuepai_page.screenshot('{index}.png'.format(index=i))
            i += 1
            self.luadriver.keyevent(4)
            time.sleep(5)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70598_DFQP_UninstallWechatandQQ(TestCase):
    '''
    游戏币房手机未安装微信/QQ邀请，邀请玩家
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 卸载微信和QQ
        self.luadriver.adb('uninstall com.tencent.mm')
        self.luadriver.adb('uninstall com.tencent.mobileqq')
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入记分房界面')
        self.yuepai_page.wait_element('记分房').click()
        time.sleep(4)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('记分房').click()
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
            self.yuepai_page.wait_element('邀请-积分房').click()
            time.sleep(1)
            self.yuepai_page.wait_element('微信邀请').click()
            time.sleep(1)
            print 'i = %s' % i
            self.yuepai_page.screenshot('wechat_invitation{index}.png'.format(index=i))
            self.yuepai_page.wait_element('QQ邀请').click()
            self.yuepai_page.wait_element('立即邀请').click()
            time.sleep(1)
            self.yuepai_page.screenshot('qq_invitation{index}.png'.format(index=i))
            i += 1
            self.luadriver.keyevent(4)
            time.sleep(1)
            self.luadriver.keyevent(4)
            time.sleep(1)
            self.luadriver.keyevent(4)
            time.sleep(5)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70599_DFQP_InvitationUIDisplay(TestCase):
    '''
    约牌房邀请界面显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 卸载微信和QQ
        self.luadriver.adb('uninstall com.tencent.mm')
        self.luadriver.adb('uninstall com.tencent.mobileqq')
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入记分房界面')
        self.yuepai_page.wait_element('记分房').click()
        time.sleep(4)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        Tag = False
        for element in elements:
            if Tag:
                self.yuepai_page.wait_element('记分房').click()
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
            self.yuepai_page.wait_element('邀请-积分房').click()
            time.sleep(1)
            print 'i = %s' % i
            self.yuepai_page.screenshot('invitation{index}.png'.format(index=i))
            self.yuepai_page.wait_element('微信邀请').click()
            time.sleep(1)
            self.yuepai_page.screenshot('wechat_invitation{index}.png'.format(index=i))
            self.yuepai_page.wait_element('QQ邀请').click()
            self.yuepai_page.wait_element('立即邀请').click()
            time.sleep(1)
            self.yuepai_page.screenshot('qq_invitation{index}.png'.format(index=i))
            self.luadriver.keyevent(4)
            self.yuepai_page.wait_element('在线好友').click()
            time.sleep(1)
            self.yuepai_page.screenshot('friend_online{index}.png'.format(index=i))
            i += 1
            self.luadriver.keyevent(4)
            time.sleep(1)
            self.luadriver.keyevent(4)
            time.sleep(1)
            self.luadriver.keyevent(4)
            time.sleep(5)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

if __name__ == '__main__':
    C70652_DFQP_NoDownloadSubgame = C70652_DFQP_NoDownloadSubgame()
    C70652_DFQP_NoDownloadSubgame.debug_run()