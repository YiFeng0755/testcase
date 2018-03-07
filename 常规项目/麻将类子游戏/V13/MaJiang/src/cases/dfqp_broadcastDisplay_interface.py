#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
房间内广播展示
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from common.common import Common
from uilib.hall_page import Hall_Page
import common.Interface as PHPInterface

class C27357_BroadcastDisplayInGameroom(TestCase):
    '''
    房间内查看普通广播显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.start_step("初始化环境")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)




    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        eles_1 = self.hall_page.get_elements('子游戏')
        print eles_1
        self.start_step('进入子游戏')
        eles_1[0].click()
        time.sleep(4)
        eles_2 = self.hall_page.get_elements('场次名称')
        print eles_2
        self.start_step('进入初级场')
        eles_2[0].click()
        time.sleep(5)
        self.start_step('开始发送广播')
        PHPInterface.broadcast(mid = 2008788,content='BroadcastDisplayInGameroomTest')
        time.sleep(2)
        self.hall_page.screenshot('广播.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

if __name__ == '__main__':
    C27357_BroadcastDisplayInGameroom().debug_run()