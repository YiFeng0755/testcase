#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌保险箱测试
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
import re
import test_datas
from datacenter import dataprovider
testdata=test_datas.logindata4
@dataprovider.DataDrive(testdata)
class C234_DFQP_Safebox(TestCase):
    '''
    银币取款操作-玩家持有银币现金小于2w，且保险箱没有钱，点击+-按钮及拖动滚动条，银币数量不改变
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
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
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        Flag = True
        while Flag:  # 将保险箱中的银币存款值置0
            self.safebox_page.wait_element('减少金条/银条数目').click()
            savings = self.safebox_page.wait_element('存款').get_attribute('text')
            if int(savings) == 0:
                self.safebox_page.wait_element('确定---保险箱').click()
                Flag = False
        time.sleep(5)
        UserID = self.casedata.get('mid')
        print 'UserID:%s'%UserID
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        if coin > 20000 or coin < 3000:
            AddMoney = 13000 - coin  # 如果当前银币多于20000或少于3000，则将银币值设置为13000
            PHPInterface.add_money(UserID, AddMoney)
        self.common.closeactivitytest(self.luadriver)#后台修改银币数量不会马上生效，故再次点击测试服按钮更新
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.start_step('获取当前银币值')
        coin = self.safebox_page.wait_element('现金').get_attribute('text')
        print type(coin)
        print '当前银币值：%s'%coin
        self.start_step('点击-按钮')
        self.safebox_page.wait_element('减少金条/银条数目').click()
        self.start_step('获取点击-按钮后的银币值')
        coin1 = self.safebox_page.wait_element('现金').get_attribute('text')
        print '点击-按钮后的银币值：%s'%coin1
        if coin1 == coin:
            print '银币数量未变'
        else:
            print '银币数量改变'
        self.start_step('点击+按钮')
        self.safebox_page.wait_element('增加金条/银条数目').click()
        self.start_step('获取点击+按钮后的银币值')
        coin2 = self.safebox_page.wait_element('现金').get_attribute('text')
        print '点击+按钮后的银币值：%s' % coin2
        if coin2 == coin1:
            print '银币数量未变'
        else:
            print '银币数量改变'
        slider = self.safebox_page.wait_element('滑动条')
        x = slider.location['x']  # slider x坐标
        y = slider.location['y']  # slider y坐标
        d = slider.size['width']
        # slider.swipe(x,y,x+d/2,y)
        self.start_step('点击滚动条')
        self.luadriver.swipe(x+d, y, x , y)
        self.start_step('获取点击滚动条后的银币值')
        coin3 = self.safebox_page.wait_element('现金').get_attribute('text')
        print '点击滚动条后的银币值：%s'%coin3
        if coin3 == coin2:
            print '银币数量未变'
        else:
            print '银币数量改变'
        self.start_step('点击确定')
        self.safebox_page.wait_element('确定---保险箱').click()
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C235_DFQP_Safebox(TestCase):
    '''
    银币取款操作-玩家持有银币现金大于2w，且保险箱没有钱，点击+-按钮及拖动滚动条，银币数量改变
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
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
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        Flag = True
        while Flag:  # 将保险箱中的银币存款值置0
            self.safebox_page.wait_element('减少金条/银条数目').click()
            savings = self.safebox_page.wait_element('存款').get_attribute('text')
            if int(savings) == 0:
                self.safebox_page.wait_element('确定---保险箱').click()
                Flag = False

        time.sleep(5)
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        if coin <= 20000:
            AddMoney = 23000 - coin  # 如果当前银币不多于20000，则将银币值设置为23000
            PHPInterface.add_money(UserID, AddMoney)
        else:
            pass
        self.common.closeactivitytest(self.luadriver)  # 后台修改银币数量不会马上生效，故再次点击测试服按钮更新
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.start_step('获取当前银币值')
        coin = self.safebox_page.wait_element('现金').get_attribute('text')
        print type(coin)
        print '当前银币值：%s'%coin
        self.start_step('点击+按钮')
        self.safebox_page.wait_element('增加金条/银条数目').click()
        self.start_step('获取点击+按钮后的银币值')
        coin1 = self.safebox_page.wait_element('现金').get_attribute('text')
        savings1 = self.safebox_page.wait_element('存款').get_attribute('text')
        print '点击+按钮后的银币值，存款值：%s，%s'%(coin1,savings1)
        if coin1 == coin:
            print '银币数量未变,存款值未变'
        else:
            print '银币数量改变，存款值改变'
        self.start_step('点击-按钮')
        self.safebox_page.wait_element('减少金条/银条数目').click()
        self.start_step('获取点击-按钮后的银币值')
        coin2 = self.safebox_page.wait_element('现金').get_attribute('text')
        savings2 = self.safebox_page.wait_element('存款').get_attribute('text')
        print '点击-按钮后的银币值，存款值：%s，%s'%(coin2,savings2)
        if coin2 == coin1:
            print '银币数量未变,存款值未变'
        else:
            print '银币数量改变，存款值改变'
        slider = self.safebox_page.wait_element('滑动条')
        x = slider.location['x']  # slider x坐标
        y = slider.location['y']  # slider y坐标
        d = slider.size['width']
        # slider.swipe(x,y,x+d/2,y)
        self.start_step('点击滚动条')
        self.luadriver.swipe(x, y, x+d, y)
        self.start_step('获取点击滚动条后的银币值')
        coin3 = self.safebox_page.wait_element('现金').get_attribute('text')
        savings3 = self.safebox_page.wait_element('存款').get_attribute('text')
        print '点击滚动条后的银币值，存款值：%s，%s'%(coin3,savings3)
        if coin3 == coin2:
            print '银币数量未变'
        else:
            print '银币数量改变'
        self.start_step('点击确定')
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(1)
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C236_DFQP_Safebox(TestCase):
    '''
    银币取款操作-保险箱有存款，直接点击确定，银币数量不变
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        if coin <= 20000:
            AddMoney = 23000 - coin  # 如果当前银币不多于20000，则将银币值设置为23000
            PHPInterface.add_money(UserID, AddMoney)
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
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
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.start_step('点击+按钮')
        self.safebox_page.wait_element('增加金条/银条数目').click()#确保有存款
        self.start_step('点击确定')
        self.safebox_page.wait_element('确定---保险箱').click()
        self.hall_page.wait_element('保险箱').click()
        self.start_step('获取当前银币值，存款值')
        coin = self.safebox_page.wait_element('现金').get_attribute('text')
        savings = self.safebox_page.wait_element('存款').get_attribute('text')
        print type(coin)
        print '当前银币值，存款值：%s，%s' % (coin, savings)
        self.start_step('点击确定')
        self.safebox_page.wait_element('确定---保险箱').click()
        self.personinfo_page.screenshot('.png')
        self.start_step('获取点击【确定】后的银币值，存款值')
        coin1 = self.safebox_page.wait_element('现金').get_attribute('text')
        savings1 = self.safebox_page.wait_element('存款').get_attribute('text')
        print '点击【确定】后的银币值，存款值：%s，%s' % (coin1, savings1)
        if coin1 == coin and savings1 == savings:
            print '银币值未变，存款值未变'
        else:
            print '银币值改变，存款值改变'

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C237_DFQP_Safebox(TestCase):
    '''
    金条取款操作-玩家持有金条小于200，且保险箱有钱，点击+-按钮，操作存取款
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        global UserID
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        PHPInterface.add_crystal(UserID,1000)
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
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
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.safebox_page.wait_element('金条-老').click()
        self.safebox_page.wait_element('增加金条/银条数目').click()  # 将保险箱存款+100,确保保险箱有钱
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(5)
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        crystal = eval(dict).get('result', {'crystal': None}).get('crystal')  # 获取当前金条值
        AddCrystal = 190 - crystal
        PHPInterface.add_crystal(UserID, AddCrystal)  # 将金条数目置190
        self.common.closeactivitytest(self.luadriver)
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.safebox_page.wait_element('金条-老').click()
        self.start_step('获取当前金条值，存款值')
        coin = self.safebox_page.wait_element('现金').get_attribute('text')
        savings = self.safebox_page.wait_element('存款').get_attribute('text')
        print type(coin)
        print '当前金条值，存款值：%s，%s' % (coin, savings)
        self.start_step('点击+按钮')
        self.safebox_page.wait_element('增加金条/银条数目').click()
        self.start_step('获取点击+按钮后的金条值')
        coin1 = self.safebox_page.wait_element('现金').get_attribute('text')
        savings1 = self.safebox_page.wait_element('存款').get_attribute('text')
        print '点击+按钮后的金条值，存款值：%s，%s' % (coin1, savings1)
        if coin1 ==coin and savings1 == savings:
            print '金条值未变，存款值未变'
        else:
            print '金条值改变，存款值改变'
        self.start_step('点击-按钮')
        self.safebox_page.wait_element('减少金条/银条数目').click()
        self.start_step('获取点击-按钮后的金条值')
        coin2 = self.safebox_page.wait_element('现金').get_attribute('text')
        savings2 = self.safebox_page.wait_element('存款').get_attribute('text')
        print '点击-按钮后的金条值，存款值：%s，%s' % (coin2, savings2)
        if coin2 == coin1 and savings2 == savings1:
            print '金条值未变，存款值未变'
        else:
            print '金条值改变，存款值改变'
        self.start_step('点击确定')
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(1)
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C238_DFQP_Safebox(TestCase):
    '''
    金条取款操作-玩家持有金条大于200，且保险箱有钱，点击+-按钮，操作存取款
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        PHPInterface.add_crystal(UserID,1000)
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
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
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.safebox_page.wait_element('金条-老').click()
        self.safebox_page.wait_element('增加金条/银条数目').click()  # 将保险箱存款+100
        self.safebox_page.wait_element('确定---保险箱').click()
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.safebox_page.wait_element('金条-老').click()
        self.start_step('获取当前金条值，存款值')
        coin = self.safebox_page.wait_element('现金').get_attribute('text')
        savings = self.safebox_page.wait_element('存款').get_attribute('text')
        print type(coin)
        print '当前金条值，存款值：%s，%s' % (coin, savings)
        self.start_step('点击+按钮')
        self.safebox_page.wait_element('增加金条/银条数目').click()
        self.start_step('获取点击+按钮后的金条值')
        coin1 = self.safebox_page.wait_element('现金').get_attribute('text')
        savings1 = self.safebox_page.wait_element('存款').get_attribute('text')
        print '点击+按钮后的金条值，存款值：%s，%s' % (coin1, savings1)
        if coin1 == coin and savings1 == savings:
            print '金条值未变，存款值未变'
        else:
            print '金条值改变，存款值改变'
        self.start_step('点击-按钮')
        self.safebox_page.wait_element('减少金条/银条数目').click()
        self.start_step('获取点击-按钮后的金条值')
        coin2 = self.safebox_page.wait_element('现金').get_attribute('text')
        savings2 = self.safebox_page.wait_element('存款').get_attribute('text')
        print '点击-按钮后的金条值，存款值：%s，%s' % (coin2, savings2)
        if coin2 == coin1 and savings2 == savings1:
            print '金条值未变，存款值未变'
        else:
            print '金条值改变，存款值改变'
        self.start_step('点击+按钮')
        self.safebox_page.wait_element('增加金条/银条数目').click()
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(1)
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C239_DFQP_Safebox(TestCase):
    '''
    金条取款操作-玩家持有金条小于200，且保险箱没有钱，点击+-按钮，操作存取款
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
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
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.safebox_page.wait_element('金条-老').click()
        Flag = True
        while Flag:  # 将保险箱中的金条存款值置0
            self.safebox_page.wait_element('减少金条/银条数目').click()
            savings = self.safebox_page.wait_element('存款').get_attribute('text')
            if int(savings) == 0:
                self.safebox_page.wait_element('确定---保险箱').click()
                Flag = False

        time.sleep(5)
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        crystal = eval(dict).get('result', {'crystal': None}).get('crystal')  # 获取当前金条值
        AddCrystal = 190- crystal
        PHPInterface.add_crystal(UserID, AddCrystal)  # 将金条数目置190
        self.common.closeactivitytest(self.luadriver)
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.safebox_page.wait_element('金条-老').click()
        self.start_step('获取当前金条值，存款值')
        coin = self.safebox_page.wait_element('现金').get_attribute('text')
        savings = self.safebox_page.wait_element('存款').get_attribute('text')
        print type(coin)
        print '当前金条值，存款值：%s，%s' % (coin, savings)
        self.start_step('点击+按钮')
        self.safebox_page.wait_element('增加金条/银条数目').click()
        self.start_step('获取点击+按钮后的金条值')
        coin1 = self.safebox_page.wait_element('现金').get_attribute('text')
        savings1 = self.safebox_page.wait_element('存款').get_attribute('text')
        print '点击+按钮后的金条值，存款值：%s，%s' % (coin1, savings1)
        if coin1 == coin and savings1 == savings:
            print '金条值未变，存款值未变'
        else:
            print '金条值改变，存款值改变'
        self.start_step('点击-按钮')
        self.safebox_page.wait_element('减少金条/银条数目').click()
        self.start_step('获取点击-按钮后的金条值')
        coin2 = self.safebox_page.wait_element('现金').get_attribute('text')
        savings2 = self.safebox_page.wait_element('存款').get_attribute('text')
        print '点击-按钮后的金条值，存款值：%s，%s' % (coin2, savings2)
        if coin2 == coin1 and savings2 == savings1:
            print '金条值未变，存款值未变'
        else:
            print '金条值改变，存款值改变'
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(1)
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C240_DFQP_Safebox(TestCase):
    '''
    金条取款操作-玩家持有金条大于200，且保险箱没有钱，点击+-按钮，操作存取款
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
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
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.safebox_page.wait_element('金条-老').click()
        Flag = True
        while Flag:  # 将保险箱中的金条存款值置0
            self.safebox_page.wait_element('减少金条/银条数目').click()
            savings = self.safebox_page.wait_element('存款').get_attribute('text')
            if int(savings) == 0:
                self.safebox_page.wait_element('确定---保险箱').click()
                Flag = False

        time.sleep(5)
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        crystal = eval(dict).get('result', {'crystal': None}).get('crystal')  # 获取当前金条值
        AddCrystal = 1000 - crystal
        PHPInterface.add_crystal(UserID, AddCrystal)  # 将金条数目置1000
        self.common.closeactivitytest(self.luadriver)
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.safebox_page.wait_element('金条-老').click()
        self.start_step('获取当前金条值，存款值')
        coin = self.safebox_page.wait_element('现金').get_attribute('text')
        savings = self.safebox_page.wait_element('存款').get_attribute('text')
        print type(coin)
        print '当前金条值，存款值：%s，%s' % (coin, savings)
        self.start_step('点击-按钮')
        self.safebox_page.wait_element('减少金条/银条数目').click()
        self.start_step('获取点击-按钮后的金条值')
        coin1 = self.safebox_page.wait_element('现金').get_attribute('text')
        savings1 = self.safebox_page.wait_element('存款').get_attribute('text')
        print '点击-按钮后的金条值，存款值：%s，%s' % (coin1, savings1)
        if coin1 == coin and savings1 == savings:
            print '金条值未变，存款值未变'
        else:
            print '金条值改变，存款值改变'
        self.start_step('点击+按钮')
        self.safebox_page.wait_element('增加金条/银条数目').click()
        self.start_step('获取点击+按钮后的金条值')
        coin2 = self.safebox_page.wait_element('现金').get_attribute('text')
        savings2 = self.safebox_page.wait_element('存款').get_attribute('text')
        print '点击+按钮后的金条值，存款值：%s，%s' % (coin2, savings2)
        if coin2 == coin1 and savings2 == savings1:
            print '金条值未变，存款值未变'
        else:
            print '金条值改变，存款值改变'
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(1)
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

@dataprovider.DataDrive(testdata)
class C241_DFQP_Safebox(TestCase):
    '''
    金条取款操作-保险箱有金条存款，不操作+-按钮，直接点击确认
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        UserID = self.casedata.get('mid')
        print 'UserID:%s' % UserID
        dict = PHPInterface.get_user_info(UserID)  # 获取玩家信息
        crystal = eval(dict).get('result', {'crystal': None}).get('crystal')  # 获取当前金条值
        AddCrystal = 1000 - crystal
        PHPInterface.add_crystal(UserID, AddCrystal)  # 将金条数目置1000
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
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
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.safebox_page.wait_element('金条-老').click()
        Flag = True
        while Flag:  # 使保险箱中的金条存款不为0
            savings = self.safebox_page.wait_element('存款').get_attribute('text')
            if int(savings) > 0:
                Flag = False
            else:
                self.safebox_page.wait_element('增加金条/银条数目').click()
                self.safebox_page.wait_element('确定---保险箱').click()
        self.start_step('进入保险箱页面')
        self.hall_page.wait_element('保险箱').click()
        self.safebox_page.wait_element('金条-老').click()
        self.safebox_page.wait_element('确定---保险箱').click()
        self.personinfo_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()


















if __name__ == '__main__':
    C234_DFQP_Safebox = C241_DFQP_Safebox()
    C234_DFQP_Safebox.debug_run()





