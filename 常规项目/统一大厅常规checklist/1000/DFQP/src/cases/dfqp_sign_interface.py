#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌每日签到测试
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from appiumcenter.luadriver import LuaDriver
from uilib.personinfo_page import Personinfo_Page
from uilib.hall_page import Hall_Page
from uilib.sign_page import Sign_Page
from uilib.exchange_page import Exchange_Page
from common.common import Common
from common import Interface as PHPInterface
import re
import test_datas
from datacenter import dataprovider
testdata=test_datas.logindata4
@dataprovider.DataDrive(testdata)
class C230_DFQP_Sign(TestCase):
    '''
    无补签卡，点击补签按钮购买补签卡
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        global UserID
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 60000 - coin
        PHPInterface.add_money(UserID, AddMoney)  # 将银币值设为60000
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.common.closefloatBall()
        self.start_step('进入任务界面')
        self.hall_page.wait_element('任务').click()
        self.start_step('进入每日签到界面')
        self.sign_page.wait_element('每日签到页面').click()
        List = self.sign_page.wait_element('补签卡数量').get_attribute('text')
        print List
        buSignupNum = re.findall(r'\d+', List)
        AddNum = int(buSignupNum[0])
        if int(buSignupNum[0]) > 0:
            PHPInterface.set_sign_card(UserID,-1,AddNum)#如果事先有补签卡，则先删除所有补签卡
            self.common.closeactivitytest(self.luadriver)
            self.start_step('进入任务界面')
            self.hall_page.wait_element('任务').click()
            self.start_step('进入每日签到界面')
            self.sign_page.wait_element('每日签到页面').click()
        self.start_step('点击获取按钮')
        self.sign_page.wait_element('获取').click()
        self.start_step('点击购买')
        self.sign_page.wait_element('购买').click()
        self.personinfo_page.screenshot('.png')
        List = self.sign_page.wait_element('补签卡数量').get_attribute('text')
        print List
        buSignupNum = re.findall(r'\d+', List)
        if buSignupNum == ['1']:
            print '补签卡成功购买到账'
        else:
            print '补签卡未能成功购买到账'
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        if coin == 10000:
            print '50000银币扣除'

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C231_DFQP_Sign(TestCase):
    '''
    有补签卡，每日签到界面点击补签按钮补签
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        PHPInterface.set_sign_card(UserID,1,1)  # 后台添加一张补签卡
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        #关闭悬浮球
        self.common.closefloatBall()
        self.start_step('进入任务界面')
        self.hall_page.wait_element('任务').click()
        self.start_step('进入每日签到界面')
        self.sign_page.wait_element('每日签到页面').click()
        try:
            self.sign_page.wait_element('补签').click()
            self.start_step('进入补签页面')
        except:
            print '已签过到'
        for i in range(1, 37):  # 轮询查找[补]按钮，找到便break循环
            element = self.luadriver.find_lua_element_by_xpath('//element/element/taskRewardLayout/content/dayRewardView/buSignupView/calendarView/element/element/dayCalendarItem/bu[%d]' % i)
            element_name = element.get_attribute('name')
            if element_name == 'bu':
                element.click()
                print '找到并点击了[补]按钮'
                try:
                    self.sign_page.wait_element('确定补签').click()
                    self.personinfo_page.screenshot('.png')
                except:
                    print '已补签过'
                    element.click()
                    self.personinfo_page.screenshot('.png')
                break
            else:
                print '继续查找[补]按钮'


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C232_DFQP_Sign(TestCase):
    '''
    有2张补签卡，每日签到界面点击2次【补】按钮
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        PHPInterface.set_sign_card(UserID,1,2)  # 后台添加两张补签卡
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        # 关闭悬浮球
        self.common.closefloatBall()
        self.start_step('进入任务界面')
        self.hall_page.wait_element('任务').click()
        self.start_step('进入每日签到界面')
        self.sign_page.wait_element('每日签到页面').click()
        try:
            self.sign_page.wait_element('补签').click()
            self.start_step('进入补签页面')
        except:
            print '已签过到'
        self.start_step('第一次点击[补]开始补签')
        for i in range(1, 37):  # 轮询查找[补]按钮，找到便break循环
            element = self.luadriver.find_lua_element_by_xpath( '//element/element/taskRewardLayout/content/dayRewardView/buSignupView/calendarView/element/element/dayCalendarItem/bu[%d]' % i)
            element_name = element.get_attribute('name')
            if element_name =='bu':
                element.click()
                print '找到并点击了[补]按钮'
                try:
                    self.sign_page.wait_element('确定补签').click()
                except:
                    print '已补签过'
                break
            else:
                print '继续查找[补]按钮'
        self.start_step('第二次点击[补]开始补签')
        for i in range(1, 37):  # 轮询查找[补]按钮，找到便break循环
            element = self.luadriver.find_lua_element_by_xpath( '//element/element/taskRewardLayout/content/dayRewardView/buSignupView/calendarView/element/element/dayCalendarItem/bu[%d]' % i)
            element_name = element.get_attribute('name')
            if element_name =='bu':
                element.click()
                self.personinfo_page.screenshot('.png')
                print '找到并点击了[补]按钮'
                try:
                    self.sign_page.wait_element('确定补签').click()
                except:
                    print '已补签过'
                break
            else:
                print '继续查找[补]按钮'


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C233_DFQP_Sign(TestCase):
    '''
    VIP用户打开每日签到界面领，签到领取银币
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        global UserID
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        PHPInterface.set_vip(UserID, 4)  # 设置用户为vip
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        dict = PHPInterface.get_user_info(UserID) #获取用户信息
        coin = eval(dict).get('result',{'coin':None}).get('coin')
        print '签到前银币：'+ str(coin)
        # 关闭悬浮球
        self.common.closefloatBall()
        self.start_step('进入任务界面')
        self.hall_page.wait_element('任务').click()
        self.start_step('进入每日签到界面')
        self.sign_page.wait_element('每日签到页面').click()
        self.start_step('进入每日签到页面开始签到')
        try:
            self.sign_page.wait_element('签到').click()
        except:
            print '已签到过'
        self.personinfo_page.screenshot('.png')
        time.sleep(5)
        dict1 = PHPInterface.get_user_info(UserID)  # 获取用户信息
        coin1 = eval(dict1).get('result', {'coin': None}).get('coin')
        print '签到后银币：' + str(coin1)
        if coin1 == coin + 1000:
            print 'vip用户签到获得1000银币'
        else:
            print 'vip用户签到没有获得1000银币'


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

if __name__ == '__main__':
    C230_DFQP_Exchange = C233_DFQP_Sign()
    C230_DFQP_Exchange.debug_run()


