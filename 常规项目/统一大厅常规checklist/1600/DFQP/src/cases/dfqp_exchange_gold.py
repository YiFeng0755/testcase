#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
金条兑换
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from appiumcenter.luadriver import LuaDriver
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.friend_page import Friend_Page
from uilib.exchange_page import Exchange_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.safebox_page import Safebox_Page
from common.common import Common
from common import Interface as PHPInterface
from common import user_util

class C31063_DFQP_Exchange_gold2(TestCase):
    '''
    金条兑换
    银币少于20w,金条兑换入口不显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        self.hall_page = Hall_Page()
        self.exchange_page = Exchange_Page()
        self.personinfo_page = Personinfo_Page()
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity_switchserver(self.luadriver)
        # self.start_step("判断是否登陆")
        # if not self.common.isloginuser(self.luadriver):
        #     self.common.loginuser(user_info['user'], user_info['password'])
        #     self.common.closeActivityBtn()
        # else:
        #     if self.personinfo_page.wait_element("账号ID").get_attribute('text') != user_info['cid']:
        #         self.common.loginuser(user_info['user'], user_info['password'])
        #         self.common.closeActivityBtn()
        # try:
        #     self.personinfo_page.wait_element("关闭").click()
        # except:
        #     print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入金条兑换界面")
        time.sleep(3)
        try:
            self.exchange_page.element_is_exist("换金条")
        except:
            return True
        time.sleep(3)
        self.exchange_page.screenshot("Exchange_gold2.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        # finally:
            # self.common.release_user(user_info['mid'])


# __qtaf_seq_tests__ = [C31069_DFQP_Exchange_Gold_Exchange3]
if __name__ == '__main__':
    # C027_DFQP_PersonInfo_NicknameAlter = C027_DFQP_PersonInfo_NicknameAlter()
    # C027_DFQP_PersonInfo_NicknameAlter.debug_run()
    debug_run_all()
