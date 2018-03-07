#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
不自动准备游戏
'''

import time
from common.common import Common
from runcenter.testcase import TestCase, debug_run_all
from runcenter.enums import EnumPriority, EnumStatus
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page
from dfqp_gameAutoReady import BaseCase

class C27638_notAutoReady_gameRoomDisplay(BaseCase):
    '''
    不自动准备游戏进入房间查看界面显示
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
                if not BaseCase.gameIsAutoReady(self, game) and BaseCase.enterGame(self, game, needClickRigt):
                    gameId = game.get_attribute("name")
                    if not self.game_page.element_is_exist("准备"):
                        self.assert_equal(gameId+"游戏没有找到准备按钮", True, False)
                    else:
                        self.game_page.screenshot(gameId + "_intoTheRoom.png")
                    BaseCase.gameToHall(self)
        BaseCase.test(self, traverseGameList)
            
    def post_test(self):
        BaseCase.post_test(self)
        
class C27639_notAutoReady_readyDisplay(BaseCase):
    '''
    进入房间查看准备后界面显示
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
                if not BaseCase.gameIsAutoReady(self, game) and BaseCase.enterGame(self, game, needClickRigt):
                    gameId = game.get_attribute("name")
                    try:
                        self.game_page.wait_element("准备").click()
                        if self.game_page.element_is_exist("准备", 2):
                            self.assert_equal(gameId+" 点击准备按钮没有准备", True, False)
                        else:
                            self.game_page.screenshot(gameId + "_afterClickReady.png")
                    except:
                        self.assert_equal(gameId+" 游戏没有找到准备按钮", True, False)
#                         self.game_page.screenshot(gameId + "_noReadBtn.png")
                
                    BaseCase.gameToHall(self)
        BaseCase.test(self, traverseGameList)
            
    def post_test(self):
        BaseCase.post_test(self)
        
class C27642_notAutoReady_15sNotReady(BaseCase):
    '''
    15s不准备，查看界面显示
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
                if not BaseCase.gameIsAutoReady(self, game) and BaseCase.enterGame(self, game, needClickRigt):
                    gameId = game.get_attribute("name")
                    if not self.game_page.element_is_exist("准备"):
                        self.assert_equal(gameId+"游戏没有找到准备按钮", True, False)
                    else:
                        time.sleep(15)
                        if not self.game_page.element_is_exist("准备"):
                            self.assert_equal(gameId+" 15S 不准备后，没有准备按钮", True, False)
                        else:
                            self.game_page.screenshot(gameId + "_after15sNotReady.png")
                    BaseCase.gameToHall(self)
        BaseCase.test(self, traverseGameList)
            
    def post_test(self):
        BaseCase.post_test(self)
        
class C27643_notAutoReady_60sNotReady(BaseCase):
    '''
    60s不准备，查看界面显示
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
                if not BaseCase.gameIsAutoReady(self, game) and BaseCase.enterGame(self, game, needClickRigt):
                    gameId = game.get_attribute("name")
                    if not self.game_page.element_is_exist("准备"):
                        self.assert_equal(gameId+"游戏没有找到准备按钮", True, False)
                    else:
                        time.sleep(60)
                        
                        self.game_page.screenshot(gameId + "_after60sNotReady.png")
                    BaseCase.gameToHall(self)
        BaseCase.test(self, traverseGameList)
            
    def post_test(self):
        BaseCase.post_test(self)
        
class C27645_notAutoReady_fakeRoomReady(BaseCase):
    '''
    假房间情况下准备
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
                if not BaseCase.gameIsAutoReady(self, game) and BaseCase.enterGame(self, game, needClickRigt):
                    gameId = game.get_attribute("name")
                    
                    if not self.game_page.element_is_exist("准备"):
                        self.assert_equal(gameId+" 进入房间没有准备按钮", True, False)
                    else:
                        time.sleep(15)
                        try:
                            self.game_page.wait_element("准备").click()
                            if self.game_page.element_is_exist("准备", 2):
                                self.assert_equal(gameId+" 假房间内准备后还存在准备按钮", True, False)
                            else:
                                self.game_page.screenshot(gameId + "_fakeRoomReady.png")
                        except:
                            self.assert_equal(gameId+" 15S不准备后，没有准备按钮", True, False)
                    
                    BaseCase.gameToHall(self)
        BaseCase.test(self, traverseGameList)
            
    def post_test(self):
        BaseCase.post_test(self)
        
