#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌兑换测试
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from appiumcenter.luadriver import LuaDriver
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.friend_page import Friend_Page
from uilib.exchange_page import Exchange_Page
from uilib.personinfo_page import Personinfo_Page
from common.common import Common
from common import Interface as PHPInterface
import test_datas
from datacenter import dataprovider
testdata=test_datas.logindata4
@dataprovider.DataDrive(testdata)
class C217_DFQP_Exchange(TestCase):
    '''
    玩家钻石不足,点击其中一个商品兑奖
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        diamond = eval(dict).get('result', {'diamond': None}).get('diamond')
        PHPInterface.add_diamond(UserID, 10-diamond)#将账号钻石置为10
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.game_page =Game_Page()
        self.hall_page = Hall_Page()
        self.friend_page = Friend_Page()
        self.exchange_page = Exchange_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入兑换界面")
        self.exchange_page.wait_element('更多').click()
        self.exchange_page.wait_element('兑换').click()
        self.start_step("进入数码家电界面")
        self.exchange_page.wait_element('数码家电').click()
        LeftNum1 = int(self.exchange_page.wait_element('剩余个数1').get_attribute('text').replace('个',''))
        print '兑换前剩余个数：'+str(LeftNum1)
        time.sleep(1)
        self.start_step('点击兑换')
        self.exchange_page.wait_element('兑换1').click()
        UserDiaNum1 = int(self.exchange_page.wait_element('钻石数量').get_attribute('text'))
        if UserDiaNum1 ==10:
            print "兑换失败但钻石未扣除"
        else:
            print "兑换失败但钻石扣除"

        LeftNum2 = int(self.exchange_page.wait_element('剩余个数1').get_attribute('text').replace('个',''))
        print '兑换后剩余个数：'+ str(LeftNum2)
        if LeftNum2 == LeftNum1:
            print '未扣除商品个数'
        else:
            print '扣除了商品个数'
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C218_DFQP_Exchange(TestCase):
    '''
    玩家钻石足够,点击其中一个商品兑奖
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        diamond = eval(dict).get('result', {'diamond': None}).get('diamond')
        PHPInterface.add_diamond(UserID, 400 - diamond)  # 将账号钻石置为400
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.game_page =Game_Page()
        self.hall_page = Hall_Page()
        self.friend_page = Friend_Page()
        self.exchange_page = Exchange_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入兑换界面")
        self.exchange_page.wait_element('更多').click()
        self.exchange_page.wait_element('兑换').click()
        self.start_step("进入数码家电界面")
        self.exchange_page.wait_element('数码家电').click()
        UserDiaNum1 = int(self.exchange_page.wait_element('钻石数量').get_attribute('text'))
        LeftNum1 = int(self.exchange_page.wait_element('剩余个数1').get_attribute('text').replace('个',''))
        print '兑换前钻石数量%s，手机充值卡剩余个数%s'%(UserDiaNum1,LeftNum1)
        time.sleep(1)
        self.start_step('点击兑换')
        self.exchange_page.wait_element('兑换1').click()
        self.exchange_page.wait_element('下一步').click()
        self.exchange_page.wait_element('充值手机号').send_keys(self.casedata['user'])
        time.sleep(1)
        self.exchange_page.wait_element('下一步').click()
        time.sleep(1)
        UserDiaNum2 = int(self.exchange_page.wait_element('钻石数量').get_attribute('text'))
        if UserDiaNum1 == UserDiaNum2 + 110:
            print "兑换成功且钻石扣除正常"
        else:
            print "兑换出现问题"

        LeftNum2 = int(self.exchange_page.wait_element('剩余个数1').get_attribute('text').replace('个',''))
        print '兑换后钻石数量%s，手机充值卡剩余个数%s'%(UserDiaNum2,LeftNum2)
        if LeftNum2 ==LeftNum1-1:
            print '扣除商品个数正常'
        else:
            print '扣除商品个数出现问题'
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C219_DFQP_Exchange(TestCase):
    '''
    兑换的奖品已兑换过，点击商品兑奖
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
        diamond = eval(dict).get('result', {'diamond': None}).get('diamond')
        PHPInterface.add_diamond(UserID, 400 - diamond)  # 将账号钻石置为400
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.game_page =Game_Page()
        self.hall_page = Hall_Page()
        self.friend_page = Friend_Page()
        self.exchange_page = Exchange_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入兑换界面")
        self.exchange_page.wait_element('更多').click()
        self.exchange_page.wait_element('兑换').click()
        self.start_step("进入数码家电界面")
        self.exchange_page.wait_element('数码家电').click()
        UserDiaNum1 = int(self.exchange_page.wait_element('钻石数量').get_attribute('text'))
        LeftNum1 = int(self.exchange_page.wait_element('剩余个数1').get_attribute('text').replace('个', ''))
        print '兑换前钻石数量%s，手机充值卡剩余个数%s' % (UserDiaNum1, LeftNum1)
        self.start_step('点击兑换')
        self.exchange_page.wait_element('兑换1').click()
        self.exchange_page.wait_element('下一步').click()
        try:
            self.exchange_page.wait_element('失败提示')
            text = self.exchange_page.wait_element('失败提示').get_attribute('text')
            print text
        except:
            print '没有失败提示'

        self.exchange_page.wait_element('充值手机号').send_keys(self.casedata['user'])
        time.sleep(1)
        self.exchange_page.wait_element('下一步').click()
        try:
            text = self.exchange_page.wait_element('失败提示').get_attribute('text')
            print text
            print '之前已兑换过'
            self.exchange_page.wait_element('下一步').click()
            self.personinfo_page.screenshot('.png')
        except:
            self.exchange_page.wait_element('关闭').click()
            self.start_step('点击兑换')
            self.exchange_page.wait_element('兑换1').click()
            self.exchange_page.wait_element('下一步').click()
            self.exchange_page.wait_element('充值手机号').send_keys(self.casedata['user'])
            time.sleep(1)
            self.exchange_page.wait_element('下一步').click()
            self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C220_DFQP_Exchange(TestCase):
    '''
    有兑奖记录,点击兑奖记录按钮,查看页面显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.game_page =Game_Page()
        self.hall_page = Hall_Page()
        self.friend_page = Friend_Page()
        self.exchange_page = Exchange_Page()
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
        self.start_step("进入兑换界面")
        self.exchange_page.wait_element("更多").click()
        self.exchange_page.wait_element('兑换').click()
        self.start_step('进入兑奖记录界面')
        self.exchange_page.wait_element('兑换-兑奖记录').click()
        self.personinfo_page.screenshot('.png')
        self.start_step('返回大厅')
        self.exchange_page.wait_element('返回').click()
        try:
            self.exchange_page.wait_element("兑换-兑奖记录")
            print '点击返回键未能成功返回大厅'
        except:
            print '点击返回键后成功返回大厅'

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C221_DFQP_Exchange(TestCase):
    '''
    兑奖记录界面查看详情
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.game_page =Game_Page()
        self.hall_page = Hall_Page()
        self.friend_page = Friend_Page()
        self.exchange_page = Exchange_Page()
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
        self.start_step("进入兑换界面")
        self.exchange_page.wait_element("更多").click()
        self.exchange_page.wait_element('兑换').click()
        self.start_step('进入兑奖记录界面')
        self.exchange_page.wait_element('兑换-兑奖记录').click()
        self.start_step('查看兑奖详情')
        self.exchange_page.wait_element('查看详情').click()
        time.sleep(1)
        self.personinfo_page.screenshot('.png')
        self.start_step('点击确定关闭弹框')
        self.exchange_page.wait_element('确定').click()
        try:
            self.exchange_page.wait_element('单号')
            print '点击确定未能正常关闭弹框'
        except:
            print '点击确定能正常关闭弹框'

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()










if __name__ == '__main__':
    C217_DFQP_Exchange = C221_DFQP_Exchange()
    C217_DFQP_Exchange.debug_run()