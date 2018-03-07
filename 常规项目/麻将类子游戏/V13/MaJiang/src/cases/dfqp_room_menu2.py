#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
子游戏房间菜单
'''
import time
from runcenter.enums import EnumPriority, EnumStatus
from runcenter.testcase import debug_run_all, TestCase
from uilib.hall_page import Hall_Page
from uilib.game_page import Game_Page
from uilib.safebox_page import Safebox_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common
import common.Interface as PHPInterface
import json

class BaseCase(TestCase):
    gameIDList = ['game203', 'game24', 'game1502', 'game23', 'game2603']
    gameOverFlag =  [ 'game203结算框标志', 'game7结算框标志', 'game20结算框标志', 'game2002结算框标志', 'game2601结算框标志', 'game2603结算框标志']
    child_game_timeout = 5

    def pre_test(self, needSetSafebox=False):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.safebox_page = Safebox_Page()
        self.start_step("获取用户mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("设置银币数为20000")
        self.common.set_coin(mid, '20000')
        if needSetSafebox == True:
            self.start_step("设置保险箱银币数为100000")
            self.common.set_safeBoxMoney(mid, 100000, 0)
            # money_dict = PHPInterface.get_safebox(mid)
            # print money_dict["safebox"]

        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def enterGame(self, gameElment, needClickRight=False):
        gameId = gameElment.get_attribute("name")
        self.start_step("点击游戏：" + gameId)
        if needClickRight:
            self.click_rightArrow()
        gameElment.click()
        if self.game_page.game_is_download():
            #主要用来兼容新版本斗地主，没有广播说明有多种玩法，新版本存在不同的游戏级别（银币场、金条场、话费场）
            if not self.game_page.element_is_exist("广播") or self.game_page.element_is_exist("游戏级别", 1):
                #切到第一种玩法
                self.game_page.click_game_play()
            self.start_step("进入游戏房间：" + gameId)
            #旧版本斗地主
            if self.game_page.element_is_exist("初级场"):
                self.game_page.wait_element("初级场").click()
                self.game_page.screenshot("%s进入房间.png" % gameId)
            # 新版本斗地主
            elif self.game_page.element_is_exist("第一个房间"):
                self.game_page.wait_element("第一个房间").click()
                self.game_page.screenshot("%s进入房间.png" % gameId)
            else:
                self.assert_equal(gameId + "进入游戏房间失败", False, True)
                self.gameToHall()
                return False
            return True
        else:
            self.assert_equal(gameId + "进入游戏失败", False, True)
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

    def clickRoomMenu(self, gameid_name):
        self.game_page.wait_element("房间内菜单").click()
        self.game_page.screenshot("%s房间内菜单按钮.png" % gameid_name)
        #点击电池，为了关闭打开的菜单
        if self.game_page.element_is_exist("电池标志"):
            self.game_page.wait_element("电池标志").click()

    def wait_for_gameover(self, gameid_name):
        if gameid_name == "game203":
            while not self.game_page.element_is_exist("game203详情按钮"):
                time.sleep(1)
            if self.game_page.element_is_exist("game203详情按钮"):
                return True
        elif gameid_name == "game23" or gameid_name == "game3":
            while not self.game_page.element_is_exist("换桌") and not self.game_page.element_is_exist("准备"):
                time.sleep(1)
            if self.game_page.element_is_exist("换桌") and self.game_page.element_is_exist("准备"):
                return True
        else:
            while not self.game_page.element_is_exist("关闭结算界面") and not self.game_page.element_is_exist("关闭结算界面1"):
                time.sleep(1)
            if self.game_page.element_is_exist("关闭结算界面"):
                self.game_page.wait_element("关闭结算界面").click()
                return True
            if self.game_page.element_is_exist("关闭结算界面1"):
                self.game_page.wait_element("关闭结算界面1").click()
                return True

    def gameToHall(self):
        self.yuepai_page.is_exist_yuepairoom()
        if self.game_page.element_is_exist("返回1"):
            self.game_page.wait_element("返回1").click()
        elif self.game_page.element_is_exist("返回大厅"):
            self.game_page.wait_element("返回大厅").click()
        time.sleep(2)

    def post_test(self):
        self.common.recover_user(mid)
        self.common.closedriver()

class C27548_RoomMenu_Playing(BaseCase):
    '''
   出牌阶段，查看房间内菜单按钮显示
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self, needSetSafebox=False):
        BaseCase.pre_test(self, needSetSafebox)

    # 遍历大厅每一页的子游戏列表
    def traversal_gameList(self, game_list, is_next=False):
        for game in game_list:
            gameid_name = game.get_attribute("name")
            gameid = int(gameid_name[4:len(gameid_name)])
            self.start_step("进入大厅游戏:%s" % gameid_name)
            self.start_step("机器人开关打开")
            PHPInterface.set_robot_flag(gameid, 0, 0, 12, 1)
            if BaseCase.enterGame(self, game, is_next):
                if not BaseCase.gameIsAutoReady(self, game):
                    try:
                        self.start_step("点击房间内准备按钮")
                        self.game_page.wait_element("准备").click()
                    except:
                        self.assert_equal(gameid_name + "未出现准备按钮", False, True)
                        BaseCase.gameToHall(self)
                        continue

                #等待几秒 确保牌局开始
                time.sleep(5)
                self.start_step("点击房间内菜单")
                self.clickRoomMenu(gameid_name)
                # BaseCase.clickRoomMenu(self, gameid_name)
                self.start_step("等待游戏结束，从游戏房间返回到大厅")
                # notoverFlag = True
                # while notoverFlag:
                #     if self.game_page.element_is_exist("换桌") or self.game_page.element_is_exist("牌局结束换桌"):
                #         notoverFlag = False
                #         self.luadriver.back()
                #     elif not self.game_page.element_is_exist("换桌") and not self.game_page.element_is_exist("牌局结束换桌"):
                #         time.sleep(1)
                if BaseCase.wait_for_gameover(self, gameid_name):
                    BaseCase.gameToHall(self)
                self.start_step("关闭机器人")
                PHPInterface.set_robot_flag(gameid, 0, 0, 12, 0)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("遍历大厅子游戏")
        self.test(self.traversal_gameList)

    def post_test(self):
        BaseCase.post_test(self)

