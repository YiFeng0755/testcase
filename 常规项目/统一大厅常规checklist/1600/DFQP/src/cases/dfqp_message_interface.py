#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
消息（私信）
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.message_page import Message_Page
from uilib.hall_page import Hall_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.backpack_page import Backpack_Page
from common.common import Common
import common.Interface as PHPInterface
import test_datas
from datacenter import dataprovider


class C61017_DFQP_Message_Display1(TestCase):
    '''
    消息界面展示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        print user_info['mid']
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("接口发送vip私信")
        # 每个用例都需要关闭活动，并切换到预发布
        self.common.closeactivity_switchserver(self.luadriver)
        return1 = PHPInterface.send_message(int(user_info['mid']), "接口发送vip私信","接口发送vip私信",4,1,0)
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
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(3)
        self.start_step("查看消息")
        self.hall_page.screenshot('message_display.png')


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

class C31026_DFQP_Message_Calls(TestCase):
    '''
    话费碎片私信
    后台配置话费碎片发送私信给玩家，查看私信图标显示并点击领取道具查看动画和背包到账情况
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        print user_info['mid']
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("接口发送话费碎片私信")
        # 每个用例都需要关闭活动，并切换到预发布
        self.common.closeactivity_switchserver(self.luadriver)
        return1 = PHPInterface.send_message(int(user_info['mid']), "接口发送话费碎片私信1","接口发送话费碎片私信1",400003,1,0)
        print return1
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
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看物品箱")
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('getcalls_Backpack.png')
        self.luadriver.keyevent(4)
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看消息")
        try:
            try:
                element = self.message_page.get_elements("小琪妹")
                element[1].click()
            except:
                self.message_page.wait_element("小琪妹").click()
            time.sleep(3)

            self.message_page.screenshot('getcalls1.png')
            self.message_page.wait_element("立即领取").click()
            time.sleep(3)
            self.message_page.screenshot('getcalls2.png')
            self.message_page.wait_element("知道了").click()
            time.sleep(2)
            self.message_page.wait_element('已领取').get_attribute('text') == "已领取"
        except:
            print ("没有消息")
        time.sleep(3)
        self.message_page.wait_element("返回").click()
        self.hall_page.wait_element("头像").click()
        self.hall_page.wait_element("同步标志")
        self.start_step("查看物品箱")
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('getcalls_Backpack2.png')

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


class C31027_DFQP_Message_VIP(TestCase):
    '''
    vip私信
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        print user_info['mid']
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("接口发送vip私信")
        # 每个用例都需要关闭活动，并切换到预发布
        self.common.closeactivity_switchserver(self.luadriver)
        return1 = PHPInterface.send_message(int(user_info['mid']), "接口发送vip私信","接口发送vip私信",4,1,0)
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
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看消息")
        try:
            try:
                element = self.message_page.get_elements("小琪妹")
                element[1].click()
            except:
                self.message_page.wait_element("小琪妹").click()
            time.sleep(3)

            self.message_page.screenshot('getcalls1.png')
            self.message_page.wait_element("立即领取").click()
            time.sleep(3)
            self.message_page.screenshot('getcalls2.png')
            self.message_page.wait_element("知道了").click()
            time.sleep(2)
            self.message_page.wait_element('已领取').get_attribute('text') == "已领取"
        except:
            print ("没有消息")
        time.sleep(3)
        self.message_page.wait_element("返回").click()
        self.hall_page.wait_element("头像").click()
        self.hall_page.wait_element("同步标志")

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


class C31028_DFQP_Message_Interactivity(TestCase):
    '''
    交互道具私信
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        print user_info['mid']
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("接口交互道具私信")
        # 每个用例都需要关闭活动，并切换到预发布
        self.common.closeactivity_switchserver(self.luadriver)
        return1 = PHPInterface.send_message(int(user_info['mid']), "接口交互道具私信","接口交互道具私信",200,1,0)
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
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看消息")
        try:
            try:
                element = self.message_page.get_elements("小琪妹")
                element[1].click()
            except:
                self.message_page.wait_element("小琪妹").click()
            time.sleep(3)

            self.message_page.screenshot('getcalls1.png')
            self.message_page.wait_element("立即领取").click()
            time.sleep(3)
            self.message_page.screenshot('getcalls2.png')
            self.message_page.wait_element("知道了").click()
            time.sleep(2)
            self.message_page.wait_element('已领取').get_attribute('text') == "已领取"
        except:
            print ("没有消息")
        time.sleep(3)
        self.message_page.wait_element("返回").click()
        self.hall_page.wait_element("头像").click()
        self.hall_page.wait_element("同步标志")

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


