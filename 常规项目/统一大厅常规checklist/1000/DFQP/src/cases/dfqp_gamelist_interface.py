#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Author: MindyZhang
'''
大厅子游戏接口配置相关用例
'''
import time
from runcenter.enums import EnumStatus,EnumPriority
from runcenter.testcase import debug_run_all,TestCase
from common.common import Common
from appiumcenter.luadriver import LuaDriver
from uilib.hall_page import Hall_Page
from uilib.game_page import Game_Page
from uilib.safebox_page import Safebox_Page
from uilib.personinfo_page import Personinfo_Page
import common.Interface as PHPInterface
import json
import test_datas
from datacenter import dataprovider

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C089_DFQP_GameList_DownLoad1(TestCase):
    '''
    大厅子游戏下载---破产账号
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10


    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化Luadriver
        capabilities = {}
        capabilities['noReset'] = False    #清除已下载游戏
        capabilities['resetKeyboard'] = False
        self.luadriver = self.common.setupdriver(capabilities)
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        time.sleep(10)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()

        # 获取用户信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print ('current_coin:',coin)
        if (coin>0):
            result_bankrupt = PHPInterface.set_user_bankrupt(self.casedata['mid'])
            print (result_bankrupt)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.luadriver.keyevent(4)

    def run_test(self):
        self.startStep = ("等待页面加载完成")
        time.sleep(10)
        self.hall_page.wait_element("同步标志")
        self.start_step("点击川味斗地主：")
        if (self.game_page.is_exist("点击川味斗地主")==True):
            self.game_page.wait_element("川味斗地主").click()
            time.sleep(3)
            self.game_page.wait_element("资源下载-确定").click()
            time.sleep(15)
            self.game_page.wait_element("返回").click()

        elif(self.game_page.is_exist("川味斗地主")==False):
            print ("第一页没有川味斗地主，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("川味斗地主")==True):
                self.game_page.wait_element("川味斗地主").click()
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有川味斗地主游戏")
                self.game_page.wait_element("左三角标").click()
                time.sleep(2)

        self.start_step("点击血战到底：")
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            self.game_page.wait_element("资源下载-确定").click()
            time.sleep(15)
            self.game_page.wait_element("返回").click()

        elif (self.game_page.is_exist("血战到底") == False):
            print ("第一页没有血战到底，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()
                time.sleep(2)

        self.start_step("点击血流成河：")
        if (self.game_page.is_exist("血流成河")==True):
            self.game_page.wait_element("血流成河").click()
            time.sleep(3)
            self.game_page.wait_element("资源下载-确定").click()
            time.sleep(15)
            self.game_page.wait_element("返回").click()
            time.sleep(2)

        elif(self.game_page.is_exist("血流成河")==False):
            print ("第一页没有血流成河，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("血流成河")==True):
                self.game_page.wait_element("血流成河").click()
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
                time.sleep(2)
            else:
                print ("没有血流成河游戏")
                self.game_page.wait_element("左三角标").click()
                time.sleep(2)

        self.start_step("点击斗牛：")
        if (self.game_page.is_exist("斗牛") == True):
            self.game_page.wait_element("斗牛").click()
            time.sleep(3)
            self.game_page.wait_element("资源下载-确定").click()
            time.sleep(15)
            self.game_page.wait_element("返回").click()
            time.sleep(2)

        elif (self.game_page.is_exist("斗牛") == False):
            print ("第一页没有斗牛，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("斗牛") == True):
                self.game_page.wait_element("斗牛").click()
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
                time.sleep(2)
            else:
                print ("没有斗牛游戏")
                self.game_page.wait_element("左三角标").click()
                time.sleep(2)

        self.start_step("点击二七十：")
        if (self.game_page.is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(3)
            self.game_page.wait_element("资源下载-确定").click()
            time.sleep(15)
            self.game_page.wait_element("返回").click()
            time.sleep(2)

        elif (self.game_page.is_exist("二七十") == False):
            print ("第一页没有二七十，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("二七十") == True):
                self.game_page.wait_element("二七十").click()
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
                time.sleep(2)
            else:
                print ("没有二七十游戏")
                self.game_page.wait_element("左三角标").click()
                time.sleep(2)


        self.start_step("点击拖拉机：")
        if (self.game_page.is_exist("拖拉机") == True):
            self.game_page.wait_element("拖拉机").click()
            time.sleep(3)
            self.game_page.wait_element("资源下载-确定").click()
            time.sleep(15)
            self.game_page.wait_element("返回").click()
            time.sleep(2)

        elif (self.game_page.is_exist("拖拉机") == False):
            print ("第一页没有拖拉机，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("拖拉机") == True):
                self.game_page.wait_element("拖拉机").click()
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
                time.sleep(2)
            else:
                print ("没有拖拉机游戏")
                self.game_page.wait_element("左三角标").click()
                time.sleep(2)

        self.start_step("点击干瞪眼：")
        if (self.game_page.is_exist("干瞪眼") == True):
            self.game_page.wait_element("干瞪眼").click()
            time.sleep(3)
            self.game_page.wait_element("资源下载-确定").click()
            time.sleep(15)
            self.game_page.wait_element("返回").click()
            time.sleep(2)

        elif (self.game_page.is_exist("干瞪眼") == False):
            print ("第一页没有干瞪眼，进入第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("干瞪眼") == True):
                self.game_page.wait_element("干瞪眼").click()
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
                time.sleep(2)
            else:
                print ("没有干瞪眼游戏")
                self.game_page.wait_element("左三角标").click()
                time.sleep(2)

        self.start_step("点击比赛场：")
        if (self.game_page.is_exist("比赛场") == True):
            self.game_page.wait_element("比赛场房间").click()
            time.sleep(5)
            self.game_page.wait_element("比赛场返回").click()
            time.sleep(3)
            self.luadriver.keyevent(4)
            time.sleep(2)

        elif (self.game_page.is_exist("比赛场") == False):
            print ("第一页没有比赛场，  第二页")
            self.game_page.wait_element("右三角标").click()
            if (self.game_page.is_exist("比赛场") == True):
                self.game_page.wait_element("比赛场房间").click()
                time.sleep(5)
                self.game_page.wait_element("比赛场返回").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("左三角标").click()
                time.sleep(2)
            else:
                print ("没有比赛场")
                self.game_page.wait_element("左三角标").click()
                time.sleep(2)

        # self.start_step("点击约牌房：")
        # # if (self.game_page.is_exist("约牌") == True):
        # try:
        #     self.game_page.wait_element("约牌").click()
        #     time.sleep(3)
        #     self.game_page.wait_element("绿色箭头返回").click()
        #     time.sleep(2)
        #     self.luadriver.keyevent(4)
        #     time.sleep(2)
        #
        # # elif (self.game_page.is_exist("约牌") == False):
        # except:
        #     print ("第一页没有约牌房，  第二页")
        #     self.game_page.wait_element("右三角标").click()
        #     if (self.game_page.is_exist("约牌") == True):
        #         self.game_page.wait_element("约牌").click()
        #
        #         self.game_page.wait_element("绿色箭头返回").click()
        #         time.sleep(2)
        #         self.luadriver.keyevent(4)
        #         time.sleep(2)
        #         self.game_page.wait_element("左三角标").click()
        #     else:
        #         print ("没有约牌房")
        #         self.game_page.wait_element("左三角标").click()

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C089_DFQP_GameList_DownLoad2(TestCase):
      '''
      大厅子游戏下载---非破产账号
      '''
      owner = "MindyZhang"
      status = EnumStatus.Design
      priority = EnumPriority.High
      timeout = 10

      def pre_test(self):
          self.common = Common()
          self.hall_page = Hall_Page()
          self.game_page = Game_Page()
          self.personinfo_page = Personinfo_Page()
          # 初始化Luadriver
          capabilities = {}
          capabilities['noReset'] = False
          self.luadriver = self.common.setupdriver(capabilities)
          PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
          #关闭弹框
          self.common.closeactivityprepublish(self.luadriver)
          self.start_step("判断账号ID是否符合条件")
          self.personinfo_page.wait_element("头像").click()
          if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
              self.common.loginuser(self.casedata['user'], self.casedata['password'])
              self.common.closeactivityprepublish(self.luadriver)
          else:
              self.personinfo_page.wait_element("关闭").click()

          # 获取用户信息
          result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
          myuser_info = json.loads(result_userinfo)
          coin = myuser_info.get('result', {'coin': None}).get('coin')
          print (coin)
          if (coin<10000):
              PHPInterface.add_money(self.casedata['mid'], 10000)
              self.common.closedriver()
              self.luadriver = self.common.setupdriver()
              # 关闭弹框
              self.common.closeactivityprepublish(self.luadriver)

      def run_test(self):
          self.startStep = ("等待页面加载完成")
          time.sleep(3)
          self.hall_page.wait_element("同步标志")
          self.start_step("点击川味斗地主：")
          if (self.game_page.is_exist("点击川味斗地主") == True):
              self.game_page.wait_element("血点击川味斗地主").click()
              time.sleep(3)
              self.game_page.wait_element("资源下载-确定").click()
              time.sleep(15)
              self.game_page.wait_element("返回").click()

          elif (self.game_page.is_exist("川味斗地主") == False):
              print ("第一页没有川味斗地主，进入第二页")
              self.game_page.wait_element("右三角标").click()
              if (self.game_page.is_exist("川味斗地主") == True):
                  self.game_page.wait_element("川味斗地主").click()
                  self.game_page.wait_element("资源下载-确定").click()
                  time.sleep(15)
                  self.game_page.wait_element("返回").click()
                  time.sleep(2)
                  self.game_page.wait_element("左三角标").click()
              else:
                  print ("没有川味斗地主游戏")
                  self.game_page.wait_element("左三角标").click()

          self.start_step("点击血战到底：")
          if (self.game_page.is_exist("血战到底") == True):
              self.game_page.wait_element("血战到底").click()
              time.sleep(3)
              self.game_page.wait_element("资源下载-确定").click()
              time.sleep(15)
              self.game_page.wait_element("返回").click()

          elif (self.game_page.is_exist("血战到底") == False):
              print ("第一页没有血战到底，进入第二页")
              self.game_page.wait_element("右三角标").click()
              if (self.game_page.is_exist("血战到底") == True):
                  self.game_page.wait_element("血战到底").click()
                  self.game_page.wait_element("资源下载-确定").click()
                  time.sleep(15)
                  self.game_page.wait_element("返回").click()
                  time.sleep(2)
                  self.game_page.wait_element("左三角标").click()
              else:
                  print ("没有血战到底游戏")
                  self.game_page.wait_element("左三角标").click()

          self.start_step("点击血流成河：")
          if (self.game_page.is_exist("血流成河") == True):
              self.game_page.wait_element("血流成河").click()
              time.sleep(3)
              self.game_page.wait_element("资源下载-确定").click()
              time.sleep(15)
              self.game_page.wait_element("返回").click()

          elif (self.game_page.is_exist("血流成河") == False):
              print ("第一页没有血流成河，进入第二页")
              self.game_page.wait_element("右三角标").click()
              if (self.game_page.is_exist("血流成河") == True):
                  self.game_page.wait_element("血流成河").click()
                  self.game_page.wait_element("资源下载-确定").click()
                  time.sleep(15)
                  self.game_page.wait_element("返回").click()
                  time.sleep(2)
                  self.game_page.wait_element("左三角标").click()
              else:
                  print ("没有血流成河游戏")
                  self.game_page.wait_element("左三角标").click()

          self.start_step("点击斗牛：")
          if (self.game_page.is_exist("斗牛") == True):
              self.game_page.wait_element("斗牛").click()
              time.sleep(3)
              self.game_page.wait_element("资源下载-确定").click()
              time.sleep(15)
              self.game_page.wait_element("返回").click()

          elif (self.game_page.is_exist("斗牛") == False):
              print ("第一页没有斗牛，进入第二页")
              self.game_page.wait_element("右三角标").click()
              if (self.game_page.is_exist("斗牛") == True):
                  self.game_page.wait_element("斗牛").click()
                  self.game_page.wait_element("资源下载-确定").click()
                  time.sleep(15)
                  self.game_page.wait_element("返回").click()
                  time.sleep(2)
                  self.game_page.wait_element("左三角标").click()
              else:
                  print ("没有斗牛游戏")
                  self.game_page.wait_element("左三角标").click()

          self.start_step("点击二七十：")
          if (self.game_page.is_exist("二七十") == True):
              self.game_page.wait_element("二七十").click()
              time.sleep(3)
              self.game_page.wait_element("资源下载-确定").click()
              time.sleep(15)
              self.game_page.wait_element("返回").click()

          elif (self.game_page.is_exist("二七十") == False):
              print ("第一页没有二七十，进入第二页")
              self.game_page.wait_element("右三角标").click()
              if (self.game_page.is_exist("二七十") == True):
                  self.game_page.wait_element("二七十").click()
                  self.game_page.wait_element("资源下载-确定").click()
                  time.sleep(15)
                  self.game_page.wait_element("返回").click()
                  time.sleep(2)
                  self.game_page.wait_element("左三角标").click()
              else:
                  print ("没有二七十游戏")
                  self.game_page.wait_element("左三角标").click()

          self.start_step("点击拖拉机：")
          if (self.game_page.is_exist("拖拉机") == True):
              self.game_page.wait_element("拖拉机").click()
              time.sleep(3)
              self.game_page.wait_element("资源下载-确定").click()
              time.sleep(15)
              self.game_page.wait_element("返回").click()

          elif (self.game_page.is_exist("拖拉机") == False):
              print ("第一页没有拖拉机，进入第二页")
              self.game_page.wait_element("右三角标").click()
              if (self.game_page.is_exist("拖拉机") == True):
                  self.game_page.wait_element("拖拉机").click()
                  self.game_page.wait_element("资源下载-确定").click()
                  time.sleep(15)
                  self.game_page.wait_element("返回").click()
                  time.sleep(2)
                  self.game_page.wait_element("左三角标").click()
              else:
                  print ("没有拖拉机游戏")
                  self.game_page.wait_element("左三角标").click()

          self.start_step("点击干瞪眼：")
          if (self.game_page.is_exist("干瞪眼") == True):
              self.game_page.wait_element("干瞪眼").click()
              time.sleep(3)
              self.game_page.wait_element("资源下载-确定").click()
              time.sleep(15)
              self.game_page.wait_element("返回").click()

          elif (self.game_page.is_exist("干瞪眼") == False):
              print ("第一页没有干瞪眼，进入第二页")
              self.game_page.wait_element("右三角标").click()
              if (self.game_page.is_exist("干瞪眼") == True):
                  self.game_page.wait_element("干瞪眼").click()
                  self.game_page.wait_element("资源下载-确定").click()
                  time.sleep(15)
                  self.game_page.wait_element("返回").click()
                  time.sleep(2)
                  self.game_page.wait_element("左三角标").click()
              else:
                  print ("没有干瞪眼游戏")
                  self.game_page.wait_element("左三角标").click()

          self.start_step("点击比赛场：")
          if (self.game_page.is_exist("比赛场") == True):
              self.game_page.wait_element("比赛场房间").click()
              time.sleep(5)
              self.game_page.wait_element("比赛场返回").click()
              time.sleep(3)

          elif (self.game_page.is_exist("比赛场") == False):
              print ("第一页没有比赛场，  第二页")
              self.game_page.wait_element("右三角标").click()
              if (self.game_page.is_exist("比赛场") == True):
                  self.game_page.wait_element("比赛场房间").click()
                  time.sleep(5)
                  self.game_page.wait_element("比赛场返回").click()
                  time.sleep(2)
                  self.luadriver.keyevent(4)
                  self.game_page.wait_element("左三角标").click()
              else:
                  print ("没有比赛场")
                  self.game_page.wait_element("左三角标").click()

          # self.start_step("点击约牌房：")
          # if (self.game_page.is_exist("约牌") == True):
          #     self.game_page.wait_element("约牌").click()
          #     time.sleep(3)
          #     self.game_page.wait_element("绿色箭头返回").click()
          #
          # elif (self.game_page.is_exist("约牌") == False):
          #     print ("第一页没有约牌房，  第二页")
          #     self.game_page.wait_element("右三角标").click()
          #     if (self.game_page.is_exist("约牌") == True):
          #         self.game_page.wait_element("约牌").click()
          #
          #         self.game_page.wait_element("绿色箭头返回").click()
          #         time.sleep(2)
          #         self.game_page.wait_element("左三角标").click()
          #     else:
          #         print ("没有约牌房")
          #         self.game_page.wait_element("左三角标").click()

      def post_test(self):
          '''
          测试用例执行完成后，清理测试环境
          '''
          self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C090_DFQP_GameList_Game1(TestCase):
    '''
    子游戏列表显示---破产账号
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()

        # 获取用户信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print (coin)
        if (coin > 0):
            result_bankrupt = PHPInterface.set_user_bankrupt(self.casedata['mid'])
            print (result_bankrupt)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)
    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(3)
        self.start_step("点击进入游戏")
        if(self.game_page.is_exist("血流成河")==True):
            self.game_page.wait_element("血流成河").click()
            time.sleep(2)
            if(self.game_page.is_exist("资源下载-确定")==True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.screenshot("Game1.png")
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                self.game_page.screenshot("Game1.png")
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("血流成河").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.screenshot("Game1.png")
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                self.game_page.screenshot("Game1.png")
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C090_DFQP_GameList_Game2(TestCase):
    '''
    子游戏列表显示---非破产账号
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()
        # 获取用户信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print (coin)
        if (coin < 10000):
            PHPInterface.add_money(self.casedata['mid'], 10000)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''

        self.start_step("等待页面加载完成")
        time.sleep(3)
        self.hall_page.wait_element("同步标志")
        time.sleep(3)
        self.start_step("点击进入游戏")
        if (self.game_page.is_exist("血流成河") == True):
            self.game_page.wait_element("血流成河").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.screenshot("Game2.png")
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                self.game_page.screenshot("Game2.png")
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("血流成河").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.screenshot("Game2.png")
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                self.game_page.screenshot("Game2.png")
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C102_DFQP_Game_Faststart1(TestCase):
    '''
    快速开始---银币场，玩家银币破产，快递开始弹破产弹框
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()

        # 获取用户信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print (coin)
        if (coin > 0):
            result_bankrupt = PHPInterface.set_user_bankrupt(self.casedata['mid'])
            print (result_bankrupt)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.luadriver.keyevent(4)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏血流成河")
        if (self.game_page.is_exist("血流成河") == True):
            self.game_page.wait_element("血流成河").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart1.png")
                self.game_page.wait_element("关闭对话框").click()
            else:
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart1.png")
                self.game_page.wait_element("关闭对话框").click()
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("血流成河").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart1.png")
                self.game_page.wait_element("关闭对话框").click()
            else:
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart1.png")
                self.game_page.wait_element("关闭对话框").click()

    def post_test(self):
        #清理测试环境
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C103_DFQP_Game_Faststart2(TestCase):
    '''
    快速开始---银币场，玩家银币足够,快速开始进入房间
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        time.sleep(10)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()
        # 获取用户信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print (coin)
        if (coin < 10000):
            PHPInterface.add_money(self.casedata['mid'], 20000)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏血战到底")
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart2.png")
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()

            else:
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart2.png")
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("血战到底").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart2.png")
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()
            else:
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart2.png")
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()

    def post_test(self):
        # 清理测试环境
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C104_DFQP_Game_Faststart3(TestCase):
    '''
    快速开始---金条场，玩家银币破产，金条不足，弹金条充值弹框
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()
        # 获取用户信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print (crystal)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print (coin)
        # 设置金条和银币数量
        if (crystal>0):
            result_crystal = PHPInterface.add_crystal(self.casedata['mid'], -crystal)
            print (result_crystal)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)
        if (coin > 0):
            result_coin = PHPInterface.set_user_bankrupt(self.casedata['mid'])
            print (result_coin)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.luadriver.keyevent(4)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏二七十")
        if (self.game_page.is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(5)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.game_page.wait_element("金条场").click()
                time.sleep(3)
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("关闭对话框").click()
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                self.game_page.wait_element("金条场").click()
                time.sleep(3)
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("关闭对话框").click()
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击快速开始")
                self.game_page.wait_element("金条场").click()
                time.sleep(3)
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("关闭对话框").click()
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                self.start_step("点击快速开始")
                self.game_page.wait_element("金条场").click()
                time.sleep(3)
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("关闭对话框").click()
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)

    def post_test(self):
        # 清理测试环境
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C105_DFQP_Game_Faststart4(TestCase):
    '''
    快速开始---金条场，玩家金条不足,弹充值弹框
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()

        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        crystal = myuser_info.get('result',{'crystal':None}).get('crystal')
        print (crystal)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        if (coin <= 0):
            PHPInterface.add_money(self.casedata['mid'],10000) #保证玩家未破产
        # if (crystal>0):
        #     result_crystal = PHPInterface.add_crystal(self.casedata['mid'], -crystal)
        #     print (result_crystal)
        #从保险箱取出所有金条
        self.hall_page.wait_element("保险箱").click()
        time.sleep(2)
        self.safebox_page.wait_element("金条保险箱").click()
        time.sleep(2)
        self.safebox_page.wait_element("取出").click()
        if (self.safebox_page.is_exist("确定---保险箱")):
            slider = self.safebox_page.wait_element("滚动条")
            addgoldbtn = self.safebox_page.wait_element("增加金条/银条数目")
            x = slider.location['x']
            y = slider.location['y']
            x1 = addgoldbtn.location['x']
            y1 = addgoldbtn.location['y']
            self.luadriver.swipe(x,y,x1,y1)
            self.safebox_page.wait_element("确定---保险箱").click()
            time.sleep(2)
            self.luadriver.keyevent(4)
        else:
            print ("保险箱没有存款")
            self.luadriver.keyevent(4)
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        crystal1 = myuser_info.get('result', {'crystal': None}).get('crystal')
        print (crystal1)
        # 设置金条满足用例条件，重启游戏
        if(crystal1>0):
            PHPInterface.add_crystal(self.casedata['mid'], -crystal1)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            self.common.closeactivityprepublish(self.luadriver)
    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏二七十")
        if (self.game_page.is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.wait_element("金条场").click()
                time.sleep(1)
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("关闭对话框").click()
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                self.game_page.wait_element("金条场").click()
                time.sleep(1)
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("关闭对话框").click()
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击快速开始")
                self.game_page.wait_element("金条场").click()
                time.sleep(1)
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("关闭对话框").click()
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                self.start_step("点击快速开始")
                self.game_page.wait_element("金条场").click()
                time.sleep(1)
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("关闭对话框").click()
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)

    def post_test(self):
        # 清理测试环境
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C106_DFQP_Game_Faststart5(TestCase):
    '''
    快速开始---金条场，玩家银币破产，金条充足,进入金条匹配最高场次
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()
        # 获取用户金条信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print ('crystal:',crystal)
        coin = myuser_info.get('result',{'coin':None}).get('coin')
        print ('coin:',coin)
        # 设置金条数量
        if (crystal < 100):
            result_crystal = PHPInterface.add_crystal(self.casedata['mid'], 400)
            print (result_crystal)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            self.common.closeactivityprepublish(self.luadriver)
        if (coin>0):
            result_coin = PHPInterface.set_user_bankrupt(self.casedata['mid'])
            print (result_coin)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.luadriver.keyevent(4)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏二七十")
        if (self.game_page.is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.wait_element("金条场").click()
                time.sleep(1)
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart5.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("关闭对话框").click()
                time.sleep(2)
            else:
                self.game_page.wait_element("金条场").click()
                time.sleep(1)
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart5.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("关闭对话框").click()
                time.sleep(2)
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击快速开始")
                self.game_page.wait_element("金条场").click()
                time.sleep(1)
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart5.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("关闭对话框").click()
                time.sleep(2)
            else:
                self.start_step("点击快速开始")
                self.game_page.wait_element("金条场").click()
                time.sleep(1)
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart5.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("关闭对话框").click()
                time.sleep(2)

    def post_test(self):
        # 清理测试环境
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C107_DFQP_Game_Faststart6(TestCase):
    '''
    快速开始---金条场，玩家银币充足，金条充足,进入金条匹配最高场次
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        time.sleep(10)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()
        # 获取用户金条信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print ('crystal:',crystal)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print ('coin:',coin)
        # 设置金条数量
        if (crystal < 100):
            result_crystal = PHPInterface.add_crystal(self.casedata['mid'], 400)
            print (result_crystal)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            self.common.closeactivityprepublish(self.luadriver)
        if (coin < 3000):
            result_coin = PHPInterface.add_money(self.casedata['mid'],3000)
            print (result_coin)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            self.common.closeactivityprepublish(self.luadriver)


    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏二七十")
        if (self.game_page.is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.game_page.wait_element("金条场").click()
                time.sleep(1)
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart6.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                self.game_page.wait_element("金条场").click()
                time.sleep(1)
                self.start_step("点击快速开始")
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart6.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击快速开始")
                self.game_page.wait_element("金条场").click()
                time.sleep(1)
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart6.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                self.start_step("点击快速开始")
                self.game_page.wait_element("金条场").click()
                time.sleep(1)
                self.game_page.wait_element("快速开始").click()
                time.sleep(2)
                self.game_page.screenshot("Faststart6.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)

    def post_test(self):
        # 清理测试环境
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C108_DFQP_Game_Intoroom1(TestCase):
    '''
    入场--银币场，玩家现金不足，总金额充足，入场弹取钱弹框
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()
        # 获取用户信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print ('coin:',coin)
        #设置玩家银币，满足用例条件
        if (coin >= 0):
            PHPInterface.set_user_bankrupt(self.casedata['mid'])
            result_coin = PHPInterface.add_money(self.casedata['mid'], 21000)
            print (result_coin)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            self.common.closeactivityprepublish(self.luadriver)

        self.hall_page.wait_element("保险箱").click()
        time.sleep(2)
        self.safebox_page.wait_element("存入").click()
        self.safebox_page.wait_element("增加金条/银条数目").click()
        time.sleep(2)
        self.safebox_page.wait_element("确定---保险箱").click()
        time.sleep(2)
        #退出游戏，重启游戏
        self.common.closedriver()
        PHPInterface.add_money(self.casedata['mid'],-3000)
        self.luadriver = self.common.setupdriver()
        self.common.closeactivityprepublish(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏血战到底")
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击中级场")
                self.game_page.wait_element("血战到底-中级场").click()
                time.sleep(1)
                self.game_page.screenshot("Intoroom1.png")
                self.game_page.wait_element("取钱入场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()

            else:
                self.start_step("点击中级场")
                self.game_page.wait_element("血战到底-中级场").click()
                time.sleep(1)
                self.game_page.screenshot("Intoroom1.png")
                self.game_page.wait_element("取钱入场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("血战到底").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击中级场")
                self.game_page.wait_element("血战到底-中级场").click()
                time.sleep(1)
                self.game_page.screenshot("Intoroom1.png")
                self.game_page.wait_element("取钱入场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()
            else:
                self.start_step("点击中级场")
                self.game_page.wait_element("血战到底-中级场").click()
                time.sleep(1)
                self.game_page.screenshot("Intoroom1.png")
                self.game_page.wait_element("取钱入场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()

    def post_test(self):
        # 清理测试环境
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C109_DFQP_Game_Intoroom2(TestCase):
    '''
    入场---银币场，玩家现金不足，总金额不足，入场弹充值弹框
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()
        self.personinfo_page = Personinfo_Page()
        self.safebox_page = Safebox_Page()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        time.sleep(10)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()

        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print ('coin',coin)
        # 从保险箱取出所有银币
        self.hall_page.wait_element("保险箱").click()
        time.sleep(2)
        self.safebox_page.wait_element("取出").click()
        if (self.safebox_page.is_exist("确定---保险箱")==True):
            print ("滑动滚动条至最大值")
            slider = self.luadriver.find_lua_element_by_xpath('//element/element/safeBoxSaveOrTakeLayout/ImageBack/slider')
            x = slider.location['x']
            y = slider.location['y']
            addgoldbtn = self.safebox_page.wait_element("增加金条/银条数目")
            x1 = addgoldbtn.location['x']
            y1 = addgoldbtn.location['y']
            self.luadriver.swipe(x,y,x1,y1)
            time.sleep(2)
            self.safebox_page.wait_element("确定---保险箱").click()
            self.luadriver.keyevent(4)
        else:
            print ("保险箱没有存款")
            self.luadriver.keyevent(4)
        time.sleep(2)
        if (coin > 0):
            PHPInterface.set_user_bankrupt(self.casedata['mid'])
            result_coin = PHPInterface.add_money(self.casedata['mid'], 10000)
            print (result_coin)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''

        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏血战到底")
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.start_step("点击中级场")
                self.game_page.wait_element("血战到底-中级场").click()
                time.sleep(1)
                self.game_page.screenshot("1.png")
                self.start_step("点击充值")
                self.game_page.wait_element("充值").click()
                self.game_page.screenshot("2.png")
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()

            else:
                self.start_step("点击中级场")
                self.game_page.wait_element("血战到底-中级场").click()
                time.sleep(1)
                self.game_page.screenshot("1.png")
                self.start_step("点击充值")
                self.game_page.wait_element("充值").click()
                self.game_page.screenshot("2.png")
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("血战到底").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.start_step("点击中级场")
                self.game_page.wait_element("血战到底-中级场").click()
                time.sleep(1)
                self.game_page.screenshot("1.png")
                self.start_step("点击充值")
                self.game_page.wait_element("充值").click()
                self.game_page.screenshot("2.png")
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()
            else:
                self.start_step("点击中级场")
                self.game_page.wait_element("血战到底-中级场").click()
                time.sleep(1)
                self.game_page.screenshot("1.png")
                self.start_step("点击充值")
                self.game_page.wait_element("充值").click()
                self.game_page.screenshot("2.png")
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()

    def post_test(self):
        # 清理测试环境
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C110_DFQP_Game_Intoroom3(TestCase):
    '''
    入场---银币场，玩家现金充足，正常进入符合银币范围的房间
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()
        # 获取用户信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print ('coin:', coin)
        if (coin < 20000):
            result_coin = PHPInterface.add_money(self.casedata['mid'], 20000)
            print (result_coin)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏血战到底")
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击中级场")
                self.game_page.wait_element("血战到底-中级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()

            else:
                self.start_step("点击中级场")
                self.game_page.wait_element("血战到底-中级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("血战到底").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击中级场")
                self.game_page.wait_element("血战到底-中级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()
            else:
                self.start_step("点击中级场")
                self.game_page.wait_element("血战到底-中级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()

    def post_test(self):
        # 清理测试环境
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C111_DFQP_Game_Intoroom4(TestCase):
    '''
    入场---银币场，玩家银币过多，弹银币太多弹框
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()
        # 获取用户信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print ('coin:', coin)
        if (coin < 20000):
            result_coin = PHPInterface.add_money(self.casedata['mid'], 20000)
            print (result_coin)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏血战到底")
        if (self.game_page.is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击初级场")
                self.game_page.wait_element("血战到底-初级场").click()
                self.game_page.screenshot(".png")
                time.sleep(1)
                self.game_page.wait_element("去高级场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("血战到底-初级场").click()
                time.sleep(1)
                self.game_page.wait_element("存钱入场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()

            else:
                self.start_step("点击初级场")
                self.game_page.wait_element("血战到底-初级场").click()
                self.game_page.screenshot(".png")
                time.sleep(1)
                self.game_page.wait_element("去高级场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("血战到底-初级场").click()
                time.sleep(1)
                self.game_page.wait_element("存钱入场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("血战到底").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击初级场")
                self.game_page.wait_element("血战到底-初级场").click()
                self.game_page.screenshot(".png")
                time.sleep(1)
                self.game_page.wait_element("去高级场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("血战到底-初级场").click()
                time.sleep(1)
                self.game_page.wait_element("存钱入场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
            else:
                self.start_step("点击初级场")
                self.game_page.wait_element("血战到底-初级场").click()
                self.game_page.screenshot(".png")
                time.sleep(1)
                self.game_page.wait_element("去高级场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("血战到底-初级场").click()
                time.sleep(1)
                self.game_page.wait_element("存钱入场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()

    def post_test(self):
        # 清理测试环境
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C112_DFQP_Game_Intoroom5(TestCase):
    '''
    入场---金条场，玩家银币破产，金条充足
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()
        # 获取用户金条信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print (crystal)
        coin = myuser_info.get('result',{'coin':None}).get('coin')
        print (coin)
        # 设置金条和银币数量
        if (crystal < 100):
            result_crystal = PHPInterface.add_crystal(self.casedata['mid'], 100)
            print (result_crystal)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)
        if (coin>0):
            result_coin = PHPInterface.set_user_bankrupt(self.casedata['mid'])
            print (result_coin)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.luadriver.keyevent(4)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏二七十")
        if (self.game_page.is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.luadriver.keyevent(4)
                time.sleep(3)
                self.game_page.wait_element("关闭对话框").click()

            else:
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.luadriver.keyevent(4)
                time.sleep(3)
                self.game_page.wait_element("关闭对话框").click()
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.luadriver.keyevent(4)
                time.sleep(3)
                self.game_page.wait_element("关闭对话框").click()
            else:
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.luadriver.keyevent(4)
                time.sleep(3)
                self.game_page.wait_element("关闭对话框").click()

    def post_test(self):
        # 清理测试环境
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C113_DFQP_Game_Intoroom6(TestCase):
    '''
    入场---金条场，玩家携带金条不足，总金条充足，取钱入场
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()
        # 获取用户金条信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print (crystal)
        coin = myuser_info.get('result',{'coin':None}).get('coin')
        print (coin)
        if (coin<=3000):
            result_coin = PHPInterface.add_money(self.casedata['mid'],10000)  #保证玩家未破产
            print (result_coin)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)
        # 设置金条和银币数量
        if (crystal <= 200):
            result_crystal = PHPInterface.add_crystal(self.casedata['mid'], 200)
            print (result_crystal)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)
        #将当前的金条存入保险箱
        self.hall_page.wait_element("保险箱").click()
        time.sleep(2)
        self.safebox_page.wait_element("金条保险箱").click()
        time.sleep(2)
        self.safebox_page.wait_element("存入").click()
        time.sleep(5)
        silder = self.safebox_page.wait_element("滚动条")
        x = silder.location['x']
        y = silder.location['y']
        # d = silder.size['width']  #width取值取不到整个滚动条的长度
        addGoldBtn = self.safebox_page.wait_element("增加金条/银条数目")
        x1 = addGoldBtn.location['x']
        y1 = addGoldBtn.location['y']
        self.luadriver.swipe(x,y,x1,y1)
        time.sleep(2)
        self.safebox_page.wait_element("确定---保险箱").click()
        time.sleep(2)

        #设置金条为固定值99，重启游戏
        PHPInterface.add_crystal(self.casedata['mid'],-101)
        self.common.closedriver()
        self.luadriver = self.common.setupdriver()
        self.common.closeactivityprepublish(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        time.sleep(3)
        self.start_step("点击进入游戏二七十")
        if (self.game_page.is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                time.sleep(2)
                self.game_page.wait_element("取钱入场").click()
                time.sleep(1)
                self.luadriver.keyevent(4)
                time.sleep(1)
            else:
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                time.sleep(2)
                self.game_page.wait_element("取钱入场").click()
                time.sleep(1)
                self.luadriver.keyevent(4)
                time.sleep(1)
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(5)
            self.game_page.wait_element("二七十").click()
            time.sleep(3)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(20)
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                time.sleep(2)
                self.game_page.wait_element("取钱入场").click()
                time.sleep(1)
                self.luadriver.keyevent(4)
                time.sleep(1)

            else:
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                time.sleep(2)
                self.game_page.wait_element("取钱入场").click()
                time.sleep(1)
                self.luadriver.keyevent(4)
                time.sleep(1)

    def post_test(self):
        # 清理测试环境
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C114_DFQP_Game_Intoroom7(TestCase):
    '''
    入场---金条场，玩家携带金条不足，总金条不足，充值入场
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        time.sleep(10)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(3)
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()
        # 获取用户金条信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print (crystal)
        coin = myuser_info.get('result',{'coin':None}).get('coin')
        if (coin<=3000):
            result_coin = PHPInterface.add_money(self.casedata['mid'],10000)  #保证玩家未破产
            print (result_coin)
        # 设置金条和银币数量
        if (crystal > 0):
            result_crystal = PHPInterface.add_crystal(self.casedata['mid'], -crystal)
            print (result_crystal)
        #从保险箱取出金条
        self.hall_page.wait_element("保险箱").click()
        time.sleep(2)
        self.safebox_page.wait_element("金条保险箱").click()
        time.sleep(2)
        self.safebox_page.wait_element("取出").click()
        time.sleep(2)
        if(self.safebox_page.is_exist("确定---保险箱")):
            silder = self.safebox_page.wait_element("滚动条")
            x = silder.location['x']
            y = silder.location['y']
            addGoldBtn = self.safebox_page.wait_element("增加金条/银条数目")
            x1 = addGoldBtn.location['x']
            y1 = addGoldBtn.location['y']
            self.luadriver.swipe(x, y, x1, y1)
            time.sleep(2)
            self.safebox_page.wait_element("确定---保险箱").click()
            time.sleep(2)
            self.luadriver.keyevent(4)
        else:
            print ("保险箱没有存款")
            self.luadriver.keyevent(4)
            time.sleep(2)

        #设置金条满足用例条件，重启游戏
        PHPInterface.add_crystal(self.casedata['mid'],-crystal)
        self.common.closedriver()
        self.luadriver = self.common.setupdriver()
        self.common.closeactivityprepublish(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏二七十")
        if (self.game_page.is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("充值").click()
                time.sleep(1)
                self.luadriver.keyevent(4)
                time.sleep(1)
            else:
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("充值").click()
                time.sleep(1)
                self.luadriver.keyevent(4)
                time.sleep(1)
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("充值").click()
                time.sleep(1)
                self.luadriver.keyevent(4)
                time.sleep(1)

            else:
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("充值").click()
                time.sleep(1)
                self.luadriver.keyevent(4)
                time.sleep(1)

    def post_test(self):
        # 清理测试环境
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C115_DFQP_Game_Intoroom8(TestCase):
    '''
    入场---金条场，玩家金条充足，进入符合金条范围的房间
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()
        # 获取用户金条信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print (crystal)
        coin = myuser_info.get('result',{'coin':None}).get('coin')
        if (coin<=0):
            result_coin = PHPInterface.add_money(self.casedata['mid'],10000)  #保证玩家未破产
            print (result_coin)
        # 设置金条和银币数量
        if (crystal <400):
            result_crystal = PHPInterface.add_crystal(self.casedata['mid'], 400)
            print (result_crystal)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            # 关闭弹框
            self.common.closeactivityprepublish(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏二七十")
        if (self.game_page.is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击中级场")
                self.game_page.wait_element("二七十-中级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()

            else:
                self.start_step("点击中级场")
                self.game_page.wait_element("二七十-中级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击中级场")
                self.game_page.wait_element("二七十-中级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()
            else:
                self.start_step("点击中级场")
                self.game_page.wait_element("二七十-中级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(1)
                self.game_page.wait_element("返回").click()


    def post_test(self):
        # 清理测试环境
        self.common.closedriver()

testdata = test_datas.logindata3
@dataprovider.DataDrive(testdata)
class C116_DFQP_Game_Intoroom9(TestCase):
    '''
    入场---金条场，玩家金条太多，弹金条太多弹框
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)

        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        self.start_step("判断账号ID是否符合条件")
        self.personinfo_page.wait_element("头像").click()
        if not (self.personinfo_page.wait_element("账号ID").get_attribute('text') == self.casedata['cid']):
            self.common.loginuser(self.casedata['user'], self.casedata['password'])
            self.common.closeactivityprepublish(self.luadriver)
        else:
            self.personinfo_page.wait_element("关闭").click()
        # 获取用户金条信息
        result_userinfo = PHPInterface.get_user_info(self.casedata['mid'])
        myuser_info = json.loads(result_userinfo)
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print (crystal)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        if (coin<=0):
            result_coin = PHPInterface.add_money(self.casedata['mid'],10000)  #保证玩家未破产
            print (result_coin)
        # 设置金条和银币数量
        if (crystal <300):
            result_crystal = PHPInterface.add_crystal(self.casedata['mid'], 300)
            print (result_crystal)
            self.common.closedriver()
            self.luadriver = self.common.setupdriver()
            self.common.closeactivityprepublish(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏二七十")
        if (self.game_page.is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("去高级场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.wait_element("存钱入场").click()
                time.sleep(1)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()

            else:
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(3)
                self.game_page.screenshot(".png")
                time.sleep(3)
                self.game_page.wait_element("去高级场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.wait_element("存钱入场").click()
                time.sleep(1)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
        else:
            self.game_page.wait_element("右三角标").click()
            time.sleep(2)
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            if (self.game_page.is_exist("资源下载-确定") == True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(15)
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("去高级场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.wait_element("存钱入场").click()
                time.sleep(1)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
            else:
                self.start_step("点击初级场")
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.screenshot(".png")
                self.game_page.wait_element("去高级场").click()
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("二七十-初级场").click()
                time.sleep(1)
                self.game_page.wait_element("存钱入场").click()
                time.sleep(1)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()

    def post_test(self):
        # 清理测试环境
        self.common.closedriver()
#__qtaf_seq_tests__ = [C089_DFQP_GameList_DownLoad1]

if __name__ =='__main__':
    debug_run_all()