class C27549_Settlement__MenuDisplay(BaseCase):
    '''
    结算阶段，查看菜单栏显示
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self, needSetSafebox=False):
        BaseCase.pre_test(self, needSetSafebox)

    # 遍历大厅每一页的子游戏列表
    def traversal_gameList(self, game_list, is_next=False):
       for game in game_list:
           gameid_name = game.get_attribute("name")
           gameid = int(gameid_name[4:len(gameid_name)])
           self.start_step("机器人开关打开")
           print PHPInterface.set_robot_flag(gameid, 0, 0, 12, 1)
           self.start_step("进入大厅游戏%s" % gameid_name)
           if BaseCase.enterGame(self, game, is_next):
               if not BaseCase.gameIsAutoReady(self, game):
                   try:
                       self.start_step("点击房间内准备按钮")
                       self.game_page.wait_element("准备").click()
                   except:
                       self.assert_equal(gameid_name + "未出现准备按钮", False, True)
                       BaseCase.gameToHall(self)
                       continue

               self.start_step("等待游戏结束")
               if BaseCase.wait_for_gameover(self, gameid_name):
                  self.clickRoomMenu(gameid_name)
               self.start_step("从%s游戏房间返回到大厅" % gameid_name)
               BaseCase.gameToHall(self)
               self.start_step("关闭机器人")
               print PHPInterface.set_robot_flag(gameid, 0, 0, 12, 0)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("遍历大厅游戏")
        self.test(self.traversal_gameList)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        BaseCase.post_test(self)

class C27552_RoomMenu_Aready(BaseCase):
    '''
    已准备状态，取款按钮置灰，无法点击
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self, needSetSafebox=False):
        BaseCase.pre_test(self, needSetSafebox)

    # 遍历大厅每一页的子游戏列表
    def traversal_gameList(self, game_list, is_next=False):
        for game in game_list:
            gameid_name = game.get_attribute("name")
            gameid = int(gameid_name[4:len(gameid_name)])
            self.start_step("关机器人")
            print PHPInterface.set_robot_flag(gameid, 0, 0, 12, 0)
            self.start_step("进入大厅游戏: %s" % gameid_name)
            if BaseCase.enterGame(self, game, is_next):
                if not BaseCase.gameIsAutoReady(self, game):
                    try:
                        self.start_step("点击房间内准备按钮")
                        self.game_page.wait_element("准备").click()
                    except:
                        self.assert_equal(gameid_name + "未出现准备按钮", False, True)
                        BaseCase.gameToHall(self)
                        continue

                self.start_step("点击菜单查看取款按钮状态")
                self.game_page.wait_element("房间内菜单").click()
                self.game_page.screenshot("%s已准备看取款按钮状态.png" % gameid_name)
                self.start_step("点击取款")
                self.game_page.wait_element("取款").click()
                if self.game_page.element_is_exist("关闭银币保险箱") == False:
                    print "取款按钮不可点击"
                #点电池标志只是为了关闭打开的菜单栏
                self.game_page.wait_element("电池标志").click()

                self.start_step("从%s游戏房间返回到大厅" % gameid_name)
                #牌局未开始
                if self.game_page.element_is_exist("换桌"):
                    BaseCase.gameToHall(self)
                # 牌局已开始
                elif BaseCase.wait_for_gameover(self, gameid_name):
                    BaseCase.gameToHall(self)
    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("遍历大厅游戏")
        self.test(self.traversal_gameList)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        BaseCase.post_test(self)