class C31029_DFQP_Message_Silver(TestCase):
    '''
    银币私信
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        print user_info['mid']
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("交互道具私信")
        dict = PHPInterface.get_user_info(user_info['mid'])  # 获取玩家信息
        global coin
        coin= eval(dict).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        return1 = PHPInterface.send_message(int(user_info['mid']), "交互道具私信","交互道具私信",0,2,0)
        print return1
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.start_step("每个用例都需要关闭活动，并切换到预发布")
        self.common.closeactivity_switchserver(self.luadriver)
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
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.element_is_exist("同步标志")
        self.hall_page.wait_element("同步标志")
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看消息")
        try:
            try:
                element = self.message_page.get_elements("小琪妹")
                element[1].click()
            except:
                self.message_page.wait_element("小琪妹").click()
            time.sleep(3)

            self.message_page.screenshot('getcalls1.png')
            self.start_step("立即领取")
            self.message_page.wait_element("立即领取").click()
            time.sleep(3)
            self.message_page.screenshot('getcalls2.png')
            self.message_page.wait_element("知道了").click()
            time.sleep(2)
            self.message_page.wait_element('已领取').get_attribute('text') == "已领取"
        except:
            print ("没有消息")
        time.sleep(6)
        # self.message_page.wait_element("返回").click()
        # self.hall_page.wait_element("头像").click()
        # self.hall_page.wait_element("同步标志")
        dict1 = PHPInterface.get_user_info(user_info['mid'])  # 获取玩家信息
        coin1 = eval(dict1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin1
        # self.assert_equal(True, coin+2,coin1)

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


class C31030_DFQP_Message_Gold(TestCase):
    '''
    金条私信
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        print user_info['mid']
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("金条私信")
        # 每个用例都需要关闭活动，并切换到预发布
        self.common.closeactivity_switchserver(self.luadriver)
        dict = PHPInterface.get_user_info(user_info['mid'])  # 获取玩家信息
        global crystal
        crystal= eval(dict).get('result', {'crystal': None}).get('crystal')  # 获取当前银币值
        print crystal
        return1 = PHPInterface.send_message(int(user_info['mid']), "金条私信","金条私信",1,1,0)
        print return1
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
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.element_is_exist("同步标志")
        self.hall_page.wait_element("同步标志")
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看消息")
        try:
            try:
                element = self.message_page.get_elements("小琪妹")
                element[1].click()
            except:
                self.message_page.wait_element("小琪妹").click()
            time.sleep(3)

            self.message_page.screenshot('getcalls1.png')
            self.start_step("立即领取")
            self.message_page.wait_element("立即领取").click()
            time.sleep(3)
            self.message_page.screenshot('getcalls2.png')
            self.message_page.wait_element("知道了").click()
            time.sleep(2)
            self.message_page.wait_element('已领取').get_attribute('text') == "已领取"
        except:
            print ("没有消息")
        time.sleep(6)
        # self.message_page.wait_element("返回").click()
        # self.hall_page.wait_element("头像").click()
        # self.hall_page.wait_element("同步标志")
        dict1 = PHPInterface.get_user_info(user_info['mid'])  # 获取玩家信息
        crystal1 = eval(dict1).get('result', {'crystal': None}).get('crystal')  # 获取当前银币值
        print crystal1
        self.assert_equal(True, crystal+1,crystal1)

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

class C31031_DFQP_Message_Object(TestCase):
    '''
    实物私信
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        print user_info['mid']
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("实物私信")
        # 每个用例都需要关闭活动，并切换到预发布
        self.common.closeactivity_switchserver(self.luadriver)
        return1 = PHPInterface.send_message(int(user_info['mid']), "实物私信","实物私信",10045,1,0)
        print return1
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
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看物品箱")
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack.png')
        self.luadriver.keyevent(4)
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看消息")
        try:
            try:
                element = self.message_page.get_elements("小琪妹")
                element[1].click()
            except:
                self.message_page.wait_element("小琪妹").click()
            time.sleep(3)

            self.message_page.screenshot('Object.png')
            self.message_page.wait_element("立即领取").click()
            time.sleep(3)
            self.message_page.screenshot('Object2.png')
            self.message_page.wait_element("知道了").click()
            time.sleep(2)
            self.message_page.wait_element('已领取').get_attribute('text') == "已领取"
        except:
            print ("没有消息")
        time.sleep(6)
        self.message_page.wait_element("返回").click()
        self.hall_page.wait_element("头像").click()
        self.hall_page.wait_element("同步标志")
        self.start_step("查看物品箱")
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack2.png')

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


class C31032_DFQP_Message_Three(TestCase):
    '''
    3种以上物品私信
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        print user_info['mid']
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.message_page = Message_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("3种以上物品私信")
        # 每个用例都需要关闭活动，并切换到预发布
        self.common.closeactivity_switchserver(self.luadriver)
        return1 = PHPInterface.send_message(int(user_info['mid']), "3种以上物品私信","3种以上物品私信",[10045,0,1],1,0)
        print return1
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
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看物品箱")
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack.png')
        self.luadriver.keyevent(4)
        time.sleep(4)
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看消息")
        try:
            try:
                element = self.message_page.get_elements("小琪妹")
                element[1].click()
            except:
                self.message_page.wait_element("小琪妹").click()
            time.sleep(3)

            self.message_page.screenshot('Object.png')
            self.message_page.wait_element("立即领取").click()
            time.sleep(3)
            self.message_page.screenshot('Object2.png')
            self.message_page.wait_element("知道了").click()
            time.sleep(2)
            print self.message_page.wait_element('已领取').get_attribute('text')
            self.message_page.wait_element('已领取').get_attribute('text') == "已领取"
        except:
            print ("没有消息")
        time.sleep(6)
        self.message_page.wait_element("返回").click()
        self.hall_page.wait_element("头像").click()
        self.hall_page.wait_element("同步标志")
        self.start_step("查看物品箱")
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack2.png')

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

# __qtaf_seq_tests__ = [C31029_DFQP_Message_Silver]
if __name__ == '__main__':
    # C002_DFQP_Login_GuestLogin = C002_DFQP_Login_GuestLogin()
    # C002_DFQP_Login_GuestLogin.debug_run()
    debug_run_all()