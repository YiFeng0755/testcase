#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌任务接口配置相关用例
'''
import time
import datetime
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.task_page import Task_Page
from uilib.hall_page import Hall_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.game_page import Game_Page
from common.common import Common
import test_datas
from datacenter import dataprovider
import common.Interface as PHPInterface
testdata=test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C309_DFCP_Task_Interface_TaskEnterGame(TestCase):
    '''
    金币足够进场，点击任务列表的牌局类任务的,做任务按钮
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.luadriver = self.common.setupdriver()
        PHPInterface.add_money(self.casedata['mid'], 5000)
        self.hall_page = Hall_Page()
        self.task_page = Task_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.hall_page.wait_element("任务").click()
        time.sleep(2)
        self.task_page.wait_element("每日任务tag").click()
        time.sleep(2)
        self.common.swipeelement(self.task_page.wait_element("玩游戏任务列表2"),self.task_page.wait_element("玩游戏任务列表1"))
        time.sleep(2)
        self.task_page.wait_element("玩游戏任务1").click()
        time.sleep(2)
        try:
            self.game_page.wait_element("资源下载-确定").click()
            time.sleep(15)
        except:
            print ("游戏已下载")
        self.hall_page.screenshot('game1.png')

    def post_test(self):
        self.common.closedriver()

testdata=test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C310_DFCP_Task_Interface_TaskEnterGame1(TestCase):
    '''
    金币不足，但是未破产，点击任务列表的牌局类任务的【做任务按钮】
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.start_step("获取当前用户的银币值")
        dict = PHPInterface.get_user_info(self.casedata['mid'])  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        AddMoney = 3000 - coin
        PHPInterface.add_money(self.casedata['mid'], AddMoney)
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.task_page = Task_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
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
        self.hall_page.wait_element("任务").click()
        time.sleep(2)
        self.task_page.wait_element("每日任务tag").click()
        time.sleep(2)
        self.common.swipeelement(self.task_page.wait_element("玩游戏任务列表2"),self.task_page.wait_element("玩游戏任务列表1"))
        time.sleep(2)
        self.task_page.wait_element("玩游戏任务1").click()
        time.sleep(2)
        try:
            self.game_page.wait_element("资源下载-确定").click()
            time.sleep(15)
        except:
            print ("游戏已下载")
        self.hall_page.screenshot('game1.png')

    def post_test(self):
        PHPInterface.add_money(self.casedata['mid'], 10000)
        self.common.closedriver()

testdata = test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C311_DFCP_Task_Interface_TaskEnterGame2(TestCase):
    '''
    破产，点击任务列表的牌局类任务的【做任务按钮】
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.luadriver = self.common.setupdriver()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page = Hall_Page()
        self.task_page = Task_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"
        self.start_step("获取当前用户的银币值")
        dict = PHPInterface.get_user_info(self.casedata['mid'])  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        AddMoney = 2000 - coin
        PHPInterface.add_money(self.casedata['mid'], AddMoney)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.hall_page.wait_element("任务").click()
        time.sleep(2)
        self.task_page.wait_element("每日任务tag").click()
        time.sleep(2)
        self.common.swipeelement(self.task_page.wait_element("玩游戏任务列表2"),self.task_page.wait_element("玩游戏任务列表1"))
        time.sleep(2)
        self.task_page.wait_element("玩游戏任务1").click()
        time.sleep(2)
        try:
            self.game_page.wait_element("资源下载-确定").click()
            time.sleep(15)
        except:
            print ("游戏已下载")
        self.hall_page.screenshot('game1.png')

    def post_test(self):
        PHPInterface.add_money(self.casedata['mid'], 10000)
        self.common.closedriver()

# __qtaf_seq_tests__ = [C311_DFCP_Task_Interface_TaskEnterGame2]
if __name__ == '__main__':
    # C311_DFCP_Hall_Interface_TaskEnterGame2 = C311_DFCP_Hall_Interface_TaskEnterGame2()
    # C311_DFCP_Hall_Interface_TaskEnterGame2.debug_run()
    debug_run_all()