class C27553_RoomMenu_NoAready(BaseCase):
    '''
    未准备状态，取款按钮高亮，可以点击
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self, needSetSafebox=False):
        BaseCase.pre_test(self, needSetSafebox)

    # 遍历大厅每一页的子游戏列表
    def traversal_gameList(self, game_list, is_next=False):
        for game in game_list:
            gameid_name = game.get_attribute("name")
            gameid = int(gameid_name[4:len(gameid_name)])
            self.start_step("关机器人")
            print PHPInterface.set_robot_flag(gameid, 0, 0, 12, 0)
            self.start_step("进入大厅游戏: %s" % gameid_name)
            if BaseCase.enterGame(self, game, is_next):
                if not BaseCase.gameIsAutoReady(self, game):
                    if self.game_page.element_is_exist("准备"):
                        self.start_step("点击菜单查看取款按钮状态")
                        self.game_page.wait_element("房间内菜单").click()
                        self.game_page.screenshot("%s未准备看取款按钮状态.png" % gameid_name)
                        self.start_step("点击取款")
                        self.game_page.wait_element("取款").click()
                        if self.game_page.element_is_exist("关闭银币保险箱") == False:
                            self.assert_equal(gameid_name + "取款按钮点击失败", False, True)
                        else:
                            self.game_page.wait_element("关闭银币保险箱").click()
                    else:
                        self.assert_equal(gameid_name + "未出现准备按钮", False, True)

                self.start_step("从%s游戏房间返回到大厅" % gameid_name)
                # 牌局未开始
                if self.game_page.element_is_exist("换桌"):
                    BaseCase.gameToHall(self)
                # 牌局已开始
                elif BaseCase.wait_for_gameover(self, gameid_name):
                    BaseCase.gameToHall(self)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("遍历大厅子游戏")
        self.test(self.traversal_gameList)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        BaseCase.post_test(self)

class C27554_RoomMenu_GetMoneyDisplay(BaseCase):
    '''
    未准备状态，牌桌保险箱取款界面显示，点击-号可以减少保险箱银币数
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self, needSetSafebox=True):
        BaseCase.pre_test(self, needSetSafebox)

    # 遍历大厅每一页的子游戏列表
    def traversal_gameList(self, game_list, is_next=False):
        for game in game_list:
            gameid_name = game.get_attribute("name")
            gameid = int(gameid_name[4:len(gameid_name)])
            self.start_step("关闭机器人")
            PHPInterface.set_robot_flag(gameid, 0, 0, 12, 0)
            if BaseCase.enterGame(self, game, is_next):
                if not BaseCase.gameIsAutoReady(self, game):
                    if self.game_page.element_is_exist("准备"):
                        self.start_step("点击房间内菜单按钮")
                        self.game_page.wait_element("房间内菜单").click()
                        self.game_page.screenshot("%s房间内菜单.png" % gameid_name)
                        self.game_page.wait_element("取款").click()
                        self.game_page.screenshot("%s保险箱.png" % gameid_name)
                        self.start_step("减少牌桌银币保险箱银币数：")
                        self.safebox_page.wait_element("减少金条/银条数目").click()
                        self.safebox_page.wait_element("确定---保险箱").click()
                    else:
                        self.assert_equal(gameid_name + "未出现准备按钮", False, True)

                self.start_step("退出子游戏房间%s到大厅" % gameid_name)
                BaseCase.gameToHall(self)
                #恢复玩家携带银币数
                self.common.set_coin(mid, "10000")
                self.common.switchserver()
                self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("遍历大厅子游戏")
        self.test(self.traversal_gameList)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        BaseCase.post_test(self)

