#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
选场界面展示
'''
import json
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.game_page import Game_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.setting_page import Setting_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common
from common import Interface as PHPInterface

class C27342_Gamelist_Broadcast(TestCase):
    '''
    有广播时选场界面广播条展示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.setting_page = Setting_Page()
        self.personinfo_page = Personinfo_Page()
        global user_info,MID
        user_info = self.common.get_user()
        self.log_info("userinfo:%s" %user_info)
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动页面")
        self.common.closeactivity(self.luadriver)
        self.start_step("登陆")
        self.hall_page.wait_element("头像").click()
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()
        MID = self.common.get_mid()
        PHPInterface.set_level(MID, 16)
        self.common.set_coin(MID, 100000)  # 将银币值设为100000
        self.common.switchserver()
        self.common.closeActivityBtn()

    def broadcast(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                if (self.game_page.element_is_exist("广播") == True):
                    self.log_info("游戏ID：%s 存在广播按钮" % game_list[i].get_attribute("name"))
                    self.game_page.wait_element("广播").click()
                    self.game_page.wait_element('输入文字').send_keys('11')
                    self.start_step('点击发送')
                    self.game_page.wait_element('发送').click()
                    time.sleep(1)
                    self.game_page.screenshot("%s_broadcast.png" % game_list[i].get_attribute("name"))
                    self.game_page.wait_element("返回1").click()
                else:
                    self.log_info("游戏ID：%s 不存在广播按钮" % game_list[i].get_attribute("name"))
            except:
                try:
                    self.hall_page.wait_element("关闭").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.game_page.wait_element("返回1").click()
            except:
                self.log_info("未找到元素")
            if is_next == True:
                self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                try:
                    self.game_page.wait_element("右三角标").click()
                except:
                    self.log_info("右三角标不存在")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.broadcast()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.broadcast(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        try:
            self.common.deletefile(self.luadriver)
            self.common.recover_user(MID)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['user'])

class C27343_Gamelist_Sendbroadcast(TestCase):
    '''
    	有广播时选场界面发送广播
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.setting_page = Setting_Page()
        self.personinfo_page = Personinfo_Page()
        global user_info,MID
        user_info = self.common.get_user()
        self.log_info("userinfo:%s" %user_info)
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动页面")
        self.common.closeactivity(self.luadriver)
        self.start_step("登陆")
        self.hall_page.wait_element("头像").click()
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()
        MID = self.common.get_mid()
        PHPInterface.set_level(MID, 16)
        user_info1 = PHPInterface.get_user_info(MID)  # 获取玩家信息
        coin = json.loads(user_info1).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        AddMoney = 100000 - coin
        PHPInterface.add_money(MID, AddMoney)  # 将银币值设为100000
        self.common.switchserver()
        self.common.closeActivityBtn()

    def send_broadcast(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                if (self.game_page.element_is_exist("广播") == True):
                    self.log_info("游戏ID：%s 存在广播按钮" % game_list[i].get_attribute("name"))
                    self.game_page.wait_element("广播").click()
                    self.game_page.wait_element('输入文字').send_keys('11')
                    self.start_step('点击发送')
                    self.game_page.wait_element('发送').click()
                    time.sleep(1)
                    self.game_page.screenshot("%s_broadcast.png" % game_list[i].get_attribute("name"))
                    self.game_page.wait_element("返回1").click()
                else:
                    self.log_info("游戏ID：%s 不存在广播按钮" % game_list[i].get_attribute("name"))
            except:
                try:
                    self.hall_page.wait_element("关闭").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.game_page.wait_element("返回1").click()
            except:
                self.log_info("未找到元素")
            if is_next == True:
                self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                try:
                    self.game_page.wait_element("右三角标").click()
                except:
                    self.log_info("右三角标不存在")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.send_broadcast()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.send_broadcast(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        try:
            self.common.recover_user(MID)
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['user'])

# __qtaf_seq_tests__ = [C27342_Gamelist_Broadcast]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
