#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
每日任务
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

class C30972_DFQP_Share1(TestCase):
    '''
    大厅进入任务页面---微信邀请好友
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        # PHPInterface.add_mission('微信分享', '微信分享', jump_code=1019, reward=100,sort_order=100,conditions={
        #     "shareCount": {
        #         "num": 1
        #     }
        # })
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.task_page = Task_Page()
        self.start_step("配置微信分享任务")

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入任务页面")
        self.hall_page.wait_element("任务").click()
        time.sleep(2)
        self.task_page.wait_element("每日任务tag").click()
        time.sleep(5)
        self.start_step("微信邀请好友")
        try:
            self.task_page.wait_element("微信邀请好友").click()
            # self.luadriver.find_element_by_xpath("//element/element/taskRewardLayout/content/dayTaskListView/element/dayTaskItem/bg/btn/doTask").click()
            time.sleep(1)
            self.task_page.screenshot('Share1.png')
        except:
            print("暂未此任务")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C30973_DFQP_Share1(TestCase):
    '''
    领取微信任务奖励
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 8
    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        PHPInterface.set_mission_to_complete(mid, 103000, 541)
        self.hall_page = Hall_Page()
        self.task_page = Task_Page()
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入任务页面")
        self.hall_page.wait_element("任务").click()
        time.sleep(2)
        self.task_page.wait_element("每日任务tag").click()
        time.sleep(5)
        self.start_step("微信邀请好友")
        try:
            self.task_page.wait_element("微信邀请好友").click()
            # self.luadriver.find_element_by_xpath("//element/element/taskRewardLayout/content/dayTaskListView/element/dayTaskItem/bg/btn/doTask").click()
            time.sleep(1)
            self.task_page.screenshot('hare1.png')
        except:
            print("暂未此任务")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.release_user(user_info['mid'])
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C30977_DFCP_Task_Interface_TaskEnterGame(TestCase):
    '''
    银币充足做牌局任务
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid,"5000")
        self.hall_page = Hall_Page()
        self.task_page = Task_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

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
        self.common.recover_user(mid)
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()


class C30976_DFCP_Task_Interface_TaskEnterGame1(TestCase):
    '''
    银币不足但未破产做牌局任务
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid,"3000")
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.task_page = Task_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)


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
        self.common.recover_user(mid)
        # self.common.release_user(user_info['mid'])
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()


class C30975_DFCP_Task_TaskandBroke(TestCase):
    '''
    破产状态做牌局任务
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid,"2000")
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)
        self.hall_page = Hall_Page()
        self.task_page = Task_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()

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
        self.common.recover_user(mid)
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()


class C30978_DFCP_Task_Interface_GetReward(TestCase):
    '''
    领取牌局任务奖励
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        PHPInterface.set_mission_to_complete(mid, 103000, 369, 1)
        self.hall_page = Hall_Page()
        self.task_page = Task_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)


    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.hall_page.wait_element("任务").click()
        time.sleep(2)
        self.task_page.wait_element("每日任务tag").click()
        time.sleep(2)
        # self.common.swipeelement(self.task_page.wait_element("玩游戏任务列表2"),self.task_page.wait_element("玩游戏任务列表1"))
        time.sleep(5)
        # self.task_page.wait_element("玩游戏任务1").click()
        # time.sleep(2)
        # try:
        #     self.game_page.wait_element("资源下载-确定").click()
        #     time.sleep(15)
        # except:
        #     print ("游戏已下载")
        # self.hall_page.screenshot('game1.png')
        elements = self.task_page.get_elements("领取奖励")
        count = 0
        print len(elements)
        while(count < len(elements)):
            element_text = elements[count].get_attribute('text')
            if element_text == '领奖励':
                print '找到并点击了领奖励'
                elements[count].click()
                time.sleep(4)
                self.task_page.screenshot("lingqujiangli %s.png" %count )
                break
            count = count + 1

    def post_test(self):

        self.common.recover_user(mid)
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()


# __qtaf_seq_tests__ = [C30975_DFCP_Task_TaskandBroke]
if __name__ == '__main__':
    # C311_DFCP_Hall_Interface_TaskEnterGame2 = C311_DFCP_Hall_Interface_TaskEnterGame2()
    # C311_DFCP_Hall_Interface_TaskEnterGame2.debug_run()
    debug_run_all()
