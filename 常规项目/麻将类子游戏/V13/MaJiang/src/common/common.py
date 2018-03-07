#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import random
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import os,time,inspect
import utils.constant as constant
from utils.confighelper import ConfigHelper
from appiumcenter.luadriver import LuaDriver
from appium_rainbow.webdriver.connectiontype import ConnectionType
from uilib.hall_page import Hall_Page
from uilib.sign_page import Sign_Page
from uilib.setting_page import Setting_Page
from uilib.personinfo_page import Personinfo_Page
import utils.user_util as user_util
from utils.loghelper import Logger
import threading
import Interface as PHPInterface
from uilib.login_page import Login_Page
from utils.constant import cfg_path

class Common():
    def __init__(self):
        self.log = Logger().get_logger()

    def platformLog(self,*arg):
        logStr = ""
        for v in arg:
            if type(v) != str:
                v = str(v)
            logStr = logStr + " " + v
        self.log.info(logStr)

    def setupdriver(self,agrs={}):
        '''初始化driver
        luadriver 用于游戏操作，对应appium
        '''
        # 初始化Luadriver
        self.luaobj = LuaDriver()
        self.luaobj.creatLuaDriver(agrs)
        self.luadriver = self.luaobj.getLuaDriver()
        return self.luadriver

    def closedriver(self):
        '''关闭driver
        '''
        self.luaobj.closeLuadriver()

    def closefloatBall(self):
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()
        self.hall_page.wait_element("设置").click()
        try:
            self.setting_page.wait_element("关闭浮动球").click()
        except:
            print "浮动球已经关闭"
        try:
            self.setting_page.wait_element("页面返回").click()
        except:
            print "已经关闭"

    def deletefile(self,driver):
        print "----删除自动登录文件----"
        config = ConfigHelper(constant.cfg_path)
        package =config.getValue('appium', 'apppackage')
        command = "shell rm -r /mnt/sdcard/."+package+"/dict/lastLoginInfo.dat"
        print command
        try:
            driver.adb(command)
        except:
            print "命令执行失败"
        command1 = "shell rm -r /mnt/sdcard/."+package+"/dict/1lastLoginInfo.dat"
        print command1
        try:

            driver.adb(command1)
        except:
            print "命令执行失败"
        command2 = "shell rm -r /mnt/sdcard/."+package+"/dict/2lastLoginInfo.dat"
        try:
            driver.adb(command2)
        except:
            print "命令执行失败"
        print command2

    def closeactivity(self,luadriver):
        '''
       关闭活动页面
       '''
        self.hall_page = Hall_Page()
        time.sleep(20)
        # try:
        #     if(self.luadriver.find_element_by_android_uiautomator('new UiSelector().textMatches("允许")')!=None):
        #         self.luadriver.find_element_by_android_uiautomator('new UiSelector().textMatches("允许")').click()
        # except:
        #     print "未出现允许按钮"

        self.hall_page.wait_element("头像",90)
        # try:
        #     if(self.luadriver.find_element_by_android_uiautomator('new UiSelector().textMatches("允许")')!=None):
        #         self.luadriver.find_element_by_android_uiautomator('new UiSelector().textMatches("允许")').click()
        # except:
        #     print "未出现允许按钮"
        try:
            self.hall_page.wait_element("新手任务",8).click()
        except:
            print "未出现新手任务按钮"
        try:
            self.hall_page.wait_element("确认登陆",2).click()
        except:
            print "未出现登陆按钮"
        try:
            self.hall_page.wait_element("立即升级绑定账号",2).click()
            self.sign_page.wait_element("关闭1",2).click()
        except:
            print "未出现立即升级绑定账号按钮"

        #2017-9-27 JessicZeng  增加关闭版本升级框
        try:
            self.hall_page.wait_element("资源下载-取消",2).click()
        except:
            print "未出现版本升级框"


        self.closeActivityBtn()
        # try:
        #     luadriver.find_element_by_name("允许").click()
        # except:
        #     print "未出现按钮"


    def closeactivity_switchserver(self,luadriver):
        '''
        关闭活动页面，切换到指定服，然后再关闭弹出的活动页面
        :param luadriver:
        :param switchserver:
        :return:
        '''
        self.closeactivity(luadriver)
        self.switchserver_init()
        self.closeactivity(luadriver)

    def switchserver(self):
        '''
        根据cfg文件切换正式服，测试服，预发布服
        @return:
        '''
        self.hall_page = Hall_Page()
        env = self.get_config_value('casecfg', 'env')
        if env=='0':
            try:
                self.hall_page.wait_element("正式服").click()
            except:
                print "切换到正式服失败"
        elif env =='1':
            try:
                self.hall_page.wait_element("测试服").click()
            except:
                print "切换到测试服失败"
        elif env =='2':
            try:
                self.hall_page.wait_element("预发布").click()
            except:
                print "切换到预发布失败"
        else:
            try:
                self.hall_page.wait_element("预发布").click()
            except:
                print "切换到预发布服失败"
    time.sleep(5)

    def switchserver_init(self):
        '''
        根据cfg文件切换正式服，测试服，预发布服
        @return:
        '''
        self.hall_page = Hall_Page()
        env = self.get_config_value('casecfg', 'env')
        if self.hall_page.element_is_exist("测试按钮"):
            self.hall_page.wait_element("测试按钮").click()
            if self.hall_page.element_is_exist("切换环境"):
                self.hall_page.wait_element("切换环境").click()
                if env == '0':
                    try:
                        # while self.hall_page.element_is_exist("正式1", 2):
                            self.hall_page.get_element("正式1").click()
                    except:
                        print "切换到正式服失败"
                elif env == '1':
                    try:
                        # while self.hall_page.element_is_exist("测试1",2):
                            self.hall_page.get_element("测试1").click()
                    except:
                        print "切换到测试服失败"
                elif env == '2':
                    try:
                        # while self.hall_page.element_is_exist("预发布1", 2):
                            self.hall_page.get_element("预发布1").click()
                    except:
                        print "切换到预发布失败"
                else:
                    try:
                        # while self.hall_page.element_is_exist("预发布1", 2):
                            self.hall_page.get_element("预发布1").click()

                    except:
                        print "切换到预发布服失败"
            else:
                self.hall_page.wait_element("关闭测试页面").click()
                if env=='0':
                    try:
                        self.hall_page.wait_element("正式服").click()
                    except:
                        print "切换到正式服失败"
                elif env =='1':
                    try:
                        self.hall_page.wait_element("测试服").click()
                    except:
                        print "切换到测试服失败"
                elif env =='2':
                    try:
                        self.hall_page.wait_element("预发布").click()
                    except:
                        print "切换到预发布失败"
                else:
                    try:
                        self.hall_page.wait_element("预发布").click()
                    except:
                        print "切换到预发布服失败"
            time.sleep(15)

    def closeActivityBtn(self):
        '''
        关闭活动弹框
        :return:
        '''
        self.sign_page = Sign_Page()
        self.hall_page = Hall_Page()
        try:
            self.hall_page.wait_element("新手任务",6).click()
        except:
            print "未出现新手任务按钮"
        i = 0
        while (i < 5):
            i += 1
            try:
                self.sign_page.wait_element("关闭1",3).click()
            except:
                print "关闭对话框"

    def switchnetwork(self, luadriver, network):
        '''
        测试用例运行过程中切换网络
        '''
        if(network == '无网络'):
            print "设置为无网络状态"
            luadriver.set_network_connection(ConnectionType.NO_CONNECTION)
        if(network == 'WIFI模式'):
            print "设置为WIFI模式"
            luadriver.set_network_connection(ConnectionType.WIFI_ONLY)
        if(network == '数据网络'):
            print "设置为数据网络模式"
            luadriver.set_network_connection(ConnectionType.DATA_ONLY)
        if(network == '飞行模式'):
            print "设置为飞行模式"
            luadriver.set_network_connection(ConnectionType.AIRPLANE_MODE)
        if(network == '全部网络打开模式'):
            print "设置为全部网络打开模式"
            luadriver.set_network_connection(ConnectionType.ALL_NETWORK_ON)

    def network_connect(self):
        '''
        2个线程的方式启动网络
        '''
        # print self.luadriver.network_connection
        if self.luadriver.network_connection != 2:
            t1 = threading.Thread(target=self.switch_network)
            t2 = threading.Thread(target=self.closebtn)
            t1.start()
            t2.start()
            t1.join()
            t2.join()

    def switch_network(self):
        '''
        测试用例运行过程中切换网络
        '''
        cmd = "shell am start -n com.example.unlock/.Unlock"
        print "adb start:" + str(time.time())
        self.luadriver.adb(cmd)
        print "adb end:" + str(time.time())

    def closebtn(self):
        time.sleep(1)
        print "closebtn" + str(time.time())
        try:
            self.luadriver.find_element_by_android_uiautomator('new UiSelector().textMatches("确定|允许")').click()
            print "close1" + str(time.time())
        except:
            print "1" + str(time.time())
        try:
            self.luadriver.find_element_by_android_uiautomator('new UiSelector().textMatches("确定|允许")').click()
            print "close2" + str(time.time())
        except:
            print "2" + str(time.time())
        try:
            self.luadriver.find_element_by_android_uiautomator('new UiSelector().textMatches("确定|允许")').click()
            print "close3" + str(time.time())
        except:
            print "3" + str(time.time())

    def swipeelement(self,element1,element2):
        # swipe_startx = element1.location['x']+element1.size['width']/2
        # swipe_starty = element1.location['y']+element1.size['height']/2
        swipe_startx = element1.location['x']
        swipe_starty = element1.location['y']
        # swipe_endx = element2.location['x']+element1.size['width']/2
        # swipe_endy = element2.location['y']+element1.size['height']/2
        swipe_endx = element2.location['x']
        swipe_endy = element2.location['y']
        print swipe_startx, swipe_starty, swipe_endx, swipe_endy
        self.luadriver.swipe(swipe_startx, swipe_starty, swipe_endx, swipe_endy,1000)

    def get_user(self):
        '''
        获取账号信息
        '''
        global user_info
        user_info = user_util.gimme_afree_account()
        while user_info ==None:
            time.sleep(5)
            user_info = user_util.gimme_afree_account()
        return user_info

    def release_user(self,user):
        '''
        释放用户
        '''
        print "release"
        print user
        try:
            user_util.release_account(user)
        except:
            print "release user fail"

    def get_cid(self):
        '''获取用户cid'''
        self.personinfo_page = Personinfo_Page()
        self.personinfo_page.wait_element("头像").click()
        cid = self.personinfo_page.wait_element("账号ID").get_attribute('text')
        print "获取的用户cid为: %s" % cid
        self.personinfo_page.wait_element("关闭").click()
        if (self.personinfo_page.element_is_exist("关闭")):  # 如果弹破产弹框，则关闭
            self.personinfo_page.wait_element("关闭").click()
        return cid

    def get_mid(self):
        cid = self.get_cid()
        time.sleep(3)
        config = ConfigHelper(constant.cfg_path)
        region = config.getValue('casecfg', 'region')
        mid = PHPInterface.get_mid(cid, region)
        print "用户mid为：%s" % mid
        return mid

    def set_coin(self,mid,value):
        # 获取用户银币信息
        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        coin = myuser_info.get('result', {'coin': None}).get('coin')
        AddMoney = int(value) - int(coin)
        result = PHPInterface.add_money(mid, AddMoney)
        print "用户银币数为：%s" % AddMoney,"加金币执行结果：",result

    def set_crystal(self,mid,value):
        # 设置金条数据
        result_userinfo = PHPInterface.get_user_info(mid)
        myuser_info = json.loads(result_userinfo)
        crystal = myuser_info.get('result', {'crystal': None}).get('crystal')  # 获取当前金条值
        print "用户金条数为：%s" % crystal
        AddMoney = int(value) - int(crystal)
        PHPInterface.add_crystal(mid, AddMoney)

    def loginuser(self,user,passwd):
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()
        time.sleep(6)
        self.setting_page.wait_element("切换账号").click()
        time.sleep(2)
        try:
            self.setting_page.wait_element("继续登录").click()
        except:
            print "不需要继续切换"
        try:
            self.setting_page.wait_element("删除历史账号").click()
        except:
            print "无历史账号"
        time.sleep(1)
        self.setting_page.wait_element("手机号码").send_keys(user)
        time.sleep(1)
        self.setting_page.wait_element("密码").send_keys(passwd)
        time.sleep(1)
        self.setting_page.wait_element("确认登陆").click()
        time.sleep(10)
        self.hall_page.wait_element("同步标志")
        time.sleep(1)

    def get_idle_userinfo_and_mid(self):
        '''
        获取一个空闲账号的mid
        :return:
        '''
        user_info = self.get_user()
        print user_info
        UserCID = user_info.get('cid')
        config = ConfigHelper(cfg_path)
        region = config.getValue('casecfg', 'region')
        UserMID = PHPInterface.get_mid(UserCID, region)
        mid_and_userinfo = {}
        mid_and_userinfo['userinfo'] = user_info
        mid_and_userinfo['mid'] = UserMID
        return mid_and_userinfo

    def unlock(self):
        #解锁
        self.luadriver.adb("shell am start -n com.example.unlock/.Unlock")
        time.sleep(4)
        self.luadriver.keyevent(3)  # home
        time.sleep(3)
        self.luadriver.adb("shell am start -n com.example.unlock/.Unlock")
        self.luadriver.keyevent(3)  # home
        time.sleep(3)
        print "读配置,拉起游戏"
        config=ConfigHelper(constant.cfg_path)
        self.luadriver.start_activity(config.getValue('appium','apppackage'), config.getValue('appium','appactivity'))

    def get_config_value(self,section,key):
        #从cfg.ini文件获取配置项的值
        config = ConfigHelper(constant.cfg_path)
        value =config.getValue(section, key)
        return value

    def set_config_value(self,section,key,value):
        #设置cfg.ini文件获取配置项的值
        config = ConfigHelper(constant.cfg_path)
        config.modifConfig(section, key,value)
        return True

    def recover_user(self,mid):
        #初始化用户
        self.set_coin(mid,'10000')
        self.set_crystal(mid,"0")
        PHPInterface.set_vip(mid,"-1")
        self.set_safeBoxMoney(mid,0,0)
        self.set_safeBoxMoney(mid,0,1)

    def random_str(self,len):
        '''生成随机字符'''
        str = ""
        for i in range(len):
            str += (random.choice("safsdfsdfoewrweorewcvmdfadfdsafdskafaklvoreiutwuerpmvcmvasieqwoejandfsxmndje"))
        return str

    def set_safeBoxMoney(self,mid, money, money_type):
        #money_type=0银币，1为金条
        safeBoxInfo = PHPInterface.get_safebox(mid)
        if money_type == 0:
            safeBoxMoney=int(safeBoxInfo.get("safebox"))
        else:
            safeBoxMoney = int(safeBoxInfo.get("crystalsafebox"))
                
        if safeBoxMoney - money > 0:
            PHPInterface.withdraw_safebox(mid, safeBoxMoney - money, money_type)
            if money_type ==0:
                PHPInterface.add_money(mid, -(safeBoxMoney - money))
            else:
                PHPInterface.add_crystal(mid, -(safeBoxMoney - money))            
        else:
            if money_type ==0:
                PHPInterface.add_money(mid, money - safeBoxMoney)
            else:
                PHPInterface.add_crystal(mid, money - safeBoxMoney)
            
            PHPInterface.deposit_safebox(mid, money - safeBoxMoney, money_type)

    def room_set_cheat(self, game_list, switch=1):
        for i in range(len(game_list)):
            gameId = filter(lambda ch: ch in '0123456789', game_list[i].get_attribute("name"))
            if switch == 1:
                print "设置子游戏:%s 标准场为作弊场" % gameId
            else:
                print "设置子游戏:%s 标准场为非作弊场" % gameId
            for i in range(4):
                PHPInterface.set_cheat(gameid=gameId, playmode=i, switch=switch)

    def set_robot(self,gameid,level=12,robotflag=0):
        '''
        设置机器人开关
        '''
        gamecfg = PHPInterface.get_levelconfig(gameid, 0, 0, level)
        robotflag1 = gamecfg.get('values', {'ADDROBOTFLAG': None}).get('ADDROBOTFLAG')
        if (robotflag1 != robotflag):
            result = PHPInterface.set_robot_flag(gameid, 0, 0, level, robotflag=robotflag)
            print result
        return True

    def checkPopVisible(self,driver,page,flagElName="同步标志"):
        '''
        根据page同步标志判断弹框是否存在，直至元素不存在或者操作次数操作3次
        :param page: 操作页
        :param flagElName: 同步标志元素name
        :return:
        '''
        cnt = 0
        while cnt < 3:
            try:
                page.get_element(flagElName)
                if driver != None :
                    driver.keyevent(4)
                    print "关闭弹框",page
            except:
                break
            cnt = cnt + 1