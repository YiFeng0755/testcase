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
from uilib.game_page import Game_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.safebox_page import Safebox_Page
import user_util
import Interface as PHPInterface

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
        time.sleep(3)
        try:
            self.setting_page.wait_element("页面返回").click()

        except:
            print "已经关闭"
        time.sleep(2)

    def changeServerView(self,name):
        self.hall_page = Hall_Page()
        self.hall_page.wait_element(name).click()
        time.sleep(5)

    def deletefile(self,driver):
        print "----删除自动登录文件----"
        config = ConfigHelper(constant.cfg_path)
        package =config.getValue('appium', 'apppackage')
        #正式服
        command = "shell rm -r /mnt/sdcard/."+package+"/dict/lastLoginInfo.dat"
        # command = "shell rm -r /mnt/sdcard/.com.boyaa.engineqpsc/dict/lastLoginInfo.dat"
        print command
        try:
            driver.adb(command)
        except:
            print "命令执行失败"
        #预发布  1lastLoginInfo.dat
        command1 = "shell rm -r /mnt/sdcard/."+package+"/dict/1lastLoginInfo.dat"
        print command1
        try:

            driver.adb(command1)
        except:
            print "命令执行失败"
        # 预发布  2lastLoginInfo.dat
        command2 = "shell rm -r /mnt/sdcard/."+package+"/dict/2lastLoginInfo.dat"
        try:
            driver.adb(command2)
        except:
            print "命令执行失败"
        print command2

    def closeactivity_switchserver(self,luadriver,switchserver):
        '''
        关闭活动页面，切换到指定服，然后再关闭弹出的活动页面
        :param luadriver:
        :param switchserver:
        :return:
        '''
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        time.sleep(8)
        try:
            luadriver.find_element_by_name("允许").click()
        except:
            print "未出现按钮"
        try:
            luadriver.find_element_by_tag_name("允许").click()
        except:
            print "未出现按钮"
        try:
            luadriver.find_elements_by_class_name("android.widget.Button")[1].click()
        except:
            print "未出现按钮"
        time.sleep(10)
        try:
            self.hall_page.wait_element("确认登陆").click()
        except:
            print "未出现登陆按钮"
        try:
            self.hall_page.wait_element("立即升级绑定账号").click()
            time.sleep(1)
            self.sign_page.wait_element("关闭1").click()
        except:
            print "未出现立即升级绑定账号按钮"
        self.closeActivityBtn()
        try:
            self.hall_page.wait_element("新手任务").click()
            time.sleep(2)
        except:
            print "未出现新手任务按钮"
        try:
            luadriver.find_element_by_name("允许").click()
        except:
            print "未出现按钮"
        while(self.hall_page.is_exist("switchserver")):
            try:
                self.hall_page.wait_element(switchserver).click()
                time.sleep(1)
            except:
                print "未出现正式服按钮"
            time.sleep(15)
            try:
                luadriver.find_element_by_name("允许").click()
            except:
                print "未出现允许按钮"
            try:
                self.hall_page.wait_element("立即升级绑定账号").click()
                time.sleep(1)
                self.sign_page.wait_element("关闭1").click()
            except:
                print "未出现立即升级绑定账号按钮"
            time.sleep(2)
            self.closeActivityBtn()

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


    def closeactivity_switchserver_reservenotice(self,luadriver,switchserver):#切换服务器但保留公告页面
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        time.sleep(15)
        try:
            luadriver.find_element_by_name("允许").click()
        except:
            print "未出现按钮"
        time.sleep(5)
        try:
            self.hall_page.wait_element("确认登陆").click()
        except:
            print "未出现登陆按钮"
        i = 0
        while (i < 3):
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
            self.hall_page.wait_element("新手任务").click()
            time.sleep(2)
        except:
            print "未出现新手任务按钮"
        try:
            luadriver.find_element_by_name("允许").click()
        except:
            print "未出现按钮"
        try:
            self.hall_page.wait_element(switchserver).click()
            time.sleep(1)
        except:
            print "未出现%s按钮"%switchserver
        time.sleep(15)
        try:
            luadriver.find_element_by_name("允许").click()
        except:
            "未出现按钮"
        time.sleep(2)

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
        # # 每个用例都需要关闭活动，把这个放在初始化里面实现
        # self.closeactivity(luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(6)
        try:
            if(self.setting_page.wait_element("立即升级").get_attribute('text') != u"立即升级"):
                return True
            else:
                return False
        except:
            return False

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

    def swipeelement(self,element1,element2):
        # element1_size_width = element1.size['width']
        # element1_size_height = element1.size["height"]
        # element1_1_x = element1.location["x"]
        # element1_1_y = element1.location["y"]
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

    def restart(self):
        self.luaobj = LuaDriver()
        self.luaobj.closeLuadriver()
        self.luaobj.creatLuaDriver()
        self.luadriver = self.luaobj.getLuaDriver()
        self.closeactivity_switchserver(self.luadriver,"预发布")
        return self.luadriver

    def random_str(self,len):
        '''生成随机字符'''
        str = ""
        for i in range(len):
            str += (random.choice("32423423324324234234234234343534532423432"))
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
            self.hall_page.wait_element("立即升级绑定账号").click()
            time.sleep(1)
            self.sign_page.wait_element("关闭1").click()
        except:
            print "未出现立即升级绑定账号按钮"
        try:
            luadriver.find_element_by_name("允许").click()
        except:
            "未出现按钮"
        try:
            self.hall_page.wait_element("确认登陆").click()
        except:
            "未出现登陆按钮"
        self.closeActivityBtn()
        try:
            self.hall_page.wait_element("新手任务").click()
            time.sleep(2)
        except:
            print "未出现新手任务按钮"
        try:
            self.hall_page.wait_element("预发布").click()
        except:
            "未出现预发布按钮"
        time.sleep(5)
        try:
            luadriver.find_element_by_name("允许").click()
        except:
            "未出现按钮"
        time.sleep(5)
        try:
            luadriver.find_element_by_name("允许").click()
        except:
            "未出现按钮"
        time.sleep(2)
        try:
            self.hall_page.wait_element("立即升级绑定账号").click()
            time.sleep(1)
            self.sign_page.wait_element("关闭1").click()
        except:
            print "未出现立即升级绑定账号按钮"
        self.closeActivityBtn()

    def game_is_exist(self,gamename):
        '''
        判断子游戏是否存在，存在返回True，不存在返回False
        :param gamename: 子游戏元素名，不查找“更多游戏”
        '''
        self.game_page = Game_Page()
        if (self.game_page.is_exist(gamename) == True):
            return True
        else:
            try:
                self.game_page.wait_element("右三角标").click()
                time.sleep(3)
                if (self.game_page.is_exist(gamename) == True):
                    return True
            except:
                print "无此按钮"
            if(self.game_page.is_exist("更多游戏") == True):
                try:
                    self.game_page.wait_element("左三角标").click()
                    time.sleep(3)
                    if (self.game_page.is_exist(gamename) == True):
                        return True
                except:
                    print "无此按钮"
            return False

    def get_user(self):
        '''
        获取账号信息
        @return:
        '''
        global user_info
        user_info = user_util.gimme_afree_account()
        while user_info ==None:
            time.sleep(5)
            user_info = user_util.gimme_afree_account()
        return user_info

    def release_user(self,user_mid):
        print "release"
        print user_mid
        try:
            user_util.release_account(user_mid)
        except:
            print "release user fail"

    def game_is_download(self):
        '''
        判断子游戏是否已下载
        '''
        self.game_page = Game_Page()
        if(self.game_page.is_exist("资源下载-确定") == True):
            self.game_page.wait_element("资源下载-确定").click()
            time.sleep(40)
        else:
            print ("游戏已下载")

    def get_cid(self):
        '''获取用户cid'''
        self.personinfo_page = Personinfo_Page()
        self.game_page = Game_Page()
        # self.start_step("获取用户mid")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(6)
        cid = self.personinfo_page.wait_element("账号ID").get_attribute('text')
        print "获取的用户cid为: %s" % cid
        self.game_page.wait_element("关闭对话框").click()
        time.sleep(3)
        if (self.game_page.is_exist("关闭对话框")):  # 如果弹破产弹框，则关闭
            self.game_page.wait_element("关闭对话框").click()
            time.sleep(3)
        return cid

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


    def get_safebox_money(self):
        '''从保险箱取出全部存款'''
        self.safebox_page = Safebox_Page()
        # self.start_step("从保险箱取出所有存款")
        self.hall_page.wait_element("保险箱").click()
        time.sleep(2)
        self.safebox_page.wait_element("取出").click()
        if (self.safebox_page.is_exist("确定---保险箱")):
            slider = self.safebox_page.wait_element("滚动条")
            addgoldbtn = self.safebox_page.wait_element("增加金条/银条数目")
            x = slider.location['x']
            y = slider.location['y']
            x1 = addgoldbtn.location['x']
            y1 = addgoldbtn.location['y']
            self.luadriver.swipe(x, y, x1, y1)
            self.safebox_page.wait_element("确定---保险箱").click()
            time.sleep(2)
            self.luadriver.keyevent(4)
        else:
            print ("保险箱没有银币存款")
            time.sleep(2)
            self.luadriver.keyevent(4)

    def get_safebox_crystal(self):
        '''从保险箱取出全部金条'''
        self.safebox_page = Safebox_Page()
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
            self.luadriver.swipe(x, y, x1, y1)
            self.safebox_page.wait_element("确定---保险箱").click()
            time.sleep(2)
            self.luadriver.keyevent(4)
        else:
            print ("保险箱没有金条存款")
            self.luadriver.keyevent(4)
