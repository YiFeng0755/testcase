#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
个人资料
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.personinfo_page import Personinfo_Page
from uilib.hall_page import Hall_Page
from common.common import Common
from datacenter import dataprovider
import test_datas
import common.Interface as PHPInterface

testdata=test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C30987_DFQP_PersonInfo_Interface_Sex1(TestCase):
    """
    头像为默认头像,修改性别
    """
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        self.start_step("重置默认头像")
        PHPInterface.reset_img(self.casedata['mid'])
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        time.sleep(2)
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivity_switchserver(self.luadriver, "预发布")
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
                self.common.loginuser(self.casedata['user'], self.casedata['password'])
                self.common.closeactivity_switchserver(self.luadriver, "预发布")
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.personinfo_page.screenshot("sex1.png")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        self.start_step("修改性别")
        print self.personinfo_page.wait_element("女").get_attribute('selected')
        if(self.personinfo_page.wait_element("女").get_attribute('selected')):
            self.personinfo_page.wait_element("男").click()
        else:
            self.personinfo_page.wait_element("女").click()
        time.sleep(1)
        if(self.personinfo_page.wait_element("女").get_attribute('selected')):
            a=1
        else:
            a=0
        print a
        # 重新登陆
        self.personinfo_page.screenshot("sex2.png")
        self.personinfo_page.wait_element("关闭").click()
        time.sleep(1)
        self.start_step("重启游戏查看性别")
        self.common.restart()
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        if(a==1):
            self.personinfo_page.wait_element("女").get_attribute('selected')
        else:
            self.personinfo_page.wait_element("男").get_attribute('selected')
        self.personinfo_page.screenshot( 'sex3.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata=test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C30991_DFQP_PersonInfo_EnterVIP(TestCase):
    """
    玩家是vip,点击个人资料，查看VIP特权页面
    """
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_vip(self.casedata['mid'],4)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivity_switchserver(self.luadriver, "预发布")
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
                self.common.loginuser(self.casedata['user'], self.casedata['password'])
                self.common.closeactivity_switchserver(self.luadriver, "预发布")
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"
        time.sleep(2)
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.wait_element("了解VIP特权").click()
        time.sleep(3)
        self.personinfo_page.screenshot('EnterVIP.png')
        self.luadriver.keyevent(4)
        time.sleep(2)
        self.personinfo_page.wait_element("头像logo")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        PHPInterface.set_vip(self.casedata['mid'],-1)
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

# __qtaf_seq_tests__ = [C30991_DFQP_PersonInfo_EnterVIP]
if __name__ == '__main__':
    # C027_DFQP_PersonInfo_NicknameAlter = C027_DFQP_PersonInfo_NicknameAlter()
    # C027_DFQP_PersonInfo_NicknameAlter.debug_run()
    debug_run_all()
