#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
大厅游戏位显示
'''

import time
from runcenter.testcase import TestCase, debug_run_all
from runcenter.enums import EnumStatus, EnumPriority
# from common.common import Common
from common.common import Common
from uilib.hall_page import Hall_Page

class c27338_hall_gameDisplay(TestCase):
    '''
    大厅游戏位显示
    '''
    owner = "GuixiangGui"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.start_step("初始化driver")
        self.luaDriver = self.common.setupdriver()
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.luaDriver)
        
    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("开始截图")
        self.hall_page.screenshot("first.png")
        try:
            self.hall_page.wait_element("更多游戏", 3).click()
            self.hall_page.screenshot("moreGame.png")
        except:
            try:
                self.hall_page.wait_element("右三角", 3).click()
                time.sleep(1)
                self.hall_page.screenshot("second.png")
                self.hall_page.wait_element("更多游戏").click()
                time.sleep(1)
                self.hall_page.screenshot("moreGame.png")
            except:
                print "右箭头或更多游戏没有找到"
        else:
            self.luaDriver.back()
            try:
                self.hall_page.wait_element("右三角", 3).click()
                self.hall_page.screenshot("3.png")
            except:
                print "右箭头没有找到"
        
        
    def post_test(self):
        self.common.closedriver()
        

# __qtaf_seq_tests__ = [C27343_Gamelist_Sendbroadcast]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
