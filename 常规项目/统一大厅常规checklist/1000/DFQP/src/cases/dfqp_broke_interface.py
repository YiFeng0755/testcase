#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌破产测试
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from appiumcenter.luadriver import LuaDriver
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.task_page import Task_Page
from common.common import Common
from common import Interface as PHPInterface

class C201_DFQP_BrokeUI1(TestCase):
    '''
    玩家没有完成分享任务
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
        self.task_page = Task_Page()
        # 截图路径
        global screenshotpath
        screenshotpath = self.common.screenshotpath()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step('关闭破产提示')
        self.luadriver.find_element_by_name('closeBtn').click()
        time.sleep(1)
        self.luadriver.find_element_by_name('freeMoney').click()









    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver('luadriver')

class C201_DFQP_Broke3(TestCase):
    '''
    玩家是VIP查看破产弹框
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
        # 截图路径
        global screenshotpath
        screenshotpath = self.common.screenshotpath()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        UserID = 2198806
        Type = 4
        PHPInterface.set_vip(UserID,Type)
        time.sleep(3)
        Money = self.luadriver.find_element_by_name('Text_gold').get_attribute('text')
        print Money
        print type(Money)
        UserMoney = int(Money.replace(',', ''))
        print UserMoney
        if UserMoney >= 3000:
            AddMoney = 3000 - UserMoney
            PHPInterface.add_money(UserID, AddMoney)
            self.start_step('请手动玩一局破产')

        else:
            AddMoney = 0
            PHPInterface.add_money(UserID, AddMoney)
            self.start_step('已破产，开始测试')
            self.start_step('关闭破产提示')
            self.luadriver.find_element_by_name('closeBtn').click()
            self.start_step('进入川味斗地主页面')
            self.game_page.wait_element('川味斗地主').click()
            self.luadriver.find_element_by_name('button').click()
            self.luadriver.get_screenshot_as_file(screenshotpath + 'C201_DFQP_Broke3.png')

    def post_test(self):
        '''
                测试用例执行完成后，清理测试环境
                '''
        self.common.closedriver('luadriver')

class C201_DFQP_Broke4(TestCase):
    '''
    玩家不是VIP查看破产弹框
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
        # 截图路径
        global screenshotpath
        screenshotpath = self.common.screenshotpath()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        UserID = 2198806
        Type = -1
        PHPInterface.set_vip(UserID,Type)
        time.sleep(3)
        Money = self.luadriver.find_element_by_name('Text_gold').get_attribute('text')
        print Money
        print type(Money)
        UserMoney = int(Money.replace(',', ''))
        print UserMoney
        if UserMoney >= 3000:
            AddMoney = 3000 - UserMoney
            PHPInterface.add_money(UserID, AddMoney)
            self.start_step('请手动玩一局破产')
        else:
            AddMoney = 0
            PHPInterface.add_money(UserID, AddMoney)
            self.start_step('已破产，开始测试')
            self.start_step('关闭破产提示')
            self.luadriver.find_element_by_name('closeBtn').click()
            self.start_step('进入川味斗地主页面')
            self.game_page.wait_element('川味斗地主').click()
            self.luadriver.find_element_by_name('button').click()
            self.luadriver.get_screenshot_as_file(screenshotpath + 'C201_DFQP_Broke4.png')

    def post_test(self):
        '''
                测试用例执行完成后，清理测试环境
                '''
        self.common.closedriver('luadriver')


class C201_DFQP_Broke5(TestCase):
    '''
    玩家领完三次救济
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
        # 截图路径
        global screenshotpath
        screenshotpath = self.common.screenshotpath()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step('关闭破产提示')
        self.luadriver.find_element_by_name('closeBtn').click()
        self.start_step('进入川味斗地主页面')
        self.game_page.wait_element('川味斗地主').click()
        self.luadriver.find_element_by_name('button').click()
        self.luadriver.get_screenshot_as_file(screenshotpath + 'C201_DFQP_Broke5.png')

    def post_test(self):
        '''
                测试用例执行完成后，清理测试环境
                '''
        self.common.closedriver('luadriver')


if __name__ == '__main__':
    C001_DFQP_Broke = C201_DFQP_Broke4()
    C001_DFQP_Broke.debug_run()