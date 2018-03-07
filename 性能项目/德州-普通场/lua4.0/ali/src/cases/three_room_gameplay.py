#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
性能测试场景1：三人场玩牌一小时
'''
import time
from runcenter.enums import EnumStatus, EnumPriority
from runcenter.testcase import TestCase, debug_run_all
from com.common import Common
from com.constantEnum import EnumSceneName, EnumSceneType
from com.globalVars import singleGlobalVar
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from com import Interface as Interface
from uilib.threeroom_page import ThreeRoom_Page

class X0001_ThreeRoom_PlayGame(TestCase):
    '''
    三人场玩牌
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 60

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.threeroom_page = ThreeRoom_Page()
        self.game_page.to_hall_page('大厅头像')

    def play_game(self):
        starttime=time.time()
        self.start_step("进入游戏房间")
        self.threeroom_page.wait_element("点石成金").click()
        self.threeroom_page.wait_element("立即报名").click()
        time.sleep(6)
        self.start_step("添加机器人")
        mid = self.common.get_config_value('casecfg', 'mid')
        print 'mid:%s' % mid
        Interface.add_robot(510, mid, 2)
        while True:
            i = 0
            self.start_step("玩游戏")
            while self.threeroom_page.element_is_exist("跟注",30):
                elements = self.threeroom_page.get_elements("跟注")
                # endtime = time.time()
                # if (endtime - starttime) / 60 > self.timeout - 3:
                #     self.start_step("玩牌超时了，可以退出游戏了")
                #     return
                if len(elements)>=2:
                    try:
                        elements[1].click()
                        self.common.taskScreenShot("threeroom_game_%s.jpg" % str(time.time()).replace('.', ''))
                    except:
                        print "未找到元素"
            endtime = time.time()
            if (endtime - starttime)/60 > self.timeout - 3:
                self.start_step("玩牌超时了，可以退出游戏了")
                return
            while self.threeroom_page.element_is_exist("再战一场", 2):
                endtime = time.time()
                if (endtime - starttime) / 60 > self.timeout - 3:
                    self.start_step("玩牌一小时，可以退出游戏了")
                    return
                self.threeroom_page.wait_element("再战一场").click()
                i += 1
                print "点击再战%s场" %i
                self.start_step("添加机器人")
                mid = self.common.get_config_value('casecfg', 'mid')
                Interface.add_robot(510, mid, 2)
                time.sleep(5)


            # if self.threeroom_page.element_is_exist("再战一场", 2):
            #     self.threeroom_page.wait_element("再战一场").click()
            #     time.sleep(5)
            #     self.start_step("添加机器人")
            #     mid = self.common.get_config_value('casecfg', 'mid')
            #     Interface.add_robot(510, mid, 2)
            #     time.sleep(3)

    def run_test(self):
        self.common.taskScreenShot("enter_threegame.jpg")
        self.start_step("进入三人场")
        self.threeroom_page.wait_element("三人场",0).click()
        if self.threeroom_page.element_is_exist("关闭对话框",2):
            self.threeroom_page.wait_element("关闭对话框").click()
        self.common.sendTagBroadcast(EnumSceneName.ThreeRoom, EnumSceneType.Start)
        self.play_game()
        # if self.threeroom_page.element_is_exist("点石成金"):
        #     self.play_game()
        time.sleep(5)
        self.common.sendTagBroadcast(EnumSceneName.ThreeRoom, EnumSceneType.Stop)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''

        self.game_page.to_hall_page('大厅头像')


# __qtaf_seq_tests__ = [D25734_ThreeRoom_PlayGame]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()


