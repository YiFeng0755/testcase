#!/usr/bin/env python
# -*- coding:utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import time,os,datetime
import random
import utils.constant as constant
from utils.loghelper import Logger
import string
from globalVars import singleGlobalVar
from cfg.constantEnum import EnumDirection
from utils.confighelper import ConfigHelper
from appiumcenter.luadriver import LuaDriver
from appiumcenter.element import Element
from appium_rainbow.webdriver.connectiontype import ConnectionType
from uilib.login_page import Login_Page
from uilib.setting_page import Setting_Page
from uilib.hall_page import Hall_Page
from uilib.sign_page import Sign_Page
from uilib.game_page import Game_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.safebox_page import Safebox_Page
import Interface as PHPInterface

class Common():

    def __init__(self):
        self.log = Logger().get_logger()
        self.resolution = None
        self.orientation = None

    def setupdriver(self,agrs={}):
        '''初始化driver
        全局共用driver  其余地方都是通过new LuaDriver().getgetLuaDriver()获取
        luadriver 用于游戏操作，对应appium
        '''
        self.platformLog("---------setupdriver---------")
        # 初始化Luadriver
        self.luaobj = LuaDriver()
        self.luaobj.creatLuaDriver(agrs)
        singleGlobalVar.set_map("luaDriver",self.luaobj.getLuaDriver())

    def closedriver(self):
        '''关闭driver
        '''
        singleGlobalVar.get("luaDriver").quit()

    def checkPopVisible(self,page,flagElName="同步标志"):
        '''
        根据page同步标志判断弹框是否存在，直至元素不存在或者操作次数操作3次
        :param page: 操作页
        :param flagElName: 同步标志元素name
        :param closeElName:关闭弹框元素name
        :return:
        '''
        cnt = 0
        while cnt < 3:
            print "cnt:"+str(cnt)
            try:
                page.get_element(flagElName)
                if singleGlobalVar.get("luaDriver") != None:
                    singleGlobalVar.get("luaDriver").keyevent(4)
            except:
                break
                print "该pop已关闭"
            cnt = cnt + 1


    def deletefile(self):
        driver = singleGlobalVar.get("luaDriver")
        self.platformLog("deleteFile  开始测试前删除配置及性能相关文件")
        config = ConfigHelper(constant.cfg_path)
        package =config.getValue('appium', 'apppackage')

        #正式服
        command = "shell rm -r /mnt/sdcard/."+package+"/dict/lastLoginInfo.dat"
        self.platformLog(command)
        try:
            driver.adb(command)
        except:
            self.platformLog("删除正式服上次登录配置文件失败")

        #预发布  1lastLoginInfo.dat
        command1 = "shell rm -r /mnt/sdcard/."+package+"/dict/1lastLoginInfo.dat"
        self.platformLog(command1)
        try:

            driver.adb(command1)
        except:
            self.platformLog("删除预发布1lastLoginInfo.dat失败")

        # 预发布  2lastLoginInfo.dat
        command2 = "shell rm -r /mnt/sdcard/."+package+"/dict/2lastLoginInfo.dat"
        self.platformLog(command2)
        try:
            driver.adb(command2)
        except:
            self.platformLog("删除预发布1lastLoginInfo.dat失败")

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

    def closeActivity(self):
        '''
        关闭活动页面，切换到指定服，然后再关闭弹出的活动页面
        :param switchserver:
        :return:
        '''
        driver = singleGlobalVar.get("luaDriver")
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()

        #性能测试中启动完成后才开始关闭活动弹框，sleep可省略
        # time.sleep(8)
        try:
            driver.find_element_by_name("允许").click()
        except:
            print "未出现允许按钮"
        try:
            driver.find_element_by_tag_name("允许").click()
        except:
            print "未出现允许按钮"
        try:
            driver.find_elements_by_class_name("android.widget.Button")[1].click()
        except:
            print "未出现android.widget.Button按钮"
        time.sleep(10)
        try:
            self.hall_page.wait_element("确认登陆").click()
        except:
            print "未出现确认登陆按钮"
        try:
            self.hall_page.wait_element("立即升级绑定账号").click()
            time.sleep(1)
            self.sign_page.wait_element("关闭1").click()
        except:
            print "未出现立即升级绑定账号按钮"
        #添加破产奖励领取，由于目前只能在正式服测试  导致所有接口不能用   先领取破产奖励，避免弹框对其他场景影响
        try:
            self.hall_page.wait_element("破产领奖按钮").click()
            self.platformLog("领取破产奖励")
        except:
            print "没有破产按钮"

        self.closeActivityBtn()
        try:
            self.hall_page.wait_element("新手任务").click()
            time.sleep(2)
        except:
            print "未出现新手任务按钮"
        try:
            driver.find_element_by_name("允许").click()
        except:
            print "未出现允许按钮"


    def closeActivityBtn(self):
        '''
        关闭活动弹框
        :return:
        '''
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        i = 0
        while (i < 4):
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


    def moveElement(self,startEl,endEl):
        '''
        滑动元素  将元素从位置1滑动到位置2  以元素中心位置进行滑动
        :param element1:  滑动开始元素名
        :param element2:  滑动结束元素名
        :return:
        '''
        swipe_startx = startEl.location['x']+startEl.size['width']/2
        swipe_starty = startEl.location['y']+startEl.size['height']/2

        swipe_endx = endEl.location['x']+endEl.size['width']/2
        swipe_endy = endEl.location['y']+endEl.size['height']/2
        singleGlobalVar.get("luaDriver").swipe(swipe_startx, swipe_starty, swipe_endx, swipe_endy,1000)

    def swipeList(self,listEl,dir=EnumDirection.Up,devPos = 20):
        '''
        滑动列表  以中心点进行滑动
        :param listEl: 需进行滑动的列表元素
        :param dir:滑动方向  EnumDirection.Up Down Left Right
        :param devPos:滑动偏移值
        :return:
        '''
        driver = singleGlobalVar.get("luaDriver")
        elLocation = listEl.location
        elSize = listEl.size
        startX = elLocation['x']
        centerX = elLocation['x'] + elSize['width']/2
        endX = elLocation['x'] + elSize['width'] - devPos
        startY = elLocation['y']
        centerY = elLocation['y'] + elSize['height']/2
        endY = elLocation['y'] + elSize['height'] - devPos
        if dir == EnumDirection.Up:
            driver.swipe(centerX,endY,centerX,startY)
        elif dir == EnumDirection.Down:
            driver.swipe(centerX, startY, centerX, endY)
        elif dir == EnumDirection.Left:
            driver.swipe(endX,centerY,startX,centerY)
        elif dir == EnumDirection.Right:
            driver.swipe(startX,centerY,endX,centerY)

        time.sleep(1)

    #从26个大小写字母及数字从随机生成指定长度的字符串
    def random_str(self,len):
        '''生成随机字符'''
        str = ""
        resourceStr = string.ascii_letters + string.digits
        for i in range(len):
            str += (random.choice(resourceStr))
        return str

    def addmoney(self,mid):
        '''
        破产账号充值
        :return:
        '''
        user_info = PHPInterface.get_user_info(mid)  # 获取玩家信息
        coin = eval(user_info).get('result', {'coin': None}).get('coin')  # 获取当前银币值
        print coin
        AddMoney = 10000 - coin
        print AddMoney
        PHPInterface.add_money(mid, AddMoney)  # 将银币值设为60000

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
        try:
            driver = singleGlobalVar.get("luaDriver")
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

    def getResumeTime(self):
        '''
        获取游戏启动完成时间，目前是头像元素出现的时间
        :return:
        '''
        time.sleep(5)
        self.platformLog("-------------getResumeTime----------")
        hallPage = Hall_Page()
        try:
            hallPage.wait_element("启动完成标志",180,0.1)
            # utc = '%.2f' % (time.time())
            print "apk start completely"
            self.platformLog("apk start completely")
        except:
            self.platformLog("获取标志app成功成功元素失败")

    def startCollectApp(self):
        '''
        启动性能采集apk
        :return:
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

    def platformLog(self,msg):
        logStr = ""
        for v in msg:
            if type(v) != str:
                v = str(v)
            logStr = logStr + v
        self.log.info(logStr)

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

    def sendStopServiceBroad(self):
        self.platformLog("sendStopServiceBroad")
        config = ConfigHelper(constant.cfg_path)
        # 广播类型
        broadcastType = "com.boyaa.stf.stopService"
        cmd_send = "shell am broadcast -a " + broadcastType
        singleGlobalVar.get("luaDriver").adb(cmd_send)



