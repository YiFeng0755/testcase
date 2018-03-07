#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
消息中心（消息）
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.message_page import Message_Page
from uilib.hall_page import Hall_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.backpack_page import Backpack_Page
from common.common import Common
import common.Interface as PHPInterface
import test_datas
from datacenter import dataprovider

class C61016_DFQP_Message_Display(TestCase):
    '''
    消息界面展示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，并切换到预发布
        self.common.closeactivity_switchserver(self.luadriver,"预发布")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.hall_page.wait_element("消息").click()
        time.sleep(3)
        self.start_step("查看消息")
        self.hall_page.screenshot('message_display.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()


class C61017_DFQP_Message_Display1(TestCase):
    '''
    消息界面展示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        print user_info['mid']
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("接口发送vip私信")
        # 每个用例都需要关闭活动，并切换到预发布
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        return1 = PHPInterface.send_message(int(user_info['mid']), "接口发送vip私信","接口发送vip私信",4,1,0)
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(user_info['user'], user_info['password'])
            self.common.closeActivityBtn()
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != user_info['cid']:
                self.common.loginuser(user_info['user'], user_info['password'])
                self.common.closeActivityBtn()
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(3)
        self.start_step("查看消息")
        self.hall_page.screenshot('message_display.png')


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['mid'])


# __qtaf_seq_tests__ = [C31029_DFQP_Message_Silver]
if __name__ == '__main__':
    # C002_DFQP_Login_GuestLogin = C002_DFQP_Login_GuestLogin()
    # C002_DFQP_Login_GuestLogin.debug_run()
    debug_run_all()