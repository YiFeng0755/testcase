#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import sys

import datetime
from utils.loghelper import Logger

from com import Interface
from com.globalVars import singleGlobalVar
from uilib.game_page import Game_Page
from uilib.level_page import Level_Page

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
        self.level_page = Level_Page()
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
        # self.hall_page = Hall_Page()
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
        while self.hall_page.element_is_exist("用户ID",1) ==False:
            self.hall_page.wait_element("头像",0).click()
        userid = self.hall_page.wait_element("用户ID").get_attribute('text')
        mid =  filter(lambda ch: ch in '0123456789', userid)
        print "获取的用户mid为: %s" % mid
        self.hall_page.wait_element("返回").click()
        if (self.hall_page.element_is_exist("关闭")):  # 如果弹破产弹框，则关闭
            self.hall_page.wait_element("关闭").click()
        self.set_config_value("casecfg","mid",str(mid))

    def set_money(self,mid,value):
        # 获取用户金币信息
        money = Interface.get_money(mid)
        addmoney = int(value) - int(money)
        # print addmoney
        if addmoney < 0:
            Interface.add_money(mid, 0 - addmoney, 1)
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
            self.hall_page.wait_element("切换环境按钮",0).click()
        imei_text = self.random_str(random.randint(4,15))
        print imei_text
        self.hall_page.wait_element("imei输入框",0).send_keys(imei_text)
        self.hall_page.wait_element("imei输入框",0).click()
        while self.hall_page.element_is_exist("imei重登录",3):
            self.hall_page.wait_element("imei重登录",0).click()
        # while self.hall_page.element_is_exist("试玩账号",1)==False:
        try:
            self.hall_page.wait_element("切换环境按钮",0).click()
            self.hall_page.wait_element("imei重登录",0).click()
        except:
            print "imei重登录"
        # self.closeactivity()
        while self.hall_page.element_is_exist("马上重连",3):
            self.hall_page.wait_element("马上重连",0).click()
        while self.hall_page.element_is_exist("试玩账号",3):
            self.hall_page.wait_element("试玩账号",0).click()
            self.hall_page.wait_element("继续游客登陆").click()
            # while self.hall_page.element_is_exist("签到"):
            #     self.hall_page.wait_element("签到").click()
        self.closeactivity()
        # self.hall_page.wait_element("同步标志")

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
            cmd_minicap = cmd_pre + self.getResolution()+  "/0 -s >/mnt/sdcard/minicap_screen/" + fileName
            self.platformLog(cmd_pre)
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