class C27555_RoomMenu_GetMoneyDisplay(BaseCase):
    '''
    未准备情况下，牌桌保险箱拖动滑动条取款
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self, needSetSafebox=True):
        BaseCase.pre_test(self, needSetSafebox)

    # 遍历大厅每一页的子游戏列表
    def traversal_gameList(self, game_list, is_next=False):
        for game in game_list:
            gameid_name = game.get_attribute("name")
            gameid = int(gameid_name[4:len(gameid_name)])
            self.start_step("关闭机器人")
            PHPInterface.set_robot_flag(gameid, 0, 0, 12, 0)
            if BaseCase.enterGame(self, game, is_next):
                if not BaseCase.gameIsAutoReady(self, game):
                    if self.game_page.element_is_exist("准备", 60):
                        self.start_step("点击房间内菜单按钮")
                        self.game_page.wait_element("房间内菜单").click()
                        self.game_page.screenshot("%s房间内菜单.png" % gameid_name)
                        self.game_page.wait_element("取款").click()
                        self.game_page.screenshot("%s保险箱.png" % gameid_name)
                        self.start_step("拖动滚动条")
                        ele = self.safebox_page.wait_element("滑动杆")
                        # print ele.location['x'], ele.location['y'], ele.size['width'], ele.size[ 'height']
                        startX = ele.location['x'] + ele.size['width']
                        y = ele.location['y'] + ele.size['height'] / 2
                        #取1/10存款
                        endX = ele.location['x']+ ele.size['width'] * 9 / 10
                        self.luadriver.swipe(startX, y, endX, y)
                        self.safebox_page.wait_element("确定---保险箱").click()
                    else:
                        if not BaseCase.gameIsAutoReady(self, game):
                            self.assert_equal(gameid_name + "未出现准备按钮", False, True)

                self.start_step("退出子游戏房间%s到大厅" % gameid_name)
                BaseCase.gameToHall(self)
                # 恢复用户携带银币数
                self.common.set_coin(mid, "10000")
                self.common.switchserver()
                self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("遍历大厅子游戏")
        self.test(self.traversal_gameList)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        BaseCase.post_test(self)

class C27556_getMoney_updateSuccess(BaseCase):
    '''
    未准备，取款成功后银币及时更新
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self, needSetSafebox=True):
        BaseCase.pre_test(self, needSetSafebox)

    # 遍历大厅每一页的子游戏列表
    def traversal_gameList(self, game_list, is_next=False):
        for game in game_list:
            gameid_name = game.get_attribute("name")
            gameid = int(gameid_name[4:len(gameid_name)])
            self.start_step("关闭机器人")
            PHPInterface.set_robot_flag(gameid, 0, 0, 12, 0)
            if BaseCase.enterGame(self, game, is_next):
                if not BaseCase.gameIsAutoReady(self, game):
                    if self.game_page.element_is_exist("准备"):
                        self.start_step("点击房间内菜单按钮")
                        self.game_page.wait_element("房间内菜单").click()
                        self.game_page.screenshot("%s房间内菜单.png" % gameid_name)
                        self.game_page.wait_element("取款").click()
                        self.game_page.screenshot("%s保险箱.png" % gameid_name)
                        self.start_step("拖动滚动条")
                        ele = self.safebox_page.wait_element("滑动杆")
                        print ele.location['x'], ele.location['y'], ele.size['width'], ele.size[ 'height']
                        startX = ele.location['x'] + ele.size['width']
                        y = ele.location['y'] + ele.size['height'] / 2
                        # 滑动杆向左滑动1/10
                        endX = ele.location['x'] + ele.size['width'] * 9 / 10
                        self.luadriver.swipe(startX, y, endX, y, 2)
                        self.safebox_page.wait_element("确定---保险箱").click()

                        # 再次点击取款查看房间内银币保险箱
                        if self.game_page.element_is_exist("准备"):
                            self.start_step("再次点击菜单栏取款按钮")
                            self.game_page.wait_element("房间内菜单").click()
                            self.game_page.wait_element("取款").click()
                            self.game_page.screenshot("%s取款后保险箱.png" % gameid_name)
                            # 验证—号可点击
                            self.safebox_page.wait_element("减少金条/银条数目").click()
                            self.safebox_page.wait_element("确定---保险箱").click()
                    else:
                        self.assert_equal(gameid_name + "未出现准备按钮", False, True)

                self.start_step("退出子游戏房间%s到大厅" % gameid_name)
                BaseCase.gameToHall(self)
                # 恢复玩家携带银币数
                self.common.set_coin(mid, "10000")
                self.common.switchserver()
                self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("遍历大厅子游戏")
        self.test(self.traversal_gameList)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        BaseCase.post_test(self)

