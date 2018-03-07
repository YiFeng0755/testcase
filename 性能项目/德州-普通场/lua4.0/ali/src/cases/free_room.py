#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
性能测试场景2:自由场玩牌一小时
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

class X0002_Freeroom(TestCase):
    '''
    进入自由场玩牌，持续玩牌一小时
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 60

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.game_page.to_hall_page('大厅头像')

    def play(self):
        count = 1
        begintime = time.time()
        if self.game_page.element_is_exist("快速开始"):
            self.game_page.wait_element("开始").click()
        time.sleep(5)
        self.start_step("添加机器人第%s次" %count)
        count += 1
        mid = self.common.get_config_value('casecfg','mid')
        Interface.add_robot(510, mid, 3)
        time.sleep(5)
        while True:
            self.start_step("继续玩牌")
            self.common.taskScreenShot("freeroom_game_%s.jpg" %str(time.time()).replace('.',''))
            while self.game_page.element_is_exist("过牌",30):
                elements = self.game_page.get_elements("过牌")
                endtime = time.time()
                if ((int(endtime) - int(begintime)) / 60) > (self.timeout - 3):
                    return
                # print len(elements)
                if len(elements)>=2:
                    elements[1].click()
                    self.common.taskScreenShot("freeroom_game_%s.jpg" % str(time.time()).replace('.', ''))
            endtime = time.time()
            # print str((int(endtime) - int(begintime))/60)
            if ((int(endtime) - int(begintime))/60) > (self.timeout - 3):
                return
            self.common.taskScreenShot("gaming_%s.jpg" %str(time.time()).replace('.',''))
            # self.start_step("添加机器人")
            # Interface.add_robot(510, mid, 1)
            if self.game_page.element_is_exist("坐下",2):
                self.game_page.wait_element("坐下").click()
                self.game_page.wait_element("确定").click()
            self.start_step("添加机器人")
            Interface.add_robot(510, mid, 3)

    def run_test(self):
        # time.sleep(10)
        # self.hall_page.wait_element("同步标志")
        self.common.taskScreenShot("hall.jpg")
        # while (self.game_page.element_is_exist("go")):
        #     driver = singleGlobalVar.get("luaDriver")
        #     driver.keyevent(4)
        self.start_step("进入自由场")
        while self.game_page.element_is_exist("自由场"):
            self.game_page.wait_element("自由场").click()
        self.common.sendTagBroadcast(EnumSceneName.FreeRoom, EnumSceneType.Start)
        self.play()
        time.sleep(10)
        self.common.sendTagBroadcast(EnumSceneName.FreeRoom, EnumSceneType.Stop)

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


