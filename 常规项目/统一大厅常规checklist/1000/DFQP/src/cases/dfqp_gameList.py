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



class C088_DFQP_GameList(TestCase):
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
        self.common.closeactivityprepublish(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        time.sleep(3)

        time.sleep(2)
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
        self.common.closedriver()

class C090_DFQP_GameNameList(TestCase):
    '''
    子游戏列表切换游戏
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        #关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例---切换游戏
        '''

        self.start_step("等待页面加载完成")

        self.hall_page.wait_element("同步标志")
        time.sleep(3)
        #前置条件：至少已下载4个游戏
        self.start_step("点击川味斗地主：")
        if (self.game_page.is_exist("点击川味斗地主") == True):
            self.game_page.wait_element("川味斗地主").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定")==True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.game_page.wait_element("返回").click()
            else:
                print ("川味斗地主已下载")
                self.game_page.wait_element("返回").click()
        else:
            print ("第一页没有川味斗地主，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("川味斗地主") == True):
                self.game_page.wait_element("川味斗地主").click()
                if (self.game_page.is_exist("资源下载-确定")==True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
                    self.game_page.wait_element("返回").click()
                else:
                    print ("川味斗地主已下载")
                    self.game_page.wait_element("返回").click()

                self.game_page.wait_element("左三角标").click()
            else:

                print ("没有川味斗地主游戏")
                self.game_page.wait_element("左三角标").click()


        self.start_step("点击血战到底：")
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            if(self.game_page.is_exist("资源下载-确定")==True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.game_page.wait_element("返回").click()
            else:
                print ("血战到底已下载")
                self.game_page.wait_element("返回").click()
        else:
            print ("第一页没有血战到底，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
                    self.game_page.wait_element("返回").click()
                else:
                    print ("血战到底已下载")
                    self.game_page.wait_element("返回").click()
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()


        self.start_step("点击血流成河：")
        if (self.game_page.is_exist("血流成河") == True):
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.game_page.wait_element("返回").click()
            else:
                print ("血战到底已下载")
                self.game_page.wait_element("返回").click()
        else:
            print ("第一页没有血流成河，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血流成河") == True):
                self.game_page.wait_element("血流成河").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
                    self.game_page.wait_element("返回").click()
                else:
                    print ("血流成河已下载")
                    self.game_page.wait_element("返回").click()
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有血流成河游戏")
                self.game_page.wait_element("左三角标").click()


        self.start_step("点击二七十：")
        if (self.game_page.is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(3)
            if(self.game_page.is_exist("资源下载-确定")==True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                print ("二七十已下载")
                self.game_page.wait_element("返回").click()
                time.sleep(2)
        else:
            print ("第一页没有二七十，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("二七十") == True):
                self.game_page.wait_element("二七十").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(15)
                    self.game_page.wait_element("返回").click()
                else:
                    print ("二七十已下载")
                    self.game_page.wait_element("返回").click()
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有二七十游戏")
                self.game_page.wait_element("左三角标").click()


        self.start_step("点击斗牛：")
        if (self.game_page.is_exist("斗牛") == True):
            self.game_page.wait_element("斗牛").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                print ("斗牛已下载")
                self.game_page.wait_element("返回").click()
                time.sleep(2)
        else:
            print ("第一页没有斗牛，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("斗牛") == True):
                self.game_page.wait_element("斗牛").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(15)
                    self.game_page.wait_element("返回").click()
                else:
                    print ("斗牛已下载")
                    self.game_page.wait_element("返回").click()
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有斗牛游戏")
                self.game_page.wait_element("左三角标").click()

        self.start_step("点击进入任意游戏")
        if (self.game_page.is_exist("血流成河")==True):
            self.game_page.wait_element("血流成河").click()  #是否可做成随机选择游戏进去？
            time.sleep(3)
        elif(self.game_page.is_exist("二七十")==True):
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
        elif(self.game_page.is_exist("血战到底")==True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(2)
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("血战到底").click()

        self.start_step("切换游戏名称")
        self.game_page.wait_element("gamename").click()
        time.sleep(2)
        self.game_page.screenshot("1.png")
        time.sleep(3)
        self.game_page.wait_element("gamenamelist1").click()
        time.sleep(2)
        self.game_page.wait_element("gamename").click()
        time.sleep(2)
        self.game_page.wait_element("gamenamelist2").click()
        time.sleep(2)
        self.game_page.wait_element("gamename").click()
        time.sleep(2)
        self.common.swipeelement(self.game_page.wait_element("gamenamelist3"),self.game_page.wait_element("gamenamelist1")) #从第一个游戏滑动到第三个游戏
        time.sleep(2)
        self.game_page.screenshot("2.png")
        self.game_page.wait_element("gamenamelist1").click()
        time.sleep(2)
        self.game_page.wait_element("gamename").click()
        time.sleep(2)
        self.game_page.wait_element("gamenamelist3").click()
        time.sleep(2)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C091_DFQP_FriendRoom(TestCase):
    '''
    子游戏列表跳转约牌房
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
        self.common.closeactivityprepublish(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例---跳转约牌房
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(3)
        self.start_step("点击进入血战到底")
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.game_page.screenshot(".png")
                time.sleep(2)
                if (self.game_page.is_exist("约牌按钮")==True):
                    self.game_page.get_element("约牌按钮").click()  # 不存在约牌和比赛按钮时，会点击不准确
                    time.sleep(3)
                    print ("进入约牌房")
                    self.game_page.wait_element("绿色箭头返回").click()
                    time.sleep(3)
                else:
                    print("无约牌房")
                self.game_page.wait_element("返回").click()
            else:
                print ("血战到底已下载")
                self.game_page.screenshot(".png")
                time.sleep(2)
                if (self.game_page.is_exist("约牌按钮") == True):
                    self.game_page.get_element("约牌按钮").click()  # 不存在约牌和比赛按钮时，会点击不准确
                    time.sleep(3)
                    print ("进入约牌房")
                    self.game_page.wait_element("绿色箭头返回").click()
                    time.sleep(3)
                else:
                    print("无约牌房")
                self.game_page.wait_element("返回").click()
        else:
            print ("第一页没有血战到底，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                self.game_page.screenshot(".png")
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
                    if (self.game_page.is_exist("约牌按钮") == True):
                        self.game_page.get_element("约牌按钮").click()  # 不存在约牌和比赛按钮时，会点击不准确
                        time.sleep(3)
                        print ("进入约牌房")
                        self.game_page.wait_element("绿色箭头返回").click()
                        time.sleep(3)
                    else:
                        print("无约牌房")
                    self.game_page.wait_element("返回").click()
                else:
                    print ("血战到底已下载")
                    self.game_page.screenshot(".png")
                    if (self.game_page.is_exist("约牌按钮") == True):
                        self.game_page.get_element("约牌按钮").click()  # 不存在约牌和比赛按钮时，会点击不准确
                        time.sleep(3)
                        print ("进入约牌房")
                        self.game_page.wait_element("绿色箭头返回").click()
                        time.sleep(3)
                    else:
                        print("无约牌房")
                    self.game_page.wait_element("返回").click()
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有血战到底游戏")

        self.start_step("点击进入血流成河")
        if (self.game_page.is_exist("血流成河") == True):
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                if (self.game_page.is_exist("约牌按钮") == True):
                    self.game_page.get_element("约牌按钮").click()
                    time.sleep(3)
                    print("进入约牌房")
                    self.game_page.wait_element("绿色箭头返回").click()
                    time.sleep(3)
                else:
                    print("无约牌房")
                self.game_page.wait_element("返回").click()
            else:
                print ("血战到底已下载")
                if (self.game_page.is_exist("约牌按钮") == True):
                    self.game_page.get_element("约牌按钮").click()
                    time.sleep(3)
                    print("进入约牌房")
                    self.game_page.wait_element("绿色箭头返回").click()
                    time.sleep(3)
                else:
                    print("无约牌房")
                self.game_page.wait_element("返回").click()
        else:
            print ("第一页没有血流成河，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血流成河") == True):
                self.game_page.wait_element("血流成河").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
                    if (self.game_page.is_exist("约牌按钮") == True):
                        self.game_page.get_element("约牌按钮").click()
                        time.sleep(3)
                        print("进入约牌房")
                        self.game_page.wait_element("绿色箭头返回").click()
                        time.sleep(3)
                    else:
                        print("无约牌房")
                    self.game_page.wait_element("返回").click()
                else:
                    print ("血流成河已下载")
                    if (self.game_page.is_exist("约牌按钮") == True):
                        self.game_page.get_element("约牌按钮").click()
                        time.sleep(3)
                        print("进入约牌房")
                        self.game_page.wait_element("绿色箭头返回").click()
                        time.sleep(3)
                    else:
                        print("无约牌房")
                    self.game_page.wait_element("返回").click()
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有血流成河游戏")
                self.game_page.wait_element("左三角标").click()

        self.start_step("点击进入川味斗地主")
        self.start_step("点击川味斗地主：")
        if (self.game_page.is_exist("点击川味斗地主") == True):
            self.game_page.wait_element("川味斗地主").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                if (self.game_page.is_exist("约牌按钮") == True):
                    self.game_page.get_element("约牌按钮").click()
                    time.sleep(3)
                    print("进入约牌房")
                    self.game_page.wait_element("绿色箭头返回").click()
                    time.sleep(3)
                else:
                    print("无约牌房")
                self.game_page.wait_element("返回").click()
            else:
                print ("川味斗地主已下载")
                if (self.game_page.is_exist("约牌按钮") == True):
                    self.game_page.get_element("约牌按钮").click()
                    time.sleep(3)
                    print("进入约牌房")
                    self.game_page.wait_element("绿色箭头返回").click()
                    time.sleep(3)
                else:
                    print("无约牌房")
                self.game_page.wait_element("返回").click()
        else:
            print ("第一页没有川味斗地主，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("川味斗地主") == True):
                self.game_page.wait_element("川味斗地主").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
                    if (self.game_page.is_exist("约牌按钮") == True):
                        self.game_page.get_element("约牌按钮").click()
                        time.sleep(3)
                        print("进入约牌房")
                        self.game_page.wait_element("绿色箭头返回").click()
                        time.sleep(3)
                    else:
                        print("无约牌房")
                    self.game_page.wait_element("返回").click()
                else:
                    print ("川味斗地主已下载")
                    if (self.game_page.is_exist("约牌按钮") == True):
                        self.game_page.get_element("约牌按钮").click()
                        time.sleep(3)
                        print("进入约牌房")
                        self.game_page.wait_element("绿色箭头返回").click()
                        time.sleep(3)
                    else:
                        print("无约牌房")
                    self.game_page.wait_element("返回").click()

                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有川味斗地主游戏")
                self.game_page.wait_element("左三角标").click()

        self.start_step("点击进入斗牛")
        if (self.game_page.is_exist("斗牛") == True):
            self.game_page.wait_element("斗牛").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                if (self.game_page.is_exist("约牌按钮") == True):
                    self.game_page.get_element("约牌按钮").click()
                    time.sleep(3)
                    print("进入约牌房")
                    self.game_page.wait_element("绿色箭头返回").click()
                    time.sleep(3)
                else:
                    print("无约牌房")
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                print ("斗牛已下载")
                if (self.game_page.is_exist("约牌按钮") == True):
                    self.game_page.get_element("约牌按钮").click()
                    time.sleep(3)
                    print("进入约牌房")
                    self.game_page.wait_element("绿色箭头返回").click()
                    time.sleep(3)
                else:
                    print("无约牌房")
                self.game_page.wait_element("返回").click()
                time.sleep(2)
        else:
            print ("第一页没有斗牛，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("斗牛") == True):
                self.game_page.wait_element("斗牛").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(15)
                    if (self.game_page.is_exist("约牌按钮") == True):
                        self.game_page.get_element("约牌按钮").click()
                        time.sleep(3)
                        print("进入约牌房")
                        self.game_page.wait_element("绿色箭头返回").click()
                        time.sleep(3)
                    else:
                        print("无约牌房")
                    self.game_page.wait_element("返回").click()
                else:
                    print ("斗牛已下载")
                    if (self.game_page.is_exist("约牌按钮") == True):
                        self.game_page.get_element("约牌按钮").click()
                        time.sleep(3)
                        print("进入约牌房")
                        self.game_page.wait_element("绿色箭头返回").click()
                        time.sleep(3)
                    else:
                        print("无约牌房")
                    self.game_page.wait_element("返回").click()
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有斗牛游戏")
                self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C092_DFQP_GameListMatch(TestCase):
    '''
    子游戏列表跳转比赛
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
        self.common.closeactivityprepublish(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例---跳转比赛
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(3)
        self.start_step("点击进入血战到底")
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.game_page.screenshot(".png")
                if(self.game_page.is_exist("子游戏比赛按钮")==True):
                    self.game_page.get_element("子游戏比赛按钮").click()
                    time.sleep(3)
                    print ("进入比赛")
                    self.game_page.wait_element("比赛场返回").click()
                    time.sleep(3)
                else:
                    print("无比赛")
                self.game_page.wait_element("返回").click()
            else:
                print ("血战到底已下载")
                self.game_page.screenshot(".png")
                if (self.game_page.is_exist("子游戏比赛按钮")==True):
                    self.game_page.get_element("子游戏比赛按钮").click()
                    time.sleep(3)
                    print ("进入比赛")
                    self.game_page.wait_element("比赛场返回").click()
                    time.sleep(3)
                else:
                    print("无比赛")
                self.game_page.wait_element("返回").click()
        else:
            print ("第一页没有血战到底，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                self.game_page.screenshot(".png")
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
                    if (self.game_page.is_exist("子游戏比赛按钮")==True):
                        self.game_page.get_element("子游戏比赛按钮").click()
                        time.sleep(3)
                        print ("进入比赛")
                        self.game_page.wait_element("比赛场返回").click()
                        time.sleep(3)
                    else:
                        print("无比赛")
                    self.game_page.wait_element("返回").click()
                else:
                    print ("血战到底已下载")
                    self.game_page.screenshot(".png")
                    if (self.game_page.is_exist("子游戏比赛按钮")==True):
                        self.game_page.get_element("子游戏比赛按钮").click()
                        time.sleep(3)
                        print ("进入比赛")
                        self.game_page.wait_element("比赛场返回").click()
                        time.sleep(3)
                    else:
                        print("无比赛")
                    self.game_page.wait_element("返回").click()
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有血战到底游戏")

        self.start_step("点击进入血流成河")
        if (self.game_page.is_exist("血流成河") == True):
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                if (self.game_page.is_exist("子游戏比赛按钮")==True):
                    self.game_page.get_element("子游戏比赛按钮").click()
                    time.sleep(3)
                    print ("进入比赛")
                    self.game_page.wait_element("比赛场返回").click()
                    time.sleep(3)
                else:
                    print("无比赛")
                self.game_page.wait_element("返回").click()
            else:
                print ("血战到底已下载")
                if (self.game_page.is_exist("子游戏比赛按钮")==True):
                    self.game_page.get_element("子游戏比赛按钮").click()
                    time.sleep(3)
                    print ("进入比赛")
                    self.game_page.wait_element("比赛场返回").click()
                    time.sleep(3)
                else:
                    print("无比赛")
                self.game_page.wait_element("返回").click()
        else:
            print ("第一页没有血流成河，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血流成河") == True):
                self.game_page.wait_element("血流成河").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
                    if (self.game_page.is_exist("子游戏比赛按钮")==True):
                        self.game_page.get_element("子游戏比赛按钮").click()
                        time.sleep(3)
                        print ("进入比赛")
                        self.game_page.wait_element("比赛场返回").click()
                        time.sleep(3)
                    else:
                        print("无比赛")
                    self.game_page.wait_element("返回").click()
                else:
                    print ("血流成河已下载")
                    if (self.game_page.is_exist("子游戏比赛按钮")==True):
                        self.game_page.get_element("子游戏比赛按钮").click()
                        time.sleep(3)
                        print ("进入比赛")
                        self.game_page.wait_element("比赛场返回").click()
                        time.sleep(3)
                    else:
                        print("无比赛")
                    self.game_page.wait_element("返回").click()
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有血流成河游戏")
                self.game_page.wait_element("左三角标").click()

        self.start_step("点击进入川味斗地主")
        self.start_step("点击川味斗地主：")
        if (self.game_page.is_exist("点击川味斗地主") == True):
            self.game_page.wait_element("川味斗地主").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                if (self.game_page.is_exist("子游戏比赛按钮")==True):
                    self.game_page.get_element("子游戏比赛按钮").click()
                    time.sleep(3)
                    print ("进入比赛")
                    self.game_page.wait_element("比赛场返回").click()
                    time.sleep(3)
                else:
                    print("无比赛")
                self.game_page.wait_element("返回").click()
            else:
                print ("川味斗地主已下载")
                if (self.game_page.is_exist("子游戏比赛按钮")==True):
                    self.game_page.get_element("子游戏比赛按钮").click()
                    time.sleep(3)
                    print ("进入比赛")
                    self.game_page.wait_element("比赛场返回").click()
                    time.sleep(3)
                else:
                    print("无比赛")
                self.game_page.wait_element("返回").click()
        else:
            print ("第一页没有川味斗地主，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("川味斗地主") == True):
                self.game_page.wait_element("川味斗地主").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
                    if (self.game_page.is_exist("子游戏比赛按钮")==True):
                        self.game_page.get_element("子游戏比赛按钮").click()
                        time.sleep(3)
                        print ("进入比赛")
                        self.game_page.wait_element("比赛场返回").click()
                        time.sleep(3)
                    else:
                        print("无比赛")
                    self.game_page.wait_element("返回").click()
                else:
                    print ("川味斗地主已下载")
                    if (self.game_page.is_exist("子游戏比赛按钮")==True):
                        self.game_page.get_element("子游戏比赛按钮").click()
                        time.sleep(3)
                        print ("进入比赛")
                        self.game_page.wait_element("比赛场返回").click()
                        time.sleep(3)
                    else:
                        print("无比赛")
                    self.game_page.wait_element("返回").click()

                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有川味斗地主游戏")
                self.game_page.wait_element("左三角标").click()

        self.start_step("点击进入斗牛")
        if (self.game_page.is_exist("斗牛") == True):
            self.game_page.wait_element("斗牛").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                if (self.game_page.is_exist("子游戏比赛按钮") == True):
                    self.game_page.get_element("子游戏比赛按钮").click()
                    time.sleep(3)
                    print ("进入比赛")
                    self.game_page.wait_element("比赛场返回").click()
                    time.sleep(3)
                else:
                    print("无比赛")
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                print ("斗牛已下载")
                if (self.game_page.is_exist("子游戏比赛按钮") == True):
                    self.game_page.get_element("子游戏比赛按钮").click()
                    time.sleep(3)
                    print ("进入比赛")
                    self.game_page.wait_element("比赛场返回").click()
                    time.sleep(3)
                else:
                    print("无比赛")
                self.game_page.wait_element("返回").click()
                time.sleep(2)
        else:
            print ("第一页没有斗牛，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("斗牛") == True):
                self.game_page.wait_element("斗牛").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(15)
                    if (self.game_page.is_exist("子游戏比赛按钮") == True):
                        self.game_page.get_element("子游戏比赛按钮").click()
                        time.sleep(3)
                        print ("进入比赛")
                        self.game_page.wait_element("比赛场返回").click()
                        time.sleep(3)
                    else:
                        print("无比赛")
                    self.game_page.wait_element("返回").click()
                else:
                    print ("斗牛已下载")
                    if (self.game_page.is_exist("子游戏比赛按钮") == True):
                        self.game_page.get_element("子游戏比赛按钮").click()
                        time.sleep(3)
                        print ("进入比赛")
                        self.game_page.wait_element("比赛场返回").click()
                        time.sleep(3)
                    else:
                        print("无比赛")
                    self.game_page.wait_element("返回").click()
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有斗牛游戏")
                self.game_page.wait_element("左三角标").click()


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C093_DFQP_GameListUserinfo(TestCase):
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
        self.common.closeactivityprepublish(self.luadriver)
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
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.start_step("查看个人资料")
                self.game_page.wait_element("头像").click()
                time.sleep(3)
                self.game_page.screenshot(".png")
                time.sleep(3)
                self.game_page.wait_element("关闭对话框").click()
                time.sleep(2)
                self.game_page.wait_element("返回").click()
            else:
                print ("血战到底已下载")
                time.sleep(3)
                self.start_step("查看个人资料")
                self.game_page.wait_element("头像").click()
                time.sleep(3)
                self.game_page.screenshot(".png")
                time.sleep(3)
                self.game_page.wait_element("关闭对话框").click()
                time.sleep(2)
                self.game_page.wait_element("返回").click()

        else:
            print ("第一页没有血战到底，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
                    self.start_step("查看个人资料")
                    self.game_page.wait_element("头像").click()
                    time.sleep(3)
                    self.game_page.screenshot(".png")
                    time.sleep(3)
                    self.game_page.wait_element("关闭对话框").click()
                    time.sleep(2)
                    self.game_page.wait_element("返回").click()
                    time.sleep(2)
                else:
                    print ("血战到底已下载")
                    time.sleep(3)
                    self.start_step("查看个人资料")
                    self.game_page.wait_element("头像").click()
                    time.sleep(3)
                    self.game_page.screenshot(".png")
                    time.sleep(3)
                    self.game_page.wait_element("关闭对话框").click()
                    time.sleep(2)
                    self.game_page.wait_element("返回").click()
                    time.sleep(2)
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C094_DFQP_GameListGold(TestCase):
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
        self.common.closeactivityprepublish(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("点击二七十：")
        if (self.game_page.is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("快捷支付")
                self.game_page.wait_element("+金币").click()
                time.sleep(5)
                self.game_page.screenshot("1.png")
                self.game_page.wait_element("绿色箭头返回").click()
                time.sleep(5)
                self.game_page.wait_element("+金条").click()
                time.sleep(5)
                self.game_page.screenshot("2.png")
                self.game_page.wait_element("绿色箭头返回").click()
                time.sleep(5)
                self.game_page.wait_element("返回").click()
                time.sleep(3)
            else:
                print ("二七十已下载")
                time.sleep(3)
                self.start_step("快捷支付")
                self.game_page.wait_element("+金币").click()
                time.sleep(5)
                self.game_page.screenshot("1.png")
                self.game_page.wait_element("绿色箭头返回").click()
                time.sleep(5)
                self.game_page.wait_element("+金条").click()
                time.sleep(5)
                self.game_page.screenshot("2.png")
                self.game_page.wait_element("绿色箭头返回").click()
                time.sleep(5)
                self.game_page.wait_element("返回").click()
                time.sleep(3)

        else:
            print ("第一页没有二七十，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("二七十") == True):
                self.game_page.wait_element("二七十").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(15)
                    self.start_step("快捷支付")
                    self.game_page.wait_element("+金币").click()
                    time.sleep(5)
                    self.game_page.screenshot("1.png")
                    self.game_page.wait_element("绿色箭头返回").click()
                    time.sleep(5)
                    self.game_page.wait_element("+金条").click()
                    time.sleep(5)
                    self.game_page.screenshot("2.png")
                    self.game_page.wait_element("绿色箭头返回").click()
                    time.sleep(5)
                    self.game_page.wait_element("返回").click()

                else:
                    print ("二七十已下载")
                    time.sleep(3)
                    self.start_step("快捷支付")
                    self.game_page.wait_element("+金币").click()
                    time.sleep(5)
                    self.game_page.screenshot("1.png")
                    self.game_page.wait_element("绿色箭头返回").click()
                    time.sleep(5)
                    self.game_page.wait_element("+金条").click()
                    time.sleep(5)
                    self.game_page.screenshot("2.png")
                    self.game_page.wait_element("绿色箭头返回").click()
                    time.sleep(5)
                    self.game_page.wait_element("返回").click()
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有二七十游戏")
                self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C095_DFQP_GamePlayList(TestCase):
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
        self.common.closeactivityprepublish(self.luadriver)
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
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                if (self.game_page.is_exist("玩法切换1") == True):
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
                print ("血战到底已下载")
                if (self.game_page.is_exist("玩法切换2") == True):
                    self.game_page.wait_element("玩法切换2").click()
                    time.sleep(2)
                    self.game_page.wait_element("玩法切换1").click()
                    time.sleep(2)
                    self.game_page.screenshot("1.png")
                    print ("玩法切换成功")
                    self.game_page.wait_element("返回").click()
                else:
                    print ("该游戏没有其他玩法")
                    self.game_page.screenshot("1.png")
                    time.sleep(3)
                    self.game_page.wait_element("返回").click()
        else:
            print ("第一页没有血战到底，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
                    if (self.game_page.is_exist("玩法切换1") == True):
                        self.game_page.wait_element("玩法切换2").click()
                        time.sleep(2)
                        self.game_page.wait_element("玩法切换1").click()
                        time.sleep(2)
                        self.game_page.screenshot("1.png")
                        print ("玩法切换成功")
                        self.game_page.wait_element("返回").click()
                    else:
                        print ("该游戏没有其他玩法")
                        self.game_page.screenshot("1.png")
                        self.game_page.wait_element("返回").click()
                else:
                    print ("血战到底已下载")
                    if (self.game_page.is_exist("玩法切换1") == True):
                        self.game_page.wait_element("玩法切换2").click()
                        time.sleep(2)
                        self.game_page.wait_element("玩法切换1").click()
                        time.sleep(2)
                        self.game_page.screenshot("1.png")
                        print ("玩法切换成功")
                        self.game_page.wait_element("返回").click()
                    else:
                        print ("该游戏没有其他玩法")
                        self.game_page.screenshot("1.png")
                        self.game_page.wait_element("返回").click()
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()

        self.start_step("点击斗牛")
        if (self.game_page.is_exist("斗牛") == True):
            self.game_page.wait_element("斗牛").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                if (self.game_page.is_exist("玩法切换1") == True):
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
                print ("斗牛已下载")
                if (self.game_page.is_exist("玩法切换1") == True):
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
            print ("第一页没有斗牛，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("斗牛") == True):
                self.game_page.wait_element("斗牛").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(15)
                    if (self.game_page.is_exist("玩法切换1") == True):
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
                    print ("斗牛已下载")
                    if (self.game_page.is_exist("玩法切换1") == True):
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
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有斗牛游戏")
                self.game_page.wait_element("左三角标").click()


        self.start_step("点击闷鸡")
        if (self.game_page.is_exist("闷鸡") == True):
            self.game_page.wait_element("闷鸡").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                if(self.game_page.is_exist("玩法切换4")==True):
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
                print ("闷鸡已下载")
                self.game_page.screenshot("3.png")
                if(self.game_page.is_exist("玩法切换4")==True):
                    self.game_page.wait_element("玩法切换2").click()
                    time.sleep(2)
                    self.game_page.wait_element("玩法切换3").click()
                    time.sleep(2)
                    self.game_page.wait_element("玩法切换4").click()
                    time.sleep(2)
                    self.game_page.wait_element("玩法切换1").click()
                    time.sleep(2)
                    print ("玩法切换成功")
                    self.game_page.wait_element("返回").click()
                    time.sleep(2)
                else:
                    print ("该游戏没有其他玩法")
                    self.game_page.wait_element("返回").click()
        else:
            print ("第一页没有闷鸡，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("闷鸡") == True):
                self.game_page.wait_element("闷鸡").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(15)
                    if(self.game_page.is_exist("玩法切换4")==True):
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
                        self.game_page.wait_element("返回").click()
                else:
                    print ("闷鸡已下载")
                    self.game_page.screenshot("3.png")
                    if(self.game_page.is_exist("玩法切换4")==True):
                        self.game_page.wait_element("玩法切换2").click()
                        time.sleep(2)
                        self.game_page.wait_element("玩法切换3").click()
                        time.sleep(2)
                        self.game_page.wait_element("玩法切换4").click()
                        time.sleep(2)
                        self.game_page.wait_element("玩法切换1").click()
                        time.sleep(2)
                        print ("玩法切换成功")
                        self.game_page.wait_element("返回").click()
                        time.sleep(2)
                    else:
                        print ("该游戏没有其他玩法")
                        self.game_page.wait_element("返回").click()
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有闷鸡游戏")
                self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C096_DFQP_GameRoom1(TestCase):
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
        self.common.closeactivityprepublish(self.luadriver)
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
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.game_page.screenshot(".png")
                time.sleep(3)
                self.game_page.wait_element("菜单").click()
                time.sleep(2)
                self.game_page.wait_element("退出房间").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(3)
                self.luadriver.keyevent(4)
                time.sleep(3)
                self.game_page.wait_element("返回").click()
            else:
                print ("血战到底已下载")
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.game_page.screenshot(".png")
                time.sleep(3)
                self.game_page.wait_element("菜单").click()
                time.sleep(2)
                self.game_page.wait_element("退出房间").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(3)
                self.luadriver.keyevent(4)
                time.sleep(3)
                self.game_page.wait_element("返回").click()
        else:
            print ("第一页没有血战到底，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
                    self.game_page.wait_element("快速开始").click()
                    time.sleep(3)
                    self.game_page.screenshot(".png")
                    time.sleep(3)
                    self.game_page.wait_element("菜单").click()
                    time.sleep(2)
                    self.game_page.wait_element("退出房间").click()
                    time.sleep(2)
                    self.luadriver.keyevent(4)
                    time.sleep(3)
                    self.luadriver.keyevent(4)
                    time.sleep(3)
                    self.game_page.wait_element("返回").click()
                else:
                    print ("血战到底已下载")
                    self.game_page.wait_element("快速开始").click()
                    time.sleep(3)
                    self.game_page.screenshot(".png")
                    time.sleep(3)
                    self.game_page.wait_element("菜单").click()
                    time.sleep(2)
                    self.game_page.wait_element("退出房间").click()
                    time.sleep(2)
                    self.luadriver.keyevent(4)
                    time.sleep(3)
                    self.luadriver.keyevent(4)
                    time.sleep(3)
                    self.game_page.wait_element("返回").click()
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C097_DFQP_GameList_MoreGames(TestCase):
    '''
    更多游戏
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
        self.common.closeactivityprepublish(self.luadriver)

        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.startStep = ("等待页面加载完成")
        time.sleep(10)

        self.hall_page.wait_element("同步标志")
        self.game_page.wait_element("右三角标").click()
        time.sleep(2)
        self.start_step("点击第二页的更多游戏")
        self.start_step("点击更多游戏")
        self.game_page.wait_element("更多游戏").click()
        time.sleep(3)
        self.game_page.screenshot("1.png")
        self.game_page.wait_element("更多游戏[1]").click()
        try:

            self.game_page.wait_element("更多游戏关闭下载弹框").click()
            time.sleep(3)
            self.game_page.wait_element("更多游戏[1]").click()
            time.sleep(3)
            self.game_page.wait_element("更多游戏-立刻下载").click()
            time.sleep(10)
            print ("游戏下载成功")
            #self.game_page.wait_element("返回").click()
        except:
            print("游戏已下载")
            time.sleep(5)
            self.game_page.wait_element("返回").click()
        time.sleep(3)

        self.game_page.wait_element("更多游戏[2]").click()

        try:
            self.game_page.wait_element("更多游戏关闭下载弹框").click()
            time.sleep(3)
            self.game_page.wait_element("更多游戏[2]").click()
            time.sleep(3)
            self.game_page.wait_element("更多游戏-立刻下载").click()
            time.sleep(10)
            print ("游戏下载成功")
            self.game_page.wait_element("更多游戏[2]").click()
            self.game_page.wait_element("返回").click()

        except:
            print("游戏已下载")
            self.game_page.wait_element("返回").click()
        time.sleep(3)

        self.game_page.wait_element("更多游戏[3]").click()
        try:
            self.game_page.wait_element("更多游戏关闭下载弹框").click()
            time.sleep(3)
            self.game_page.wait_element("更多游戏[3]").click()
            time.sleep(3)
            self.game_page.wait_element("更多游戏-立刻下载").click()
            time.sleep(10)
            print ("游戏下载成功")
            self.game_page.wait_element("更多游戏[3]").click()
            self.game_page.wait_element("返回").click()

        except:

            print("游戏已下载")
            self.game_page.wait_element("返回").click()

        self.game_page.wait_element("更多游戏[4]").click()
        try:
            self.game_page.wait_element("更多游戏关闭下载弹框").click()
            time.sleep(3)
            self.game_page.wait_element("更多游戏[4]").click()
            time.sleep(3)
            self.game_page.wait_element("更多游戏-立刻下载").click()
            time.sleep(10)
            print ("游戏下载成功")
            self.game_page.wait_element("更多游戏[4]").click()
            self.game_page.wait_element("返回").click()

        except:
            print("游戏已下载")
            self.game_page.wait_element("返回").click()
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
        self.common.closedriver()

class C098_DFQP_GameRoom2(TestCase):
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
        self.common.closeactivityprepublish(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("点击血战到底：")
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
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
                print ("血战到底已下载")
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
                time.sleep(3)
        else:
            print ("第一页没有血战到底，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
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
                    time.sleep(3)
                else:
                    print ("血战到底已下载")
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
                    time.sleep(3)
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C099_DFQP_GameRoom3(TestCase):
    '''
    游戏房间内---点击头像
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
        self.common.closeactivityprepublish(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''

        self.start_step("点击血战到底：")
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
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
                print ("血战到底已下载")
                time.sleep(3)
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
            print ("第一页没有血战到底，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
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
                    print ("血战到底已下载")
                    time.sleep(3)
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
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C100_DFQP_GameRoom4(TestCase):
    '''
    游戏房间内---聊天
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
        self.common.closeactivityprepublish(self.luadriver)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("点击血战到底：")
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.start_step("点击聊天按钮")
                self.game_page.wait_element("房间聊天按钮").click()
                time.sleep(3)
                self.game_page.screenshot("1.png")
                self.game_page.wait_element("表情").click()
                time.sleep(2)
                self.game_page.wait_element("表情1").click()
                time.sleep(2)
                self.game_page.screenshot("2.png")
                self.game_page.wait_element("房间聊天按钮").click()
                time.sleep(3)
                # self.game_page.wait_element("聊天记录").click()
                # time.sleep(2)
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
                print ("血战到底已下载")
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.start_step("点击聊天按钮")
                self.game_page.wait_element("房间聊天按钮").click()
                time.sleep(3)
                self.game_page.screenshot("1.png")
                time.sleep(2)
                self.game_page.wait_element("表情").click()
                time.sleep(2)
                self.game_page.wait_element("表情1").click()
                time.sleep(2)
                self.game_page.screenshot("2.png")
                self.game_page.wait_element("房间聊天按钮").click()
                time.sleep(3)
                # self.game_page.wait_element("聊天记录").click()
                # time.sleep(2)
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
                time.sleep(2)
        else:
            print ("第一页没有血战到底，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
                    self.game_page.wait_element("快速开始").click()
                    time.sleep(3)
                    self.start_step("点击聊天按钮")
                    self.game_page.wait_element("房间聊天按钮").click()
                    time.sleep(3)
                    self.game_page.screenshot("1.png")
                    self.game_page.wait_element("表情").click()
                    time.sleep(2)
                    self.game_page.wait_element("表情1").click()
                    time.sleep(2)
                    self.game_page.screenshot("2.png")
                    self.game_page.wait_element("房间聊天按钮").click()
                    time.sleep(3)
                    # self.game_page.wait_element("聊天记录").click()
                    # time.sleep(2)
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
                    time.sleep(2)
                else:
                    print ("血战到底已下载")
                    self.game_page.wait_element("快速开始").click()
                    time.sleep(3)
                    self.start_step("点击聊天按钮")
                    self.game_page.wait_element("房间聊天按钮").click()
                    time.sleep(3)
                    self.game_page.screenshot("1.png")
                    self.game_page.wait_element("表情").click()
                    time.sleep(2)
                    self.game_page.wait_element("表情1").click()
                    time.sleep(2)
                    self.game_page.screenshot("2.png")
                    self.game_page.wait_element("房间聊天按钮").click()
                    time.sleep(3)
                    # self.game_page.wait_element("聊天记录").click()
                    # time.sleep(2)
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
                    time.sleep(2)
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C101_DFQP_GameRoom5(TestCase):
    '''
    游戏房间内---准备，换桌
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
        self.common.closeactivityprepublish(self.luadriver)
        time.sleep(10)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("点击血战到底：")
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.start_step("点击换桌")
                self.game_page.wait_element("换桌").click()
                time.sleep(3)
                self.start_step("点击准备")
                self.game_page.wait_element("准备").click()
                time.sleep(5)
                self.game_page.wait_element("菜单").click()
                time.sleep(2)
                self.game_page.wait_element("托管").click()
                time.sleep(3)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
            else:
                print ("血战到底已下载")
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.start_step("点击换桌")
                self.game_page.wait_element("换桌").click()
                time.sleep(3)
                self.start_step("点击准备")
                self.game_page.wait_element("准备").click()
                time.sleep(5)
                self.game_page.wait_element("菜单").click()
                time.sleep(2)
                self.game_page.wait_element("托管").click()
                time.sleep(3)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
        else:
            print ("第一页没有血战到底，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                if (self.game_page.is_exist("资源下载-确定") == True):
                    self.game_page.wait_element("资源下载-确定").click()
                    time.sleep(20)
                    self.game_page.wait_element("快速开始").click()
                    time.sleep(3)
                    self.start_step("点击换桌")
                    self.game_page.wait_element("换桌").click()
                    time.sleep(3)
                    self.start_step("点击准备")
                    self.game_page.wait_element("准备").click()
                    time.sleep(5)
                    self.game_page.wait_element("菜单").click()
                    time.sleep(2)
                    self.game_page.wait_element("托管").click()
                    time.sleep(3)
                    self.luadriver.keyevent(4)
                    time.sleep(2)
                    self.luadriver.keyevent(4)
                    time.sleep(2)
                    self.game_page.wait_element("返回").click()
                    time.sleep(2)
                else:
                    print ("血战到底已下载")
                    self.game_page.wait_element("快速开始").click()
                    time.sleep(3)
                    self.start_step("点击换桌")
                    self.game_page.wait_element("换桌").click()
                    time.sleep(3)
                    self.start_step("点击准备")
                    self.game_page.wait_element("准备").click()
                    time.sleep(5)
                    self.game_page.wait_element("菜单").click()
                    time.sleep(2)
                    self.game_page.wait_element("托管").click()
                    time.sleep(3)
                    self.luadriver.keyevent(4)
                    time.sleep(2)
                    self.luadriver.keyevent(4)
                    time.sleep(2)
                    self.game_page.wait_element("返回").click()
                    time.sleep(2)
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

__qtaf_seq_tests__ = [C101_DFQP_GameRoom5]

if __name__ == '__main__':
    debug_run_all()
