class C27557_getMoney_goUpgrade(BaseCase):
    '''
    未准备时在房间保险箱取款成功，点准备后升场
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self, needSetSafebox=True):
        BaseCase.pre_test(self, needSetSafebox)

    # 遍历大厅每一页的子游戏列表
    def traversal_gameList(self, game_list, is_next=False):
        for game in game_list:
            gameid_name= game.get_attribute("name")
            gameid = int(gameid_name[4:len(gameid_name)])
            self.start_step("关闭机器人")
            PHPInterface.set_robot_flag(gameid, 0, 0, 12, 0)
            if BaseCase.enterGame(self, game, is_next):
                if not BaseCase.gameIsAutoReady(self, game):
                    if self.game_page.element_is_exist("准备"):
                        self.start_step("点击房间内菜单按钮")
                        self.game_page.wait_element("房间内菜单").click()
                        self.game_page.wait_element("取款").click()
                        # self.game_page.screenshot("%s保险箱.png" % gameid_name)

                        # self.start_step("拖动滑动杆")
                        ele = self.safebox_page.wait_element("滑动杆")
                        startX = ele.location['x'] + ele.size['width']
                        y = ele.location['y'] + ele.size['height'] / 2
                        # 滑动杆向左滑动1/5
                        endX = ele.location['x'] + ele.size['width'] * 4 / 5
                        # endX = ele.location['x']
                        self.luadriver.swipe(startX, y, endX, y)
                        self.safebox_page.wait_element("确定---保险箱").click()
                        # self.start_step("取款成功后点准备会升场")
                        self.game_page.wait_element("准备").click()
                        self.game_page.screenshot("%s升场.png" % gameid_name)
                    else:
                        self.assert_equal(gameid_name + "未出现准备按钮", False, True)

                self.start_step("退出子游戏房间%s到大厅" % gameid_name)
                BaseCase.gameToHall(self)
                # 恢复玩家携带银币数
                self.common.set_coin(mid, "10000")
                self.common.switchserver()
                self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("遍历大厅子游戏")
        self.test(self.traversal_gameList)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.set_safeBoxMoney(mid, 0, 0)
        self.common.closedriver()

class C27558_PlayOneRound_GetMoney(BaseCase):
    '''
    玩牌一局后取款
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self, needSetSafebox=True):
        BaseCase.pre_test(self, needSetSafebox)

    # 遍历大厅每一页的子游戏列表
    def traversal_gameList(self, game_list, is_next=False):
        for game in game_list:
            gameid_name = game.get_attribute("name")
            gameid = int(gameid_name[4:len(gameid_name)])
            self.start_step("机器人开关打开")
            print PHPInterface.set_robot_flag(gameid, 0, 0, 12, 1)
            if BaseCase.enterGame(self, game, is_next):
                if not self.game_page.element_is_exist("换桌"):
                    self.assert_equal(gameid_name + " 游戏没有找到换桌按钮", True, False)

                if not BaseCase.gameIsAutoReady(self, game) :
                    if self.game_page.element_is_exist("准备"):
                        self.start_step("点击准备")
                        self.game_page.wait_element("准备").click()
                    else:
                        self.assert_equal(gameid_name + " 游戏没有找到准备按钮", True, False)
                        BaseCase.gameToHall(self)
                        continue

                # 下局取款
                if BaseCase.wait_for_gameover(self, gameid_name):
                    # self.start_step("一局后取款")
                    self.game_page.wait_element("房间内菜单").click()
                    self.game_page.wait_element("取款").click()
                    self.safebox_page.wait_element("减少金条/银条数目").click()
                    self.safebox_page.wait_element("确定---保险箱").click()
                    self.game_page.screenshot("%s一局后取款.png"% gameid_name)
                self.start_step("关闭机器人")
                print PHPInterface.set_robot_flag(gameid, 0, 0, 12, 0)
                self.start_step("退出子游戏房间%s到大厅" % gameid_name)
                BaseCase.gameToHall(self)
                # 恢复银币数
                self.common.set_coin(mid, "10000")
                self.common.switchserver()
                self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("遍历大厅子游戏")
        self.test(self.traversal_gameList)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        BaseCase.post_test(self)

