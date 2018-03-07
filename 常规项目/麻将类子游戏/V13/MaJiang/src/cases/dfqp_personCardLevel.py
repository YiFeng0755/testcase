#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
个人资料卡弹框层级
'''

from common.common import Common
from runcenter.testcase import TestCase, debug_run_all
from runcenter.enums import EnumPriority, EnumStatus
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page


class C27417_personCardLevel_openOtherView(TestCase):
    '''
    个人资料卡打开情况下，打开其他界面查看层级
    '''
    owner = "GuixiangGui"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    
    def pre_test(self):
        self.game_page = Game_Page()
        self.hall_page = Hall_Page()
        self.yuepai_page =Yuepai_Page()
        self.common = Common()
        self.start_step("初始化driver")
        self.driver = self.common.setupdriver()
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.driver)
        
    def run_test(self):
        
        def test_game(gameId):
            self.start_step("%s 子游戏初级场" %gameId)
            self.game_page.wait_element("初级场").click()
            elist = ["聊天", "聊天1", "对局流水", "番数说明", "牌型", "规则", "菜单键"]
            for eName in elist:
                # if not self.game_page.element_is_exist("物品箱", 3):
                if self.game_page.element_is_exist(eName, 2):
                    try:
                        self.game_page.get_elements("头像frame")[0].click()
                        self.game_page.screenshot(gameId + "_" + eName + "_headview.png")
                        self.game_page.wait_element(eName).click()
                        self.game_page.screenshot(gameId + "_" + eName + ".png")
                    except:
                        self.game_page.screenshot(gameId+"_notfoundhead"+".png")
                        # return
            self.yuepai_page.is_exist_yuepairoom()
                # if self.game_page.element_is_exist(eName, 2):
                #     self.game_page.wait_element(eName).click()
                #     self.game_page.screenshot(gameId+"_"+eName+".png")
        
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
                # if self.game_page.element_not_exist("广播"):
                #     self.game_page.game_play_way()
                test_game(gameElement.get_attribute("name"))
                 
                while True:
                    if self.hall_page.element_is_exist("客服", 3):
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
        self.common.closedriver()

# __qtaf_seq_tests__ = [C27343_Gamelist_Sendbroadcast]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
