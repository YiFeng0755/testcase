#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
保险箱
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from appiumcenter.luadriver import LuaDriver
from uilib.personinfo_page import Personinfo_Page
from uilib.hall_page import Hall_Page
from uilib.sign_page import Sign_Page
from uilib.safebox_page import Safebox_Page
from common.common import Common
from common import Interface as PHPInterface
import json
import test_datas
from datacenter import dataprovider

class C31044_DFQP_Safebox_Bringless2w(TestCase):
    '''
    携带银币数小于20000
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid=mid, value='10000')
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        # global user_info,UserID
        # user_info = self.common.get_user()
        # print user_info
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)


    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(4)
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        time.sleep(4)
        self.start_step("将银币存入保险箱")
        self.safebox_page.wait_element("银币保险箱").click()
        time.sleep(4)
        self.safebox_page.wait_element("存入").click()
        time.sleep(4)
        self.safebox_page.screenshot("safebox.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.release_user(UserID)
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31045_DFQP_Safebox_Bring3w(TestCase):
    '''
    	携带银币数大于20000
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid=mid, value='30000')
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        # global user_info,UserID
        # user_info = self.common.get_user()
        # print user_info
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        time.sleep(3)
        self.start_step("将银币存入保险箱")
        self.safebox_page.wait_element("银币保险箱").click()
        time.sleep(3)
        self.safebox_page.wait_element("存入").click()
        time.sleep(3)
        try:
            self.safebox_page.wait_element("存入").click()
            time.sleep(3)
        except:
            print "无此按钮"
        self.start_step("拖动滑动条")
        self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
        time.sleep(8)
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(5)
        self.safebox_page.screenshot('safebox1.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.release_user(user_info['mid'])
        # self.common.deletefile(self.luadriver)
        self.common.recover_user(mid=mid)
        self.common.closedriver()

class C31046_DFQP_Safebox_Safeboxis0(TestCase):
    '''
    保险箱银币数为0时取款
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid=mid, value='10000')
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入保险箱")
        self.hall_page.wait_element('保险箱').click()
        time.sleep(3)
        Safebox_info = PHPInterface.get_safebox(mid)
        coin_saving = Safebox_info.get('safebox')
        if coin_saving > 0:
            self.start_step("将银币取出保险箱")
            self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
            time.sleep(3)
            self.safebox_page.wait_element('确定---保险箱').click()
            time.sleep(3)
        user_info = PHPInterface.get_user_info(mid)  # 获取玩家信息
        coin = json.loads(user_info).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        if coin > 20000:
            AddMoney =10000 - coin
            PHPInterface.add_money(mid, AddMoney)
            self.luadriver.keyevent(4)
            self.common.closeactivity_switchserver(self.luadriver)
            self.hall_page.wait_element('保险箱').click()
            time.sleep(3)
            self.safebox_page.wait_element("取出").click()
            time.sleep(3)
            self.safebox_page.screenshot('safebox1.png')
        time.sleep(3)
        self.safebox_page.wait_element("取出").click()
        time.sleep(4)
        self.safebox_page.wait_element("存入").click()
        time.sleep(2)
        self.safebox_page.screenshot('safebox2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.release_user(UserID)
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31047_DFQP_Safebox_Safeboxnot0(TestCase):
    '''
    保险箱银币不为0时取款
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid=mid, value='40000')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity(self.luadriver)


    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入保险箱")
        self.hall_page.wait_element("保险箱").click()
        time.sleep(2)
        self.safebox_page.wait_element("存入").click()
        time.sleep(2)
        try:
            self.safebox_page.wait_element("存入").click()
            time.sleep(3)
        except:
            print "无此按钮"
        self.start_step("将银币存入保险箱")
        self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
        time.sleep(2)
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(3)
        self.safebox_page.screenshot('1.png')
        self.start_step("将银币取出保险箱")
        self.safebox_page.wait_element("取出").click()
        time.sleep(2)
        self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
        time.sleep(2)
        self.safebox_page.screenshot('2.png')
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(2)
        self.safebox_page.screenshot('3.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31048_DFQP_Safebox(TestCase):
    '''
    携带金币数小于200
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_crystal(mid=mid, value='100')
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # global UserID
        # UserID = user_info.get('mid')
        # print 'UserID:%s' % UserID
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        time.sleep(2)
        self.start_step("将金条存入保险箱")
        self.safebox_page.wait_element("金条保险箱").click()
        time.sleep(2)
        self.safebox_page.wait_element("存入").click()
        time.sleep(2)
        self.safebox_page.screenshot("safebox.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.release_user(UserID)
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31048_DFQP_Safebox2(TestCase):
    '''
        携带金币数大于200
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_crystal(mid=mid, value='300')
        # global user_info,UserID
        # user_info = self.common.get_user()
        # print user_info
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        time.sleep(3)
        self.start_step("将金条存入保险箱")
        self.safebox_page.wait_element("金条保险箱").click()
        time.sleep(2)
        self.safebox_page.wait_element("存入").click()
        time.sleep(3)
        try:
            self.safebox_page.wait_element("存入").click()
            time.sleep(3)
        except:
            print "无此按钮"
        self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
        time.sleep(3)
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(3)
        self.safebox_page.screenshot('safebox1.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.release_user(UserID)
        # self.common.deletefile(self.luadriver)
        self.common.recover_user(mid)
        self.common.closedriver()

class C31048_DFQP_Safebox3(TestCase):
    '''
    保险箱金币数为0时取款
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity(self.luadriver)


    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入保险箱")
        self.hall_page.wait_element('保险箱').click()
        time.sleep(3)
        self.safebox_page.wait_element('金条保险箱').click()
        time.sleep(3)
        self.safebox_page.wait_element("取出").click()
        time.sleep(3)
        Safebox_info = PHPInterface.get_safebox(mid)
        crystal_saving = Safebox_info.get('crystalsafebox')
        if crystal_saving > 0:
            self.start_step("将金条取出保险箱")
            self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
            time.sleep(3)
            self.safebox_page.wait_element('确定---保险箱').click()
            time.sleep(3)
        user_info1 = PHPInterface.get_user_info(mid)  # 获取玩家信息
        crystal = json.loads(user_info1).get('result', {'crystal': None}).get('crystal')  # 获取当前金条值
        if crystal > 200:
            AddMoney = 100 - crystal
            PHPInterface.add_money(mid, AddMoney)
            self.luadriver.keyevent(4)
            self.common.closeactivity_switchserver(self.luadriver)
            self.hall_page.wait_element('保险箱').click()
            time.sleep(3)
            self.safebox_page.wait_element("取出").click()
        self.safebox_page.screenshot('1.png')
        self.safebox_page.wait_element("存入").click()
        time.sleep(1)
        self.safebox_page.screenshot('2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.release_user(user_info['mid'])
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31048_DFQP_Safebox4(TestCase):
    '''
    保险箱金币不为0时取款
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_crystal(mid=mid, value='400')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity(self.luadriver)


    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.hall_page.wait_element('保险箱').click()
        time.sleep(3)
        self.safebox_page.wait_element('金条保险箱').click()
        time.sleep(3)
        self.safebox_page.wait_element("存入").click()
        time.sleep(3)
        self.start_step("将金条存入保险箱")
        self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
        time.sleep(3)
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(3)
        self.safebox_page.screenshot('1.png')
        self.start_step("将金条取出保险箱")
        self.safebox_page.wait_element('取出').click()
        time.sleep(3)
        self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
        time.sleep(3)
        self.safebox_page.screenshot('2.png')
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(3)
        self.safebox_page.screenshot('3.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.release_user(UserID)
        # self.common.deletefile(self.luadriver)
        # self.common.closedriver()
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
            self.common.recover_user(mid)
        except:
            self.log_info("close driver fail")

__qtaf_seq_tests__ = [C31047_DFQP_Safebox_Safeboxnot0]
if __name__ == '__main__':
    # C31045_DFQP_safebox1 = C31046_DFQP_Safebox()
    # C31045_DFQP_safebox1.debug_run()
    debug_run_all()




