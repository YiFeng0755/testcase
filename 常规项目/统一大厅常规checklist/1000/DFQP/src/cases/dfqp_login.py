#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌登陆,注册，绑定测试
'''
import time,test_datas
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from appiumcenter.luadriver import LuaDriver
from uilib.login_page import Login_Page
from uilib.setting_page import Setting_Page
from uilib.hall_page import Hall_Page
from common.common import Common
from appium_rainbow.webdriver.connectiontype import ConnectionType
from datacenter import dataprovider

class C001_DFQP_Login_GuestLogin(TestCase):
    '''
    无网络,点击启动游戏
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.Normal
    timeout = 5
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)
        # 设置为无网络的方式
        # 获取状态名
        # self.get_connection_name1(self.luadriver.network_connection)
        # print self.luadriver.network_connection
        # self.luadriver.set_network_connection(0)
        self.common.switchnetwork(self.luadriver, u"无网络")
        # 声明方法
        self.login_page = Login_Page()

    def run_test(self):
        #测试用例
        self.start_step("启动游戏")
        time.sleep(15)
        self.start_step("设置网络弹出框")
        self.login_page.wait_element("设置网络").is_displayed()
        self.login_page.wait_element("关闭弹出页面").click()
        self.common.closeactivity(self.luadriver)
        self.start_step("点击物品箱，查看弹出框")
        self.login_page.wait_element("物品箱").click()
        time.sleep(2)
        self.login_page.wait_element("设置网络").click()
        time.sleep(2)
        self.start_step("进入手机网络设置页面")
        self.luadriver.find_elements_by_class_name("android.widget.TextView")[0].is_displayed()
        self.login_page.screenshot('GuestLogin1.png')

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        #设置网络
        self.luadriver.set_network_connection(ConnectionType.WIFI_ONLY)
        self.common.closedriver()

