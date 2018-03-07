#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
升场
'''

import time
import re
from common.common import Common
from runcenter.testcase import TestCase, debug_run_all
from runcenter.enums import EnumPriority, EnumStatus
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page
import common.Interface as PHPInterface


class c27667_roomUpgrade_safeBoxWithdrawals(TestCase):
    '''
    保险箱取款升场
    '''
    owner = "GuixiangGui"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.game_page = Game_Page()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.common = Common()
        self.start_step("初始化driver")
        self.driver = self.common.setupdriver()
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.driver)
        self.mid = self.common.get_config_value("casecfg", "mid")

    def run_test(self):
        def test_game(btnElement, screenName, gameElement, needClickRight=False):
            gameId = gameElement.get_attribute("name")
            self.common.set_coin(self.mid, self.tiro_high_limit-200)
            self.common.set_safeBoxMoney(self.mid, 20000, 0)
            self.common.switchserver()
            self.common.closeactivity(self.driver)
            
            if needClickRight and self.hall_page.element_is_exist("右三角"):
                self.hall_page.wait_element("右三角").click()
            gameElement.click()
            if not self.game_page.game_is_download():
                self.assert_equal(gameId+"游戏下载失败", True, False)
                raise
            
            if not self.game_page.element_is_exist("广播"):
                self.game_page.click_game_play()
            self.game_page.wait_element("初级场").click()
            
            self.start_step("开始%s升场测试" %gameId)
            self.game_page.wait_element("菜单键").click()
            
            try:
                self.game_page.wait_element("取款").click()
                self.game_page.wait_element("减号").click()
                self.game_page.wait_element("确定").click()
                self.game_page.wait_element(btnElement).click()
                self.start_step("开始截图")
                self.game_page.screenshot(screenName)
            except:
                self.assert_equal(gameId+"取款失败", True, False)
                raise
            
            self.yuepai_page.is_exist_yuepairoom()

        def traverseGameList(gameList, needClickRight=False):
            for gameElement in gameList:
                gameId = gameElement.get_attribute("name")
                levelConfig = PHPInterface.get_levelconfig(re.search('\d+', gameId).group(), 0, 0, 12)
                self.tiro_high_limit = int(levelConfig.get("values").get("HIGH_LIMIT"))
                if self.tiro_high_limit<0:
                    self.log_info("没有升场情况 :"+gameId)
                    continue
                
                try:
                    test_game("换桌", gameId + "_change.png", gameElement, needClickRight)
                    test_game("准备", gameId + "_ready.png", gameElement, needClickRight)
                except:
                    self.assert_equal("保险箱取款升场失败。" + gameId, True, False) 
                    self.game_page.screenshot(gameId + "_failed.png")
                try:
                    self.start_step("退出房间")
                    self.yuepai_page.is_exist_yuepairoom()
                    self.game_page.wait_element("返回1").click()
                except:
                    self.log_info("退出房间失败")

        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.mid = self.common.get_config_value("casecfg", "mid")
        gameList = self.game_page.get_game_list()
        traverseGameList(gameList)

        try:
            self.hall_page.wait_element("右三角").click()
            gameList = self.game_page.get_game_list()
            traverseGameList(gameList, True)
        except:
            self.log_info("没有右三角按钮")
    def post_test(self):
        self.common.closedriver()
        self.common.recover_user(self.mid)


class c27669_roomUpgrade_mallBuyCoins(TestCase):
    '''
    商城购买升场
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
        time.sleep(2)
        self.common.closeactivity(self.driver)

    def run_test(self):
        def test_game(btnElement, screenName, gameElement, needClickRight=False):
            gameId = gameElement.get_attribute("name")
            print "tiro high limit:", self.tiro_high_limit-200
            self.common.set_coin(self.mid, self.tiro_high_limit-200)
            self.common.set_crystal(self.mid, 1000)
            self.common.switchserver()
            time.sleep(2)
            self.common.closeactivity(self.driver)
            
            if needClickRight and self.hall_page.element_is_exist("右三角"):
                self.hall_page.wait_element("右三角").click()
            gameElement.click()
            if not self.game_page.game_is_download():
                self.assert_equal(gameId+"游戏下载失败", True, False)
                raise
            
            if not self.game_page.element_is_exist("广播"):
                self.game_page.click_game_play()
            self.game_page.wait_element("初级场").click()
            # endTime = time.time() + 180
            # while time.time() < endTime:
            #     if self.game_page.element_is_exist("换场", 2):
            #         break
            #     if self.game_page.element_is_exist("叫地主", 2):
            #         try:
            #             self.game_page.wait_element("叫地主", 2).click()
            #         except:
            #             print "没有叫地主按钮"
            # else:
            #     return
            self.game_page.wait_element("菜单键").click()
            self.game_page.wait_element("商城").click()
            try:
                self.game_page.wait_element("金条购买数量").click()
                self.game_page.wait_element("金条购买方式").click()
