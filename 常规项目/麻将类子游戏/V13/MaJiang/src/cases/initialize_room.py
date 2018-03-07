#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
游戏房间初始化，目前只初始化了斗地主
'''
import re
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase

from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common


class GameRoom_Initialize(TestCase):
    '''
    游戏房间初始化，目前只初始化了斗地主
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

    def gameroom_init(self,is_next=False):
        # game_list = self.game_page.get_game_list()
        game_list = ['game203']
        print game_list
        for i in range(len(game_list)):
            # self.start_step("打开机器人开关")
            gamename = game_list[i]
            if (self.game_page.game_is_exist(self.luadriver,gamename) == True):
                gameid = filter(lambda ch: ch in '0123456789', gamename)
                print gameid
                # gameid = '203'
                # gamename = "game203"
                # self.game_page.set_robot(gameid=gameid,robotflag=1)
                self.start_step("进入子游戏:%s" % game_list[i])
                time.sleep(1)
                self.luadriver.find_lua_element_by_name(gamename).click()
                self.game_page.game_is_download()
                try:
                    self.game_page.wait_element("同步标志", 20)
                    self.log_info("进入游戏ID：%s 的房间" % gamename)
                    try:
                        self.log_info("进入游戏ID：%s 的第一个玩法" % gamename)
                        elements = self.game_page.game_play_way()
                        elements[0][1].click()
                    except:
                        self.log_info("当前子游戏初级场")
                    self.game_page.wait_element("房间场次").click()
                    # self.game_page.screenshot("%s.png" % game_list[i])
                    self.start_step("判断当前游戏是否自动准备，如果是，则继续玩游戏，否则，退出房间")
                    if (self.game_page.element_is_exist("抢地主",30) == True):
                        self.game_page.wait_element("抢地主").click()
                        while(self.yuepai_page.element_is_exist("准备",3) == False):
                            try:
                                self.yuepai_page.wait_element("菜单键").click()
                                self.game_page.wait_element("托管").click()
                                self.game_page.screenshot("%s.png" % gameid)
                                break
                            except:
                                self.log_info("托管失败")
                        try:
                            self.yuepai_page.wait_element("准备",100)
                        except:
                            self.log_info("等待准备按钮出现失败")
                except:
                    try:
                        self.hall_page.wait_element("关闭对话框").click()
                    except:
                        self.log_info("未找到元素")
                try:
                    self.start_step("退出房间")
                    self.yuepai_page.is_exist_yuepairoom()
                    self.game_page.wait_element("返回1").click()
                    if is_next == True:
                        self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                        self.game_page.wait_element("右三角标").click()
                except:
                    self.log_info("未找到元素")
                self.start_step("关闭机器人开关")
                self.common.set_robot(gameid=gameid, robotflag=0)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.gameroom_init()
        # self.start_step("点击大厅第二页")
        # if (self.game_page.element_is_exist("右三角标") == True):
        #     self.game_page.wait_element("右三角标").click()
        # else:
        #     self.game_page.wait_element("左三角标").click()
        # self.start_step("查看第二屏子游戏列表，是否有规则按钮")
        # self.gameroom_init(is_next=True)


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # mid = self.common.get_config_value("casecfg", "mid")
        # self.common.recover_user(mid)
        self.common.closedriver()

# __qtaf_seq_tests__ = [C039_DFQP_Activity]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
