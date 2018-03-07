#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
公告
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.sign_page import Sign_Page
from uilib.hall_page import Hall_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.backpack_page import Backpack_Page
from common.common import Common
import common.Interface as PHPInterface
import test_datas
from datacenter import dataprovider

testdata = test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C30981_DFQP_Notice_Display(TestCase):
    '''
    公告页面查看
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.sign_page = Sign_Page()
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        return1 = PHPInterface.set_notice('公告自动化测试',"公告自动化测试",id=103000,end_time=int(time.time() + 60 * 4),is_html=0)
        print return1
        self.start_step("配置公告")
        try:
            self.luadriver.find_element_by_name("允许").click()
        except:
            print "未出现按钮"
        time.sleep(15)
        try:
            self.hall_page.wait_element("确认登陆").click()
        except:
            print "未出现登陆按钮"
        # print self.casedata['mid']

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.hall_page.screenshot("notice.png")
        self.sign_page.wait_element("关闭1").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

# __qtaf_seq_tests__ = [C006_DFQP_Message_Object]
if __name__ == '__main__':
    # C002_DFQP_Login_GuestLogin = C002_DFQP_Login_GuestLogin()
    # C002_DFQP_Login_GuestLogin.debug_run()
    debug_run_all()