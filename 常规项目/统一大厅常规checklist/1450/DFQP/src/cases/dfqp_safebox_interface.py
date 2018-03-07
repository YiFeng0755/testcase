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
testdata=test_datas.logindata4
@dataprovider.DataDrive(testdata)
class C31044_DFQP_Safebox(TestCase):
    '''
    携带银币数小于20000
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        UserID = self.casedata.get('mid2')
        print 'UserID:%s'%UserID
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        if coin > 20000 or coin < 3000:
            AddMoney = 10000 - coin  # 如果当前银币多于20000或少于3000，则将银币值设置为10000
            PHPInterface.add_money(UserID, AddMoney)
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
            self.common.closeactivity_switchserver(self.luadriver, "预发布")
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
                self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
                self.common.closeactivity_switchserver(self.luadriver, "预发布")
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(4)
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.start_step("将银币存入保险箱")
        self.safebox_page.wait_element("银币保险箱").click()
        self.safebox_page.wait_element("存入").click()
        self.safebox_page.screenshot("safebox.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata=test_datas.logindata4
@dataprovider.DataDrive(testdata)
class C31045_DFQP_Safebox(TestCase):
    '''
    	携带银币数大于20000
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        UserID = self.casedata.get('mid2')
        print 'UserID:%s' % UserID
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        if coin <= 20000:
            AddMoney = 30000 - coin  # 如果当前银币不多于20000，则将银币值设置为30000
            PHPInterface.add_money(UserID, AddMoney)
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
            self.common.closeactivity_switchserver(self.luadriver, "预发布")
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
                self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
                self.common.closeactivity_switchserver(self.luadriver, "预发布")
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        time.sleep(3)
        self.start_step("将银币存入保险箱")
        self.safebox_page.wait_element("银币保险箱").click()
        self.safebox_page.wait_element("存入").click()
        time.sleep(3)
        self.start_step("将银币存入保险箱")
        self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
        self.safebox_page.wait_element('确定---保险箱').click()
        self.safebox_page.screenshot('safebox1.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata=test_datas.logindata4
@dataprovider.DataDrive(testdata)
class C31046_DFQP_Safebox(TestCase):
    '''
    保险箱银币数为0时取款
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        global UserID
        UserID = self.casedata.get('mid2')
        print 'UserID:%s' % UserID
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
        i = 0
        while i < 3:
            i += 1
            try:
                self.personinfo_page.wait_element("关闭").click()
            except:
                print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入保险箱")
        self.hall_page.wait_element('保险箱').click()
        self.safebox_page.wait_element("取出").click()
        Safebox_info = PHPInterface.get_safebox(UserID)
        coin_saving = Safebox_info.get('safebox')
        if coin_saving > 0:
            self.start_step("将银币取出保险箱")
            self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
            self.safebox_page.wait_element('确定---保险箱').click()
            time.sleep(3)
        user_info = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        if coin > 20000:
            AddMoney =10000 - coin
            PHPInterface.add_money(UserID, AddMoney)
            self.luadriver.keyevent(4)
            self.common.closeactivity_switchserver(self.luadriver, "预发布")
            self.hall_page.wait_element('保险箱').click()
            self.safebox_page.wait_element("取出").click()
        self.safebox_page.screenshot('safebox1.png')
        self.safebox_page.wait_element("存入").click()
        time.sleep(1)
        self.safebox_page.screenshot('safebox2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata=test_datas.logindata4
@dataprovider.DataDrive(testdata)
class C31047_DFQP_Safebox(TestCase):
    '''
    保险箱银币不为0时取款
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        UserID = self.casedata.get('mid2')
        print 'UserID:%s' % UserID
        user_info = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = json.loads(user_info).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 40000 - coin
        PHPInterface.add_money(UserID, AddMoney)  # 将银币值设为40000
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
        i = 0
        while i < 3:
            i += 1
            try:
                self.personinfo_page.wait_element("关闭").click()
            except:
                print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入保险箱")
        self.hall_page.wait_element("保险箱").click()
        self.safebox_page.wait_element("存入").click()
        time.sleep(2)
        self.start_step("将银币存入保险箱")
        self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(3)
        self.safebox_page.screenshot('1.png')
        self.start_step("将银币取出保险箱")
        self.safebox_page.wait_element("取出").click()
        self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
        self.safebox_page.screenshot('2.png')
        self.safebox_page.wait_element('确定---保险箱').click()
        self.safebox_page.screenshot('3.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata = test_datas.logindata4
@dataprovider.DataDrive(testdata)
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
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        global UserID
        UserID = self.casedata.get('mid2')
        print 'UserID:%s' % UserID
        PHPInterface.add_crystal(UserID,100)
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
        i = 0
        while i < 3:
            i += 1
            try:
                self.personinfo_page.wait_element("关闭").click()
            except:
                print "已关闭窗口"


    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.start_step("将金条存入保险箱")
        self.safebox_page.wait_element("金条保险箱").click()
        self.safebox_page.wait_element("存入").click()
        self.safebox_page.screenshot("safebox.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata = test_datas.logindata4
@dataprovider.DataDrive(testdata)
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
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        UserID = self.casedata.get('mid2')
        print 'UserID:%s' % UserID
        PHPInterface.add_crystal(UserID,300)
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
        i = 0
        while i < 3:
            i += 1
            try:
                self.personinfo_page.wait_element("关闭").click()
            except:
                print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        time.sleep(3)
        self.start_step("将金条存入保险箱")
        self.safebox_page.wait_element("金条保险箱").click()
        self.safebox_page.wait_element("存入").click()
        time.sleep(3)
        self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(3)
        self.safebox_page.screenshot('safebox1.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata = test_datas.logindata4
@dataprovider.DataDrive(testdata)
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
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
        i = 0
        while i < 3:
            i += 1
            try:
                self.personinfo_page.wait_element("关闭").click()
            except:
                print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入保险箱")
        self.hall_page.wait_element('保险箱').click()
        self.safebox_page.wait_element('金条保险箱').click()
        self.safebox_page.wait_element("取出").click()
        Safebox_info = PHPInterface.get_safebox(UserID)
        crystal_saving = Safebox_info.get('crystalsafebox')
        if crystal_saving > 0:
            self.start_step("将金条取出保险箱")
            self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
            self.safebox_page.wait_element('确定---保险箱').click()
            time.sleep(3)
        user_info = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        crystal = json.loads(user_info).get('result', {'crystal': None}).get('crystal')  # 获取当前金条值
        if crystal > 200:
            AddMoney = 100 - crystal
            PHPInterface.add_money(UserID, AddMoney)
            self.luadriver.keyevent(4)
            self.common.closeactivity_switchserver(self.luadriver, "预发布")
            self.hall_page.wait_element('保险箱').click()
            self.safebox_page.wait_element("取出").click()
        self.safebox_page.screenshot('1.png')
        self.safebox_page.wait_element("存入").click()
        time.sleep(1)
        self.safebox_page.screenshot('2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()

testdata = test_datas.logindata4
@dataprovider.DataDrive(testdata)
class C31048_DFQP_Safebox4(TestCase):
    '''
    保险箱金币不为0时取款
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        UserID = self.casedata.get('mid2')
        print 'UserID:%s' % UserID
        PHPInterface.add_crystal(UserID, 400)
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user2'], self.casedata['password2'])
        i = 0
        while i < 3:
            i += 1
            try:
                self.personinfo_page.wait_element("关闭").click()
            except:
                print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.hall_page.wait_element('保险箱').click()
        self.safebox_page.wait_element('金条保险箱').click()
        self.safebox_page.wait_element("存入").click()
        time.sleep(3)
        self.start_step("将金条存入保险箱")
        self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(3)
        self.safebox_page.screenshot('1.png')
        self.start_step("将金条取出保险箱")
        self.safebox_page.wait_element('取出').click()
        self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
        self.safebox_page.screenshot('2.png')
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(3)
        self.safebox_page.screenshot('3.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.deletefile(self.luadriver)
        self.common.closedriver()


# __qtaf_seq_tests__ = [C30964_DFQP_BuSign]
if __name__ == '__main__':
    C31045_DFQP_safebox1 = C31046_DFQP_Safebox()
    C31045_DFQP_safebox1.debug_run()
    #debug_run_all()




