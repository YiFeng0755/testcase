#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
游戏币房（创建）
'''
import time,sys
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

class C70562_DFQP_CreateUI(TestCase):
    '''
    查看游戏币房的创建界面
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        self.start_step("初始化环境")
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
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(2)
        self.yuepai_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70563_DFQP_CloseCreateUI1(TestCase):
    '''
    点击x关闭游戏币房创建界面
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.start_step("初始化环境")
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
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(2)
        self.yuepai_page.wait_element('返回').click()
        time.sleep(1)
        self.yuepai_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70564_DFQP_CloseCreateUI2(TestCase):
    '''
    点击物理返回键关闭游戏币房创建界面
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.start_step("初始化环境")
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
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(2)
        self.luadriver.keyevent(4)
        time.sleep(1)
        self.yuepai_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70565_DFQP_CustomValue(TestCase):
    '''
    勾选游戏底注-自定义选项，查看自定义输入框默认数值
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.start_step("初始化环境")
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
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(2)
        self.yuepai_page.screenshot('1.png')
        self.yuepai_page.wait_element('自定义单选按钮').click()
        self.yuepai_page.screenshot('2.png')
        custom_value = self.yuepai_page.wait_element('自定义输入框').get_attribute('text')
        print custom_value
        print type(custom_value)
        if custom_value == '1' :
            print '自定义值为1'
        else:
            print '自定义值不为1'
            sys.exit()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70566_DFQP_CustomValueEqual0(TestCase):
    '''
    选择底注输入0或-1后的显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.start_step("初始化环境")
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
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(2)
        self.yuepai_page.wait_element('自定义单选按钮').click()
        self.yuepai_page.wait_element('自定义输入框').send_keys('0')
        self.yuepai_page.wait_element('自定义输入框').click()
        self.yuepai_page.wait_element('自定义输入框').send_keys('0')
        self.yuepai_page.screenshot('1.png')
        self.luadriver.keyevent(66)
        self.yuepai_page.screenshot('2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70567_DFQP_CustomValueEqual99999(TestCase):
    '''
    选择底注输入999999999后的显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.start_step("初始化环境")
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
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(2)
        self.yuepai_page.wait_element('自定义单选按钮').click()
        self.yuepai_page.wait_element('自定义输入框').send_keys('0')
        self.yuepai_page.wait_element('自定义输入框').click()
        self.yuepai_page.wait_element('自定义输入框').send_keys('999999999')
        self.yuepai_page.screenshot('1.png')
        self.luadriver.keyevent(66)
        self.yuepai_page.screenshot('2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70568_DFQP_JoinLimit0(TestCase):
    '''
    进房限制输入0或-1后的显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.start_step("初始化环境")
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
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(2)
        self.yuepai_page.wait_element('进房限制').send_keys('0')
        self.yuepai_page.wait_element('进房限制').click()
        self.yuepai_page.wait_element('进房限制').send_keys('0')
        self.yuepai_page.screenshot('1.png')
        self.luadriver.keyevent(66)
        self.yuepai_page.screenshot('2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70569_DFQP_JoinLimit100000000(TestCase):
    '''
    进房限制输入100000000后的显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.start_step("初始化环境")
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
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(2)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        for element in elements:
            text = element.get_attribute('text')
            if not text.isdigit():
                element.click()
            else:
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
            elements1 = self.yuepai_page.get_elements('输入框')
            elements1[0].send_keys('100000000')
            print 'i = %s' % i
            self.yuepai_page.screenshot('input_field{index}.png'.format(index=i))
            self.yuepai_page.wait_element('开房').click()
            time.sleep(3)
            self.yuepai_page.screenshot('open_room{index}.png'.format(index=i))
            i += 1
            self.luadriver.keyevent(4)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70571_DFQP_NotEnoughCoin(TestCase):
    '''
    银币不足，创建一个麻将约牌房
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.start_step("初始化环境")
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
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(2)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        for element in elements:
            text = element.get_attribute('text')
            if not text.isdigit():
                element.click()
            else:
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
            time.sleep(3)
            print 'i = %s' % i
            self.yuepai_page.screenshot('{index}.png'.format(index=i))
            i += 1
            self.luadriver.keyevent(4)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70572_DFQP_NotEnoughCrystal(TestCase):
    '''
    金条不足，创建一个麻将约牌房
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.start_step("初始化环境")
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
        self.start_step('进入银币/金条房界面')
        self.yuepai_page.wait_element('银币/金条房').click()
        time.sleep(2)
        elements = self.yuepai_page.get_elements('子游戏')
        i = 1
        for element in elements:
            text = element.get_attribute('text')
            if not text.isdigit():
                element.click()
            else:
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
            self.start_step('点击金条单选按钮')
            self.yuepai_page.wait_element('金条单选按钮').click()
            self.yuepai_page.wait_element('开房').click()
            time.sleep(3)
            print 'i = %s' % i
            self.yuepai_page.screenshot('{index}.png'.format(index=i))
            i += 1
            self.luadriver.keyevent(4)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()



if __name__ == '__main__':
    C70568_DFQP_JoinLimit0 = C70568_DFQP_JoinLimit0()
    C70568_DFQP_JoinLimit0.debug_run()
