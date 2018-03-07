#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
选场界面展示
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.game_page import Game_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common


class C27028_Gamelist_Display(TestCase):
    '''
    选场界面显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动")
        self.common.closeactivity(self.luadriver)

    def gamelist_distplay(self,is_next=False):
        game_list = self.game_page.get_game_list()
        self.start_step("遍历第一页的子游戏%d个" %len(game_list))
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" %game_list[i].get_attribute("name"))
            game_list[i].click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志",20)
            except:
                self.game_page.screenshot("fail1.png")
                try:
                    self.hall_page.wait_element("关闭").click()
                except:
                    self.log_info("未找到元素")
            self.game_page.screenshot("%s.png" %game_list[i].get_attribute("name"))
            try:
                self.game_page.wait_element("返回1").click()
            except:
                self.log_info("未找到元素")
            if is_next == True:
                self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                try:
                    self.game_page.wait_element("右三角标").click()
                except:
                    self.log_info("当前为第二页")


    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.gamelist_distplay()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.gamelist_distplay(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27348_Gamelist_OnlineNum(TestCase):
    '''
    查看场次按钮的人数显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def onlinenum(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志",20)
                online_num = self.game_page.get_elements("在线人数")
                for j in range(len(online_num)):
                    if online_num[j] >= 0:
                        self.log_info("游戏ID：%s 在线人数 %s" % (game_list[i].get_attribute("name"), online_num[j].get_attribute("text")))
                        self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    else:
                        raise Exception("游戏ID：%s 在线人数 %s" % ( game_list[i].get_attribute("name"), online_num[j].get_attribute("text")))
            except:
                self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
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
                    self.log_info("当前为第二页")


    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.onlinenum()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.onlinenum(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27349_Gamelist_Name(TestCase):
    '''
    1.查看场次按钮的场次名称显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def gamelist_name(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
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
                name = self.game_page.get_elements("未选中的场次玩法名称")
                for j in range(len(name)):
                    name[j].click()
                    self.game_page.screenshot("%s_%d.png" % (game_list[i].get_attribute("name"), j))
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
                    self.log_info("当前为第二页")


    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.gamelist_name()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.gamelist_name(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27350_Gamelist_Name(TestCase):
    '''
    2.查看场次按钮的玩法名称显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def gamelist_name(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
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
                name = self.game_page.get_elements("未选中的场次玩法名称")
                for j in range(len(name)):
                    name[j].click()
                    self.game_page.screenshot("%s_%d.png" % (game_list[i].get_attribute("name"), j))
            except:
                try:
                    self.hall_page.wait_element("关闭").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.game_page.wait_element("返回1").click()
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

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.gamelist_name()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.gamelist_name(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27351_Gamelist_Yuepai(TestCase):
    '''
    没有约牌房，选场界面约牌房入口显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def game_yuepai(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
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
                if (self.game_page.element_is_exist("约牌按钮") == False):
                    self.log_info("游戏ID：%s 不存在约牌房" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.game_page.wait_element("返回1").click()
                else:
                    self.log_info("游戏ID：%s 存在约牌房" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
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
                    self.log_info("当前为第二页")


    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.game_yuepai()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.game_yuepai(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27352_Gamelist_Match(TestCase):
    '''
    子游戏无比赛场时查看选场界面
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def game_match(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i].get_attribute("name"))
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                if (self.game_page.element_is_exist("子游戏比赛按钮") == False):
                    self.log_info("游戏ID：%s 不存在比赛场" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("_%s.png" % game_list[i].get_attribute("name"))
                    self.game_page.wait_element("返回1").click()
                else:
                    self.log_info("游戏ID：%s 存在比赛场" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("_%s.png" % game_list[i].get_attribute("name"))
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
                    self.log_info("当前为第二页")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.game_match()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.game_match(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27353_Gamelist_Yuepai(TestCase):
    '''
    有约牌房，选场界面约牌房入口显示位置
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def yuepai_display(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志",20)
                if (self.game_page.element_is_exist("约牌按钮") == True):
                    self.log_info("游戏ID：%s 存在约牌房" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.game_page.wait_element("返回1").click()
                else:
                    self.log_info("游戏ID：%s 不存在约牌按钮" % game_list[i].get_attribute("name"))
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
                    self.log_info("当前为第二页")


    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.yuepai_display()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.yuepai_display(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27354_Gamelist_Yuepai_Enter(TestCase):
    '''
    点击选场界面的约牌房入口
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def yuepai_enter(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            game_list[i].click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            self.game_page.wait_element("同步标志", 20)
            if (self.game_page.element_is_exist("约牌按钮") == True):
                self.log_info("游戏ID：%s 存在约牌房" % game_list[i].get_attribute("name"))
                self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                self.game_page.wait_element("约牌按钮", 20).click()
                self.start_step("创建免费记分房")
                self.yuepai_page.wait_element('记分房', 20).click()
                self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                elements = self.game_page.get_elements("返回")
                for j in range(len(elements)):
                    elements[j].click()
                self.game_page.wait_element("返回").click()
            else:
                self.log_info("游戏ID：%s 不存在约牌按钮" % game_list[i].get_attribute("name"))
                self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
        try:
            self.game_page.wait_element("返回1").click()
        except:
            self.log_info("未找到元素")
        if is_next == True:
            self.log_info("is_next为True则表示遍历的是第二页的子游戏")
            try:
                self.game_page.wait_element("右三角标").click()
            except:
                self.log_info("当前为第二页")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.yuepai_enter()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.yuepai_enter(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27355_Gamelist_Match_Enter(TestCase):
    '''
    选场界面比赛场入口显示位置
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 22

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def match_enter(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if (self.game_page.game_is_download() == False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                if (self.game_page.element_is_exist("子游戏比赛按钮") == True):
                    self.log_info("游戏ID：%s 存在比赛按钮" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.game_page.wait_element("返回1").click()
                else:
                    self.log_info("游戏ID：%s 不存在比赛按钮" % game_list[i].get_attribute("name"))
            except:
                try:
                    self.hall_page.wait_element("关闭").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.game_page.wait_element("返回1").click()
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

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.match_enter()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.match_enter(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27356_Gamelist_Match_Yuepai(TestCase):
    '''
    	同时存在比赛和约牌房两个入口时查看按钮显示位置
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def  match_yuepai(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
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
                if (self.game_page.element_is_exist("子游戏比赛按钮") == True and self.game_page.element_is_exist(
                        "约牌按钮") == True):
                    self.log_info("游戏ID：%s 存在比赛和约牌按钮" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.game_page.wait_element("返回1").click()
                else:
                    self.log_info("游戏ID：%s 不存在比赛和约牌按钮" % game_list[i].get_attribute("name"))
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
                    self.log_info("当前为第二页")


    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.match_yuepai()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.match_yuepai(is_next=True)


    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27340_Gamelist_Broadcast(TestCase):
    '''
    无广播时选场界面的广播条展示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def broadcast(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
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
                if (self.game_page.element_is_exist("广播") == True):
                    self.log_info("游戏ID：%s 存在广播按钮" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
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
                    self.log_info("当前为第二页")


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
        self.common.closedriver()

class C27341_Gamelist_Sendbroadcast(TestCase):
    '''
    无广播时选场界面发送广播
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def send_broadcast(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
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
                if (self.game_page.element_is_exist("广播") == True):
                    self.log_info("游戏ID：%s 存在广播按钮" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.game_page.wait_element("广播").click()
                    self.game_page.wait_element("立即升级")
                    self.game_page.screenshot("%s_broadcasttips.png" % game_list[i].get_attribute("name"))
                    self.game_page.wait_element("关闭广播提示").click()
                    self.game_page.wait_element("返回1").click()
                else:
                    self.log_info("游戏ID：%s 不存在广播按钮" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
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
                    self.log_info("当前为第二页")


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
        self.common.closedriver()

class C27344_Gamelist_Nobroadcast(TestCase):
    '''
    子游戏增加金条场时，选场界面不显示广播条
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def no_broadcast(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
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
                if (self.game_page.element_is_exist("广播") == False):
                    self.log_info("游戏ID：%s 有多个玩法tab" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                else:
                    self.log_info("游戏ID：%s 没有多个玩法tab" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("%s_broadcast.png" % game_list[i].get_attribute("name"))
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
                    self.log_info("当前为第二页")


    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.no_broadcast()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.no_broadcast(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27345_Gamelist_Gold(TestCase):
    '''
    点击金条场tab正常切换到金条场玩法选场界面
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def gold_room(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i].get_attribute("name"))
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                if (self.game_page.element_is_exist("广播") == False):
                    self.log_info("游戏ID：%s 有多个玩法tab" % game_list[i].get_attribute("name"))
                    try:
                        self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i].get_attribute("name"))
                        elements = self.game_page.game_play_way()
                        elements[len(elements)-1][1].click()
                        self.game_page.screenshot("%s_gold.png" % game_list[i].get_attribute("name"))
                    except:
                        self.log_info("金条场进入失败")
                else:
                    self.log_info("游戏ID：%s 没有多个玩法tab" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("%s_notgold.png" % game_list[i].get_attribute("name"))
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
                    self.log_info("当前为第二页")


    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.gold_room()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.gold_room(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27346_Gamelist_Enterdisplay(TestCase):
    '''
    游戏入口默认进入标准场玩法界面
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def enter_display(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
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
                if (self.game_page.element_is_exist("广播") == False):
                    self.log_info("游戏ID：%s 有多个玩法tab" % game_list[i].get_attribute("name"))
                    try:
                        self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i])
                        elements = self.game_page.game_play_way()
                        elements[0][1].click()
                    except:
                        self.log_info("当前子游戏初级场")
                    self.game_page.screenshot("%s_1.png" % game_list[i].get_attribute("name"))
                    try:
                        self.game_page.wait_element("返回1").click()
                    except:
                        self.log_info("未找到元素")
                    game_list[i].click()
                    self.game_page.screenshot("%s_2.png" % game_list[i].get_attribute("name"))
                else:
                    self.log_info("游戏ID：%s 没有多个玩法tab" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
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
                    self.log_info("当前为第二页")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.enter_display()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.enter_display(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27347_Gamelist_Enterdisplay(TestCase):
    '''
    玩家从房间退出时，退出到对应玩法的选场列表
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def enter_display(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
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
                if (self.game_page.element_is_exist("广播") == False):
                    self.log_info("游戏ID：%s 有多个玩法tab" % game_list[i].get_attribute("name"))
                    try:
                        self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i])
                        elements = self.game_page.game_play_way()
                        elements[0][1].click()
                        self.game_page.screenshot("%s_gold.png" % game_list[i].get_attribute("name"))
                        self.game_page.wait_element("房间场次").click()
                        self.game_page.screenshot("%s_gold1.png" % game_list[i].get_attribute("name"))
                        time.sleep(3)
                        self.yuepai_page.is_exist_yuepairoom()
                        self.game_page.screenshot("%s_gold3.png" % game_list[i].get_attribute("name"))
                    except:
                        self.log_info("进入子游戏初级场失败")
                else:
                    self.log_info("游戏ID：%s 没有多个玩法tab" % game_list[i].get_attribute("name"))
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
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
                    self.log_info("当前为第二页")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.enter_display()
        while(self.hall_page.element_is_exist("同步标志")==False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.enter_display(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

__qtaf_seq_tests__ = [C27347_Gamelist_Enterdisplay]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