class C27560_NoReady_NoStart_Exit(BaseCase):
    '''
    未准备，且牌局未开始情况下，点击退出
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self, needSetSafebox=False):
        BaseCase.pre_test(self, needSetSafebox)

    # 遍历大厅每一页的子游戏列表
    def traversal_gameList(self, game_list, is_next=False):
        for game in game_list:
            gameid_name = game.get_attribute("name")
            gameid = int(gameid_name[4:len(gameid_name)])
            # 关机器人
            print PHPInterface.set_robot_flag(gameid, 0, 0, 12, 0)
            self.start_step("点击大厅游戏位:%s" % gameid_name)
            if BaseCase.enterGame(self, game, is_next):
                if not BaseCase.gameIsAutoReady(self, game):
                    if self.game_page.element_is_exist("准备"):
                        pass
                    else:
                        self.assert_equal(gameid_name + "未出现准备按钮", False, True)
                        BaseCase.gameToHall(self)
                        continue

                # 能获取到换桌，说明牌局未开始
                if self.game_page.element_is_exist("换桌"):
                    self.start_step("退出游戏房间")
                    BaseCase.gameToHall(self)
                else:
                    self.assert_equal(gameid_name + "未出现换桌按钮", False, True)
                    BaseCase.gameToHall(self)
                    continue

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("遍历大厅子游戏")
        self.test(self.traversal_gameList)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        BaseCase.post_test(self)

class C27560_Already_NoStart_Exit(BaseCase):
    '''
    已准备，且牌局未开始情况下，点击退出
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self, needSetSafebox=False):
        BaseCase.pre_test(self, needSetSafebox)

    # 遍历大厅每一页的子游戏列表
    def traversal_gameList(self,game_list, is_next=False):
        for game in game_list:
            gameid_name = game.get_attribute("name")
            gameid = int(gameid_name[4:len(gameid_name)])
            # 关机器人
            print PHPInterface.set_robot_flag(gameid, 0, 0, 12, 0)
            self.start_step("点击大厅游戏位:%s" % gameid_name)
            if BaseCase.enterGame(self, game, is_next):
                if not BaseCase.gameIsAutoReady(self, game):
                    try:
                        self.start_step("点击准备")
                        self.game_page.wait_element("准备").click()
                    except:
                        self.assert_equal(gameid_name + "未出现准备按钮", False, True)
                        BaseCase.gameToHall(self)
                        continue

                # 能获取到换桌，说明牌局未开始
                if self.game_page.element_is_exist("换桌"):
                    self.start_step("退出游戏房间")
                    BaseCase.gameToHall(self)
                else:
                    self.assert_equal(gameid_name + "未出现换桌按钮", False, True)
                    BaseCase.gameToHall(self)
                    continue

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("遍历大厅子游戏")
        self.test(self.traversal_gameList)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        BaseCase.post_test(self)

__qtaf_seq_tests__ = [C27548_RoomMenu_Playing]
if __name__ == '__main__':
    C27548_RoomMenu_Playing().debug_run()
    # C27549_Settlement__MenuDisplay().debug_run()
    # C27552_RoomMenu_Aready().debug_run()
    # C27553_RoomMenu_NoAready().debug_run()
    # C27554_RoomMenu_GetMoneyDisplay().debug_run()
    # C27555_RoomMenu_GetMoneyDisplay().debug_run()
    # C27556_getMoney_updateSuccess().debug_run()
    # C27557_getMoney_goUpgrade().debug_run()
    # C27558_PlayOneRound_GetMoney().debug_run()
    # C27560_NoReady_NoStart_Exit().debug_run()
    # C27560_Already_NoStart_Exit().debug_run()
    # debug_run_all()
