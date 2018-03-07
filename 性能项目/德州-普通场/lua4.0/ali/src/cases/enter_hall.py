#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
性能测试场景1：进入大厅
'''
import time
from runcenter.enums import EnumStatus, EnumPriority
from runcenter.testcase import TestCase, debug_run_all
from com.common import Common
from com.constantEnum import EnumSceneName, EnumSceneType
from com.globalVars import singleGlobalVar
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from com import Interface

class X0001_EnterHall(TestCase):
    '''
    点击登录按钮，转圈，转圈后流畅显示，无明显卡顿
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        time.sleep(10)
        self.game_page.to_hall_page("女孩")

    def run_test(self):
        time.sleep(10)
        # self.hall_page.wait_element("同步标志")
        self.common.taskScreenShot("login.jpg")
        self.start_step("进入登陆页面")
        if self.hall_page.element_is_exist("暂不认证"):
            self.hall_page.wait_element("暂不认证").click()
        if self.hall_page.element_is_exist("内网"):
            self.hall_page.wait_element("内网").click()
        self.common.sendTagBroadcast(EnumSceneName.EnterHall, EnumSceneType.Start)
        while not self.hall_page.element_is_exist("大厅头像"):
            while self.hall_page.element_is_exist("游客登录"):
                try:
                    self.hall_page.wait_element("游客登录").click()
                except:
                    print "未找到此按钮"
        if self.hall_page.element_is_exist("暂不认证"):
            self.hall_page.wait_element("暂不认证").click()
        if self.hall_page.element_is_exist("进入游戏",2):
            self.hall_page.wait_element("进入游戏").click()
        self.game_page.to_hall_page("大厅头像")
        self.hall_page.wait_element("大厅头像",60)
        self.start_step("德州小测验")
        while (self.game_page.element_is_exist("go",2)):
            driver = singleGlobalVar.get("luaDriver")
            driver.keyevent(4)
            if self.hall_page.element_is_exist("取消"):
                self.hall_page.wait_element("取消").click()
        self.common.sendTagBroadcast(EnumSceneName.EnterHall, EnumSceneType.Stop)
        self.start_step("获取mid")
        self.hall_page.wait_element("大厅头像").click()
        mid = self.hall_page.wait_element("mid").get_attribute('text')
        self.common.set_config_value("casecfg", "mid", str(mid))
        self.start_step("查看是否需要添加金币")
        money = self.hall_page.wait_element("金币数").get_attribute('text')
        money = money.replace(',','')
        print money
        if int(money) < 10000:
            Interface.add_Money(mid,10000)
        self.hall_page.wait_element("关闭").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.game_page.to_hall_page("大厅头像")


# __qtaf_seq_tests__ = [D25734_ThreeRoom_PlayGame]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()


