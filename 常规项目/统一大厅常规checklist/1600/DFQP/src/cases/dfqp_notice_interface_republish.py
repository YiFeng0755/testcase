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

class C33362_DFQP_Notice_Text(TestCase):
    '''
    查看文本公告
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
        return1 = PHPInterface.set_notice('yyyy', "tttt", app_id=103000, weight=1, end_time=int(time.time() + 60 * 2),is_html=0,conditions={"poptype":2})
        print return1
        self.start_step("配置公告")
        self.common.closeactivity_switchserver(self.luadriver)
        Flag = True
        while Flag:  # 关闭干扰活动弹框，找到公告弹框
            try:
                self.hall_page.wait_element('公告标题')
                print '找到公告标题'
                Flag = False
            except:
                try:
                    self.sign_page.wait_element("关闭1").click()
                except:
                    print '未找到关闭按钮'
                time.sleep(2)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.hall_page.screenshot("notice_text.png")
        self.sign_page.wait_element("关闭1").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C33363_DFQP_Notice_HTML(TestCase):
    '''
    查看富文本公告
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.sign_page = Sign_Page()
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        return1 = PHPInterface.set_notice('公告自动化测试', "文本公告测试", app_id=103000, end_time=int(time.time() + 60 * 2), is_html=1,conditions={"poptype":2})
        print return1
        self.start_step("配置公告")
        self.common.closeactivity_switchserver(self.luadriver)
        Flag = True
        while Flag:  # 关闭干扰活动弹框，找到公告弹框
            try:
                self.hall_page.wait_element('公告标题')
                print '找到公告标题'
                Flag = False
            except:
                try:
                    self.sign_page.wait_element("关闭1").click()
                except:
                    print '未找到关闭按钮'
                time.sleep(2)

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

class C33364_DFQP_Notice_Picture(TestCase):
    '''
    图片公告，不配置跳转
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
        return1 = PHPInterface.set_notice(title='666666', content={"htmlpic":"https://dfqppic.266.com/dfqp/pic/notice/mycff2zj.png"}, app_id=103000, end_time=int(time.time() + 60 * 2), is_html=2,conditions={"poptype":2})
        print return1
        time.sleep(10)
        self.start_step("配置公告")
        self.common.closeactivity_switchserver(self.luadriver)
        Flag = True
        while Flag:  # 关闭干扰活动弹框，找到公告弹框
            try:
                self.hall_page.wait_element('公告图片')
                print '找到公告图片'
                Flag = False
            except:
                try:
                    self.sign_page.wait_element("关闭1").click()
                except:
                    print '未找到关闭按钮'
                time.sleep(2)

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

class C33365_DFQP_Notice_Picture_ActivityCentre(TestCase):
    '''
    图片公告，配置跳转到活动中心
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
        return1 = PHPInterface.set_notice(title='666666',content={"htmlpic": "https://dfqppic.266.com/dfqp/pic/notice/mycff2zj.png","cmd": 1014}, app_id=103000, end_time=int(time.time() + 60 * 2), is_html=2,conditions={"poptype":2})
        print return1
        time.sleep(10)
        self.start_step("配置公告")
        self.common.closeactivity_switchserver(self.luadriver)
        Flag = True
        while Flag:  # 关闭干扰活动弹框，找到公告弹框
            try:
                self.hall_page.wait_element('公告图片')
                print '找到公告图片'
                Flag = False
            except:
                try:
                    self.sign_page.wait_element("关闭1").click()
                except:
                    print '未找到关闭按钮'
                time.sleep(2)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.hall_page.wait_element('公告图片').click()
        time.sleep(3)
        self.hall_page.screenshot("notice.png")
        try:
            self.sign_page.wait_element("关闭1").click()
        except:
            print '未找到关闭按钮'

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C33366_DFQP_Notice_Picture_Match(TestCase):
    '''
    图片公告，配置跳转到比赛
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
        return1 = PHPInterface.set_notice(title='666666', content={"htmlpic": "https://dfqppic.266.com/dfqp/pic/notice/mycff2zj.png", "cmd": 1021,"gameid": 203,"level": 12,"matchconfigid": 12323232}, app_id=103000, end_time=int(time.time() + 60 * 2), is_html=2,conditions={"poptype":2})
        print return1
        time.sleep(10)
        self.start_step("配置公告")
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.hall_page.wait_element('公告图片').click()
        time.sleep(3)
        self.hall_page.screenshot("notice.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C33367_DFQP_Notice_Picture_ChildGame(TestCase):
    '''
    图片公告，配置跳转到子游戏
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
        return1 = PHPInterface.set_notice(title='666666', content={"htmlpic": "https://dfqppic.266.com/dfqp/pic/notice/mycff2zj.png", "cmd": 1022,"gameid": 203,"level": 12}, app_id=103000, end_time=int(time.time() + 60 * 2), is_html=2,conditions={"poptype":2})
        print return1
        time.sleep(10)
        self.start_step("配置公告")
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.hall_page.wait_element('公告图片').click()
        try:
            self.sign_page.wait_element("关闭1").click()
        except:
            print '未找到关闭按钮'
        time.sleep(3)
        self.hall_page.screenshot("notice.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C33368_DFQP_Notice_Picture_Mall(TestCase):
    '''
    图片公告，配置跳转到商城
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
        return1 = PHPInterface.set_notice(title='666666', content={"htmlpic": "https://dfqppic.266.com/dfqp/pic/notice/mycff2zj.png", "cmd": 1008}, app_id=103000, end_time=int(time.time() + 60 * 2), is_html=2, conditions={"poptype": 2})
        print return1
        time.sleep(10)
        self.start_step("配置公告")
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.hall_page.wait_element('公告图片').click()
        time.sleep(3)
        self.hall_page.screenshot("notice.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()



# __qtaf_seq_tests__ = [C33363_DFQP_Notice_HTML]
if __name__ == '__main__':
    #C33368_DFQP_Notice_Picture_Mall= C33368_DFQP_Notice_Picture_Mall()
    #C33368_DFQP_Notice_Picture_Mall.debug_run()
    debug_run_all()