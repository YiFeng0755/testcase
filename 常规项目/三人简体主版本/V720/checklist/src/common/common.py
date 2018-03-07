#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import random
import sys

from selenium_rainbow.common.exceptions import NoSuchElementException

from uilib.game_page import Game_Page

reload(sys)
sys.setdefaultencoding( "utf-8" )
import time
import utils.constant as constant
from utils.confighelper import ConfigHelper
from appiumcenter.luadriver import LuaDriver
from appium_rainbow.webdriver.connectiontype import ConnectionType
from uilib.hall_page import Hall_Page
import threading
import Interface

class Common():

    def setupdriver(self,agrs={}):
        '''初始化driver
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

    def closeactivity_switchserver(self,luadriver):
        '''
        关闭活动页面，切换到指定服，然后再关闭弹出的活动页面
        '''
        # self.hall_page = Hall_Page()
        self.closeactivity()
        self.switchserver()
        time.sleep(8)
        self.closedriver()
        capabilities = {}
        capabilities['noReset'] = True
        self.setupdriver(capabilities)
        # self.hall_page.wait_element("同步标志", 12).click()
        self.closeactivity()

    def closeactivity(self):
        '''
       关闭活动页面
       '''
        self.hall_page = Hall_Page()
        time.sleep(6)
        self.hall_page.wait_element("同步标志")
        # self.hall_page.wait_element("同步标志").click()
        try:
            self.hall_page.wait_element("返回", 3).click()
        except:
            print "未出现关闭按钮"
        j = 0
        while j<2:
            try:
                elements = self.luadriver.find_elements_by_class_name("android.widget.Button")
                for h in range(len(elements)):
                    elements[h].click()
            except:
                print "未出现原生按钮"
            j +=1
        i = 0
        while i<2:
            try:
                if self.hall_page.element_is_exist("签到",2):
                    self.hall_page.wait_element("签到").click()
                self.hall_page.wait_element("关闭", 1).click()
            except:
                print "未出现关闭按钮"
            try:
                self.hall_page.wait_element("关闭1", 1).click()
            except:
                print "未出现关闭按钮"
            try:
                self.hall_page.wait_element("关闭3", 1).click()
            except:
                print "未出现关闭按钮"
            i +=1

    def user_money(self,money=1000):
        #判断当前用户金币数目,如果破产则增加金币
        env = self.get_config_value('casecfg', 'env')
        if env == "0":
            #如果是外网环境，则通过图片方式来获取金币数
            image_element = self.hall_page.wait_element("金币显示")
            # print "image_element"+image_element
            text = self.image_text(image_element)
            print "text:"+text
            if text.isdigit():
                if int(text) < int(money):
                    self.setting_imei()
            elif text.isdigit()==False:
                self.setting_imei()

        elif env == "1":
            mid = self.get_config_value('casecfg', 'mid')
            # money1 = Interface.get_money(mid)
            # if int(money1) < int(money):
            self.set_money(mid,money)

    def switchserver(self):
        '''
        根据cfg文件切换正式服，测试服，预发布服
        @return:
        '''
        self.hall_page = Hall_Page()
        self.hall_page.wait_element("切换环境按钮").click()
        while self.hall_page.element_is_exist("内网登录")==False:
            self.hall_page.wait_element("切换环境按钮").click()
            time.sleep(5)
        env = self.get_config_value('casecfg', 'env')
        if env=='0':
            try:
                self.hall_page.wait_element("外网正式登陆",20).click()
            except:
                print "外网正式登陆失败"
        elif env =='1':
            try:
                self.hall_page.wait_element("内网登录",20).click()
            except:
                print "内网登录失败"
        elif env =='2':
            try:
                self.hall_page.wait_element("外网测试登录",20).click()
            except:
                print "外网测试登录失败"
        time.sleep(3)
        i = 0
        while (i < 3):
            i += 1
            try:
                self.hall_page.wait_element("关闭",3).click()
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
            self.luadriver.find_element_by_android_uiautomator('new UiSelector().textMatches("确定|允许|允许一次")').click()
            # print "close1" + str(time.time())
        except:
            print "1:" + str(time.time())
        try:
            self.luadriver.find_element_by_android_uiautomator('new UiSelector().textMatches("确定|允许|允许一次")').click()
            # print "close2" + str(time.time())
        except:
            print "2:" + str(time.time())
        try:
            self.luadriver.find_element_by_android_uiautomator('new UiSelector().textMatches("确定|允许|允许一次")').click()
            # print "close3" + str(time.time())
        except:
            print "3:" + str(time.time())

    def swipeelement(self,element1,element2):
        swipe_startx = element1.location['x']
        swipe_starty = element1.location['y']
        swipe_endx = element2.location['x']
        swipe_endy = element2.location['y']
        print swipe_startx, swipe_starty, swipe_endx, swipe_endy
        self.luadriver.swipe(swipe_startx, swipe_starty, swipe_endx, swipe_endy,1000)

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

    def random_str(self,len):
        '''生成随机字符'''
        str = ""
        for i in range(len):
            str += (random.choice("safsdfsdfoewrweorewcvmdfadfdsafdskafaklvoreiutwuerpmvcmvasieqwoejandfsx1232183721873219731212345678890qweqweoieroeitoretoyriosadjaslkjf"
                                  "dsafkjljsxkznvcmxnvdfkjglajmndje"))
        return str

    def get_mid(self):
        '''获取用户mid'''
        self.hall_page = Hall_Page()
        self.hall_page.wait_element("头像").click()
        while self.hall_page.element_is_exist("用户ID") ==False:
            self.hall_page.wait_element("头像").click()
            time.sleep(1)
        userid = self.hall_page.wait_element("用户ID").get_attribute('text')
        mid =  filter(lambda ch: ch in '0123456789', userid)
        print "获取的用户mid为: %s" % mid
        self.hall_page.wait_element("返回").click()
        if (self.hall_page.element_is_exist("关闭")):  # 如果弹破产弹框，则关闭
            self.hall_page.wait_element("关闭").click()
        return mid

    def set_money(self,mid,value):
        # 获取用户金币信息
        money = Interface.get_money(mid)
        addmoney = int(value) - int(money)
        # print addmoney
        if addmoney < 0:
            Interface.add_money(mid, 0-addmoney,1)
        else:
            Interface.add_money(mid, addmoney, 0)
        # print Interface.get_money(mid)

    def image_text(self,elment1,image_name='11.bmp',lan="eng"):
        self.game_page = Game_Page()
        path = self.game_page.get_screenshot_by_element(elment1, image_name)
        # print path
        from utils.util import image_get_text
        text = image_get_text(path,lang=lan)
        # print "text:"+text
        return text

    def setting_imei(self):
        self.hall_page = Hall_Page()
        while self.hall_page.element_is_exist("imei输入框",1)==False:
            self.hall_page.wait_element("切换环境按钮").click()
        imei_text = self.random_str(random.randint(4,15))
        print imei_text
        self.hall_page.wait_element("imei输入框").send_keys(imei_text)
        self.hall_page.wait_element("imei输入框").click()
        while self.hall_page.element_is_exist("imei重登录"):
            self.hall_page.wait_element("imei重登录").click()
        # while self.hall_page.element_is_exist("试玩账号",1)==False:
        try:
            self.hall_page.wait_element("切换环境按钮").click()
            self.hall_page.wait_element("imei重登录").click()
        except:
            print "imei重登录"
        # self.closeactivity()
        while self.hall_page.element_is_exist("马上重连"):
            self.hall_page.wait_element("马上重连").click()
        while self.hall_page.element_is_exist("试玩账号"):
            self.hall_page.wait_element("试玩账号").click()
            self.hall_page.wait_element("继续游客登陆",20).click()
            # while self.hall_page.element_is_exist("签到"):
            #     self.hall_page.wait_element("签到").click()
        self.closeactivity()
        # self.hall_page.wait_element("同步标志")





