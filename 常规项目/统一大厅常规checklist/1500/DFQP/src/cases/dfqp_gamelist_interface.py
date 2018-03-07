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

class C31148_DFQP_GameList_DownLoad(TestCase):
      '''
      大厅子游戏下载
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
          self.common.closeactivity_switchserver(self.luadriver,"预发布")
          time.sleep(10)

          self.start_step("获取用户mid")
          cid = self.common.get_cid()
          time.sleep(3)
          mid = PHPInterface.get_mid(cid, region=1)
          print "用户mid为：%s" % mid

          # 获取用户银币信息
          self.start_step("获取用户银币信息")
          result_userinfo = PHPInterface.get_user_info(mid)
          myuser_info = json.loads(result_userinfo)
          coin = myuser_info.get('result', {'coin': None}).get('coin')
          print "用户银币数为：%s" % coin
          if (coin<10000):
              PHPInterface.add_money(mid, 10000)
              self.common.closeactivityprepublish(self.luadriver)
              time.sleep(10)

      def run_test(self):
          self.startStep = ("等待页面加载完成")
          time.sleep(3)
          self.hall_page.wait_element("同步标志")
          self.start_step("点击川味斗地主：")
          if (self.common.game_is_exist("川味斗地主") == True):
              self.game_page.wait_element("川味斗地主").click()
              time.sleep(3)
              self.common.game_is_download()
              time.sleep(2)
              self.game_page.wait_element("返回").click()
          else:
              print ("没有川味斗地主游戏")
              self.game_page.wait_element("左三角标").click()

          self.start_step("点击血战到底：")
          if (self.common.game_is_exist("血战到底") == True):
              self.game_page.wait_element("血战到底").click()
              time.sleep(3)
              self.common.game_is_download()
              time.sleep(2)
              self.game_page.wait_element("返回").click()
          else:
              print ("没有血战到底游戏")
              self.game_page.wait_element("左三角标").click()

          self.start_step("点击血流成河：")
          if (self.common.game_is_exist("血流成河") == True):
              self.game_page.wait_element("血流成河").click()
              time.sleep(3)
              self.common.game_is_download()
              time.sleep(2)
              self.game_page.wait_element("返回").click()
          else:
              print ("没有血流成河游戏")
              self.game_page.wait_element("左三角标").click()

          self.start_step("点击斗牛：")
          if (self.common.game_is_exist("斗牛") == True):
              self.game_page.wait_element("斗牛").click()
              time.sleep(3)
              self.common.game_is_download()
              time.sleep(2)
              self.game_page.wait_element("返回").click()
          else:
              print ("没有斗牛游戏")
              self.game_page.wait_element("左三角标").click()

          self.start_step("点击二七十：")
          if (self.common.game_is_exist("二七十") == True):
              self.game_page.wait_element("二七十").click()
              time.sleep(3)
              self.common.game_is_download()
              time.sleep(2)
              self.game_page.wait_element("返回").click()

          else:
              print ("没有二七十游戏")
              self.game_page.wait_element("左三角标").click()

          self.start_step("点击拖拉机：")
          if (self.common.game_is_exist("拖拉机") == True):
              self.game_page.wait_element("拖拉机").click()
              time.sleep(3)
              self.common.game_is_download()
              time.sleep(2)
              self.game_page.wait_element("返回").click()
          else:
              print ("没有拖拉机游戏")
              self.game_page.wait_element("左三角标").click()

          self.start_step("点击干瞪眼：")
          if (self.common.game_is_exist("干瞪眼") == True):
              self.game_page.wait_element("干瞪眼").click()
              time.sleep(3)
              self.common.game_is_download()
              time.sleep(2)
              self.game_page.wait_element("返回").click()

          else:
              print ("没有干瞪眼游戏")
              self.game_page.wait_element("左三角标").click()

      def post_test(self):
          '''
          测试用例执行完成后，清理测试环境
          '''
          # self.common.deletefile(self.luadriver)
          self.common.closedriver()

class C31149_DFQP_GameList_Game(TestCase):
    '''
    子游戏列表显示
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

        self.start_step("获取用户mid")
        cid = self.common.get_cid()
        mid = PHPInterface.get_mid(cid, region=1)
        print "用户mid为：%s" % mid

        self.start_step("获取用户银币信息")
        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print "用户银币数为：%s" % coin
        if (coin < 10000):
            PHPInterface.add_money(mid, 10000)
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
        if (self.common.game_is_exist("血流成河") == True):
            self.game_page.wait_element("血流成河").click()
            time.sleep(2)
            self.common.game_is_download()
            time.sleep(3)
            self.game_page.screenshot(".png")
            time.sleep(2)
            self.game_page.wait_element("返回").click()
            time.sleep(2)
        else:
            print ("没有血流成河")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31150_DFQP_GameNameList(TestCase):
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
        time.sleep(10)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        """子游戏列表接口需调试"""
        self.start_step("获取子游戏列表")
        app_games = PHPInterface.get_app_games(103000,hall=1500,display=0)
        print json.dumps(app_games)

    def run_test(self):
        '''
        测试用例---切换游戏
        '''

        self.start_step("等待页面加载完成")

        self.hall_page.wait_element("同步标志")
        time.sleep(3)
        #前置条件：至少已下载4个游戏
        self.start_step("点击川味斗地主：")
        if (self.common.game_is_exist("川味斗地主") == True):
            self.game_page.wait_element("川味斗地主").click()
            time.sleep(3)
            self.common.game_is_download()
            time.sleep(3)
            self.game_page.wait_element("返回").click()
            time.sleep(3)
        else:
            print ("没有川味斗地主游戏")
            self.game_page.wait_element("左三角标").click()

        self.start_step("点击血战到底：")
        if (self.common.game_is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            self.common.game_is_download()
            time.sleep(3)
            self.game_page.wait_element("返回").click()
            time.sleep(3)
        else:
            print ("没有血战到底游戏")
            self.game_page.wait_element("左三角标").click()

        self.start_step("点击血流成河：")
        if (self.common.game_is_exist("血流成河") == True):
            self.game_page.wait_element("血流成河").click()
            time.sleep(3)
            self.common.game_is_download()
            time.sleep(3)
            self.game_page.wait_element("返回").click()
            time.sleep(3)
        else:
            print ("没有血流成河游戏")
            self.game_page.wait_element("左三角标").click()

        self.start_step("点击二七十：")
        if (self.common.game_is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(3)
            self.common.game_is_download()
            time.sleep(3)
            self.game_page.wait_element("返回").click()
            time.sleep(2)

        else:
            print ("没有二七十游戏")
            self.game_page.wait_element("左三角标").click()

        self.start_step("点击斗牛：")
        if (self.common.game_is_exist("斗牛") == True):
            self.game_page.wait_element("斗牛").click()
            time.sleep(3)
            self.common.game_is_download()
            time.sleep(3)
            self.game_page.wait_element("返回").click()
            time.sleep(2)
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
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31185_DFQP_Game_Bankrupt(TestCase):
    '''
    快速开始---银币场，玩家银币破产，快速开始弹破产弹框
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

        self.start_step("获取用户mid")
        cid = self.common.get_cid()
        global mid
        mid = PHPInterface.get_mid(cid, region=1)
        print "用户mid为：%s" % mid

        self.start_step("获取用户银币和金条数量")
        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print "用户银币数为：%s" % coin

        if (coin > 0):
            PHPInterface.set_user_bankrupt(mid)
            self.common.closeactivityprepublish(self.luadriver)
        # else:
        #     self.luadriver.keyevent(4)
        #     time.sleep(2)

        self.start_step("获取用户保险箱存款信息")
        safebox_info = PHPInterface.get_safebox(mid)
        safebox_crystal = safebox_info.get('crystalsafebox')
        print "保险箱金条存款为：%s" % safebox_crystal
        if (safebox_crystal > 0):
            self.common.get_safebox_crystal()
            time.sleep(3)

        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print "用户金条数为：%s" % crystal

        if (crystal > 0):
            PHPInterface.add_crystal(mid,-crystal)
            self.common.closeactivityprepublish(self.luadriver)
            time.sleep(10)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏血流成河")
        if (self.common.game_is_exist("血流成河") == True):
            self.game_page.wait_element("血流成河").click()
            time.sleep(2)
            self.common.game_is_download()
            time.sleep(3)
            self.start_step("点击快速开始")
            self.game_page.wait_element("快速开始").click()
            time.sleep(2)
            self.game_page.screenshot("1.png")
            time.sleep(3)
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.game_page.wait_element("返回").click()
            time.sleep(3)

        else:
            print ("没有血流成河游戏")

        self.start_step("点击进入游戏二七十金条场")
        if (self.common.game_is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            self.common.game_is_download()
            time.sleep(3)
            self.game_page.wait_element("金条场").click()
            time.sleep(1)
            self.start_step("点击快速开始")
            self.game_page.wait_element("快速开始").click()
            time.sleep(2)
            self.game_page.screenshot("2.png")
            time.sleep(2)
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.game_page.screenshot("3.png")
            time.sleep(3)
            self.luadriver.keyevent(4)
            time.sleep(2)
        else:
            print ("没有游戏二七十")
        PHPInterface.add_money(mid,20000)
    def post_test(self):
        #清理测试环境
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31156_DFQP_Game_Faststart2(TestCase):
    '''
    快速开始---玩家银币,金条足够,快速开始分别匹配最高场次房间
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

        self.start_step("获取用户mid")
        cid = self.common.get_cid()
        mid = PHPInterface.get_mid(cid, region=1)
        print "用户mid为：%s" % mid

        self.start_step("获取用户银币信息")
        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print "用户银币数为：%s" % coin

        self.start_step("获取用户金条信息")
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print "用户金条数为：%s" % crystal

        self.start_step("获取游戏场次配置信息")
        gamecfg1 = PHPInterface.get_levelconfig(2, 0, 0, 12)
        # print json.dumps(gamecfg1)
        low_limit1 = gamecfg1.get('values', {'LOW_LIMIT': None}).get('LOW_LIMIT')
        # print high_limit1
        gamecfg2 = PHPInterface.get_levelconfig(9, 1, 0, 12)
        # print json.dumps(gamecfg2)
        low_limit2 = gamecfg2.get('values', {'LOW_LIMIT': None}).get('LOW_LIMIT')
        # print high_limit2
        if (coin <= low_limit1):
            PHPInterface.add_money(mid, low_limit1 - coin + 1000)
            self.common.closeactivityprepublish(self.luadriver)
        if (crystal <= low_limit2):
            PHPInterface.add_crystal(mid, low_limit2 - crystal + 10)
            self.common.closeactivityprepublish(self.luadriver)

        self.start_step("关闭血战到底和二七十的机器人开关")
        # 获取机器人配置，关闭机器人
        robotflag1 = gamecfg1.get('values', {'ADDROBOTFLAG': None}).get('ADDROBOTFLAG')
        print "机器人开关状态为(1为开启，0为关闭): %s" % robotflag1
        if (robotflag1 != 0):
            PHPInterface.set_robot_flag(2, 0, 0, 12, 0)
        robotflag2 = gamecfg2.get('values', {'ADDROBOTFLAG': None}).get('ADDROBOTFLAG')
        print "机器人开关状态为(1为开启，0为关闭): %s" % robotflag2
        if (robotflag2 != 0):
            PHPInterface.set_robot_flag(2, 0, 0, 12, 0)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏血战到底")
        if (self.common.game_is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(2)
            self.common.game_is_download()
            time.sleep(3)
            self.start_step("点击快速开始")
            self.game_page.wait_element("快速开始").click()
            time.sleep(2)
            self.game_page.screenshot("Faststart2.png")
            time.sleep(2)
            self.luadriver.keyevent(4)
            time.sleep(1)
            self.game_page.wait_element("返回").click()
        else:
            print ("血战到底不存在")


        self.start_step("点击进入游戏二七十金条场")
        if (self.common.game_is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            self.common.game_is_download()
            time.sleep(3)
            self.game_page.wait_element("金条场").click()
            time.sleep(1)
            self.start_step("点击快速开始")
            self.game_page.wait_element("快速开始").click()
            time.sleep(2)
            self.game_page.screenshot("Faststart5.png")
            time.sleep(2)
            self.luadriver.keyevent(4)
            time.sleep(2)
        else:
            print ("没有二七十游戏")

    def post_test(self):
        # 清理测试环境
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31157_DFQP_Game_Faststart3(TestCase):
    '''
    快速开始---玩家银币不足（未破产），金条不足，快速开始弹充值弹框
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
        self.start_step("获取用户mid")
        cid = self.common.get_cid()

        mid = PHPInterface.get_mid(cid, region=1)
        print "用户mid为：%s" % mid

        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print "用户银币数为：%s" % coin
        if(coin<0):
            self.luadriver.keyevent(4)
            time.sleep(2)
        self.start_step("从保险箱取出所有存款")
        self.common.get_safebox_money()
        time.sleep(3)
        self.common.get_safebox_crystal()
        time.sleep(3)

        self.start_step("获取用户银币信息")
        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print "用户银币数为：%s" % coin
        if (coin > 0):
            PHPInterface.set_user_bankrupt(mid)
            PHPInterface.add_money(mid, 3500)
            self.common.closeactivityprepublish(self.luadriver)

        self.start_step("获取用户金条信息")
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print "用户金条数为：%s" % crystal
        # 设置金条满足用例条件
        if (crystal > 0):
            PHPInterface.add_crystal(mid, -crystal)
            self.common.closeactivityprepublish(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏二七十金条场")
        if (self.common.game_is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(5)
            self.common.game_is_download()
            time.sleep(3)
            self.game_page.wait_element("金条场").click()
            time.sleep(3)
            self.start_step("金条场点击快速开始")
            self.game_page.wait_element("金条场").click()
            time.sleep(3)
            self.game_page.wait_element("快速开始").click()
            time.sleep(2)
            self.game_page.screenshot("1.png")
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(2)
            self.start_step("银币场点击快速开始")
            self.game_page.wait_element("普通场").click()
            time.sleep(3)
            self.game_page.wait_element("快速开始").click()
            time.sleep(2)
            self.game_page.screenshot("2.png")
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(2)
            self.game_page.wait_element("返回").click()
            time.sleep(2)

        else:
            print ("没有二七十游戏")

    def post_test(self):
        # 清理测试环境
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31158_DFQP_Game_Faststart1(TestCase):
    '''
    入场--金条场，银币场，玩家现金不足，总金额充足，入场弹取钱弹框，取钱入场
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
        self.start_step("获取用户mid")
        cid = self.common.get_cid()

        mid = PHPInterface.get_mid(cid, region=1)
        print "用户mid为：%s" % mid

        # 获取用户信息
        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print "用户银币数为：%s" % coin
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print "用户金条数为：%s" % crystal
        #设置玩家银币，满足用例条件

        self.start_step("获取游戏场次配置信息")
        gamecfg1 = PHPInterface.get_levelconfig(2, 0, 0, 13)
        # print json.dumps(gamecfg1)
        # low_limit1 = gamecfg1.get('values', {'LOW_LIMIT': None}).get('LOW_LIMIT')
        # print high_limit1
        gamecfg2 = PHPInterface.get_levelconfig(9, 1, 0, 12)
        # print json.dumps(gamecfg2)
        # low_limit2 = gamecfg2.get('values', {'LOW_LIMIT': None}).get('LOW_LIMIT')
        # print high_limit2
        # if (coin <= low_limit1):
        #     PHPInterface.add_money(mid, low_limit1 - coin + 1000)
        #     self.common.closeactivityprepublish(self.luadriver)
        # if (crystal <= low_limit2):
        #     PHPInterface.add_crystal(mid, low_limit2 - crystal + 10)
        #     self.common.closeactivityprepublish(self.luadriver)


        self.start_step("设置用户银币和金条数量")
        if (coin >= 0):
            PHPInterface.set_user_bankrupt(mid)
            result_coin = PHPInterface.add_money(mid, 21000)
            print (result_coin)
            self.common.closeactivityprepublish(self.luadriver)
            time.sleep(10)
        if (crystal >=0):
            PHPInterface.add_crystal(mid,-crystal)
            result_crystal = PHPInterface.add_crystal(mid, 201)
            print (result_crystal)
            self.common.closeactivityprepublish(self.luadriver)
            time.sleep(10)
        self.hall_page.wait_element("保险箱").click()
        time.sleep(2)
        self.safebox_page.wait_element("存入").click()
        time.sleep(3)
        self.safebox_page.wait_element("增加金条/银条数目").click()
        time.sleep(2)
        self.safebox_page.wait_element("确定---保险箱").click()
        time.sleep(3)
        self.safebox_page.wait_element("金条保险箱").click()
        time.sleep(3)
        self.safebox_page.wait_element("存入").click()
        time.sleep(3)
        self.safebox_page.wait_element("增加金条/银条数目").click()
        time.sleep(3)
        self.safebox_page.wait_element("确定---保险箱").click()
        time.sleep(3)
        self.luadriver.keyevent(4)
        time.sleep(5)
        PHPInterface.add_money(mid,-3000)
        #设置金条为固定值99，重启游戏
        PHPInterface.add_crystal(mid,-101)
        self.common.closeactivityprepublish(self.luadriver)
        time.sleep(10)



        self.start_step("关闭血战到底和二七十的机器人开关")
        # 获取机器人配置，关闭机器人
        robotflag1 = gamecfg1.get('values', {'ADDROBOTFLAG': None}).get('ADDROBOTFLAG')
        print "机器人开关状态为(1为开启，0为关闭): %s" % robotflag1
        if (robotflag1 != 0):
            PHPInterface.set_robot_flag(2, 0, 0, 13, 0)

        robotflag2 = gamecfg2.get('values', {'ADDROBOTFLAG': None}).get('ADDROBOTFLAG')
        print "机器人开关状态为(1为开启，0为关闭): %s" % robotflag2
        if (robotflag2 != 0):
            PHPInterface.set_robot_flag(2, 0, 0, 12, 0)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏血战到底")
        if (self.common.game_is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(2)
            self.common.game_is_download()
            time.sleep(3)
            self.start_step("点击中级场")
            self.game_page.wait_element("血战到底-中级场").click()
            time.sleep(1)
            self.game_page.screenshot("1.png")
            time.sleep(2)
            self.game_page.wait_element("取钱入场").click()
            time.sleep(2)
            self.luadriver.keyevent(4)
            time.sleep(1)
            self.game_page.wait_element("返回").click()
        else:
            print ("没有血战到底游戏")

        self.start_step("点击进入游戏二七十金条场")
        if (self.common.game_is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            self.common.game_is_download()
            time.sleep(5)
            self.game_page.wait_element("金条场").click()
            time.sleep(1)
            self.start_step("点击快速开始")
            self.game_page.wait_element("快速开始").click()
            time.sleep(2)
            self.game_page.screenshot("2.png")
            time.sleep(2)
            self.game_page.wait_element("取钱入场").click()
            time.sleep(2)
            self.luadriver.keyevent(4)
            time.sleep(2)

        else:
            print ("没有二七十")

    def post_test(self):
        # 清理测试环境
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31159_DFQP_Game_Intoroom1(TestCase):
    '''
    入场---银币场/金条场，玩家银币/金条过多，弹银币/金条太多弹框,分别点击存钱，去高级场
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
        self.start_step("获取用户mid")
        cid = self.common.get_cid()
        global mid
        mid = PHPInterface.get_mid(cid, region=1)
        print "用户mid为：%s" % mid

        # 获取用户信息
        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print "用户银币数为：%s" % coin
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print "用户金条数为：%s" % crystal
        gamecfg1 = PHPInterface.get_levelconfig(2,0,0,12)
        # print json.dumps(gamecfg1)
        high_limit1 = gamecfg1.get('values',{'HIGH_LIMIT':None}).get('HIGH_LIMIT')
        # print high_limit1
        gamecfg2 = PHPInterface.get_levelconfig(9,1,0,12)
        # print json.dumps(gamecfg2)
        high_limit2 = gamecfg2.get('values',{'HIGH_LIMIT':None}).get('HIGH_LIMIT')
        # print high_limit2
        if (coin <= high_limit1):
            PHPInterface.add_money(mid, high_limit1-coin+1000)
            self.common.closeactivityprepublish(self.luadriver)
        if (crystal <= high_limit2):
            PHPInterface.add_crystal(mid, high_limit2-crystal+10)
            self.common.closeactivityprepublish(self.luadriver)
    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏血战到底")
        if (self.common.game_is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(2)
            self.common.game_is_download()
            time.sleep(3)
            self.start_step("点击初级场")
            self.game_page.wait_element("血战到底-初级场").click()
            time.sleep(2)
            self.game_page.screenshot(".png")
            time.sleep(2)
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
            time.sleep(2)

        else:
            print ("没有血战到底")

        self.start_step("点击进入游戏二七十")
        if (self.common.game_is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            self.common.game_is_download()
            time.sleep(15)
            self.start_step("点击金条场初级场")
            self.game_page.wait_element("金条场").click()
            time.sleep(3)
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
            time.sleep(2)
        else:
            print ("没有二七十")

    def post_test(self):
        # 清理测试环境
        self.common.closedriver()


class C31160_DFQP_Game_Intoroom2(TestCase):
    '''
    入场---金条场，银币场，玩家携带金条/银币不足，总金条不足，充值入场
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
        self.start_step("获取用户mid")
        cid = self.common.get_cid()

        mid = PHPInterface.get_mid(cid, region=1)
        print "用户mid为：%s" % mid

        if(self.game_page.is_exist("关闭对话框")==True):
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(2)
        #从保险箱取出所有金条和银币
        self.start_step("从保险箱取出所有金条和银币")
        self.common.get_safebox_money()
        time.sleep(3)
        self.common.get_safebox_crystal()
        time.sleep(3)

        # 获取用户信息
        self.start_step("获取当前银币和金条数量")
        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print "用户银币数为：%s" % coin
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print "用户金条数为：%s" % crystal

        if (coin > 0):
            PHPInterface.set_user_bankrupt(mid)
            result_coin = PHPInterface.add_money(mid, 10000)
            print (result_coin)
            self.common.closeactivityprepublish(self.luadriver)
            time.sleep(5)
        #设置金条满足用例条件
        if(crystal>0):
            PHPInterface.add_crystal(mid,-crystal)
            self.common.closeactivityprepublish(self.luadriver)
            time.sleep(5)

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击进入游戏二七十")
        if (self.common.game_is_exist("二七十") == True):
            self.game_page.wait_element("二七十").click()
            time.sleep(2)
            self.common.game_is_download()
            time.sleep(3)
            self.start_step("点击普通场中级场")
            self.game_page.wait_element("普通场").click()
            time.sleep(2)
            self.game_page.wait_element("二七十-中级场").click()
            time.sleep(2)
            self.game_page.screenshot("1.png")
            time.sleep(2)
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            # self.luadriver.keyevent(4)
            # time.sleep(3)
            self.start_step("点击金条场初级场")
            self.game_page.wait_element("金条场").click()
            time.sleep(2)
            self.game_page.wait_element("二七十-初级场").click()
            time.sleep(2)
            self.game_page.screenshot("2.png")
            time.sleep(2)
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.luadriver.keyevent(4)
            time.sleep(3)

        else:
            print ("没有二七十")

    def post_test(self):
        # 清理测试环境
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31164_DFQP_Game_Gameroom_head1(TestCase):
    '''
    房间内默认头像显示
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

        self.start_step("获取用户mid")
        cid = self.common.get_cid()

        mid = PHPInterface.get_mid(cid, region=1)
        print "用户mid为：%s" % mid
        # 获取用户银币信息
        self.start_step("获取用户银币信息")
        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print "用户银币数为：%s" % coin
        if (coin < 10000):
            PHPInterface.add_money(mid, 10000)
            self.common.closeactivityprepublish(self.luadriver)
            time.sleep(10)

    def run_test(self):
        """
        测试用例
        """
        self.start_step("点击头像")
        self.hall_page.wait_element("头像").click()
        time.sleep(3)
        self.game_page.screenshot("1.png")
        time.sleep(2)
        self.start_step("修改性别")

        if (self.personinfo_page.wait_element("男").get_attribute('selected') == 'true'):
            print ("默认头像为男")
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.start_step("点击血战到底：")
            if (self.common.game_is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                time.sleep(3)
                self.common.game_is_download()
                time.sleep(2)
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.start_step("点击头像")
                self.game_page.wait_element("头像---未开始游戏").click()
                time.sleep(3)
                self.game_page.screenshot("1-1.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()
            self.start_step("默认头像为男，修改性别为女")
            self.hall_page.wait_element("头像").click()
            time.sleep(3)
            self.personinfo_page.wait_element("女").click()
            time.sleep(2)
            self.game_page.screenshot("2.png")
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.start_step("点击血战到底：")
            if (self.common.game_is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                time.sleep(3)
                self.common.game_is_download()
                time.sleep(3)
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.start_step("点击头像")
                self.game_page.wait_element("头像---未开始游戏").click()
                time.sleep(3)
                self.game_page.screenshot("2-1.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()

            self.start_step("修改性别为保密")
            self.hall_page.wait_element("头像").click()
            time.sleep(3)
            self.personinfo_page.wait_element("保密").click()
            time.sleep(2)
            time.sleep(2)
            self.game_page.screenshot("3.png")
            time.sleep(2)
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.start_step("点击血战到底：")
            if (self.common.game_is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                time.sleep(3)
                self.common.game_is_download()
                time.sleep(3)
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.start_step("点击头像")
                self.game_page.wait_element("头像---未开始游戏").click()
                time.sleep(3)
                self.game_page.screenshot("3-1.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)

            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()

        elif (self.personinfo_page.wait_element("女").get_attribute('selected') == 'true'):

            print ("性别已选中女")
            self.game_page.screenshot("4.png")
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.start_step("点击血战到底：")
            if (self.common.game_is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                time.sleep(3)
                self.common.game_is_download()
                time.sleep(3)
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.start_step("点击头像")
                self.game_page.wait_element("头像---未开始游戏").click()
                time.sleep(3)
                self.game_page.screenshot("4-1.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()
            self.start_step("默认头像为女，修改性别为男")
            self.hall_page.wait_element("头像").click()
            time.sleep(3)
            self.personinfo_page.wait_element("男").click()
            time.sleep(2)
            self.game_page.screenshot("5.png")
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.start_step("点击血战到底：")
            if (self.game_page.is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                time.sleep(3)
                self.common.game_is_download()
                time.sleep(2)
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.start_step("点击头像")
                self.game_page.wait_element("头像---未开始游戏").click()
                time.sleep(3)
                self.game_page.screenshot("5-1.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()

            self.start_step("修改性别为保密")
            self.hall_page.wait_element("头像").click()
            time.sleep(3)
            self.personinfo_page.wait_element("保密").click()
            time.sleep(2)
            time.sleep(2)
            self.game_page.screenshot("6.png")
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.start_step("点击血战到底：")
            if (self.common.game_is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                time.sleep(3)
                self.common.game_is_download()
                time.sleep(2)
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.start_step("点击头像")
                self.game_page.wait_element("头像---未开始游戏").click()
                time.sleep(3)
                self.game_page.screenshot("6-1.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)

            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()
        else:
            self.personinfo_page.wait_element("保密").get_attribute('selected')
            print ("性别已选中保密")
            self.game_page.screenshot("7.png")
            time.sleep(2)
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.start_step("点击血战到底：")
            if (self.game_page.is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                time.sleep(3)
                self.common.game_is_download()
                time.sleep(2)
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.start_step("点击头像")
                self.game_page.wait_element("头像---未开始游戏").click()
                time.sleep(3)
                self.game_page.screenshot("7-1.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)
            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()
            self.start_step("默认头像为保密，修改性别为女")
            self.hall_page.wait_element("头像").click()
            time.sleep(3)
            self.personinfo_page.wait_element("女").click()
            time.sleep(2)
            self.game_page.screenshot("8.png")
            time.sleep(2)
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.start_step("点击血战到底：")
            if (self.common.game_is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                time.sleep(3)
                self.common.game_is_download()
                time.sleep(2)
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.start_step("点击头像")
                self.game_page.wait_element("头像---未开始游戏").click()
                time.sleep(3)
                self.game_page.screenshot("8-1.png")
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(2)
                self.game_page.wait_element("返回").click()
                time.sleep(2)

            else:
                print ("没有血战到底游戏")
                self.game_page.wait_element("左三角标").click()

            self.start_step("修改性别为男")
            self.hall_page.wait_element("头像").click()
            time.sleep(3)
            self.personinfo_page.wait_element("男").click()
            time.sleep(2)

            self.game_page.screenshot("9.png")
            time.sleep(2)
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.start_step("点击血战到底：")
            if (self.common.game_is_exist("血战到底") == True):
                self.game_page.wait_element("血战到底").click()
                time.sleep(3)
                self.common.game_is_download()
                time.sleep(2)
                self.game_page.wait_element("快速开始").click()
                time.sleep(3)
                self.start_step("点击头像")
                self.game_page.wait_element("头像---未开始游戏").click()
                time.sleep(3)
                self.game_page.screenshot("9-1.png")
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
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31164_DFQP_Game_Gameroom_head2(TestCase):
    '''
    房间内vip头像显示
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

        self.start_step("获取用户mid")
        cid = self.common.get_cid()
        global mid
        mid = PHPInterface.get_mid(cid, region=1)
        print "用户mid为：%s" % mid
        # 获取用户银币信息
        self.start_step("获取用户银币信息")
        result_userinfo = PHPInterface.get_user_info(mid)

        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print "用户银币数为：%s" % coin
        if (coin < 10000):
            PHPInterface.add_money(mid, 10000)
            self.common.closeactivityprepublish(self.luadriver)
            time.sleep(10)

        vip = myuser_info.get('result',{'vip':None}).get('vip')
        print "用户vip类型为：%s" % vip
        if(vip == -1):
            self.start_step("设置玩家为vip")
            PHPInterface.set_vip(mid,4)    #添加vip体验卡
            self.common.closeactivityprepublish(self.luadriver)
            time.sleep(10)

    def run_test(self):
        """
        测试用例
        """
        self.start_step("点击头像")
        self.hall_page.wait_element("头像").click()
        time.sleep(3)
        self.game_page.screenshot("1.png")
        time.sleep(2)
        self.game_page.wait_element("关闭对话框").click()
        time.sleep(3)
        self.start_step("点击血战到底：")
        if (self.common.game_is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            self.common.game_is_download()
            time.sleep(2)
            self.game_page.wait_element("快速开始").click()
            time.sleep(9)
            self.start_step("点击头像")
            self.game_page.wait_element("头像---未开始游戏").click()
            time.sleep(3)
            self.game_page.screenshot("1-1.png")
            self.luadriver.keyevent(4)
            time.sleep(2)
            self.luadriver.keyevent(4)
            time.sleep(2)
            self.game_page.wait_element("返回").click()
            time.sleep(2)
        else:
            print ("没有血战到底游戏")
            self.game_page.wait_element("左三角标").click()
        PHPInterface.set_vip(mid, -1)
    def post_test(self):

        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31167_DFQP_GameRoom_Ready(TestCase):
    '''
    游戏房间内---准备，换桌
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

        self.start_step("获取用户mid")
        cid = self.common.get_cid()
        mid = PHPInterface.get_mid(cid, region=1)
        print "用户mid为：%s" % mid
        # 获取用户信息
        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        print "用户银币数为：%s" % coin
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')
        print "用户金条数为：%s" % crystal
        gamecfg = PHPInterface.get_levelconfig(2,0,0,12)
        print gamecfg
        high_limit = gamecfg.get('values', {'HIGH_LIMIT': None}).get('HIGH_LIMIT')
        print high_limit
        # 设置银币满足进入当前房间
        PHPInterface.set_user_bankrupt(mid)
        PHPInterface.add_money(mid,high_limit-1000)
        #获取机器人配置，关闭机器人
        robotflag = gamecfg.get('values',{'ADDROBOTFLAG':None}).get('ADDROBOTFLAG')
        print "机器人开关状态为(1为开启，0为关闭): %s" % robotflag
        if(robotflag != 0):
            PHPInterface.set_robot_flag(2,0,0,12,0)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("点击血战到底：")
        if (self.common.game_is_exist("血战到底") == True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(5)
            self.common.game_is_download()
            time.sleep(5)
            self.game_page.wait_element("血战到底-初级场").click()
            time.sleep(10)
            self.start_step("点击换桌")
            self.game_page.wait_element("换桌").click()
            time.sleep(3)
            self.game_page.screenshot("1.png")
            time.sleep(2)
            self.start_step("点击准备")
            self.game_page.wait_element("准备").click()
            time.sleep(5)
            self.game_page.wait_element("菜单").click()
            time.sleep(2)
            # self.game_page.wait_element("托管").click()
            # time.sleep(3)
            self.luadriver.keyevent(4)
            time.sleep(2)
            self.luadriver.keyevent(4)
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

class C31169_DFQP_Game_Gameroom_faceview1(TestCase):
    '''
    普通玩家发表情
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
        time.sleep(10)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        self.start_step("获取用户mid")
        cid = self.common.get_cid()
        global mid
        mid = PHPInterface.get_mid(cid, region=1)
        print "用户mid为：%s" % mid
        self.start_step("获取用户VIP信息")
        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        vip = myuser_info.get('result', {'vip': None}).get('vip')
        print "用户vip类型为：%s" % vip
        if (vip != -1):
            self.start_step("设置玩家为vip")
            PHPInterface.set_vip(mid, -1)  # 添加vip体验卡
            self.common.closeactivityprepublish(self.luadriver)
            time.sleep(10)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("点击血战到底：")
        if(self.common.game_is_exist("血战到底")==True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            self.common.game_is_download()
            time.sleep(3)
            self.game_page.wait_element("快速开始").click()
            time.sleep(3)
            # if (self.game_page.is_exist("更多按钮")==True):
            #     reconnect = self.game_page.wait_element("更多按钮")
            #     # reconnect = self.luadriver.find_element_by_name('reconnect')
            #     reconnect1 = int(reconnect.location['x'])
            #     menu = self.game_page.wait_element("菜单")
            #     # menu = self.luadriver.find_element_by_name('menu_btn')
            #     menu1 = int(menu.location['x'])
            #     print (reconnect1,menu1)
            #     self.luadriver.drag_and_drop(reconnect1,menu1)
            #     time.sleep(3)
            self.start_step("点击聊天按钮")
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("表情").click()
            time.sleep(2)
            self.start_step("发送所有普通表情")
            self.game_page.wait_element("普通表情1").click()
            time.sleep(1)
            self.game_page.screenshot("1.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情2").click()
            time.sleep(1)
            self.game_page.screenshot("2.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情3").click()
            time.sleep(1)
            self.game_page.screenshot("3.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情4").click()
            time.sleep(1)
            self.game_page.screenshot("4.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情5").click()
            time.sleep(1)
            self.game_page.screenshot("5.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情6").click()
            time.sleep(1)
            self.game_page.screenshot("6.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情7").click()
            time.sleep(1)
            self.game_page.screenshot("7.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情8").click()
            time.sleep(1)
            self.game_page.screenshot("8.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情9").click()
            time.sleep(1)
            self.game_page.screenshot("9.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情10").click()
            time.sleep(1)
            self.game_page.screenshot("10.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情11").click()
            time.sleep(1)
            self.game_page.screenshot("11.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情12").click()
            time.sleep(1)
            self.game_page.screenshot("12.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.common.swipeelement(self.game_page.wait_element("普通表情11"),self.game_page.wait_element("普通表情1"))
            time.sleep(3)
            self.game_page.wait_element("普通表情8").click()
            time.sleep(1)
            self.game_page.screenshot("13.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情9").click()
            time.sleep(1)
            self.game_page.screenshot("14.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情10").click()
            time.sleep(1)
            self.game_page.screenshot("15.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情11").click()
            time.sleep(1)
            self.game_page.screenshot("16.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("普通表情12").click()
            time.sleep(1)
            self.game_page.screenshot("17.png")
            time.sleep(2)
            self.start_step("查看VIP表情")
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)

            self.game_page.wait_element("VIP表情tab").click()
            time.sleep(3)
            self.game_page.screenshot("vip.png")
            time.sleep(2)
            self.game_page.wait_element("立即成为VIP").click()
            time.sleep(3)
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.luadriver.keyevent(4)
            time.sleep(3)
            # self.game_page.wait_element("菜单").click()
            # time.sleep(2)
            # self.game_page.wait_element("退出").click()
            # time.sleep(3)
            self.game_page.wait_element("返回").click()
        else:
            print ("血战到底游戏不存在")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()


class C31169_DFQP_Game_Gameroom_faceview2(TestCase):
    '''
    VIP玩家发表情
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
        # 关闭弹框
        self.common.closeactivityprepublish(self.luadriver)
        time.sleep(10)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.personinfo_page = Personinfo_Page()
        self.start_step("获取用户mid")
        cid = self.common.get_cid()
        global mid
        mid = PHPInterface.get_mid(cid, region=1)
        print "用户mid为：%s" % mid
        self.start_step("获取用户VIP信息")
        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        vip = myuser_info.get('result', {'vip': None}).get('vip')
        print "用户vip类型为：%s" % vip
        if (vip == -1):
            self.start_step("设置玩家为vip")
            PHPInterface.set_vip(mid, 4)  # 添加vip体验卡
            self.common.closeactivityprepublish(self.luadriver)
            time.sleep(10)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("点击血战到底：")
        if(self.common.game_is_exist("血战到底")==True):
            self.game_page.wait_element("血战到底").click()
            time.sleep(3)
            self.common.game_is_download()
            time.sleep(3)
            self.game_page.wait_element("快速开始").click()
            time.sleep(3)
            self.start_step("点击聊天按钮")
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("表情").click()
            time.sleep(2)
            self.start_step("发送所有VIP表情")
            self.game_page.wait_element("VIP表情1").click()
            time.sleep(1)
            self.game_page.screenshot("1.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情2").click()
            time.sleep(1)
            self.game_page.screenshot("2.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情3").click()
            time.sleep(1)
            self.game_page.screenshot("3.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情4").click()
            time.sleep(1)
            self.game_page.screenshot("4.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情5").click()
            time.sleep(1)
            self.game_page.screenshot("5.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情6").click()
            time.sleep(1)
            self.game_page.screenshot("6.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情7").click()
            time.sleep(1)
            self.game_page.screenshot("7.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情8").click()
            time.sleep(1)
            self.game_page.screenshot("8.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情9").click()
            time.sleep(1)
            self.game_page.screenshot("9.png")
            time.sleep(2)

            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.common.swipeelement(self.game_page.wait_element("VIP表情7"),self.game_page.wait_element("VIP表情1"))
            time.sleep(3)
            self.game_page.wait_element("VIP表情1").click()
            time.sleep(1)
            self.game_page.screenshot("13.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情2").click()
            time.sleep(1)
            self.game_page.screenshot("14.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情3").click()
            time.sleep(1)
            self.game_page.screenshot("15.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情4").click()
            time.sleep(1)
            self.game_page.screenshot("16.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情5").click()
            time.sleep(1)
            self.game_page.screenshot("17.png")
            time.sleep(2)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情6").click()
            time.sleep(1)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情7").click()
            time.sleep(1)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情8").click()
            time.sleep(1)
            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情9").click()
            time.sleep(1)

            self.game_page.wait_element("房间聊天按钮").click()
            time.sleep(3)
            self.game_page.wait_element("VIP表情续费").click()
            time.sleep(3)
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
            self.luadriver.keyevent(4)
            time.sleep(3)
            # self.game_page.wait_element("菜单").click()
            # time.sleep(2)
            # self.game_page.wait_element("退出").click()
            # time.sleep(3)
            self.game_page.wait_element("返回").click()
        else:
            print ("血战到底游戏不存在")

        PHPInterface.set_vip(mid, -1)
    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()


# class C31164_DFQP_Game_Gameroom_head3(TestCase):
#     '''
#     房间内自定义头像显示
#     '''
#     owner = "MindyZhang"
#     status = EnumStatus.Design
#     priority = EnumPriority.High
#     timeout = 10
#
#     def pre_test(self):
#         self.common = Common()
#         self.hall_page = Hall_Page()
#         self.game_page = Game_Page()
#         self.personinfo_page = Personinfo_Page()
#         # 初始化Luadriver
#         self.luadriver = self.common.setupdriver()
#         PHPInterface.set_env(PHPInterface.PRE_REPUBLISH_ENV)
#         # 关闭弹框
#         self.common.closeactivityprepublish(self.luadriver)
#         time.sleep(10)
#
#         self.start_step("获取用户mid")
#         self.personinfo_page.wait_element("头像").click()
#         time.sleep(3)
#         cid = self.personinfo_page.wait_element("账号ID").get_attribute('text')
#         print "获取的用户cid为: %s" % cid
#         global mid
#         mid = PHPInterface.get_mid(cid, region=1)
#         print "用户mid为：%s" % mid
#         # 获取用户银币信息
#         self.start_step("获取用户银币信息")
#         result_userinfo = PHPInterface.get_user_info(mid)
#         myuser_info = json.loads(result_userinfo)
#         coin = myuser_info.get('result', {'coin': None}).get('coin')
#         print "用户银币数为：%s" % coin
#         if (coin < 10000):
#             PHPInterface.add_money(mid, 10000)
#             self.common.closeactivityprepublish(self.luadriver)
#             time.sleep(10)
#         else:
#             self.game_page.wait_element("关闭对话框").click()
#             time.sleep(3)
#
#         vip = myuser_info.get('result',{'vip':None}).get('coin')
#         if(vip == -1):
#             self.start_step("设置玩家为vip")
#             PHPInterface.set_vip(mid,4)    #添加vip体验卡
#             self.common.closeactivityprepublish(self.luadriver)
#             time.sleep(10)
#     def run_test(self):
#         """
#         测试用例
#         """
#         self.start_step("点击头像")
#         self.hall_page.wait_element("头像").click()
#         time.sleep(3)
#         self.game_page.screenshot("1.png")
#         time.sleep(2)
#         self.game_page.wait_element("修改头像").click()
#         time.sleep(3)
#         self.start_step("拍照修改头像")
#         self.luadriver.find_element_by_id("android:id/text1").click()
#         time.sleep(3)
#         self.luadriver.keyevent(27)
#         # self.luadriver.find_element_by_accessibility_id("拍照").click()
#         time.sleep(10)
#         try:
#             # 取消选中
#             # self.luadriver.find_elements_by_class_name("android.widget.ImageView")[2].click()
#             # 选中图片
#             self.luadriver.find_elements_by_class_name("android.widget.ImageView")[4].click()
#         except:
#             print "未找到元素1"
#         try:
#             self.luadriver.find_elements_by_class_name("android.widget.TextView")[1].click()
#         except:
#             print "未找到元素2"
#         time.sleep(5)
#         try:
#             self.luadriver.find_element_by_id("com.android.gallery3d:id/head_select_right").click()
#         except:
#             print "未找到元素3"
#         try:
#             self.luadriver.find_element_by_id("com.sec.android.gallery3d:id/save").click()
#         except:
#             print "未找到元素3"
#         time.sleep(5)
#         self.game_page.screenshot('2.png')
#
#         self.game_page.wait_element("关闭对话框").click()
#         time.sleep(3)
#         self.start_step("点击血战到底：")
#         if (self.game_page.is_exist("血战到底") == True):
#             self.game_page.wait_element("血战到底").click()
#             time.sleep(3)
#
#             self.common.game_is_download()
#             time.sleep(2)
#             self.game_page.wait_element("快速开始").click()
#             time.sleep(3)
#             self.start_step("点击头像")
#             self.game_page.wait_element("头像---未开始游戏").click()
#             time.sleep(3)
#             self.game_page.screenshot("1-1.png")
#             self.luadriver.keyevent(4)
#             time.sleep(2)
#             self.luadriver.keyevent(4)
#             time.sleep(2)
#             self.game_page.wait_element("返回").click()
#             time.sleep(2)
#
#
#             else:
#                 print ("没有血战到底游戏")
#                 self.game_page.wait_element("左三角标").click()
#         PHPInterface.set_vip(mid, -1)
#     def post_test(self):
#
#         self.common.deletefile(self.luadriver)
#         self.common.closedriver()

__qtaf_seq_tests__ = [C31169_DFQP_Game_Gameroom_faceview1]

if __name__ =='__main__':
    debug_run_all()

