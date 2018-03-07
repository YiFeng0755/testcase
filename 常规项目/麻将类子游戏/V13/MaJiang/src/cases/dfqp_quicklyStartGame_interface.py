#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
快速开始
'''

import re
import time
from common.common import Common
import common.Interface as PHPInterface
from runcenter.testcase import TestCase, debug_run_all
from runcenter.enums import EnumPriority, EnumStatus
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page


class C27385_quicklyStartGame_coinsEnough(TestCase):
    '''
    玩家自身携带条件不足够进入全部玩法场次时，快速开始入场
    '''
    owner = "GuixiangGui"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    
    def pre_test(self):
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.common = Common()
        self.start_step("初始化driver")
        self.driver = self.common.setupdriver()
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.driver)
        
    def run_test(self):
        
        def test_game(gameElement, needClickRight, isTiro = True):
            gameId = gameElement.get_attribute("name")
            self.start_step("进入子游戏%s " %gameId)
            levelConfig = PHPInterface.get_levelconfig(re.search('\d+', gameId).group(), 0, 0, 12)
            tiro_high_limit = int(levelConfig.get("values").get("HIGH_LIMIT"))
            screenName = gameId
            if tiro_high_limit < 0 and not isTiro:
                return
            if isTiro:
                if tiro_high_limit < 0:
                    tiro_high_limit = int(levelConfig.get("values").get("LOW_LIMIT"))+500
                self.common.set_coin(self.mid, tiro_high_limit-100)
                screenName = screenName+'Tiro.png'
            else:
                self.common.set_coin(self.mid, tiro_high_limit+100)
                screenName = screenName+'Midrange.png'
            
            self.common.switchserver()
            self.common.closeActivityBtn()
                
            if needClickRight and self.hall_page.element_is_exist("右三角"):
                self.hall_page.wait_element("右三角").click()
                
            self.start_step("开始快速开场测试")
            gameElement.click()
            
            self.game_page.wait_element("快速开始").click()
            if self.game_page.element_is_exist("菜单键", 10):
                self.game_page.screenshot(screenName)
            else:
                self.game_page.screenshot(gameId+"_intoRoom_fail.png")
                
            self.yuepai_page.is_exist_yuepairoom()
            # while True:
            #     if self.hall_page.element_is_exist("预发布"):
            #         break
            #     self.driver.back()
        
        def traverseGameList(gameList, needClickRight=False):
            for gameElement in gameList:
                if needClickRight and self.hall_page.element_is_exist("右三角"):
                    self.hall_page.wait_element("右三角").click()
                gameElement.click()
                if self.hall_page.element_is_exist("重新获取", 3):
                    self.game_page.screenshot(gameElement.get_attribute("name")+"_open_failed.png")
                    self.hall_page.wait_element("关闭对话框").click()
                    continue              
                self.game_page.game_is_download()
                if self.game_page.element_not_exist("广播"):
                    self.game_page.click_game_play()
                roomLevel = self.game_page.get_elements("房间场次")
                if len(roomLevel)>1:
                    try:
                        test_game(gameElement, needClickRight, True)
                        test_game(gameElement, needClickRight, False)
                    except:
                        self.game_page.screenshot(gameElement.get_attribute("name")+"_failed.png")
                 
                try:
                    self.start_step("退出房间")
                    self.yuepai_page.is_exist_yuepairoom()
                    self.game_page.wait_element("返回1").click()
                except:
                    self.log_info("退出房间失败")
        
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("遍历首页游戏列表")
        traverseGameList(self.game_page.get_game_list())
        try:
            self.hall_page.wait_element("右三角").click()
            traverseGameList(self.game_page.get_game_list(), True)
        except:
            print "没有右三角按钮"
            
    def post_test(self):
        self.common.closedriver()
        self.common.recover_user(self.mid)
        
class C27386_quicklyStartGame_coinsBankruptcy(TestCase):
    '''
    玩家自身携带条件不足够进入全部玩法场次时，快速开始入场
    '''
    owner = "GuixiangGui"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    
    def pre_test(self):
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.common = Common()
        self.start_step("初始化driver")
        self.driver = self.common.setupdriver()
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.driver)
        
    def run_test(self):
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        print mid
        def test_game(gameElement, needClickRight, isSafeBox = False):
            gameId = gameElement.get_attribute("name")
            self.start_step("进入子游戏%s " % gameId)
            levelConfig = PHPInterface.get_levelconfig(re.search('\d+', gameId).group(), 0, 0, 12)
            bankrupt_limit = int(levelConfig.get("values").get("BANKRUPT_LIMIT"))
            print bankrupt_limit
            global screenName
            screenName = gameId
            if isSafeBox:
                self.common.set_safeBoxMoney(mid, bankrupt_limit+100, 0)
                self.common.set_coin(mid, bankrupt_limit-100)
                screenName = screenName+'_safeBox_have_money.png'
            else:
                self.common.set_safeBoxMoney(mid, 0, 0)
                self.common.set_coin(mid, bankrupt_limit-100)
                screenName = screenName+'_safeBox_no_money.png'
            
            self.common.switchserver()
            self.common.closeActivityBtn()
            
            if needClickRight and self.hall_page.element_is_exist("右三角"):
                self.hall_page.wait_element("右三角").click()
            gameElement.click()
            if self.hall_page.element_is_exist("重新获取", 3):
                self.game_page.screenshot(gameElement.get_attribute("name")+"_open_failed.png")
                self.hall_page.wait_element("关闭对话框").click()
                return
            self.game_page.game_is_download()
            if self.game_page.element_not_exist("广播"):
                self.game_page.click_game_play()
                
#             if needClickRight and self.hall_page.element_is_exist("右三角"):
#                 self.hall_page.wait_element("右三角").click()

            self.start_step("开始快速开场测试"+gameId)
            # gameElement.click()
            #
            self.game_page.wait_element("快速开始").click()
            time.sleep(2)
            self.game_page.screenshot(screenName)
            while self.hall_page.element_is_exist("关闭对话框", 3):
                self.hall_page.wait_element("关闭对话框").click()
            # while True:
            #     self.driver.back()
            #     if(self.hall_page.element_is_exist("预发布")):
            #         break
        
        def traverseGameList(gameList, needClickRight=False):
            for gameElement in gameList:
                
                    
                test_game(gameElement, needClickRight, False)
                test_game(gameElement, needClickRight, True)
#                 try:
#                     test_game(gameElement, needClickRight, False)
#                     test_game(gameElement, needClickRight, True)
#                 except:
#                     self.game_page.screenshot(gameElement.get_attribute("name")+"_failed.png")
#                 self.start_step("开始快速开场测试")
#                 # gameElement.click()
#                 self.game_page.wait_element("快速开始").click()
#                 self.game_page.screenshot(screenName)
                while True:
                    if(self.hall_page.element_is_exist("客服")):
                        break
                    self.driver.back()
                    

                    
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("遍历首页游戏列表")
        traverseGameList(self.game_page.get_game_list())
        try:
            self.hall_page.wait_element("右三角").click()
            traverseGameList(self.game_page.get_game_list(), True)
        except:
            print "没有右三角按钮"
            
    def post_test(self):
        self.common.recover_user(mid)
        self.common.closedriver()

__qtaf_seq_tests__ = [C27385_quicklyStartGame_coinsEnough]
if __name__ =="__main__":
#     levelConfig = PHPInterface.get_levelconfig(2000, 0, 0, 12)
#     print levelConfig
    debug_run_all()
    # PHPInterface.set_robot_flag(203, 0, 0, 12, 1)
#     print PHPInterface.get_mid(2430877, 54)
#     print PHPInterface.get_user_info(100120886)2460587
#     Common().set_coin("2460259", "30000")
#     Common().set_safeBoxMoney(2460587, 20000, 0)
#     print PHPInterface.deposit_safebox(100120886, 10000, "0")