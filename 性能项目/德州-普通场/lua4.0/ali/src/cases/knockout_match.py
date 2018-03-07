#!/usr/bin/env python
#coding=utf-8

'''
性能测试场景3:淘汰赛玩牌一小时
'''
import time
from runcenter.enums import EnumStatus, EnumPriority
from runcenter.testcase import TestCase, debug_run_all
from com.common import Common
from com.constantEnum import EnumSceneName, EnumSceneType
from com.globalVars import singleGlobalVar
from uilib.threeroom_page import ThreeRoom_Page
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.knockout_page import Knockout_Page
from com import Interface as Interface

class X0003_Knockout_match(TestCase):
    '''
    进入淘汰赛玩牌，持续玩牌一小时
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 60

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.knockout_page = Knockout_Page()
        self.threeroom_page = ThreeRoom_Page()
        self.game_page.to_hall_page('大厅头像')

    def play(self):
        self.start_step("报名参赛")
        self.knockout_page.wait_element('报名').click()
        time.sleep(5)
        self.start_step("添加机器人")
        mid = self.common.get_config_value('casecfg', 'mid')
        print 'mid:%s' % mid
        Interface.add_robot(510, mid, 5)
        begintime = time.time()
        while True:
            self.common.taskScreenShot("taotai_game_%s.jpg" %str(time.time()).replace('.',''))
            while self.knockout_page.element_is_exist("过牌",30):
                endtime = time.time()
                if ((int(endtime) - int(begintime)) / 60) > (self.timeout - 3):
                    self.common.taskScreenShot("playing_end.jpg")
                    return
                elements = self.knockout_page.get_elements("过牌")
                # print len(elements)
                try:
                    elements[1].click()
                    self.common.taskScreenShot("taotai_game_%s.jpg" % str(time.time()).replace('.', ''))
                except:
                    print "未找到元素"
            endtime = time.time()
            # print endtime - begintime
            if ((int(endtime) - int(begintime)) / 60) > (self.timeout - 3):
                self.common.taskScreenShot("playing_end.jpg")
                return
            if self.knockout_page.element_is_exist("再战一场", 2):
                self.knockout_page.wait_element('再战一场').click()
                time.sleep(5)
                Interface.add_robot(510, mid, 5)

    def run_test(self):
        self.start_step("进入淘汰赛")
        self.game_page.wait_element("淘汰赛").click()
        self.common.taskScreenShot("knockout.jpg")
        self.common.sendTagBroadcast(EnumSceneName.Knockout, EnumSceneType.Start)
        self.play()
        time.sleep(10)
        self.common.sendTagBroadcast(EnumSceneName.Knockout, EnumSceneType.Stop)

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