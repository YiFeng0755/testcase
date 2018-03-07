#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
金条兑换
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
from uilib.safebox_page import Safebox_Page
from common.common import Common
from common import Interface as PHPInterface
from common import user_util

class C31064_DFQP_Exchange_gold1(TestCase):
    '''
    金条兑换
    银币大于20w,金条兑换入口显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        self.start_step("设置银币大于20w")
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        dict = PHPInterface.get_user_info(user_info.get('mid'))  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 200001 - coin
        print AddMoney
        PHPInterface.add_money(user_info.get('mid'), AddMoney)  # 将银币值设为60000
        print PHPInterface.get_user_info(user_info.get('mid'))
        self.hall_page = Hall_Page()
        self.exchange_page = Exchange_Page()
        self.personinfo_page = Personinfo_Page()
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(user_info['user'], user_info['password'])
            self.common.closeActivityBtn()
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != user_info['cid']:
                self.common.loginuser(user_info['user'], user_info['password'])
                self.common.closeActivityBtn()
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入金条兑换界面")
        self.exchange_page.wait_element("换金条").click()
        time.sleep(3)
        self.exchange_page.wait_element("确定兑换")
        self.exchange_page.screenshot("Exchange_gold1.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['mid'])

class C31063_DFQP_Exchange_gold2(TestCase):
    '''
    金条兑换
    银币少于20w,金条兑换入口不显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        self.start_step("设置银币小于20w")
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        dict = PHPInterface.get_user_info(user_info.get('mid'))  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 190000 - int(coin)
        print AddMoney
        PHPInterface.add_money(user_info.get('mid'), AddMoney)  # 将设置银币值
        print PHPInterface.get_user_info(user_info.get('mid'))
        self.hall_page = Hall_Page()
        self.exchange_page = Exchange_Page()
        self.personinfo_page = Personinfo_Page()
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(user_info['user'], user_info['password'])
            self.common.closeActivityBtn()
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != user_info['cid']:
                self.common.loginuser(user_info['user'], user_info['password'])
                self.common.closeActivityBtn()
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入金条兑换界面")
        time.sleep(3)
        try:
            self.exchange_page.is_exist("换金条")
        except:
            return True
        time.sleep(3)
        self.exchange_page.screenshot("Exchange_gold2.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['mid'])

class C31065_DFQP_Exchange_GoldDisplay(TestCase):
    '''
    金条兑换,界面显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        self.start_step("设置银币大于20w")
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        dict = PHPInterface.get_user_info(user_info.get('mid'))  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 200001 - int(coin)
        print AddMoney
        PHPInterface.add_money(user_info.get('mid'), AddMoney)  # 将设置银币值
        print PHPInterface.get_user_info(user_info.get('mid'))
        self.hall_page = Hall_Page()
        self.exchange_page = Exchange_Page()
        self.personinfo_page = Personinfo_Page()
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(user_info['user'], user_info['password'])
            self.common.closeActivityBtn()
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != user_info['cid']:
                self.common.loginuser(user_info['user'], user_info['password'])
                self.common.closeActivityBtn()
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入金条兑换界面")
        time.sleep(3)
        self.exchange_page.wait_element("换金条").click()
        time.sleep(3)
        self.exchange_page.screenshot("GoldDisplay.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['mid'])

class C31066_DFQP_Exchange_Gold_Exchange(TestCase):
    '''
    携带银币不足兑换
    总银币大于20w，携带银币小于103000
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 8
    def pre_test(self):
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        self.start_step("设置银币大于20w")
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        dict = PHPInterface.get_user_info(user_info.get('mid'))  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 200001 - int(coin)
        print AddMoney
        PHPInterface.add_money(user_info.get('mid'), AddMoney)  # 将设置银币值
        print PHPInterface.get_user_info(user_info.get('mid'))
        self.hall_page = Hall_Page()
        self.exchange_page = Exchange_Page()
        self.safebox_page = Safebox_Page()
        self.personinfo_page = Personinfo_Page()
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动，并切换到测试服")
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(user_info['user'], user_info['password'])
            self.common.closeActivityBtn()
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != user_info['cid']:
                self.common.loginuser(user_info['user'], user_info['password'])
                self.common.closeActivityBtn()
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
        self.start_step("进入保险箱")
        self.safebox_page.wait_element("银币").click()
        self.safebox_page.wait_element("存入").click()
        time.sleep(3)
        self.start_step("将银币存入保险箱")
        self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(5)
        self.luadriver.keyevent(4)
        self.start_step("进入金条兑换界面")
        time.sleep(3)
        self.exchange_page.wait_element("换金条").click()
        time.sleep(3)
        self.exchange_page.screenshot("Gold_Exchange.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.luadriver.keyevent(4)
            self.start_step("将银币取出")
            self.hall_page.wait_element('保险箱').click()
            time.sleep(3)
            self.start_step("将银币存入保险箱")
            self.safebox_page.wait_element("银币").click()
            self.safebox_page.wait_element("取出").click()
            time.sleep(3)
            self.start_step("将银币取出保险箱")
            self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
            self.safebox_page.wait_element('确定---保险箱').click()
            time.sleep(6)
        except:
            self.log_info("将银币取出保险箱失败")
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['mid'])

class C31067_DFQP_Exchange_Gold_Exchange1(TestCase):
    '''
    携带银币充足兑换
    总银币大于20w，携带银币大于103000
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 8
    def pre_test(self):
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        self.start_step("设置银币大于20w")
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        dict = PHPInterface.get_user_info(user_info.get('mid'))  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 200001 - int(coin)
        print AddMoney
        PHPInterface.add_money(user_info.get('mid'), AddMoney)  # 将设置银币值
        print PHPInterface.get_user_info(user_info.get('mid'))
        self.hall_page = Hall_Page()
        self.exchange_page = Exchange_Page()
        self.safebox_page = Safebox_Page()
        self.personinfo_page = Personinfo_Page()
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(user_info['user'], user_info['password'])
            self.common.closeActivityBtn()
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != user_info['cid']:
                self.common.loginuser(user_info['user'], user_info['password'])
                self.common.closeActivityBtn()
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
        self.safebox_page.wait_element("银币").click()
        self.safebox_page.wait_element("存入").click()
        time.sleep(3)
        self.start_step("将银币存入保险箱")
        element1 = self.safebox_page.wait_element("滚动条")
        element2 = self.safebox_page.wait_element("增加金条/银条数目")
        swipe_startx = element1.location['x']
        swipe_starty = element1.location['y']
        swipe_endx = element2.location['x']
        swipe_endy = element2.location['y']
        print swipe_startx, swipe_starty, swipe_endx, swipe_endy,swipe_endx
        self.luadriver.swipe(swipe_startx, swipe_starty, swipe_startx+(swipe_endx-swipe_startx)/2, swipe_endy, 1000)
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(5)
        self.luadriver.keyevent(4)
        self.start_step("进入金条兑换界面")
        time.sleep(3)
        self.exchange_page.wait_element("换金条").click()
        time.sleep(3)
        self.exchange_page.screenshot("Gold_Exchange1.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.luadriver.keyevent(4)
            self.start_step("将银币取出")
            # self.hall_page.wait_element('保险箱').click()
            time.sleep(3)
            self.hall_page.wait_element('保险箱').click()
            time.sleep(3)
            self.start_step("进入保险箱")
            self.safebox_page.wait_element("银币").click()
            self.safebox_page.wait_element("取出").click()
            time.sleep(3)
            self.start_step("将银币取出保险箱")
            self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
            self.safebox_page.wait_element('确定---保险箱').click()
            time.sleep(6)
        except:
            self.log_info("将银币取出保险箱失败")
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['mid'])

class C31068_DFQP_Exchange_Gold_Exchange2(TestCase):
    '''
    成功兑换金条
    总银币大于20w，携带银币大于103000
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 8
    def pre_test(self):
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        self.start_step("设置银币大于20w")
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        dict = PHPInterface.get_user_info(user_info.get('mid'))  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 200001 - int(coin)
        print AddMoney
        PHPInterface.add_money(user_info.get('mid'), AddMoney)  # 将设置银币值
        print PHPInterface.get_user_info(user_info.get('mid'))
        self.hall_page = Hall_Page()
        self.exchange_page = Exchange_Page()
        self.safebox_page = Safebox_Page()
        self.personinfo_page = Personinfo_Page()
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动，并切换到预发布")
        self.common.closeactivity_switchserver(self.luadriver,"预发布")
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(user_info['user'], user_info['password'])
            self.common.closeActivityBtn()
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != user_info['cid']:
                self.common.loginuser(user_info['user'], user_info['password'])
                self.common.closeActivityBtn()
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
        self.safebox_page.wait_element("银币").click()
        self.safebox_page.wait_element("存入").click()
        time.sleep(3)
        self.start_step("将银币存入保险箱")
        element1 = self.safebox_page.wait_element("滚动条")
        element2 = self.safebox_page.wait_element("增加金条/银条数目")
        swipe_startx = element1.location['x']
        swipe_starty = element1.location['y']
        swipe_endx = element2.location['x']
        swipe_endy = element2.location['y']
        print swipe_startx, swipe_starty, swipe_endx, swipe_endy,swipe_endx
        self.luadriver.swipe(swipe_startx, swipe_starty, swipe_startx+(swipe_endx-swipe_startx)/2, swipe_endy, 1000)
        self.safebox_page.wait_element('确定---保险箱').click()
        time.sleep(5)
        self.luadriver.keyevent(4)
        self.start_step("进入金条兑换界面")
        time.sleep(3)
        dict = PHPInterface.get_user_info(user_info.get('mid'))  # 获取玩家信息
        crystal = eval(dict).get('result', {'crystal': None}).get('crystal')  # 获取当前金币
        self.exchange_page.wait_element("换金条").click()
        time.sleep(3)
        self.exchange_page.wait_element("确定兑换").click()
        time.sleep(2)
        self.exchange_page.screenshot("Gold_Exchange1.png")
        dict1 = PHPInterface.get_user_info(user_info.get('mid'))  # 获取玩家信息
        crystal1 = eval(dict1).get('result', {'crystal': None}).get('crystal')  # 获取当前金币
        self.assert_equal(True,crystal+200,crystal1)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.luadriver.keyevent(4)
            self.start_step("将银币取出")
            self.hall_page.wait_element('保险箱').click()
            time.sleep(3)
            self.start_step("进入保险箱")
            self.safebox_page.wait_element("银币").click()
            self.safebox_page.wait_element("取出").click()
            time.sleep(3)
            self.start_step("将银币取出保险箱")
            self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
            self.safebox_page.wait_element('确定---保险箱').click()
            time.sleep(6)
        except:
            self.log_info("将银币取出保险箱失败")
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['mid'])

