#!/usr/bin/env python
# -*- coding:utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import os,time,inspect
import random
import utils.util as util
from utils.confighelper import ConfigHelper
import utils.constant as constant
from runcenter.testcase import TestCase
from utils.confighelper import ConfigHelper
from appiumcenter.luadriver import LuaDriver
from appium_rainbow.webdriver.connectiontype import ConnectionType
from uilib.login_page import Login_Page
from uilib.setting_page import Setting_Page
from uilib.hall_page import Hall_Page
from uilib.sign_page import Sign_Page


class Common():

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
        luadriver 用于游戏操作，对应appium_for_bebe
        nativedriver 用于原生应用操作，对应appium_hybrid_support
        '''
        self.luaobj.closeLuadriver()

    def closefloatBall(self):
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()
        self.hall_page.wait_element("设置").click()
        time.sleep(2)
        try:
            self.setting_page.wait_element("关闭浮动球").click()
        except:
            print "浮动球已经关闭"
        self.setting_page.wait_element("页面返回").click()
        time.sleep(2)

    def changeServerView(self,name):
        self.hall_page = Hall_Page()
        self.hall_page.wait_element(name).click()
        time.sleep(5)

    def deletefile(self,driver):
        print "----删除自动登录文件----"
        #正式服
        command = "shell rm -r /mnt/sdcard/.com.boyaa.engineqpsc/dict/lastLoginInfo.dat"
        driver.adb(command)
        #测试服  1lastLoginInfo.dat
        command1 = "shell rm -r /mnt/sdcard/.com.boyaa.engineqpsc/dict/1lastLoginInfo.dat"
        driver.adb(command1)
        print command1

    def closeactivitytest(self,luadriver):
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        try:
            luadriver.find_element_by_name("允许").click()
        except:
            "未出现按钮"
        time.sleep(5)
        try:
            self.hall_page.wait_element("确认登陆").click()
        except:
            "未出现登陆按钮"
        i = 0
        while (i < 2):
            i += 1
            try:
                self.sign_page.wait_element("关闭1").click()
                time.sleep(1)
            except:
                try:
                    self.sign_page.wait_element("关闭1").click()
                    time.sleep(1)
                except:
                    "关闭对话框"
        try:
            self.hall_page.wait_element("测试服").click()
        except:
            "未出现测试服按钮"
        time.sleep(15)
        i = 0
        while(i < 2):
                i += 1
                try:
                    self.sign_page.wait_element("关闭1").click()
                    time.sleep(1)
                except:
                    try:
                        self.sign_page.wait_element("关闭1").click()
                        time.sleep(1)
                    except:
                        "关闭对话框"


    def closeactivity(self,luadriver):
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        try:
            luadriver.find_element_by_name("允许").click()
        except:
            print "未出现按钮"
        time.sleep(15)
        try:
            self.hall_page.wait_element("确认登陆").click()
        except:
            print "未出现登陆按钮"
        i = 0
        while (i < 2):
            i += 1
            try:
                self.sign_page.wait_element("关闭1").click()
                time.sleep(1)
            except:
                try:
                    self.sign_page.wait_element("关闭1").click()
                    time.sleep(1)
                except:
                    print "关闭对话框"
        try:
            self.hall_page.wait_element("正式服").click()
        except:
            print "未出现正式服按钮"
        time.sleep(15)
        i = 0
        while(i < 2):
                i += 1
                try:
                    self.sign_page.wait_element("关闭1").click()
                    time.sleep(1)
                except:
                    try:
                        self.sign_page.wait_element("关闭1").click()
                        time.sleep(1)
                    except:
                        print "关闭对话框"


    def switchnetwork(self,luadriver, network):
        '''
        测试用例运行过程中切换网络
        '''
        if(network == '无网络'):
            print "设置为无网络状态"
            luadriver.set_network_connection(ConnectionType.NO_CONNECTION)
            print luadriver.network_connection
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


    def isloginuser(self,luadriver):
        '''
        判断是否是注册账号登陆，如果不是则切换到注册账号
        :param user:
        :param passwd:
        :return:
        '''
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.closeactivity(luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(6)
        print self.setting_page.wait_element("安全绑定").get_attribute('text')
        if(self.setting_page.wait_element("安全绑定").get_attribute('text') != u"安全绑定"):
            return True
        else:
            return False

    def loginuser(self,user,passwd):
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()
        time.sleep(6)
        self.setting_page.wait_element("切换账号").click()
        time.sleep(2)
        try:
            self.setting_page.wait_element("继续切换账号").click()
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

    def swipeelement(self,element1,element2):
        element1_size_width = element1.size['width']
        element1_size_height = element1.size["height"]
        element1_1_x = element1.location["x"]
        element1_1_y = element1.location["y"]
        swipe_startx = element1.location['x']+element1.size['width']/2
        swipe_starty = element1.location['y']+element1.size['height']/2
        swipe_endx = element2.location['x']+element1.size['width']/2
        swipe_endy = element2.location['y']+element1.size['height']/2
        print element1_size_width,element1_size_height,element1_1_x,element1_1_y
        print swipe_startx, swipe_starty, swipe_endx, swipe_endy
        self.luadriver.swipe(swipe_startx, swipe_starty, swipe_endx, swipe_endy,1000)

    def restart(self):
        self.luaobj.closeLuadriver()
        self.luaobj.creatLuaDriver()
        self.luadriver = self.luaobj.getLuaDriver()
        self.closeactivity(self.luadriver)
        return self.luadriver

    def random_str(self,len):
        '''生成随机字符'''
        str = ""
        for i in range(len):
            str += (random.choice("SDFJSDFJSDJFSDJF4234234SDFJSDFDSFJSADJFsfjdskjfkdsjfkdsjf428347832748327"))
        return str

    def getdata(self,string):
        string1 = string.encode('gbk')
        print type(string1)
        data = filter(str.isdigit, string1)
        print data
        return data

    def closeactivityprepublish(self, luadriver):
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        try:
            luadriver.find_element_by_name("允许").click()
        except:
            "未出现按钮"
        time.sleep(5)
        try:
            self.hall_page.wait_element("确认登陆").click()
        except:
            "未出现登陆按钮"
        i = 0
        while (i < 2):
            i += 1
            try:
                self.sign_page.wait_element("关闭1").click()
                time.sleep(1)
            except:
                try:
                    self.sign_page.wait_element("关闭1").click()
                    time.sleep(1)
                except:
                    "关闭对话框"
        try:
            self.hall_page.wait_element("预发布").click()
        except:
            "未出现预发布按钮"
        time.sleep(10)
        i = 0
        while (i < 2):
            i += 1
            try:
                self.sign_page.wait_element("关闭1").click()
                time.sleep(1)
            except:
                try:
                    self.sign_page.wait_element("关闭1").click()
                    time.sleep(1)
                except:
                    "关闭对话框"
