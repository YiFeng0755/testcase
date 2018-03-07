#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
自动准备
'''

import time
from common.common import Common
from runcenter.testcase import TestCase, debug_run_all
from runcenter.enums import EnumPriority, EnumStatus
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page

class BaseCase(TestCase):
    gameIDList = ['game203', 'game24', 'game1502', 'game2603']#斗鸡游戏'game23'，在测试线会倒计时自动准备正式服不会需要确认
    def pre_test(self):
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.common = Common()
        self.start_step("初始化driver")
        self.driver = self.common.setupdriver()
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.driver)
    
    def enterGame(self, gameElment, needClickRight=False):
        gameId = gameElment.get_attribute("name")
        self.start_step("点击游戏："+gameId)
        if needClickRight:
            self.click_rightArrow()
        gameElment.click()
        if self.game_page.game_is_download():
            if not self.game_page.element_is_exist("广播") or self.game_page.element_is_exist("游戏级别", 1):
            #判断点击场次上方的（标准场、叫分场、或者是金条场）
                self.game_page.click_game_play()
            self.start_step("进入游戏房间："+gameId)
            if self.game_page.element_is_exist("初级场"):
                self.game_page.wait_element("初级场").click()
            elif self.game_page.element_is_exist("第一个房间"):
                self.game_page.wait_element("第一个房间").click()
            else:
                self.assert_equal(gameId+"进入游戏房间失败", False, True)
                self.gameToHall()
                return False
            return True
        else:
            self.assert_equal(gameId+"进入游戏失败", False, True)
            return False
        
    def gameIsAutoReady(self, gameElment):
        gameId = gameElment.get_attribute("name")
        return gameId in self.gameIDList
    
    def click_rightArrow(self):
        if self.hall_page.element_is_exist("右三角"):
            self.hall_page.wait_element("右三角").click()
            time.sleep(1)
            return True
        return False
            
    def test(self, traverseGameList):
        game_list = self.game_page.get_game_list()
        traverseGameList(game_list)
        if self.click_rightArrow():
            game_list = self.game_page.get_game_list()
            traverseGameList(game_list, True)
            
    def gameToHall(self):
        self.yuepai_page.is_exist_yuepairoom()
        if self.game_page.element_is_exist("返回1"):
            self.game_page.wait_element("返回1").click()
        elif self.game_page.element_is_exist("返回大厅"):
            self.game_page.wait_element("返回大厅").click()
        time.sleep(2)
    
    def post_test(self):
        self.common.closedriver()

class C27627_readyBtnStatus(BaseCase):
    '''
    进入房间查看准备按钮及状态
    '''
    owner = "GuixiangGui"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    
    def pre_test(self):
        BaseCase.pre_test(self)
        
    def run_test(self):
        def traverseGameList(game_list, needClickRigt=False):
            for game in game_list:
                if BaseCase.gameIsAutoReady(self, game) and BaseCase.enterGame(self, game, needClickRigt):
                    gameId = game.get_attribute("name")
                    if not self.game_page.element_is_exist("换桌"):
                        self.assert_equal(gameId+"游戏没有换桌按钮", True, False)
                    elif self.game_page.element_is_exist("准备", 0.2):
                        gameId = game.get_attribute("name")
                        self.assert_equal(gameId+"游戏没有自动准备", True, False)
#                         self.game_page.screenshot(gameId + "_notAutoReady.png")
                    BaseCase.gameToHall(self)
                    
        BaseCase.test(self, traverseGameList)
    
    def post_test(self):
        BaseCase.post_test(self)

class C27631_onReady_changeTable(BaseCase):
    '''
    准备状态下换桌
    '''
    owner = "GuixiangGui"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    
    def pre_test(self):
        BaseCase.pre_test(self)
    
    def run_test(self):
        def traverseGameList(game_list, needClickRigt=False):
            for game in game_list:
                if BaseCase.gameIsAutoReady(self, game) and BaseCase.enterGame(self, game, needClickRigt):
                    gameId = game.get_attribute("name")
                    try:
                        self.game_page.wait_element("换桌").click()
                        time.sleep(0.5)
                        if self.game_page.element_is_exist("准备", 0.5):
                            self.assert_equal(gameId+"游戏换桌后没有自动准备", True, False)
                        else:
                            self.game_page.screenshot(gameId + "_after_changeTable.png")
                    except:
                        self.assert_equal(gameId+"没有找到换桌按钮", False, True)
                        
                    BaseCase.gameToHall(self)
                    
        BaseCase.test(self, traverseGameList)
    
    def post_test(self):
        BaseCase.post_test(self)

class C27632_onReady_continuousChangeTable(BaseCase):
    '''
        连续换桌5次查看桌面显示
    '''
    owner = "GuixiangGui"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    
    def pre_test(self):
        BaseCase.pre_test(self)
    
    def run_test(self):
        def traverseGameList(game_list, needClickRigt=False):
            for game in game_list:
                if BaseCase.gameIsAutoReady(self, game) and BaseCase.enterGame(self, game, needClickRigt):
                    gameId = game.get_attribute("name")
                    try:
                        for i in range(0,5):
                            self.game_page.wait_element("换桌").click()
                            if i!=4:
                                time.sleep(3.5)
                        time.sleep(0.5)
                        if self.game_page.element_is_exist("准备", 0.5):
                            self.assert_equal(gameId+"游戏换桌后没有自动准备", True, False)
#                                 self.game_page.screenshot(gameId + "_notAutoReady.png")
                        else:
                            self.game_page.screenshot(gameId + "_after_continuousChangeTable.png")
                    except:
                        self.assert_equal(gameId+"游戏没有换桌按钮", True, False)
                    
                    BaseCase.gameToHall(self)
        BaseCase.test(self, traverseGameList)
    
    def post_test(self):
        BaseCase.post_test(self)

# __qtaf_seq_tests__ = [C27627_readyBtnStatus]#C27632_onReady_continuousChangeTable,C27627_readyBtnStatus,C27631_onReady_changeTable
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()