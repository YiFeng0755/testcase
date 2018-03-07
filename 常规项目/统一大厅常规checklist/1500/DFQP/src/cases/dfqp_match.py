#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Author: MindyZhang
'''
大厅比赛场
'''
import time
import test_datas
from runcenter.enums import EnumStatus,EnumPriority
from runcenter.testcase import TestCase,debug_run_all
from appiumcenter.luadriver import LuaDriver
from common.common import Common
from uilib.hall_page import Hall_Page
from uilib.match_page import Match_Page
from datacenter import dataprovider

class C31228_DFQP_Match(TestCase):
    '''
    大厅比赛场界面显示
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        #初始化luadriver
        self.common = Common()
        self.luadriver = self.common.setupdriver()
        time.sleep(5)
        #关闭活动弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.hall_page = Hall_Page()
        self.match_page = Match_Page()

    def run_test(self):
        '''
        测试用例
        '''

        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.start_step("点击比赛场按钮")
        self.hall_page.wait_element("比赛场").click()
        time.sleep(5)
        self.match_page.screenshot(".png")
        time.sleep(3)
        self.start_step("点击已报名")
        self.match_page.wait_element("比赛场-已报名").click()
        time.sleep(3)
        print ("未报名比赛")
        self.luadriver.keyevent(4)
        time.sleep(3)
        self.start_step("点击+银币")
        self.match_page.wait_element("+银币").click()
        time.sleep(3)
        self.match_page.wait_element("箭头返回").click()
        time.sleep(3)
        self.start_step("点击+金条")
        # while(self.match_page.is_exist("+金条")):
        self.match_page.get_element("+金条").click()
        time.sleep(3)
        self.match_page.wait_element("箭头返回").click()
        time.sleep(3)
        self.match_page.wait_element("返回").click()
        time.sleep(3)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31229_DFQP_Match_MatchType(TestCase):
    '''
    大厅比赛场---比赛类型Tab页切换
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):

        self.common = Common()
        #初始化luadriver
        print ("pre_test")
        self.luadriver = self.common.setupdriver()
        time.sleep(5)
        self.common.closeactivityprepublish(self.luadriver)

        self.hall_page = Hall_Page()
        self.match_page = Match_Page()


    def run_test(self):
        '''
        测试用例
        '''

        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.start_step("点击比赛场按钮")
        self.hall_page.wait_element("比赛场").click()
        time.sleep(3)
        self.match_page.screenshot("1.png")
        time.sleep(3)
        self.start_step("点击切换比赛tab")
        if(self.match_page.is_exist("话费赛") == True):
            self.match_page.wait_element("话费赛").click()
            time.sleep(3)
            self.match_page.screenshot("2.png")
        else:
            print ("没有话费赛")
        if(self.match_page.is_exist("实物赛") == True):
            self.match_page.wait_element("实物赛").click()
            time.sleep(3)
            self.match_page.screenshot("3.png")
        else:
            print ("没有实物赛")
        if (self.match_page.is_exist("iphone赛") == True):
            self.match_page.wait_element("iphone赛").click()
            time.sleep(3)
            self.match_page.screenshot("4.png")
        else:
            print ("没有iphone赛")

        self.match_page.wait_element("全部比赛").click()
        time.sleep(3)
        self.match_page.wait_element("返回").click()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31233_DFQP_Match_Bag(TestCase):
    '''
    大厅比赛场---物品箱
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):

        self.common = Common()
        #初始化luadriver
        print ("pre_test")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivityprepublish(self.luadriver) #关闭活动弹框
        time.sleep(10)
        self.hall_page = Hall_Page()
        self.match_page = Match_Page()

    def run_test(self):
        '''
        测试用例
        '''

        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.start_step("点击比赛场按钮")
        self.hall_page.wait_element("比赛场").click()
        time.sleep(3)
        self.start_step("点击物品箱")
        self.match_page.wait_element("比赛场-物品箱").click()
        time.sleep(3)
        self.match_page.screenshot(".png")
        time.sleep(3)
        self.luadriver.keyevent(4)
        time.sleep(3)
        self.match_page.wait_element("返回").click()
        time.sleep(3)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31235_DFQP_Match_Rank(TestCase):
    '''
    大厅比赛场---无战绩
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):

        self.common = Common()
        #初始化luadriver
        print ("pre_test")
        self.luadriver = self.common.setupdriver()
        time.sleep(10)
        self.common.closeactivityprepublish(self.luadriver) #关闭活动弹框
        self.hall_page = Hall_Page()
        self.match_page = Match_Page()

    def run_test(self):
        '''
        测试用例
        '''

        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.start_step("点击比赛场按钮")
        self.hall_page.wait_element("比赛场").click()
        time.sleep(3)
        self.start_step("点击战绩查看")
        self.match_page.wait_element("比赛场-战绩").click()
        time.sleep(3)
        self.match_page.screenshot("1.png")
        time.sleep(3)
        self.start_step("查看历史战绩")
        self.match_page.wait_element("历史战绩").click()
        time.sleep(2)
        self.match_page.screenshot("2.png")
        time.sleep(2)
        self.start_step("查看战绩总览")
        self.match_page.wait_element("战绩总览").click()
        time.sleep(2)
        self.common.swipeelement(self.match_page.wait_element("累计获得奖励"),self.match_page.wait_element("总体数据"))
        time.sleep(3)
        self.match_page.screenshot("3.png")
        time.sleep(3)
        self.luadriver.keyevent(4)
        time.sleep(2)
        self.match_page.wait_element("返回").click()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31270_DFQP_Match_Agenda(TestCase):
    '''
    大厅比赛场---今日赛程
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):

        self.common = Common()
        #初始化luadriver
        print ("pre_test")
        self.luadriver = self.common.setupdriver()
        time.sleep(10)
        self.common.closeactivityprepublish(self.luadriver) #关闭活动弹框

        self.hall_page = Hall_Page()
        self.match_page = Match_Page()

    def run_test(self):
        '''
        测试用例
        '''

        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.start_step("点击今日赛程按钮")
        self.match_page.wait_element("今日赛程").click()
        time.sleep(3)
        self.match_page.screenshot("1.png")
        time.sleep(3)
        if(self.match_page.is_exist("比赛详情1")==True):
            self.match_page.wait_element("比赛详情1").click()
            time.sleep(3)
            self.match_page.screenshot("2.png")
            self.match_page.wait_element("关闭").click()
        else:
            print ("无赛程")
            self.luadriver.keyevent(4)
            time.sleep(2)
        self.hall_page.wait_element("同步标志")
    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31261_DFQP_Match_Invitational1(TestCase):
    '''
    大厅比赛场---邀请赛创建页面
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):

        self.common = Common()
        #初始化luadriver
        print ("pre_test")
        self.luadriver = self.common.setupdriver()

        self.common.closeactivityprepublish(self.luadriver) #关闭活动弹框
        time.sleep(10)
        self.hall_page = Hall_Page()
        self.match_page = Match_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.start_step("点击比赛场按钮")
        self.hall_page.wait_element("比赛场").click()
        time.sleep(3)
        self.start_step("点击邀请赛")
        self.match_page.wait_element("比赛场-邀请赛").click()
        time.sleep(3)
        self.match_page.screenshot("1.png")
        time.sleep(3)
        self.start_step("创建邀请赛")
        self.match_page.wait_element("创建邀请赛").click()
        time.sleep(3)
        self.match_page.screenshot("2.png")
        time.sleep(3)
        if(self.match_page.is_exist("立即升级")==True):
            self.match_page.wait_element("立即升级").click()
            time.sleep(3)
            # self.match_page.wait_element("已有账号登录").click()
            # time.sleep(3)
            #self.common.loginuser(self.casedata['user'],self.casedata['password'])
            self.match_page.wait_element("手机号码").click()
            time.sleep(2)
            # self.match_page.wait_element("手机号码").send_keys('18028781683')
            # self.match_page.wait_element("密码").send_keys('111111')
            self.match_page.wait_element("确定").click()
            time.sleep(10)
            self.match_page.wait_element("关闭").click()
            time.sleep(2)
        else:
            self.match_page.screenshot("3.png")
            time.sleep(2)
            self.match_page.wait_element("箭头返回").click()
        self.match_page.wait_element("箭头返回").click()
        time.sleep(3)
        self.match_page.wait_element("返回").click()
        self.hall_page.wait_element("同步标志")
    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31232_DFQP_Match_UserInfo(TestCase):
    '''
    大厅比赛场---查看个人头像
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        #初始化luadriver
        self.common = Common()
        self.luadriver = self.common.setupdriver()
        time.sleep(5)
        #关闭活动弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.hall_page = Hall_Page()
        self.match_page = Match_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        # self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.start_step("点击比赛场按钮")
        self.hall_page.wait_element("比赛场").click()
        time.sleep(3)
        self.start_step("点击头像")
        self.match_page.wait_element("头像").click()
        time.sleep(3)
        self.match_page.screenshot(".png")
        time.sleep(3)
        self.hall_page.wait_element("关闭对话框").click()
        time.sleep(3)
        self.match_page.wait_element("返回").click()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31230_DFQP_Match_List(TestCase):
    '''
    大厅比赛场---列表刷新
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        #初始化luadriver
        self.common = Common()
        self.luadriver = self.common.setupdriver()
        time.sleep(5)
        #关闭活动弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.hall_page = Hall_Page()
        self.match_page = Match_Page()

    def run_test(self):
        '''
        测试用例
        '''

        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.start_step("点击比赛场按钮")
        self.hall_page.wait_element("比赛场").click()
        time.sleep(3)
        self.match_page.screenshot("1.png")
        self.common.swipeelement(self.match_page.wait_element("比赛列表第三行"),self.match_page.wait_element("比赛列表第一行"))
        time.sleep(3)
        self.match_page.screenshot("2.png")
        time.sleep(3)

        self.match_page.wait_element("返回").click()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()


__qtaf_seq_tests__ = [C31228_DFQP_Match]
if __name__ == "__main__":
    debug_run_all()





