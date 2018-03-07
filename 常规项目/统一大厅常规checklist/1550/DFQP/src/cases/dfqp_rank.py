#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
排行
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.rank_page import Rank_Page
from common.common import Common

class C31121_DFQP_Rank_Enterearn(TestCase):
    '''
    收益排行榜，查看界面显示
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver, "环境切换")
        self.rank_page = Rank_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入排行榜页面")
        self.hall_page.wait_element("排行榜").click()
        time.sleep(2)
        self.start_step("各个页面切换")
        self.rank_page.wait_element("富豪榜").click()
        time.sleep(1)
        self.rank_page.wait_element("收益榜").click()
        time.sleep(4)
        self.rank_page.wait_element("今日").click()
        time.sleep(4)
        self.rank_page.screenshot('Rank_Enter.png')
        time.sleep(1)
        self.rank_page.wait_element("返回").click()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31120_DFQP_Rank_Userinfo(TestCase):
    '''
    点击查看每个排行榜
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver, "环境切换")

        self.rank_page = Rank_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入排行榜页面")
        self.hall_page.wait_element("排行榜").click()
        time.sleep(3)
        self.start_step("查看个人信息")
        self.rank_page.wait_element("收益榜").click()
        self.rank_page.screenshot( 'Rank_Userinfo21.png')
        self.rank_page.wait_element("富豪榜").click()
        self.rank_page.screenshot('Rank_Userinfo21.png')
        time.sleep(2)
        self.rank_page.wait_element("返回").click()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31122_DFQP_Rank_Userinfodetail(TestCase):
    '''
    点击查看每个排行榜玩家头像、id、昵称、性别、vip标志、数据
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver, "环境切换")
        self.rank_page = Rank_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入排行榜页面")
        self.hall_page.wait_element("排行榜").click()
        time.sleep(3)
        if (self.rank_page.is_exist("用户头像")):
            self.start_step("查看个人信息")
            self.rank_page.wait_element("用户头像").click()
            self.start_step("加好友")
            self.rank_page.wait_element("加好友").click()
            time.sleep(2)
            self.rank_page.wait_element("关闭对话框").click()
            self.start_step("举报功能")
            self.rank_page.wait_element("用户头像").click()
            self.rank_page.wait_element("举报").click()
            time.sleep(2)
            self.start_step("取消举报")
            self.rank_page.wait_element("色情昵称").click()
            time.sleep(2)
            self.rank_page.wait_element("取消举报").click()
            time.sleep(5)
            self.start_step("确定举报")
            self.rank_page.wait_element("用户头像").click()

            self.rank_page.wait_element("举报").click()
            time.sleep(2)
            self.rank_page.wait_element("色情头像").click()
            time.sleep(2)
            self.rank_page.wait_element("确定举报").click()
            self.rank_page.screenshot('Userinfodetail.png')
            time.sleep(2)
            self.rank_page.wait_element("返回").click()
            self.hall_page.wait_element("同步标志")
        else:
            self.rank_page.screenshot("userinfo_fail")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31124_DFQP_Rank_Yesterday(TestCase):
    '''
    收益榜昨日/今日数据
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver, "环境切换")

        self.rank_page = Rank_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入排行榜页面")
        self.hall_page.wait_element("排行榜").click()
        time.sleep(3)
        self.rank_page.wait_element("收益榜").click()
        time.sleep(3)
        self.start_step("切换昨日今日排行榜")
        self.rank_page.wait_element("昨日").click()
        self.rank_page.screenshot('Rank_Yesterday1.png')
        time.sleep(2)
        self.rank_page.wait_element("今日").click()
        self.rank_page.screenshot('Rank_Yesterday2.png')
        time.sleep(2)
        self.rank_page.wait_element("返回").click()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31125_DFQP_Rank_Enterrich(TestCase):
    '''
    查看富豪榜排行信息,滑动查看
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver, "环境切换")
        self.rank_page = Rank_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入排行榜页面")
        self.hall_page.wait_element("排行榜").click()
        time.sleep(2)
        self.start_step("进入富豪榜")
        self.rank_page.wait_element("富豪榜").click()
        time.sleep(2)
        self.rank_page.wait_element("昨日").click()
        self.common.swipeelement(self.rank_page.wait_element("富豪榜第三行"),self.rank_page.wait_element("富豪榜第一行"))
        time.sleep(2)
        self.rank_page.screenshot( 'Enterrich.png')
        time.sleep(2)
        self.start_step("快速提升排名")
        self.rank_page.wait_element("快速提升排名").click()
        time.sleep(8)
        self.luadriver.keyevent(4)
        time.sleep(3)
        self.rank_page.wait_element("返回").click()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31126_DFQP_Rank_RichUserinfo(TestCase):
    '''
    点击查看富豪榜排行榜玩家头像、id、昵称、性别、vip标志、数据
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver, "环境切换")

        self.rank_page = Rank_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入排行榜页面")
        self.hall_page.wait_element("排行榜").click()
        time.sleep(3)
        self.start_step("进入富豪榜")
        self.rank_page.wait_element("富豪榜").click()
        time.sleep(5)
        if(self.rank_page.is_exist("用户头像")):
            self.start_step("查看个人信息")
            self.rank_page.wait_element("用户头像").click()
            self.start_step("加好友")
            self.rank_page.wait_element("加好友").click()
            time.sleep(2)
            self.rank_page.wait_element("关闭对话框").click()
            self.start_step("举报功能")
            self.rank_page.wait_element("用户头像").click()
            self.rank_page.wait_element("举报").click()
            time.sleep(2)
            self.start_step("取消举报")
            self.rank_page.wait_element("色情昵称").click()
            time.sleep(2)
            self.rank_page.wait_element("取消举报").click()
            time.sleep(5)
            self.start_step("确定举报")
            self.rank_page.wait_element("用户头像").click()
            time.sleep(4)
            self.rank_page.wait_element("举报").click()
            time.sleep(2)
            self.rank_page.wait_element("色情头像").click()
            time.sleep(2)
            self.rank_page.wait_element("确定举报").click()
            self.rank_page.screenshot('RichUserinfo.png')
            time.sleep(2)
            self.rank_page.wait_element("返回").click()
            time.sleep(3)
            self.hall_page.wait_element("同步标志")
        else:
            self.rank_page.screenshot("userinfo_fail")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31128_DFQP_Rank_RichYesterday(TestCase):
    '''
    富豪榜昨日/今日数据
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver, "环境切换")

        self.rank_page = Rank_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入排行榜页面")
        self.hall_page.wait_element("排行榜").click()
        time.sleep(3)
        self.start_step("进入富豪榜")
        self.rank_page.wait_element("富豪榜").click()
        time.sleep(2)
        self.start_step("切换昨日今日排行榜")
        self.rank_page.wait_element("昨日").click()
        self.rank_page.screenshot('RichYesterday.png')
        time.sleep(2)
        self.rank_page.wait_element("今日").click()
        self.rank_page.screenshot('RichYesterday.png')
        time.sleep(2)
        self.rank_page.wait_element("返回").click()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31129_DFQP_Rank_Entermall(TestCase):
    '''
    点击快速提升排名按钮
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver, "环境切换")

        self.rank_page = Rank_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入排行榜页面")
        self.hall_page.wait_element("排行榜").click()
        time.sleep(2)
        self.start_step("进入富豪榜")
        self.rank_page.wait_element("富豪榜").click()
        time.sleep(2)
        self.start_step("快速提升排名")
        self.rank_page.wait_element("快速提升排名").click()
        time.sleep(5)
        self.rank_page.screenshot('Entermall.png')
        self.rank_page.wait_element("返回1").click()
        time.sleep(4)
        self.rank_page.wait_element("返回").click()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

__qtaf_seq_tests__ = [C31124_DFQP_Rank_Yesterday]
if __name__ == '__main__':
    # C056_DFQP_Rank_Enterrich = C056_DFQP_Rank_Enterrich()
    # C056_DFQP_Rank_Enterrich.debug_run()
    debug_run_all()
