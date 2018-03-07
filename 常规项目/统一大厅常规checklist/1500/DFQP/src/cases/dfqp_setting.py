#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
设置
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.setting_page import Setting_Page
from uilib.hall_page import Hall_Page
from common.common import Common

class C31098_DFQP_Setting(TestCase):
    '''
    设置界面显示
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
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入活动页面")
        self.hall_page.wait_element("设置").click()
        time.sleep(1)
        self.setting_page.wait_element("关于我们")
        self.setting_page.screenshot('Setting.png')
        self.setting_page.wait_element("页面返回").click()
        time.sleep(2)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31099_DFQP_Setting_Effect(TestCase):
    '''
    大厅配置音效设置
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
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入设置页面")
        self.hall_page.wait_element("设置").click()
        time.sleep(2)
        self.setting_page.wait_element("静音").click()
        self.setting_page.wait_element("震动").click()
        self.setting_page.screenshot('Effect.png')
        self.start_step("重启游戏")
        self.luadriver = self.common.restart()
        self.hall_page.wait_element("设置").click()
        self.setting_page.screenshot('Effect.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31101_DFQP_Setting_floatBall(TestCase):
    '''
    打开或者关闭浮动球、比赛围观按钮，查看效果
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
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入设置页面")
        self.hall_page.wait_element("设置").click()
        time.sleep(2)
        self.setting_page.wait_element("关闭浮动球").click()
        self.setting_page.wait_element("围观").click()
        self.setting_page.screenshot('floatBall1.png')
        self.start_step("重启游戏")
        self.luadriver = self.common.restart()
        self.hall_page.wait_element("设置").click()
        self.setting_page.screenshot('floatBall2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31103_DFQP_Setting_AboutUs(TestCase):
    '''
    点击关于我们，查看页面显示
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
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入设置页面")
        self.hall_page.wait_element("设置").click()
        time.sleep(2)
        self.setting_page.wait_element("关于我们").click()
        time.sleep(2)
        self.setting_page.screenshot('AboutUs.png')
        self.setting_page.wait_element("页面返回").click()
        self.setting_page.wait_element("设置")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31104_DFQP_Setting_Agreement(TestCase):
    '''
    切换到服务协议界面，查看
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
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入设置页面")
        self.hall_page.wait_element("设置").click()
        time.sleep(5)
        self.setting_page.wait_element("关于我们").click()
        time.sleep(2)
        self.setting_page.wait_element("服务协议").click()
        time.sleep(2)
        self.setting_page.screenshot('Agreement.png')
        self.setting_page.wait_element("页面返回").click()
        self.setting_page.wait_element("设置")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31105_DFQP_Setting_Privacy(TestCase):
    '''
    切换到隐私策略界面，查看
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
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入设置页面")
        self.hall_page.wait_element("设置").click()
        time.sleep(2)
        self.setting_page.wait_element("关于我们").click()
        time.sleep(2)
        self.setting_page.wait_element("隐私策略").click()
        time.sleep(2)
        self.setting_page.screenshot('C045_DFQP_Setting_Privacy.png')
        self.setting_page.wait_element("页面返回").click()
        self.setting_page.wait_element("设置")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31106_DFQP_Setting_Version(TestCase):
    '''
    	版号声明页面显示
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
        self.common.closeactivity_switchserver(self.luadriver,"预发布")

        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入设置页面")
        self.hall_page.wait_element("设置").click()
        time.sleep(2)
        self.setting_page.wait_element("关于我们").click()
        time.sleep(2)
        self.setting_page.wait_element("版本声明").click()
        time.sleep(2)
        self.setting_page.screenshot( 'C046_DFQP_Setting_Version.png')
        self.setting_page.wait_element("页面返回").click()
        self.setting_page.wait_element("设置")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31107_DFQP_Setting_AboutUsSwitch(TestCase):
    '''
    切换到各个页面查看
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
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入设置页面")
        self.hall_page.wait_element("设置").click()
        time.sleep(2)
        self.setting_page.wait_element("关于我们").click()
        time.sleep(2)
        self.setting_page.wait_element("版本声明").click()
        time.sleep(1)
        # self.setting_page.wait_element("关于我们").click()
        # time.sleep(1)
        self.setting_page.wait_element("服务协议").click()
        time.sleep(1)
        self.setting_page.wait_element("隐私策略").click()
        time.sleep(1)
        self.setting_page.screenshot( 'AboutUsSwitch.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31108_DFQP_Setting_Help1(TestCase):
    '''
    点击游戏帮助按钮，查看通用tab栏
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
        self.common.closeactivity_switchserver(self.luadriver,"预发布")

        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入设置页面")
        self.hall_page.wait_element("设置").click()
        time.sleep(2)
        self.setting_page.wait_element("帮助").click()
        time.sleep(2)
        self.luadriver.swipe(295, 400, 95, 400)
        self.luadriver.swipe(295, 400, 295, 600)
        self.setting_page.screenshot('Setting_Help1.png')
        self.setting_page.wait_element("页面返回1").click()
        self.setting_page.wait_element("设置")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C31102_DFQP_Setting_floatBalljump(TestCase):
    '''
    浮动球配置跳转点击查看
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
        self.common.closeactivity_switchserver(self.luadriver,"预发布")

        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入设置页面")
        self.hall_page.wait_element("设置").click()
        time.sleep(2)
        self.start_step("设置浮动球")
        try:
            self.setting_page.wait_element("打开浮动球").click()
        except:
            print "浮动球已经打开"
        time.sleep(2)
        self.start_step("浮动球操作")
        self.setting_page.wait_element("浮动球").click()
        time.sleep(2)
        try:
            self.setting_page.wait_element("点击浮动球页面").click()
        except:
            print "浮动球页面无法点击"
        time.sleep(3)
        self.setting_page.screenshot( 'floatBalljump.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

# __qtaf_seq_tests__ = [C31107_DFQP_Setting_AboutUsSwitch]
if __name__ == '__main__':
    # C042_DFQP_Setting_floatBall = C042_DFQP_Setting_floatBall()
    # C042_DFQP_Setting_floatBall.debug_run()
    debug_run_all()
