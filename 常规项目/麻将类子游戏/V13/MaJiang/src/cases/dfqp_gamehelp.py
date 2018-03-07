#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
游戏帮助
'''
import json
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.sign_page import Sign_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common

global game_list1,game_list2
game_list1 = []
game_list2 = []

class C27028_Gamehelp_display(TestCase):
    '''
    有帮助按钮的场次
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 12
    pending = True
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.sign_page = Sign_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

    def see_rule(self, list, is_next=False):
        game_list = []
        if len(list) == 0:
            self.log_info("重新获取游戏列表")
            game_list0 = self.game_page.get_game_list()
            for i in range(len(game_list0)):
                game_list.append(game_list0[i].get_attribute("name"))
        elif str(list[0]) == "nogame":
            return
        else:
            self.log_info("使用已有的list")
            game_list = list
        print game_list
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i])
            time.sleep(1)
            self.luadriver.find_lua_element_by_name(game_list[i]).click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.sign_page.wait_element("关闭1").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                self.log_info("进入游戏ID：%s 的房间" % game_list[i])
                try:
                    self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i])
                    elements = self.game_page.game_play_way()
                    elements[0][1].click()
                except:
                    self.log_info("当前子游戏初级场")
                self.game_page.wait_element("房间场次").click()
                self.game_page.screenshot("%s.png" % game_list[i])
                if (self.game_page.element_is_exist("规则") == True):
                    if game_list[i] not in list:
                        list.append(game_list[i])
                    self.game_page.wait_element("规则").click()
                    self.log_info("进入游戏ID：%s 的房间,有规则说明" % game_list[i])
                    self.game_page.screenshot("%s_rule.png" % game_list[i])
                    self.luadriver.keyevent(4)
                    time.sleep(2)
                else:
                    self.log_info("游戏ID：%s 的房间无规则说明" % game_list[i])
            except:
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")
        if len(list)==0:
            list.append(u"nogame")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表，是否有规则按钮")
        self.see_rule(game_list1)
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表，是否有规则按钮")
        self.see_rule(game_list2,is_next=True)
        print game_list1
        print game_list2

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C27029_Gamehelp_Locate(TestCase):
    '''
    查看帮助按钮在房间界面中的位置
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 12
    pending = True
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

    def see_rule(self, list, is_next=False):
        game_list = []
        if len(list) == 0:
            self.log_info("重新获取游戏列表")
            game_list0 = self.game_page.get_game_list()
            for i in range(len(game_list0)):
                game_list.append(game_list0[i].get_attribute("name"))
        elif str(list[0]) == "nogame":
            return
        else:
            self.log_info("使用已有的list")
            game_list = list
        print game_list
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i])
            time.sleep(1)
            self.luadriver.find_lua_element_by_name(game_list[i]).click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                try:
                    self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i])
                    elements = self.game_page.game_play_way()
                    elements[0][1].click()
                except:
                    self.log_info("当前子游戏初级场")
                self.log_info("进入游戏ID：%s 的房间" % game_list[i])
                self.game_page.wait_element("房间场次").click()
                self.game_page.screenshot("%s.png" % game_list[i])
                if (self.game_page.element_is_exist("规则") == True):
                    if game_list[i] not in list:
                        list.append(game_list[i])
                    self.game_page.wait_element("规则").click()
                    self.log_info("进入游戏ID：%s 的房间,有规则说明" % game_list[i])
                    self.game_page.screenshot("%s_rule.png" % game_list[i])
                    while self.game_page.element_is_exist("帮助标题"):
                        self.luadriver.keyevent(4)
                        time.sleep(2)
                else:
                    self.log_info("游戏ID：%s 的房间无规则说明" % game_list[i])
            except:
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")
        if len(list)==0:
            list.append(u"nogame")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表，是否有规则按钮")
        self.see_rule(game_list1)
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表，是否有规则按钮")
        self.see_rule(game_list2,is_next=True)
        print game_list1
        print game_list2

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C27030_Gamehelp_Reconnect(TestCase):
    '''
    	游戏过程中重连，帮助按钮不会消失
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 20
    pending = True
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

    def see_rule_reconnect(self, list, is_next=False):
        game_list = []
        if len(list) == 0:
            self.log_info("重新获取游戏列表")
            game_list0 = self.game_page.get_game_list()
            for i in range(len(game_list0)):
                game_list.append(game_list0[i].get_attribute("name"))
        elif str(list[0]) == "nogame":
            return
        else:
            self.log_info("使用已有的list")
            game_list = list
        print game_list
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i])
            time.sleep(1)
            self.luadriver.find_lua_element_by_name(game_list[i]).click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                try:
                    self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i])
                    elements = self.game_page.game_play_way()
                    elements[0][1].click()
                except:
                    self.log_info("当前子游戏初级场")
                self.log_info("进入游戏ID：%s 的房间" % game_list[i])
                self.game_page.wait_element("房间场次").click()
                self.game_page.screenshot("%s.png" % game_list[i])
                if (self.game_page.element_is_exist("规则") == True):
                    if game_list[i] not in list:
                        list.append(game_list[i])
                    self.game_page.wait_element("规则").click()
                    self.log_info("进入游戏ID：%s 的房间,有规则说明" % game_list[i])
                    self.game_page.screenshot("%s_rule.png" % game_list[i])
                    self.luadriver.keyevent(4)
                    self.game_page.wait_element("更多").click()
                    self.hall_page.wait_element("测试按钮").click()
                    self.game_page.wait_element("重连").click()
                    time.sleep(3)
                    self.game_page.wait_element("规则", 30).click()
                    self.game_page.screenshot("%s_rule1.png" % game_list[i])
                    helps = self.game_page.get_elements("帮助列表")
                    for i in range(len(helps)):
                        helps[i].click()
                        time.sleep(1)
                        self.game_page.screenshot("%s_help_%d.png" % (game_list[i], i))
                    self.luadriver.keyevent(4)
                else:
                    self.log_info("游戏ID：%s 的房间无规则说明" % game_list[i])
            except:
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")
        if len(list)==0:
            list.append(u"nogame")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表，是否有规则按钮")
        self.see_rule_reconnect(game_list1)
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表，是否有规则按钮")
        self.see_rule_reconnect(game_list2,is_next=True)
        print game_list1
        print game_list2

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C27031_Gamehelp_Level(TestCase):
    '''
    	帮助面板展开后层级显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    pending = True
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

    def see_rule_display(self, list, is_next=False):
        game_list = []
        if len(list) == 0:
            self.log_info("重新获取游戏列表")
            game_list0 = self.game_page.get_game_list()
            print game_list0
            for i in range(len(game_list0)):
                game_list.append(game_list0[i].get_attribute("name"))
        elif str(list[0]) == "nogame":
            return
        else:
            self.log_info("使用已有的list")
            game_list = list
        print game_list
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i])
            time.sleep(1)
            self.luadriver.find_lua_element_by_name(game_list[i]).click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                try:
                    self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i])
                    elements = self.game_page.game_play_way()
                    elements[0][1].click()
                except:
                    self.log_info("当前子游戏初级场")
                self.log_info("进入游戏ID：%s 的房间" % game_list[i])
                self.game_page.wait_element("房间场次").click()
                self.game_page.screenshot("%s.png" % game_list[i])
                if (self.game_page.element_is_exist("规则") == True):
                    if game_list[i] not in list:
                        list.append(game_list[i])
                    self.game_page.wait_element("规则").click()
                    self.log_info("进入游戏ID：%s 的房间,有规则说明" % game_list[i])
                    self.game_page.screenshot("%s_rule.png" % game_list[i])
                    try:
                        self.game_page.wait_element("房间内聊天").click()
                    except:
                        self.log_info("点击帮助外的其他按钮无反应")
                    self.game_page.screenshot("%s_rule1.png" % game_list[i])
                    try:
                        self.luadriver.keyevent(4)
                        time.sleep(2)
                    except:
                        self.log_info("按键盘返回键无响应")
                        self.luadriver.keyevent(4)
                else:
                    self.log_info("游戏ID：%s 的房间无规则说明" % game_list[i])
            except:
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")
        if len(list)==0:
            list.append(u"nogame")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表，是否有规则按钮")
        self.see_rule_display(game_list1)
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表，是否有规则按钮")
        self.see_rule_display(game_list2,is_next=True)
        print game_list1
        print game_list2

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C27032_Gamehelp_Defaulttab(TestCase):
    '''
    帮助面板打开时默认选中“基本规则”tab
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    pending = True
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

    def see_rule(self, list, is_next=False):
        game_list = []
        if len(list) == 0:
            self.log_info("重新获取游戏列表")
            game_list0 = self.game_page.get_game_list()
            for i in range(len(game_list0)):
                game_list.append(game_list0[i].get_attribute("name"))
        elif str(list[0]) == "nogame":
            return
        else:
            self.log_info("使用已有的list")
            game_list = list
        print game_list
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i])
            time.sleep(1)
            self.luadriver.find_lua_element_by_name(game_list[i]).click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                try:
                    self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i])
                    elements = self.game_page.game_play_way()
                    elements[0][1].click()
                except:
                    self.log_info("当前子游戏初级场")
                self.log_info("进入游戏ID：%s 的房间" % game_list[i])
                self.game_page.wait_element("房间场次").click()
                self.game_page.screenshot("%s.png" % game_list[i])
                if (self.game_page.element_is_exist("规则") == True):
                    if game_list[i] not in list:
                        list.append(game_list[i])
                    self.game_page.wait_element("规则").click()
                    self.log_info("进入游戏ID：%s 的房间,有规则说明" % game_list[i])
                    self.game_page.screenshot("%s_rule.png" % game_list[i])
                    self.luadriver.keyevent(4)
                    time.sleep(2)
                else:
                    self.log_info("游戏ID：%s 的房间无规则说明" % game_list[i])
            except:
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")
        if len(list)==0:
            list.append(u"nogame")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表，是否有规则按钮")
        self.see_rule(game_list1)
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表，是否有规则按钮")
        self.see_rule(game_list2,is_next=True)
        print game_list1
        print game_list2

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C27033_Gamehelp_Helptip(TestCase):
    '''
    帮助面板标题显示为“帮助”
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    pending = True
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

    def see_rule_title(self, list, is_next=False):
        game_list = []
        if len(list) == 0:
            self.log_info("重新获取游戏列表")
            game_list0 = self.game_page.get_game_list()
            for i in range(len(game_list0)):
                game_list.append(game_list0[i].get_attribute("name"))
        elif str(list[0]) == "nogame":
            return
        else:
            self.log_info("使用已有的list")
            game_list = list
        print game_list
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i])
            time.sleep(1)
            self.luadriver.find_lua_element_by_name(game_list[i]).click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                self.log_info("进入游戏ID：%s 的房间" % game_list[i])
                try:
                    self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i])
                    elements = self.game_page.game_play_way()
                    elements[0][1].click()
                except:
                    self.log_info("当前子游戏初级场")
                self.game_page.wait_element("房间场次").click()
                self.game_page.screenshot("%s.png" % game_list[i])
                if (self.game_page.element_is_exist("规则") == True):
                    if game_list[i] not in list:
                        list.append(game_list[i])
                    self.game_page.wait_element("规则").click()
                    self.log_info("进入游戏ID：%s 的房间,有规则说明" % game_list[i])
                    self.game_page.screenshot("%s_default_rule.png" % game_list[i])
                    self.game_page.wait_element("帮助标题").get_attribute("text")=="帮助"
                    self.luadriver.keyevent(4)
                    time.sleep(2)
                else:
                    self.log_info("游戏ID：%s 的房间无规则说明" % game_list[i])
            except:
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")
        if len(list)==0:
            list.append(u"nogame")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表，是否有规则按钮")
        self.see_rule_title(game_list1)
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表，是否有规则按钮")
        self.see_rule_title(game_list2,is_next=True)
        print game_list1
        print game_list2

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C27034_Gamehelp_Helptext(TestCase):
    '''
    帮助面板中各tab页右侧主要内容描述正确，无错别字；
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    pending = True
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

    def see_rule_content(self, list, is_next=False):
        game_list = []
        if len(list) == 0:
            self.log_info("重新获取游戏列表")
            game_list0 = self.game_page.get_game_list()
            for i in range(len(game_list0)):
                game_list.append(game_list0[i].get_attribute("name"))
        elif str(list[0]) == "nogame":
            return
        else:
            self.log_info("使用已有的list")
            game_list = list
        print game_list
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i])
            time.sleep(1)
            self.luadriver.find_lua_element_by_name(game_list[i]).click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                try:
                    self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i])
                    elements = self.game_page.game_play_way()
                    elements[0][1].click()
                except:
                    self.log_info("当前子游戏初级场")
                self.log_info("进入游戏ID：%s 的房间" % game_list[i])
                self.game_page.wait_element("房间场次").click()
                self.game_page.screenshot("%s.png" % game_list[i])
                if (self.game_page.element_is_exist("规则") == True):
                    if game_list[i] not in list:
                        list.append(game_list[i])
                    self.game_page.wait_element("规则").click()
                    self.log_info("进入游戏ID：%s 的房间,有规则说明" % game_list[i])
                    self.game_page.screenshot("%s_default_rule.png" % game_list[i])
                    self.log_info("查看帮助页面内容")
                    helps = self.game_page.get_elements("帮助列表")
                    black_help = ["帮助"]
                    for i in range(len(helps)):
                        try:
                            name = helps[i].get_attribute('text').decode('utf-8')
                            if name != None:
                                if name not in black_help:
                                    black_help.append(name)
                                    helps[i].click()
                                    time.sleep(1)
                                    self.game_page.screenshot("help_%d.png" % i)
                        except:
                            print ""
                    self.luadriver.keyevent(4)
                    time.sleep(2)
                else:
                    self.log_info("游戏ID：%s 的房间无规则说明" % game_list[i])
            except:
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")
        if len(list)==0:
            list.append(u"nogame")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表，是否有规则按钮")
        self.see_rule_content(game_list1)
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表，是否有规则按钮")
        self.see_rule_content(game_list2,is_next=True)
        print game_list1
        print game_list2

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C27036_Gamehelp_Helptext_Switch(TestCase):
    '''
    帮助面板中各tab快速切换，查看是否显示正常
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    pending = True
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

    def see_rule_content(self, list, is_next=False):
        game_list = []
        if len(list) == 0:
            self.log_info("重新获取游戏列表")
            game_list0 = self.game_page.get_game_list()
            for i in range(len(game_list0)):
                game_list.append(game_list0[i].get_attribute("name"))
        elif str(list[0]) == "nogame":
            return
        else:
            self.log_info("使用已有的list")
            game_list = list
        print game_list
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i])
            time.sleep(1)
            self.luadriver.find_lua_element_by_name(game_list[i]).click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                try:
                    self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i])
                    elements = self.game_page.game_play_way()
                    elements[0][1].click()
                except:
                    self.log_info("当前子游戏初级场")
                self.log_info("进入游戏ID：%s 的房间" % game_list[i])
                self.game_page.wait_element("房间场次").click()
                self.game_page.screenshot("%s.png" % game_list[i])
                if (self.game_page.element_is_exist("规则") == True):
                    if game_list[i] not in list:
                        list.append(game_list[i])
                    self.game_page.wait_element("规则").click()
                    self.log_info("进入游戏ID：%s 的房间,有规则说明" % game_list[i])
                    self.game_page.screenshot("%s_default_rule.png" % game_list[i])
                    self.log_info("查看帮助页面内容")
                    helps = self.game_page.get_elements("帮助列表")
                    black_help = ["帮助"]
                    for i in range(len(helps)):
                        try:
                            name = helps[i].get_attribute('text').decode('utf-8')
                            if name != None:
                                if name not in black_help:
                                    black_help.append(name)
                                    helps[i].click()
                                    time.sleep(1)
                                    self.game_page.screenshot("help_%d.png" % i)
                        except:
                            print ""
                    self.luadriver.keyevent(4)
                    time.sleep(2)
                else:
                    self.log_info("游戏ID：%s 的房间无规则说明" % game_list[i])
            except:
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")
        if len(list)==0:
            list.append(u"nogame")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表，是否有规则按钮")
        self.see_rule_content(game_list1)
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表，是否有规则按钮")
        self.see_rule_content(game_list2,is_next=True)
        print game_list1
        print game_list2

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C27035_Gamehelp_Helpswipe(TestCase):
    '''
    帮助面板中各tab页右侧主要内容描述超出一页的可以正常滑动显示正常
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    pending = True
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

    def see_rule_swipe(self, list, is_next=False):
        game_list = []
        if len(list) == 0:
            self.log_info("重新获取游戏列表")
            game_list0 = self.game_page.get_game_list()
            for i in range(len(game_list0)):
                game_list.append(game_list0[i].get_attribute("name"))
        elif str(list[0]) == "nogame":
            return
        else:
            self.log_info("使用已有的list")
            game_list = list
        print game_list
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i])
            time.sleep(1)
            self.luadriver.find_lua_element_by_name(game_list[i]).click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                try:
                    self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i])
                    elements = self.game_page.game_play_way()
                    elements[0][1].click()
                except:
                    self.log_info("当前子游戏初级场")
                self.log_info("进入游戏ID：%s 的房间" % game_list[i])
                self.game_page.wait_element("房间场次").click()
                self.game_page.screenshot("%s.png" % game_list[i])
                if (self.game_page.element_is_exist("规则") == True):
                    if game_list[i] not in list:
                        list.append(game_list[i])
                    self.game_page.wait_element("规则").click()
                    self.log_info("进入游戏ID：%s 的房间,有规则说明" % game_list[i])
                    self.game_page.screenshot("%s_default_rule.png" % game_list[i])
                    scroll_element = self.game_page.wait_element("帮助内容")
                    self.luadriver.swipe(scroll_element.location['x'], scroll_element.location['y'],
                                         scroll_element.location['x'],
                                         scroll_element.location['x'] + scroll_element.size['height'] / 2, 1000)
                    self.game_page.screenshot("%s_swipe_help.png" % game_list[i])
                    self.luadriver.keyevent(4)
                    time.sleep(2)
                else:
                    self.log_info("游戏ID：%s 的房间无规则说明" % game_list[i])
            except:
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")
        if len(list)==0:
            list.append(u"nogame")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表，是否有规则按钮")
        self.see_rule_swipe(game_list1)
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表，是否有规则按钮")
        self.see_rule_swipe(game_list2,is_next=True)
        print game_list1
        print game_list2

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

# __qtaf_seq_tests__ = [C27033_Gamehelp_Helptip]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
