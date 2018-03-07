#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
选房间入场
'''
import json
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from utils import constant
from utils.confighelper import ConfigHelper

from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common
from  uilib.game_page import Game_Page
from uilib.safebox_page import Safebox_Page
import test_datas
from datacenter import dataprovider
import common.Interface as PHPInterface

class C27363_Go_Broke(TestCase):
    '''
    携带银币不足最小房间下限时点击房间入场
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    def pre_test(self):
        try:
            self.common = Common()
            self.hall_page = Hall_Page()
            self.yuepai_page = Yuepai_Page()
            self.game_page = Game_Page()
            self.start_step("获取mid")
            global mid
            mid = self.common.get_config_value("casecfg", "mid")
            # self.start_step("携带10银币")
            # self.common.set_coin(mid=mid,value='10')
            # 初始化Luadriver
            self.start_step("初始化driver")
            self.luadriver = self.common.setupdriver()
            # 每个用例都需要关闭活动，把这个放在初始化里面实现
            self.common.closeactivity(self.luadriver)
        except:
            self.hall_page.get_element("重连游戏").click()

    def bian_li(self,isChange=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
        #得到大厅所有的游戏控件
            name = game_list[i].get_attribute("name")
            gameid = int(name[4:len(name)])
            gamecfg = PHPInterface.get_levelconfig(gameid, 0, 0, 12)
            # 获取场次配置信息
            low_limit = gamecfg.get("values", {"LOW_LIMIT": None}).get("LOW_LIMIT")
            # 初级场下限是%d
            self.common.set_coin(mid, low_limit -10)
            # 选取合适的银币数，少于入场下限
            self.common.switchserver()
            self.common.closeactivity(self.luadriver)
            if isChange and self.hall_page.element_is_exist("换页"):
                self.hall_page.wait_element("换页").click()
            game_list[i].click()
            time.sleep(4)
            try:
                self.game_page.game_is_download()
                #下载游戏
                time.sleep(2)
                self.hall_page.screenshot("%s_1.png" % game_list[i].get_attribute("name"))
                self.hall_page.wait_element("快速开始").click()
                self.hall_page.screenshot("%s_2.png" % game_list[i].get_attribute("name"))
                self.hall_page.wait_element("关闭对话框").click()
                if self.hall_page.wait_element("返回1") != None:
                    self.hall_page.wait_element("返回1").click()
            except:
                try:
                    self.hall_page.wait_element("重新获取").click()
                    self.hall_page.screenshot("%s_downloadfail.png" % game_list[i].get_attribute("name"))
                except:
                    self.log_info("重新获取元素並未存在")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("获取子游戏列表")
        self.bian_li()
        self.hall_page.wait_element("换页").click()
        self.bian_li(True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27364_Buy_Money(TestCase):
    '''
    银币不够入场界面购买银币
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("获取mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("携带5000银币")
        self.common.set_coin(mid=mid, value='3000')
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def action(self,isChange=False):
        #显示银币不够入场界面购买银币的界面
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            # 得到大厅所有的游戏控件
            # self.start_step("获取游戏id" %game_list[i].get_attribute("name"))
            name = game_list[i].get_attribute("name")
            gameid = int(name[4:len(name)])
            gamecfg = PHPInterface.get_levelconfig(gameid, 0, 0, 13)
            #获取场次配置信息
            low_limit = gamecfg.get("values", {"LOW_LIMIT": None}).get("LOW_LIMIT")
            #初级场下限是%d
            self.common.set_coin(mid, low_limit + 1)
            #选取合适的银币数
            self.common.switchserver()
            self.common.closeactivity(self.luadriver)

            if isChange and self.hall_page.element_is_exist("换页"):
                self.hall_page.wait_element("换页").click()
            try:
                game_list[i].click()
                time.sleep(2)
                self.game_page.game_is_download()
                ele = self.hall_page.get_elements("场次名称")
                ele[1].click()
                time.sleep(2)
                try:
                    if self.hall_page.element_is_exist("选择购买数量"):
                        self.hall_page.screenshot("%s_1.png" % game_list[i].get_attribute("name"))
                        ele = self.hall_page.get_elements("购买按钮")
                        ele[1].click()
                        time.sleep(2)
                        self.hall_page.screenshot("%s_2.png" % game_list[i].get_attribute("name"))
                except:
                    print "没有出现购买界面"
                try:
                    while(self.hall_page.element_is_exist("预发布") != True):
                        self.luadriver.back()
                        time.sleep(30)
                        #等待牌局打完
                except:
                    print "退出牌局失败"
                if self.hall_page.element_is_exist("关闭对话框"):
                    self.hall_page.wait_element("关闭对话框").click()
                elif self.hall_page.wait_element("返回1") != None:
                    self.hall_page.wait_element("返回1").click()
            except:
                try:
                    self.hall_page.wait_element("重新获取").click()
                    self.hall_page.screenshot("%s_downloadfail.png" % game_list[i].get_attribute("name"))
                except:
                    self.log_info("重新获取元素並未存在")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("获取子游戏列表")
        self.action()
        self.hall_page.wait_element("换页").click()
        self.action(True)


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.recover_user(mid)
        self.common.closedriver()

class C27361_Carry_Littlemony(TestCase):
    '''
    携带1000银币点击游戏位
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.start_step("获取mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("携带1000银币")
        self.common.set_coin(mid=mid,value='1000')
        self.common.switchserver()
        self.common.closeactivity(self.luadriver)

    def bian_li(self,isChange=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            if isChange and self.hall_page.element_is_exist("换页"):
                self.hall_page.wait_element("换页").click()
            try:
                game_list[i].click()
                time.sleep(2)
                self.game_page.game_is_download()
                time.sleep(2)
                self.hall_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                if self.hall_page.wait_element("返回1") != None:
                    self.hall_page.wait_element("返回1").click()
            except:
                try:
                    self.hall_page.wait_element("重新获取").click()
                    self.hall_page.screenshot("%s_downloadfail.png" % game_list[i].get_attribute("name"))
                except:
                    self.log_info("重新获取元素並未存在")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("获取子游戏列表")
        self.bian_li()
        self.hall_page.wait_element("换页").click()
        self.bian_li(True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C70531_Carry_Muchmoney(TestCase):
    '''
    携带高级场的银币数，点击初级场入场
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("获取mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("携带1000000银币")
        self.common.set_coin(mid=mid,value='1000000')
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def action(self,isChange=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            # 得到大厅所有的游戏控件
            if isChange and self.hall_page.element_is_exist("换页"):
                self.hall_page.wait_element("换页").click()
            try:
                game_list[i].click()
                time.sleep(2)
                self.game_page.game_is_download()
                time.sleep(4)
                ele = self.hall_page.get_elements("场次名称")
                ele[0].click()
                #点击初级场(存在直接进入房间的情况)
                try:
                    while(self.hall_page.element_is_exist("预发布") != True):
                        self.luadriver.back()
                        time.sleep(10)
                        print "等待牌局打完"
                except:
                    print "退出牌局失败"
                time.sleep(2)
                self.hall_page.screenshot("%s_1.png" % game_list[i].get_attribute("name"))
                time.sleep(2)
                if self.hall_page.element_is_exist("关闭对话框"):
                    self.hall_page.wait_element("关闭对话框").click()
                    self.hall_page.screenshot("%s_2.png" % game_list[i].get_attribute("name"))
                    time.sleep(2)
                    self.hall_page.wait_element("返回1").click()

                # self.hall_page.wait_element("关闭对话框").click()
                # time.sleep(2)
                elif self.hall_page.element_is_exist("返回1"):
                    self.hall_page.wait_element("返回1").click()
            except:
                try:
                    self.hall_page.wait_element("重新获取").click()
                    self.hall_page.screenshot("%s_downloadfail.png" % game_list[i].get_attribute("name"))
                except:
                    self.log_info("重新获取元素並未存在")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("获取子游戏列表")
        self.action()
        self.hall_page.wait_element("换页").click()
        self.action(True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27360_Carry_Zeromony(TestCase):
    '''
    携带0银币点击游戏位
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("获取mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("携带0银币")
        self.common.set_coin(mid=mid,value='0')
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def bian_li(self,isChange=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            if isChange and self.hall_page.element_is_exist("换页"):
                self.hall_page.wait_element("换页").click()
            try:
                game_list[i].click()
                self.game_page.game_is_download()
                ele = self.hall_page.get_elements("场次名称")
                time.sleep(2)
                if len(ele) == 3:
                    ele[2].click()
                    time.sleep(3)
                    self.hall_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                elif len(ele) == 4:
                    ele[3].click()
                    time.sleep(3)
                    self.hall_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                else:
                    ele[1].click()
                    time.sleep(3)
                    self.hall_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                #点击高倍场
                time.sleep(4)
                self.hall_page.wait_element("关闭对话框").click()
                if self.hall_page.wait_element("返回1") != None:
                    self.hall_page.wait_element("返回1").click()
            except:
                try:
                    self.hall_page.wait_element("重新获取").click()
                    self.hall_page.screenshot("%s_downloadfail.png" % game_list[i].get_attribute("name"))
                except:
                    self.log_info("重新获取元素並未存在")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("获取子游戏列表")
        self.bian_li()
        self.hall_page.wait_element("换页").click()
        self.bian_li(True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C70531_Go_Higescreenings(TestCase):
    '''
    银币高出房间限制界面去高倍场
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("获取mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("携带10000000银币")
        self.common.set_coin(mid=mid,value='10000000')
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def action(self):
        self.hall_page.wait_element("菜单").click()
        self.hall_page.wait_element("退出").click()
        try:
            while (self.hall_page.element_is_exist("预发布") != True):
                self.luadriver.back()
                time.sleep(10)
                # 等待牌局打完
        except:
            print "退出牌局失败"

    def bian_li(self, isChange=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            try:
                if isChange and self.hall_page.element_is_exist("换页"):
                    self.hall_page.wait_element("换页").click()
                game_list[i].click()
                self.game_page.game_is_download()
                ele = self.hall_page.get_elements("场次名称")
                time.sleep(2)
                ele[0].click()
                try:
                    while(self.hall_page.element_is_exist("预发布") != True):
                        self.luadriver.back()
                        time.sleep(10)
                        #等待牌局打完
                except:
                    print "退出牌局失败"
                try:
                    if self.hall_page.element_is_exist("温馨提示"):
                        self.hall_page.screenshot("%s_MuchMoney.png" % game_list[i].get_attribute("name"))
                        self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "没有温馨提示框"
                try:
                    if len(ele) == 3:
                        ele[2].click()
                        time.sleep(3)
                        self.hall_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                        self.action()
                    elif len(ele) == 2:
                        ele[1].click()
                        time.sleep(3)
                        self.hall_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                        self.action()
                    else:
                        ele[3].click()
                        time.sleep(3)
                        self.hall_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                        self.action()
                except:
                    print "没有回到返回按钮界面"
                if self.hall_page.wait_element("返回1") != None:
                    self.hall_page.wait_element("返回1").click()
            except:
                try:
                    self.hall_page.wait_element("重新获取").click()
                    self.hall_page.screenshot("%s_downloadfail.png" % game_list[i].get_attribute("name"))
                except:
                    self.log_info("重新获取元素並未存在")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("获取子游戏列表")
        self.bian_li()
        self.hall_page.wait_element("换页").click()
        self.bian_li(True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C70531_Money_Test(TestCase):
    '''
    验证关闭银币不够入场界面提示
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("获取mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("携带3000银币")
        self.common.set_coin(mid=mid,value='3000')
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)


    def action(self, isChange=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            try:
                if isChange and self.hall_page.element_is_exist("换页"):
                    self.hall_page.wait_element("换页").click()
                    #判断是否需要换页
                game_list[i].click()
                time.sleep(2)
                self.game_page.game_is_download()
                time.sleep(2)
                ele = self.hall_page.get_elements("场次名称")
                time.sleep(2)
                ele[1].click()
                #携带三千银币，点击中级场
                time.sleep(2)
                #获取到资金不足界面
                try:
                    while (self.hall_page.element_is_exist("预发布") != True):
                        self.luadriver.back()
                        time.sleep(10)
                        # 等待牌局打完
                except:
                    print "退出牌局失败"
                self.hall_page.screenshot("%s_1.png" % game_list[i].get_attribute("name"))
                time.sleep(2)
                if self.hall_page.element_is_exist("关闭对话框"):
                    self.hall_page.wait_element("关闭对话框").click()
                #点击关闭按钮
                    self.hall_page.screenshot("%s_2.png" % game_list[i].get_attribute("name"))
                #截屏判断是否正常返回
                    time.sleep(2)
                elif self.hall_page.wait_element("返回1") != None:
                    self.hall_page.wait_element("返回1").click()
            except:
                try:
                    self.hall_page.wait_element("重新获取").click()
                    self.hall_page.screenshot("%s_downloadfail.png" % game_list[i].get_attribute("name"))
                except:
                    self.log_info("重新获取元素並未存在")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("获取子游戏列表")
        self.action()
        self.hall_page.wait_element("换页").click()
        self.action(True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27364_Money_Notenough(TestCase):
    '''
    携带银币少于入场下限但未破产情况下入场
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.start_step("获取mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.closeactivity(self.luadriver)

    def action(self):
        try:
            while (self.hall_page.element_is_exist("预发布") != True):
                self.luadriver.back()
                time.sleep(10)
                print "等待牌局打完"
        except:
            print "退出牌局失败"

    def bian_li(self, isChange=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            gameid_name = game_list[i].get_attribute("name")
            self.start_step("获取游戏ID: %s 初级场下限是" % gameid_name)
            gameid = int(gameid_name[4:len(gameid_name)])
            gamecfg = PHPInterface.get_levelconfig(gameid, 0, 0, 12)
            #获取入场下限的配置
            low_limit = gamecfg.get('values', {'LOW_LIMIT': None}).get('LOW_LIMIT')
            self.log_info("游戏ID: %s 初级场下限是%d" % (gameid_name, low_limit))
            self.common.set_coin(mid=mid, value= low_limit - 10)
            self.common.switchserver()
            self.common.closeActivityBtn()
            try:
                if isChange and self.hall_page.element_is_exist("换页"):
                    self.hall_page.wait_element("换页").click()
                #判断是否需要换页
                game_list[i].click()
                time.sleep(2)
                self.game_page.game_is_download()
                ele = self.hall_page.get_elements("场次名称")
                time.sleep(2)
                if len(ele) == 3:
                    ele[2].click()
                    time.sleep(3)
                    self.hall_page.screenshot("%s_Highscreen.png" % game_list[i].get_attribute("name"))
                    self.action()
                    #得到返回界面
                    time.sleep(2)
                elif len(ele) == 2:
                    ele[1].click()
                    time.sleep(3)
                    self.hall_page.screenshot("%s_Middlescreen.png" % game_list[i].get_attribute("name"))
                    self.action()
                    time.sleep(2)
                elif len(ele) == 1:
                    self.hall_page.screenshot("%s_NotHaveHighscreen.png" % game_list[i].get_attribute("name"))
                else:
                    ele[3].click()
                    time.sleep(3)
                    self.hall_page.screenshot("%s_Otherscreen.png" % game_list[i].get_attribute("name"))
                    self.action()
                    time.sleep(2)
                    #点击高级场
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                    self.yuepai_page.is_exist_yuepairoom()
                except:
                    print "退出房间失败"
                if self.hall_page.wait_element("返回1") != None:
                    self.hall_page.wait_element("返回1").click()
            except:
                try:
                    self.hall_page.wait_element("重新获取").click()
                    self.hall_page.screenshot("%s_downloadfail.png" % game_list[i].get_attribute("name"))
                except:
                    self.log_info("重新获取元素並未存在")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("获取子游戏列表")
        self.bian_li()
        self.hall_page.wait_element("换页").click()
        self.bian_li(True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C70531_Notbroke_Havesafebox(TestCase):
    '''
    携带银币大于破产线但不够入场，保险箱有钱情况下入场
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 20

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("获取mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_safeBoxMoney(mid, 10000000, money_type=0)
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def bian_li(self,isChange=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            gameid_name = game_list[i].get_attribute("name")
            self.start_step("获取游戏ID: %s 初级场下限是" % gameid_name)
            gameid = int(gameid_name[4:len(gameid_name)])
            gamecfg = PHPInterface.get_levelconfig(gameid, 0, 0, 12)
            low_limit = gamecfg.get('values', {'LOW_LIMIT': None}).get('LOW_LIMIT')
            self.log_info("游戏ID: %s 初级场下限是%d" % (gameid_name, low_limit))
            self.common.set_coin(mid=mid, value= low_limit - 10)
            self.common.switchserver()
            self.common.closeActivityBtn()
            try:
                if isChange and self.hall_page.element_is_exist("换页"):
                    self.hall_page.wait_element("换页").click()
                # 判断是否需要换页
                game_list[i].click()
                time.sleep(2)
                self.game_page.game_is_download()
                time.sleep(2)
                ele = self.hall_page.get_elements("场次名称")
                time.sleep(2)
                ele[1].click()
                #点击中级场
                try:
                    while (self.hall_page.element_is_exist("预发布") != True):
                        self.luadriver.back()
                        time.sleep(10)
                        print "等待牌局打完"
                except:
                    print "退出牌局失败"
                # 保险箱有钱，身上携带现金不够，点击中级场
                time.sleep(2)
                # 获取到进入该房间还需要xxx银币界面
                self.hall_page.screenshot("%s_1.png" % game_list[i].get_attribute("name"))
                time.sleep(2)
                if self.hall_page.element_is_exist("关闭对话框"):
                    self.hall_page.wait_element("关闭对话框").click()
                # 点击关闭按钮
                    time.sleep(2)
                elif self.hall_page.wait_element("返回1") != None:
                     self.hall_page.wait_element("返回1").click()
            except:
                try:
                    self.hall_page.wait_element("重新获取").click()
                    self.hall_page.screenshot("%s_downloadfail.png" % game_list[i].get_attribute("name"))
                except:
                    self.log_info("重新获取元素並未存在")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        #设置身上携带的银币数
        self.bian_li()
        self.hall_page.wait_element("换页").click()
        self.bian_li(True)


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.start_step("从保险箱取出银币")
        self.common.set_safeBoxMoney(mid, 0, 0)
        self.common.closedriver()

class C27362_Safebox_Havemony(TestCase):
    '''
   携带银币3000以下，保险箱存有银币时点击游戏位
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 20

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("获取mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_safeBoxMoney(mid, 3000, money_type=0)
        self.common.set_coin(mid=mid,value='2998')
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    # def set_safeboxmoney(self):
    #     #设置保险箱的银币数
    #     self.hall_page.wait_element("保险箱").click()
    #     time.sleep(4)
    #     self.hall_page.wait_element("存钱").click()
    #     time.sleep(4)
    #     self.common.swipeelement(self.hall_page.wait_element("滚动条"), self.hall_page.wait_element("添加"))
    #     self.hall_page.wait_element("确定按钮").click()
    #     time.sleep(3)
    #     self.hall_page.wait_element("空白页").click()
    #     time.sleep(3)
    #
    # def set_bodymoney(self):
    #     #设置自身携带的银币数
    #     self.start_step("获取mid")
    #     global mid
    #     mid = self.common.get_config_value("casecfg", "mid")
    #     self.start_step("携带3000银币")
    #     self.common.set_coin(mid=mid, value='250')
    #     time.sleep(3)
    #     self.common.switchserver()
    #     # 每个用例都需要关闭活动，把这个放在初始化里面实现
    #     self.common.closeactivity(self.luadriver)

    def bian_li(self,isChange=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            if isChange and self.hall_page.element_is_exist("换页"):
                self.hall_page.wait_element("换页").click()
            game_list[i].click()
            time.sleep(2)
            self.game_page.game_is_download()
            time.sleep(2)
            self.hall_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
            try:
                if self.hall_page.wait_element("返回1") != None:
                    self.hall_page.wait_element("返回1").click()
            except:
                try:
                    self.hall_page.wait_element("重新获取").click()
                    self.hall_page.screenshot("%s_downloadfail.png" % game_list[i].get_attribute("name"))
                except:
                    self.log_info("重新获取元素並未存在")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        # self.start_step("存钱到保险箱")
        # self.set_safeboxmoney()
        # self.set_bodymoney()
        self.start_step("获取子游戏列表")
        self.bian_li()
        self.hall_page.wait_element("换页").click()
        self.bian_li(True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.start_step("从保险箱取出银币")
        self.common.set_safeBoxMoney(mid, 0, 0)
        self.common.closedriver()

class C70531_Save_Money(TestCase):
    '''
    银币高出房间限制界面存钱入场
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 20

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        self.start_step("获取mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("携带1000000银币")
        self.common.set_coin(mid=mid,value='100000000')
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def action(self, isChange=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            # 得到大厅所有的游戏控件
            if isChange and self.hall_page.element_is_exist("换页"):
                self.hall_page.wait_element("换页").click()
            try:
                game_list[i].click()
                self.game_page.game_is_download()
                ele = self.hall_page.get_elements("场次名称")
                ele[0].click()
                # 点击初级场
                try:
                    self.hall_page.wait_element("存钱入场").click()
                except:
                    self.log_info("未出现存钱入场的按钮")
                time.sleep(3)
                self.hall_page.screenshot("%s_1.png" % game_list[i].get_attribute("name"))
                try:
                    self.yuepai_page.is_exist_yuepairoom()
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "退出房间失败"
                if self.hall_page.wait_element("返回1") != None:
                    self.hall_page.wait_element("返回1").click()
            except:
                try:
                    self.hall_page.wait_element("重新获取").click()
                    self.hall_page.screenshot("%s_downloadfail.png" % game_list[i].get_attribute("name"))
                except:
                    self.log_info("重新获取元素並未存在")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("获取子游戏列表")
        self.action()
        self.hall_page.wait_element("换页").click()
        self.action(True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.start_step("从保险箱取出银币")
        self.common.set_safeBoxMoney(mid, 0, 0)
        self.common.closedriver()

class C70531_Use_Safebox(TestCase):
    '''
    携带银币少于破产线，但保险箱有钱情况下入场
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 60

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    # def first_body(self,money):
    #     #设置自身携带银币数
    #     self.start_step("获取mid")
    #     self.common.set_coin(mid=mid,value=money)
    #     self.common.switchserver()
    #     self.common.closeActivityBtn()
    #
    # def safebox_money(self):
    #     self.start_step("存钱到保险箱")
    #     self.hall_page.wait_element("保险箱").click()
    #     self.hall_page.wait_element("存钱").click()
    #     self.common.swipeelement(self.hall_page.wait_element("滚动条"), self.hall_page.wait_element("添加"))
    #     self.hall_page.wait_element("确定按钮").click()
    #     if self.hall_page.element_is_exist("存钱") ==True:
    #         self.hall_page.wait_element("空白页").click()

    def action(self,isChange=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            # 得到大厅所有的游戏控件
            # self.first_body("35000")
            self.common.set_coin(mid=mid, value="1000")
            self.common.set_safeBoxMoney(mid,34000,money_type=0)
            self.common.switchserver()
            self.common.closeActivityBtn()
            # # 首先设置初始自身携带的银币数
            # self.safebox_money()
            # # 将自身携带的银币数存入保险箱
            # self.first_body("1000")
            # 再次设置自身携带的银币数
            # if isChange and self.hall_page.element_is_exist("换页"):
            #     self.hall_page.wait_element("换页").click()
            try:
                game_list[i].click()
                self.game_page.game_is_download()
                ele = self.hall_page.get_elements("场次名称")
                ele[0].click()
                #点击初级场
                self.hall_page.screenshot("%s_1.png" % game_list[i].get_attribute("name"))
                self.hall_page.wait_element("关闭按钮").click()
                #判断点击关闭按钮是否可以正常返回
                ele[0].click()
                # 点击初级场
                self.hall_page.wait_element("打开保险箱").click()
                self.hall_page.wait_element("取出").click()
                self.common.swipeelement(self.hall_page.wait_element("滚动条"), self.hall_page.wait_element("添加"))
                self.hall_page.wait_element("确定按钮").click()
                self.hall_page.wait_element("頭像").click()
                ele[0].click()
                # 点击初级场
                self.hall_page.screenshot("%s_2.png" % game_list[i].get_attribute("name"))
                try:
                    self.start_step("退出房间")
                    self.yuepai_page.is_exist_yuepairoom()
                    self.game_page.wait_element("返回1").click()
                    if isChange == True:
                        self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                        try:
                            self.game_page.wait_element("右三角标").click()
                        except:
                            self.log_info("当前为第二页")
                except:
                    self.log_info("未找到元素")
            except:
                try:
                    self.hall_page.wait_element("重新获取").click()
                    self.hall_page.screenshot("%s_1.png" % game_list[i].get_attribute("name"))
                except:
                    print "截图失败"

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        # self.start_step("存钱到保险箱")
        self.action()
        self.hall_page.wait_element("换页").click()
        self.action(True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.start_step("从保险箱取出银币")
        self.common.set_safeBoxMoney(mid, 0, 0)
        self.common.closedriver()

__qtaf_seq_tests__ = [C70531_Use_Safebox]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
    # print PHPInterface.get_mid(2430929, 20)
    # mid = Common().get_config_value("casecfg", "mid")
    # Common().set_coin(mid, 3000)
    # PHPInterface.get_levelconfig()