class C002_DFQP_Switchtoback1(TestCase):
    '''
    游客登陆，切后台登录后切换到后台5分钟再启动游戏
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.Normal
    timeout = 5
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)
        # 声明方法
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()


    def run_test(self):
        # 测试用例
        self.hall_page.wait_element("同步标志")
        self.start_step("启动游戏")
        time.sleep(10)
        self.luadriver.keyevent(3)  # home
        time.sleep(20)
        #拉起游戏
        self.luadriver.start_activity("com.boyaa.enginedlqp.maindevelop", "com.boyaa.enginedlqp.maindevelop.Game")
        time.sleep(10)
        try:
            self.hall_page.wait_element("重新登录").click()
        except:
            print "未找到按钮"
        self.login_page.screenshot('Switchtoback1.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

testdata=test_datas.logindata1
@dataprovider.DataDrive(testdata)
class C003_DFQP_Login_Login(TestCase):
    '''
    注册账号登陆，设置网络为无网络后，启动游戏
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.Normal
    timeout = 5
    def pre_test(self):
        self.common = Common()
        self.luadriver = self.common.setupdriver()
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(self.casedata['user'],self.casedata['password'])
        self.common.switchnetwork(self.luadriver,u"无网络")
        # 声明方法
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()


    def run_test(self):
        #测试用例
        self.hall_page.wait_element("同步标志")
        time.sleep(12)
        self.start_step("无网络，进入游戏页面")
        self.login_page.wait_element("设置网络").is_displayed()
        self.login_page.wait_element("关闭弹出页面").click()
        self.common.closeactivity(self.luadriver)
        self.login_page.wait_element("物品箱").click()
        time.sleep(2)
        self.login_page.wait_element("设置网络").click()
        time.sleep(2)
        self.start_step("进入手机网络设置页面")
        self.luadriver.find_elements_by_class_name("android.widget.TextView")[0].is_displayed()
        self.login_page.screenshot('Login_UseLogin1.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.switchnetwork(self.luadriver,"WIFI模式")
        self.common.closedriver()

testdata=test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C004_DFQP_Switchtoback2(TestCase):
    '''
    注册账号登陆，切后台登录后切换到后台5分钟再启动游戏
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(self.casedata['user'],self.casedata['password'])
        # 声明方法
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()


    def run_test(self):
        # 测试用例
        self.hall_page.wait_element("同步标志")
        self.start_step("启动游戏")
        time.sleep(10)
        self.luadriver.keyevent(3)  # home
        time.sleep(30)
        # time.sleep(10)
        self.luadriver.start_activity("com.boyaa.enginedlqp.maindevelop", "com.boyaa.enginedlqp.maindevelop.Game")
        time.sleep(5)
        self.hall_page.wait_element("头像").click()
        time.sleep(2)
        self.hall_page.screenshot('Switchtoback2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

testdata=test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C005_DFQP_Login_UseLogin2(TestCase):
    '''
    注册账号登陆，登录成功后重新登录
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        # 初始化nativeDriver
        self.common = Common()
        self.luadriver = self.common.setupdriver()
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(self.casedata['user'],self.casedata['password'])
        # 声明方法
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()
        # # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.hall_page.wait_element("头像").click()
        self.common.loginuser(self.casedata['user1'], self.casedata['password1'])
        time.sleep(20)
        self.hall_page.wait_element("同步标志")
        self.hall_page.screenshot('Login_UseLogin2_0.png')
        self.hall_page.wait_element("头像").click()
        self.hall_page.screenshot('Login_UseLogin2_1.png')


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

testdata=test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C006_DFQP_Login_LoginSwitch(TestCase):
    '''
    注册账号登陆，切换账号
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 声明方法
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        #测试用例
        self.hall_page.wait_element("同步标志")
        if not self.common.isloginuser(self.luadriver):
            self.common.loginuser(self.casedata['user'],self.casedata['password'])
        try:
            self.hall_page.wait_element("头像").click()
        except:
            print "已登陆"
        self.common.loginuser(self.casedata['user'], self.casedata['password'])
        self.common.closeactivity(self.luadriver)
        time.sleep(2)
        self.hall_page.wait_element("头像").click()
        time.sleep(2)
        self.hall_page.screenshot('Login_UseLoginSwitch.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C007_DFQP_Load(TestCase):
    '''
    后台不配置节日闪屏图片
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 声明方法
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        # 测试用例
        self.hall_page.screenshot('Load_0.png')
        time.sleep(0.5)
        self.hall_page.screenshot('Load_1.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

testdata=test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C008_DFQP_Bandding(TestCase):
    '''
    游客，手机没有插SIM卡:点击注册绑定手机，不会自动识别电话号码
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)
        # 声明方法
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        # 测试用例
        self.hall_page.wait_element("同步标志")
        self.start_step("注册登录")
        self.hall_page.wait_element("头像").click()
        time.sleep(2)
        self.setting_page.wait_element("安全绑定").click()
        self.setting_page.wait_element("你的手机号码").get_attribute('text')=="您的手机号"
        self.setting_page.wait_element("你的手机号码").send_keys(self.casedata['user'])
        time.sleep(2)
        self.setting_page.wait_element("确认登陆").click()
        time.sleep(2)
        self.setting_page.wait_element("直接登陆")
        self.setting_page.screenshot('Bandding.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

testdata=test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C009_DFQP_VisitorLogin(TestCase):
    '''
    游客，切换绑定过mid的注册账号,点击切换账号
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)

        self.common.closeactivity(self.luadriver)
        # 声明方法
        self.login_page = Login_Page()
        self.setting_page = Setting_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        # 测试用例
        self.hall_page.wait_element("同步标志")
        self.start_step("获取游客信息")
        self.hall_page.wait_element("头像").click()
        time.sleep(3)
        # id1 = self.setting_page.wait_element("账号ID").get_attribute('text')
        # print id1
        self.setting_page.wait_element("安全绑定")
        self.common.loginuser(self.casedata['user'], self.casedata['password'])
        self.common.closeactivity(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(3)
        # id2 = self.setting_page.wait_element("账号ID").get_attribute('text')
        # print id2
        phonenum = self.setting_page.wait_element("安全绑定").get_attribute('text')
        print phonenum
        self.start_step("判断是否手机登录")
        self.assert_notequal(False, phonenum, "安全绑定")
        self.setting_page.screenshot('VisitorLogin.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

# __qtaf_seq_tests__ = [C006_DFQP_Login_LoginSwitch]
if __name__ == '__main__':
    # C008_DFQP_Bandding = C008_DFQP_Bandding()
    # C008_DFQP_Bandding.debug_run()
    debug_run_all()