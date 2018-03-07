#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import sys

import datetime
from utils.loghelper import Logger

from com import Interface
from com.globalVars import singleGlobalVar
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


class Common():
    def __init__(self):
        self.log = Logger().get_logger()
        self.resolution = None
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

    def setupdriver(self,agrs={}):
        '''初始化driver
        '''
        # 初始化Luadriver
        self.luaobj = LuaDriver()
        self.luaobj.creatLuaDriver(agrs)
        self.luadriver = self.luaobj.getLuaDriver()
        singleGlobalVar.set_map("luaDriver", self.luaobj.getLuaDriver())

    def closedriver(self):
        '''关闭driver
        '''
        singleGlobalVar.get("luaDriver").quit()

    def platformLog(self,msg):
        logStr = ""
        for v in msg:
            if type(v) != str:
                v = str(v)
            logStr = logStr + v
        self.log.info(logStr)

    def closeactivity(self):
        '''
       关闭活动页面
       '''
        # self.hall_page = Hall_Page()
        time.sleep(6)
        self.hall_page.wait_element("同步标志")
        # self.hall_page.wait_element("同步标志").click()
        try:
            self.hall_page.wait_element("返回", 1).click()
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
        while i<1:
            try:
                if self.hall_page.element_is_exist("签到",1):
                    self.hall_page.wait_element("签到",0).click()
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


    def deletefile(self):
        driver = singleGlobalVar.get("luaDriver")
        self.platformLog("deleteFile  开始测试前删除配置及性能相关文件")
        config = ConfigHelper(constant.cfg_path)
        package =config.getValue('appium', 'apppackage')
        #删除性能测试结果文件
        delCsvCmd = "shell rm -r /mnt/sdcard/" + package + "_result.csv"
        self.platformLog(delCsvCmd)
        try:
            driver.adb(delCsvCmd)
        except:
            self.platformLog("删除性能测试文件失败")
        #minicap截图文件夹
        delMinicapCmd = "shell rm -rf /mnt/sdcard/minicap_screen"
        self.platformLog(delMinicapCmd)
        try:
            driver.adb(delMinicapCmd)
        except:
            self.platformLog("删除minicap截图文件夹失败")
        mkdirCmd = "shell mkdir /mnt/sdcard/minicap_screen"
        self.platformLog(mkdirCmd)
        try:
            driver.adb(mkdirCmd)
        except:
            self.platformLog("新建minicap截图文件夹失败")


    def delete_command(self, filepath, flag=False):
        driver = singleGlobalVar.get("luaDriver")
        config = ConfigHelper(constant.cfg_path)
        package =config.getValue('appium', 'apppackage')
        if flag == True:
            delFile = "shell rm -r "+ filepath + package
        else:
            delFile = "shell rm -r "+ filepath
        try:
            self.platformLog("deleteFile "+ delFile)
            driver.adb(delFile)
        except:
            self.platformLog("删除文件失败%s" %filepath)

    def getResumeTime(self):
        '''
        获取游戏启动完成时间，目前是头像元素出现的时间
        '''
        time.sleep(2)
        self.platformLog("-------------getResumeTime----------")
        try:
            self.hall_page.wait_element("启动完成标志",180,0.1)
            # utc = '%.2f' % (time.time())
            print "apk start completely"
            self.platformLog("apk start completely")
        except:
            self.platformLog("获取标志app成功成功元素失败")

    def startCollectApp(self):
        '''
        启动性能采集apk
        '''
        self.platformLog("startCollectApp start pmonitor apk")
        config = ConfigHelper(constant.cfg_path)
        #性能采集apk acticity
        apkName = config.getValue('appium', 'collectApkName')
        # 被测apk packageName
        testAPKName = config.getValue('appium', 'apppackage')
        # 最终生成结果文件在手机中目录
        resultFilePath = "/mnt/sdcard/" + testAPKName + "_result.csv"

        # SDK 17后由于权限问题，需要加--user 0
        startCmd = "shell am start --user 0 -n " + apkName + " --es packageName " + testAPKName + " --es filePath " + resultFilePath
        self.platformLog(startCmd)
        singleGlobalVar.get("luaDriver").adb(startCmd)

    def sendStopServiceBroad(self):
        self.platformLog("sendStopServiceBroad")
        # 广播类型
        broadcastType = "com.boyaa.stf.stopService"
        cmd_send = "shell am broadcast -a " + broadcastType
        singleGlobalVar.get("luaDriver").adb(cmd_send)

    def sendTagBroadcast(self,tagName,tagType):
        '''
        向性能采集apk发送场景广播
        :param tagName:
        :param tagType:
        :return:
        '''
        #广播类型
        broadcastType = "com.boyaa.stf.UIScript"
        cmd_send ="shell am broadcast -a " + broadcastType + " --es tagName " + tagName + " --es tagType " + tagType
        self.platformLog(cmd_send)
        singleGlobalVar.get("luaDriver").adb(cmd_send)


    def getResolution(self):
        '''
        获取分辨率
        :return: 直接返回的是minicap截图需要的分辨率参数 游戏会自动设置横屏，所以width>height
        '''
        if(self.resolution == None):
            screenWidth = singleGlobalVar.get("luaDriver").get_window_size()['width']
            screenHeigth = singleGlobalVar.get("luaDriver").get_window_size()['height']
            self.resolution = str(screenWidth) + "x" + str(screenHeigth) + "@" + str(screenWidth) + "x" + str(screenHeigth)
        return self.resolution

    def taskScreenShot(self,fileName):
        '''
        由于appium截图效率问题，改为stf平台的minicap进行截图，其中-P如下：
        The format of the -P argument is: {RealWidth}x{RealHeight}@{VirtualWidth}x{VirtualHeight}/{Orientation}. The "virtual" size is the size of the desired projection.
        The orientation argument tells minicap what the current orientation of the device is (in degrees),
        可执行minicap命令：
        adb shell LD_LIBRARY_PATH=/data/local/tmp exec /data/local/tmp/minicap -P 720x1280@720x1280/90 -s >/sdcard/minicap_1504612944860.jpg
        :param page:  元素所在page页
        :param fileName: 截图保存的文件名
        :return:
        '''
        driver = singleGlobalVar.get("luaDriver")
        try:
            broadcastType = "com.boyaa.stf.screenShot"
            cmd_send = "shell am broadcast -a " + broadcastType + " --es sShotName " + fileName
            self.platformLog(cmd_send)
            driver.adb(cmd_send)
        except:
            self.platformLog("通知apk截图时间失败")

        try:
            cmd_pre = "shell LD_LIBRARY_PATH=/data/local/tmp exec /data/local/tmp/minicap -P "
            cmd_minicap = cmd_pre + self.getResolution() + "/0 -s >/mnt/sdcard/minicap_screen/" + fileName
            self.platformLog(cmd_minicap)
            driver.adb(cmd_minicap)
        except:
            self.platformLog("调用minicap截图失败")

    @staticmethod
    def printStr(*info):
        '''
        打印log，自动将所有传入非字符串类型转换为字符串然后打印出来
        '''
        logStr = ""
        for v in info:
            if type(v) != str:
                v = str(v)
            logStr = logStr + v
        timeStamp = str(datetime.datetime.now())
        print timeStamp + " " + logStr

    def set_config_value(self,section,key,value):
        #设置cfg.ini文件获取配置项的值
        config = ConfigHelper(constant.cfg_path)
        config.modifConfig(section, key,value)
        return True

    def get_config_value(self,section,key):
        #从cfg.ini文件获取配置项的值
        config = ConfigHelper(constant.cfg_path)
        value =config.getValue(section, key)
        return value