class C31069_DFQP_Exchange_Gold_Exchange3(TestCase):
    '''
    成功兑换金条
    总银币大于20w，携带银币等于103000
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 8

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        global user_info
        user_info = self.common.get_user()
        print user_info
        self.start_step("设置银币大于20w")
        dict = PHPInterface.get_user_info(user_info.get('mid'))  # 获取玩家信息
        # dict = PHPInterface.get_user_info(2182942)  # 获取玩家信息
        print dict
        # PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 200001 - int(coin)
        print AddMoney
        PHPInterface.add_money(user_info.get('mid'), AddMoney)  # 将设置银币值
        print PHPInterface.get_user_info(user_info.get('mid'))
        self.hall_page = Hall_Page()
        self.exchange_page = Exchange_Page()
        self.safebox_page = Safebox_Page()
        self.personinfo_page = Personinfo_Page()
        self.start_step("关闭活动，并切换到测试服")
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.start_step("判断是否登陆")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(user_info['user'], user_info['password'])
            self.common.closeActivityBtn()
        else:
            if self.personinfo_page.wait_element("账号ID").get_attribute('text') != user_info['cid']:
                self.common.loginuser(user_info['user'], user_info['password'])
                self.common.closeActivityBtn()
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
        time.sleep(5)
        self.luadriver.keyevent(4)
        self.start_step("进入金条兑换界面")
        time.sleep(3)
        dict = PHPInterface.get_user_info(user_info.get('mid'))  # 获取玩家信息
        crystal = eval(dict).get('result', {'crystal': None}).get('crystal')  # 获取当前金币
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 103000 - int(coin)
        print AddMoney
        PHPInterface.add_money(user_info.get('mid'), AddMoney)  # 将设置银币值
        dict = PHPInterface.get_user_info(user_info.get('mid'))  # 获取玩家信息
        coin = eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.exchange_page.wait_element("换金条").click()
        time.sleep(3)
        self.exchange_page.wait_element("确定兑换").click()
        time.sleep(2)
        self.exchange_page.screenshot("Gold_Exchange1.png")
        dict1 = PHPInterface.get_user_info(user_info.get('mid'))  # 获取玩家信息
        crystal1 = eval(dict1).get('result', {'crystal': None}).get('crystal')  # 获取当前金币
        self.assert_equal(True, crystal + 200, crystal1)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            self.luadriver.keyevent(4)
            self.start_step("将银币取出")
            self.hall_page.wait_element('保险箱').click()
            time.sleep(3)
            self.start_step("进入保险箱")
            self.safebox_page.wait_element("银币").click()
            self.safebox_page.wait_element("取出").click()
            time.sleep(3)
            self.start_step("将银币取出保险箱")
            self.common.swipeelement(self.safebox_page.wait_element("滚动条"), self.safebox_page.wait_element("增加金条/银条数目"))
            self.safebox_page.wait_element('确定---保险箱').click()
            time.sleep(6)
        except:
            self.log_info("将银币取出保险箱失败")
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['mid'])


__qtaf_seq_tests__ = [C31069_DFQP_Exchange_Gold_Exchange3]
if __name__ == '__main__':
    # C027_DFQP_PersonInfo_NicknameAlter = C027_DFQP_PersonInfo_NicknameAlter()
    # C027_DFQP_PersonInfo_NicknameAlter.debug_run()
    debug_run_all()
