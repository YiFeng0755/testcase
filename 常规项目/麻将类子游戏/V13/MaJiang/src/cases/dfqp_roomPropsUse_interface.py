#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
房间内道具使用
'''

import re
from common.common import Common
import common.Interface as PHPInterface
from runcenter.testcase import TestCase, debug_run_all
from runcenter.enums import EnumPriority, EnumStatus
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page

toolsID = [203, 202, 201, 200] #炸弹，拖鞋，鸡蛋，鲜花

class base(TestCase):
    def pre_test(self, propsCount):
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.common = Common()
        mid = self.common.get_config_value("casecfg", "mid")
#         PHPInterface
        self.start_step("初始化driver")
        self.driver = self.common.setupdriver()
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.driver)
        
    def test(self, useCount=1):
        def test_game(gameId):
            
            headsEle = self.game_page.get_elements("头像frame")
            propsEle = self.game_page.get_elements("道具")
            headsEle[0].click()
            self.game_page.screenshot(gameId+"_propsDisplay"+".png")
            propsEle[0].click()
            self.game_page.screenshot(gameId+"_self_interactive"+".png")
            if len(headsEle)>1:
                count = self.useCount
                while count > 0:
                    headsEle[1].click()
                    propsEle[0].click()
                    count = count-1
                
                self.game_page.screenshot(gameId+"_playerB_interactive"+".png")
                propsEle[0].click()
                self.game_page.screenshot(gameId+"_afterUse_display"+".png")
            while True:
                if self.hall_page.element_is_exist("预发布"):
                    break
                self.driver.back()
        
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
                gameId = gameElement.get_attribute("name")
                PHPInterface.set_robot_flag(re.search("\d+", gameId), 0, 0, 12, 1)
                if self.game_page.element_not_exist("广播"):
                    self.game_page.click_game_play()
                self.game_page.get_elements("房间场次")[0].click()
                test_game(gameId)
                PHPInterface.set_robot_flag(re.search("\d+", gameId), 0, 0, 12, 0)
                while True:
                    if self.hall_page.element_is_exist("客服", 3):
                        break
                    self.driver.back()
        self.useCount = useCount
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

class c27438_roomPropsUse_noPropsDisplay(base):
    '''
    没有道具时显示
    '''
    owner = "GuixiangGui"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    
    def pre_test(self):
        base.pre_test(self,0)
        
    def run_test(self):
        base.test(self)
        
    def post_test(self):
        base.post_test(self)
    
    
class c27439_roomPropsUse_propsLess100Display(base):
    '''
    道具小于等于99时显示
    '''
    owner = "GuixiangGui"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    
    def pre_test(self):
#         PHPInterface.
        base.pre_test(self,99)
        
    def run_test(self):
        base.test(self)
        
    def post_test(self):
        base.post_test(self)
        
        
class c27440_roomPropsUse_propsMore99Display(base):
    '''
    道具大于99时显示
    '''
    owner = "GuixiangGui"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    
    def pre_test(self):
#         PHPInterface.
        base.pre_test(self,102)
        
    def run_test(self):
        base.test(self)
        
    def post_test(self):
        base.post_test(self)
        
class c27441_roomPropsUse_propsOnlyOneDisplay(base):
    '''
    道具只有1个时显示
    '''
    owner = "GuixiangGui"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    
    def pre_test(self):
#         PHPInterface.
        base.pre_test(self,1)
        
    def run_test(self):
        base.test(self)
        
    def post_test(self):
        base.post_test(self)
        
class c27446_roomPropsUse_useTenPropsDisplay(base):
    '''
    连续使用10个道具显示
    '''
    owner = "GuixiangGui"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    
    def pre_test(self):
#         PHPInterface.
        base.pre_test(self,11)
        
    def run_test(self):
        base.test(self,10)
        
    def post_test(self):
        base.post_test(self)

__qtaf_seq_tests__ = [c27438_roomPropsUse_noPropsDisplay]
if __name__ == "__main__":
     debug_run_all()