#                 crystalBtns = self.game_page.get_elements("金条购买数量")
#                 if len(crystalBtns)==0:
#                     self.assert_equal(gameId+"选择购买数量界面获取金条购买失败", True, False)
#                     raise
#                 for crystalBtn in crystalBtns:
#                     print crystalBtn.get_attribute("text")
#                 crystalBtns[0].click()
#                 buyBtns = self.game_page.get_elements("金条购买方式")
#                 if len(buyBtns)==0:
#                     self.assert_equal(gameId+"购买方式界面获取购买按钮失败", True, False)
#                     raise
#                 for buyBtn in buyBtns:
#                     text = buyBtn.get_attribute("text")
#                     if "金条" in text:
#                         buyBtn.click()
#                         break
                self.hall_page.wait_element("关闭对话框").click()
            except:
                self.assert_equal(gameId+"游戏购买失败", True, False)
                if self.hall_page.element_is_exist("关闭对话框"):
                    self.hall_page.wait_element("关闭对话框").click()
                raise
            self.game_page.wait_element(btnElement).click()
            self.game_page.screenshot(screenName)
            
            self.yuepai_page.is_exist_yuepairoom()

        def traverseGameList(gameList, needClickRight=False):
            for gameElement in gameList:
                gameId = gameElement.get_attribute("name")
                levelConfig = PHPInterface.get_levelconfig(re.search('\d+', gameId).group(), 0, 0, 12)
                self.tiro_high_limit = int(levelConfig.get("values").get("HIGH_LIMIT"))
                print gameId, self.tiro_high_limit
                if self.tiro_high_limit<0:
                    self.log_info("没有升场情况 :"+gameId)
                    continue
                
                try:
                    test_game("换桌", gameId + "_change.png", gameElement, needClickRight)
                    test_game("准备", gameId + "_ready.png", gameElement, needClickRight)
                except:
                    self.assert_equal("商城购买升场失败。" + gameId, True, False)
                    self.game_page.screenshot(gameId + "_failed.png")
                try:
                    self.start_step("退出房间")
                    self.yuepai_page.is_exist_yuepairoom()
                    if self.game_page.element_is_exist("返回1"):
                        self.game_page.wait_element("返回1").click()
                except:
                    self.log_info("退出房间失败")
                    raise

        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.mid = self.common.get_config_value("casecfg", "mid")
        print self.mid
        
#         self.hall_page.wait_element("预发布").click()
#         self.driver.back()
        traverseGameList(self.game_page.get_game_list())
        try:
            self.hall_page.wait_element("右三角").click()
            traverseGameList(self.game_page.get_game_list(), True)
        except:
            self.log_info("没有右三角按钮") 

    def post_test(self):
        self.common.closedriver()
        self.common.recover_user(self.mid)


# __qtaf_seq_tests__ = [c27669_roomUpgrade_mallBuyCoins]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
#     print PHPInterface.get_levelconfig(203, 0, 0, 12)
#     PHPInterface.add_crystal(2460259, "2000")