class C27646_notAutoReady_fakeRoomChangeTable(BaseCase):
    '''
    假房间情况下换桌
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
                if not BaseCase.gameIsAutoReady(self, game) and BaseCase.enterGame(self, game, needClickRigt):
                    gameId = game.get_attribute("name")
                    
                    if not self.game_page.element_is_exist("准备"):
                        self.assert_equal(gameId+" 进入房间没有准备按钮", True, False)
                    else:
                        time.sleep(15)
                        try:
                            self.game_page.wait_element("换桌").click()
                            if not self.game_page.element_is_exist("准备", 30):
                                self.assert_equal(gameId+" 假房间内换桌后不存在准备按钮", True, False)
                            else:
                                self.game_page.screenshot(gameId + "_fakeRoomReady.png")
                        except:
                            self.assert_equal(gameId+" 15S不准备后，没有换桌按钮", True, False)
                    
                    BaseCase.gameToHall(self)
        BaseCase.test(self, traverseGameList)
            
    def post_test(self):
        BaseCase.post_test(self)
        
class C27647_notAutoReady_ChangeTableAfterReady(BaseCase):
    '''
    准备后换桌
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
                if not BaseCase.gameIsAutoReady(self, game) and BaseCase.enterGame(self, game, needClickRigt):
                    gameId = game.get_attribute("name")
                    try:
                        self.game_page.wait_element("准备").click()
                        try:
                            self.game_page.wait_element("换桌").click()
                            if self.game_page.element_is_exist("准备", 2):
                                self.assert_equal(gameId+" 点击准备后换桌准备又出现", True, False)
                            else:
                                self.game_page.screenshot(gameId + "_afterReadyChangeTable.png")
                        except:
                            self.assert_equal(gameId+" 游戏没有找到换桌按钮", True, False)
                        
                    except:
                        self.assert_equal(gameId+" 游戏没有找到准备按钮", True, False)
                    
                    
                    BaseCase.gameToHall(self)
        BaseCase.test(self, traverseGameList)
            
    def post_test(self):
        BaseCase.post_test(self)
        
class C27648_notAutoReady_changeTableBeforeReady(BaseCase):
    '''
    不准备情况下，点击换桌
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
                if not BaseCase.gameIsAutoReady(self, game) and BaseCase.enterGame(self, game, needClickRigt):
                    gameId = game.get_attribute("name")
                    try:
                        changeBtn = self.game_page.wait_element("换桌")
                        time.sleep(1)
                        changeBtn.click()
                        if not self.game_page.element_is_exist("准备", 30):
                            self.assert_equal(gameId+" 点击换桌按钮后准备按钮消失", True, False)
                        else:
                            self.game_page.screenshot(gameId + "_changeTableBeforeReady.png")
                    except:
                        self.assert_equal(gameId+" 游戏没有找到换桌按钮", True, False)
#                         self.game_page.screenshot(gameId + "_noChangeTableBtn.png")
                    
                    
                    BaseCase.gameToHall(self)
        BaseCase.test(self, traverseGameList)
            
    def post_test(self):
        BaseCase.post_test(self)
        
class C27649_notAutoReady_readyAfterContinuousChangeTable(BaseCase):
    '''
    多次交替点击换桌、准备，查看游戏界面显示
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
                
                if not BaseCase.gameIsAutoReady(self, game) and BaseCase.enterGame(self, game, needClickRigt):
                    gameId = game.get_attribute("name")
                    hasChangeBtn = True
                    for i in range(0,5):
                        try:
                            self.game_page.wait_element("换桌").click()
                            if i != 4:
                                time.sleep(6)
                            
                        except:
                            self.assert_equal(gameId+" 游戏没有找到换桌按钮", True, False)
                            hasChangeBtn = False
#                             self.game_page.screenshot(gameId + "_noChangeTableBtn.png")
                            break
                    if hasChangeBtn:    
                        if not self.game_page.element_is_exist("准备", 30):
                            self.assert_equal(gameId+" 多次点击换桌按钮后准备按钮消失", True, False)
                        else:
                            self.game_page.wait_element("准备").click()
                            self.game_page.screenshot(gameId + "_readyAfterContinuousChangeTable.png")
                    
                    BaseCase.gameToHall(self)
        BaseCase.test(self, traverseGameList)
            
    def post_test(self):
        BaseCase.post_test(self)
        
# __qtaf_seq_tests__ = [C27638_notAutoReady_gameRoomDisplay]#C27632_onReady_continuousChangeTable,C27627_readyBtnStatus,C27631_onReady_changeTable
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()