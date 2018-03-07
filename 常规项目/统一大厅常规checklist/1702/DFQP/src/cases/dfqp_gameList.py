#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Author: MindyZhang
'''
大厅子游戏测试
'''

import time
from runcenter.enums import EnumStatus,EnumPriority
from runcenter.testcase import debug_run_all,TestCase
from common.common import Common
from appiumcenter.luadriver import LuaDriver
from uilib.hall_page import Hall_Page
from uilib.game_page import Game_Page
from uilib.match_page import Match_Page
from uilib.personinfo_page import Personinfo_Page

class C31147_DFQP_GameList(TestCase):
    '''
    大厅子游戏入口展示
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        #初始化luadriver
        self.luadriver = self.common.setupdriver()
        time.sleep(5)
        #关闭活动弹框
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看大厅游戏入口显示")
        self.game_page.screenshot("1.png")
        self.start_step("进入第二页")
        self.game_page.wait_element("右三角标").click()
        time.sleep(2)
        self.game_page.screenshot("2.png")
        self.start_step("查看更多游戏")
        self.game_page.wait_element("更多游戏").click()
        time.sleep(2)
        self.game_page.screenshot("3.png")
        self.game_page.wait_element("绿色箭头返回").click()
        time.sleep(2)
        self.start_step("点击左三角标返回上一页")
        self.game_page.wait_element("左三角标").click()
        time.sleep(3)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31153_DFQP_FriendRoom_Match(TestCase):
    '''
    子游戏列表跳转约牌房和比赛场
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        # 初始化Luadriver
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver( )
        # 关闭弹框
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例---跳转约牌房和比赛场
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(3)
        self.start_step("点击大厅首页的子游戏")
        self.start_step("获取子游戏列表")
        game_list = self.common.get_game_list()
        for i in range(len(game_list)):
            game_list[i].click()
            time.sleep(5)
            self.game_page.game_is_download()
            time.sleep(2)
            if (self.game_page.element_is_exist("约牌按钮")==True):
                self.game_page.get_element("约牌按钮").click()  # 不存在约牌和比赛按钮时，会点击不准确
                time.sleep(3)
                print ("进入约牌房")
                self.game_page.wait_element("返回1").click()
                time.sleep(3)
            else:
                print("无约牌房")
            if (self.game_page.element_is_exist("子游戏比赛按钮") == True):
                self.game_page.get_element("子游戏比赛按钮").click()
                time.sleep(3)
                print ("进入比赛")
                self.game_page.wait_element("比赛场返回").click()
                time.sleep(3)
            else:
                print("无比赛")
            self.game_page.wait_element("返回").click()
        self.start_step("点击大厅第二页")
        if(self.game_page.element_is_exist("更多游戏") == True):
            self.game_page.wait_element("左三角标").click()
        else:
            self.game_page.wait_element("右三角标").click()
        time.sleep(4)
        self.start_step("获取第二页的子游戏")
        game_list1 = self.common.get_game_list()
        for i in range(len(game_list1)):
            game_list1[i].click()
            time.sleep(5)
            self.game_page.game_is_download()
            time.sleep(2)
            if (self.game_page.element_is_exist("约牌按钮")==True):
                self.game_page.get_element("约牌按钮").click()  # 不存在约牌和比赛按钮时，会点击不准确
                time.sleep(3)
                print ("进入约牌房")
                self.game_page.wait_element("返回1").click()
                time.sleep(3)
            else:
                print("无约牌房")
            if (self.game_page.element_is_exist("子游戏比赛按钮") == True):
                self.game_page.get_element("子游戏比赛按钮").click()
                time.sleep(3)
                print ("进入比赛")
                self.game_page.wait_element("比赛场返回").click()
                time.sleep(3)
            else:
                print("无比赛")
            self.game_page.wait_element("返回").click()


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31151_DFQP_GameListUserinfo(TestCase):
    '''
    子游戏列表查看个人资料
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):

        self.common = Common()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        time.sleep(5)
        # 关闭活动弹框
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(3)

        self.start_step("点击进入血战到底")
        if (self.game_page.game_is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            self.game_page.game_is_download()
            time.sleep(2)
            self.start_step("查看个人资料")
            self.game_page.wait_element("头像").click()
            time.sleep(3)
            self.game_page.screenshot(".png")
            time.sleep(3)
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(2)
            self.game_page.wait_element("返回").click()
        else:
            print ("没有血战到底游戏")
            self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31152_DFQP_GameListGold(TestCase):
    '''
    子游戏列表查看快捷支付
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()

        # 关闭弹框
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("点击二七十：")
        if (self.game_page.game_is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(3)
            self.game_page.game_is_download()
            time.sleep(3)
            self.start_step("快捷支付")
            self.game_page.wait_element("+银币").click()
            time.sleep(5)
            self.game_page.screenshot("1.png")
            self.game_page.wait_element("绿色箭头返回").click()
            time.sleep(5)
            self.game_page.wait_element("+金条1").click()
            time.sleep(5)
            self.game_page.screenshot("2.png")
            self.game_page.wait_element("绿色箭头返回").click()
            time.sleep(5)
            self.game_page.wait_element("返回").click()
            time.sleep(3)

        else:
            print ("没有二七十游戏")
            self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31155_DFQP_GamePlayList(TestCase):
    '''
    游戏玩法切换
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()

        # 关闭弹框
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")

        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.start_step("点击血战到底：")
        if (self.game_page.game_is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            self.game_page.game_is_download()
            time.sleep(2)
            if (self.game_page.element_is_exist("玩法切换2") == True):
                self.game_page.wait_element("玩法切换2").click()
                time.sleep(2)
                self.game_page.wait_element("玩法切换1").click()
                time.sleep(2)
                print ("玩法切换成功")
                self.game_page.wait_element("返回").click()
            else:
                print ("该游戏没有其他玩法")
                self.game_page.wait_element("返回").click()
        else:
            print ("没有血战到底游戏")
            self.game_page.wait_element("左三角标").click()

        self.start_step("点击斗牛")
        if (self.game_page.game_is_exist("斗牛") == True):
            self.game_page.wait_element("斗牛").click()
            time.sleep(3)
            self.game_page.game_is_download()
            time.sleep(2)
            if (self.game_page.element_is_exist("玩法切换1") == True):
                self.game_page.wait_element("玩法切换2").click()
                time.sleep(2)
                self.game_page.wait_element("玩法切换1").click()
                time.sleep(2)
                self.game_page.screenshot("2.png")
                print ("玩法切换成功")
                self.game_page.wait_element("返回").click()
            else:
                print ("该游戏没有其他玩法")
                self.game_page.screenshot("2.png")
                self.game_page.wait_element("返回").click()
        else:
            print ("没有斗牛游戏")
            self.game_page.wait_element("左三角标").click()

        self.start_step("点击闷鸡")
        if (self.game_page.game_is_exist("闷鸡") == True):
            self.game_page.wait_element("闷鸡").click()
            time.sleep(3)
            self.game_page.game_is_download()
            time.sleep(2)
            if(self.game_page.element_is_exist("玩法切换4")==True):
                self.game_page.wait_element("玩法切换2").click()
                time.sleep(2)
                self.game_page.wait_element("玩法切换3").click()
                time.sleep(2)
                self.game_page.wait_element("玩法切换4").click()
                time.sleep(2)
                self.game_page.wait_element("玩法切换1").click()
                time.sleep(2)
                self.game_page.screenshot("3.png")
                print ("玩法切换成功")
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                print ("该游戏没有其他玩法")
                self.game_page.screenshot("3.png")
                self.game_page.wait_element("返回").click()

        else:
            print ("没有闷鸡游戏")
            self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31161_DFQP_GameRoom1(TestCase):
    '''
    游戏房间内显示
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()

        # 关闭弹框
        self.common.closeactivity(self.luadriver)
        time.sleep(10)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(3)
        self.start_step("点击血战到底：")
        if (self.game_page.game_is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            self.game_page.game_is_download()
            time.sleep(3)
            self.game_page.wait_element("快速开始").click()
            time.sleep(3)
            self.game_page.screenshot(".png")
            time.sleep(3)
            self.game_page.wait_element("菜单").click()
            time.sleep(2)
            self.game_page.wait_element("退出房间").click()
            time.sleep(2)
            # self.luadriver.keyevent(4)
            # time.sleep(3)
            # self.luadriver.keyevent(4)
            # time.sleep(3)
            self.game_page.wait_element("返回").click()
            time.sleep(2)
        else:
            print ("没有血战到底游戏")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31148_DFQP_GameList_DownLoad_MoreGames(TestCase):
    '''
    更多游戏
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        capabilities = {}
        capabilities['noReset'] = False
        self.luadriver = self.common.setupdriver(capabilities)

        # 关闭弹框
        self.common.closeactivity(self.luadriver)
        self.common.closefloatBall()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.startStep = ("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.game_page.wait_element("右三角标").click()
        time.sleep(2)
        self.start_step("点击第二页的更多游戏")
        self.start_step("点击更多游戏")
        self.game_page.wait_element("更多游戏").click()
        time.sleep(3)
        self.game_page.screenshot("1.png")
        self.start_step("下载更多游戏列表的第一个游戏")
        self.game_page.screenshot("download.png")
        self.game_page.wait_element("更多游戏[1]").click()
        try:
            self.game_page.wait_element("更多游戏关闭下载弹框").click()
            time.sleep(3)
            self.game_page.wait_element("更多游戏[1]").click()
            time.sleep(3)
            self.game_page.wait_element("更多游戏-立刻下载").click()
            time.sleep(20)
            print ("游戏下载成功")
            self.game_page.wait_element("更多游戏[1]").click()
            self.game_page.screenshot("download1.png")
            time.sleep(3)
            self.game_page.wait_element("返回").click()
            time.sleep(3)

        except:
            print("游戏已下载")
            time.sleep(5)
            self.game_page.wait_element("返回").click()
        time.sleep(3)

        self.start_step("下载更多游戏列表第二个游戏")
        self.game_page.wait_element("更多游戏[2]").click()

        try:

            # self.game_page.wait_element("更多游戏[2]").click()
            time.sleep(3)
            self.game_page.wait_element("更多游戏-立刻下载").click()
            time.sleep(20)
            print ("游戏下载成功")
            self.game_page.wait_element("更多游戏[2]").click()
            time.sleep(5)
            self.game_page.wait_element("返回").click()
            time.sleep(3)
            self.game_page.wait_element("更多游戏[2]").click()
            self.game_page.screenshot("download2.png")
            time.sleep(3)
            self.game_page.wait_element("返回").click()
            time.sleep(3)

        except:
            print("游戏已下载")
            self.game_page.wait_element("返回").click()
        time.sleep(3)

        self.start_step("下载更多游戏列表第三个游戏")
        self.game_page.wait_element("更多游戏[3]").click()
        try:
            # self.game_page.wait_element("更多游戏[3]").click()
            time.sleep(3)
            self.game_page.wait_element("更多游戏-立刻下载").click()
            time.sleep(20)
            print ("游戏下载成功")
            self.game_page.screenshot("download3.png")
            # self.game_page.wait_element("更多游戏[3]").click()
            # time.sleep(3)
            while(self.game_page.element_is_exist("更多游戏[3]")==False):
                self.game_page.wait_element("返回").click()
            time.sleep(3)
        except:

            print("游戏已下载")
            self.game_page.wait_element("返回").click()
        time.sleep(3)
        self.start_step("下载更多游戏列表第四个游戏")
        self.game_page.wait_element("更多游戏[4]").click()
        try:
            # self.game_page.wait_element("更多游戏[4]").click()
            time.sleep(3)
            self.game_page.wait_element("更多游戏-立刻下载").click()
            time.sleep(20)
            print ("游戏下载成功")
            self.game_page.wait_element("更多游戏[4]").click()
            self.game_page.screenshot("download4.png")
            time.sleep(3)
            self.game_page.wait_element("返回").click()
            time.sleep(3)

        except:
            print("游戏已下载")
            self.game_page.wait_element("返回").click()
        time.sleep(3)
        self.game_page.screenshot("2.png")
        time.sleep(2)
        self.game_page.wait_element("绿色箭头返回").click()
        time.sleep(2)
        self.game_page.wait_element("左三角标").click()
        time.sleep(2)
    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31162_DFQP_GameRoom2(TestCase):
    '''
    游戏房间---菜单栏功能
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()

        # 关闭活动弹框
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("点击血战到底：")
        if (self.game_page.game_is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            self.game_page.game_is_download()
            time.sleep(2)
            self.game_page.wait_element("快速开始").click()
            time.sleep(3)
            self.start_step("点击菜单")
            time.sleep(3)
            self.game_page.wait_element("菜单").click()
            time.sleep(2)
            self.game_page.screenshot('1.png')
            self.start_step("点击设置")
            self.game_page.wait_element("设置").click()
            self.game_page.screenshot("2.png")
            time.sleep(3)
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.start_step("点击托管")
            self.game_page.wait_element("菜单").click()
            time.sleep(2)
            self.game_page.wait_element("托管").click()
            time.sleep(3)
            self.game_page.screenshot("3.png")
            self.start_step("点击商城")
            self.game_page.wait_element("商城").click()
            time.sleep(3)
            self.game_page.screenshot("4.png")
            # self.game_page.wait_element("关闭对话框").click()
            self.luadriver.keyevent(4)
            time.sleep(2)
            self.game_page.wait_element("菜单").click()
            time.sleep(2)
            self.start_step("点击取款")
            self.game_page.wait_element("取款").click()
            self.game_page.screenshot("5.png")
            time.sleep(2)
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(2)
            # self.game_page.wait_element("菜单").click()
            # time.sleep(2)
            # self.game_page.wait_element("退出房间").click()
            self.luadriver.keyevent(4)
            time.sleep(3)
            self.game_page.wait_element("返回").click()
        else:
            print ("没有血战到底游戏")
            self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31165_DFQP_GameRoom3(TestCase):
    '''
    游戏房间内---个人资料显示
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()

        # 关闭弹框
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''

        self.start_step("点击血战到底：")
        if (self.game_page.game_is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            self.game_page.game_is_download()
            time.sleep(2)
            self.game_page.wait_element("快速开始").click()
            time.sleep(3)
            self.start_step("点击头像")
            self.game_page.wait_element("头像---未开始游戏").click()
            time.sleep(3)
            self.game_page.screenshot(".png")
            self.luadriver.keyevent(4)
            time.sleep(2)
            self.luadriver.keyevent(4)
            time.sleep(2)
            self.game_page.wait_element("返回").click()
            time.sleep(2)

        else:
            print ("没有血战到底游戏")
            self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31166_DFQP_GameRoom4(TestCase):
    '''
    游戏房间内---牌局未开启时聊天
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()

        # 关闭弹框
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("点击血战到底：")
        if (self.game_page.game_is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            self.game_page.game_is_download()
            time.sleep(2)
            self.game_page.wait_element("快速开始").click()
            time.sleep(3)
            self.start_step("点击聊天按钮")
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.screenshot("1.png")
            self.game_page.wait_element("表情").click()
            time.sleep(2)
            elements = self.game_page.get_elements("VIP表情1")
            print len(elements)
            if(self.game_page.element_is_exist("普通表情1") == True):
                self.game_page.wait_element("普通表情1").click()
                time.sleep(2)
                self.game_page.screenshot("2.png")
            else:
                self.game_page.wait_element("VIP表情1").click()
                time.sleep(2)
                self.game_page.screenshot("2.png")
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("常用").click()
            self.game_page.screenshot("3.png")
            self.game_page.wait_element("常用1").click()
            time.sleep(2)
            self.luadriver.keyevent(4)
            time.sleep(2)
            # self.game_page.wait_element("菜单").click()
            # time.sleep(2)
            # self.game_page.wait_element("退出").click()
            # time.sleep(3)
            self.game_page.wait_element("返回").click()

        else:

            print ("没有血战到底游戏")
            self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31154_DFQP_GameRoom_Agenda(TestCase):
    '''
    子游戏房间列表---点击今日赛程
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):

        self.common = Common()
        #初始化luadriver
        print ("pre_test")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)

        self.hall_page = Hall_Page()
        self.match_page = Match_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''

        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.start_step("点击血战到底：")
        if (self.game_page.game_is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            self.game_page.game_is_download()
            time.sleep(2)
            self.start_step("点击今日赛程按钮")
            self.match_page.wait_element("今日赛程").click()
            time.sleep(3)
            self.match_page.screenshot("1.png")
            time.sleep(3)
            if (self.match_page.element_is_exist("比赛详情1") == True):
                self.match_page.wait_element("比赛详情1").click()
                time.sleep(3)
                self.match_page.screenshot("2.png")
                self.match_page.wait_element("关闭").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
            else:
                print ("无赛程")
                self.luadriver.keyevent(4)
                time.sleep(2)

        else:
            print ("没有血战到底游戏")
            self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()


__qtaf_seq_tests__ = [C31153_DFQP_FriendRoom_Match]

if __name__ == '__main__':
    debug_run_all()
























