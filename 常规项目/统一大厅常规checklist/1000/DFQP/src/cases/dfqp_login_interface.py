#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌登陆接口配置相关用例
'''
import time
import datetime
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.sign_page import Sign_Page
from uilib.hall_page import Hall_Page
from uilib.setting_page import Setting_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.mall_page import Mall_Page
from uilib.backpack_page import Backpack_Page
from common.common import Common
import test_datas
from datacenter import dataprovider
import common.Interface as PHPInterface

class C301_DFCP_Login_Interface_anonymousSignIn(TestCase):
    '''
    游客被封账号登录
    '''
    owner = "RealLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    #用例超时时间，单位：分钟
    #其他配置时间的地方，单位均为：秒
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.luadriver = self.common.setupdriver()
        # 删除缓存文件
        self.common.deletefile(self.luadriver)
        self.hall_page = Hall_Page()
        #关闭APP重新打开
        self.common.closedriver()
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivitytest(self.luadriver)
        #获取Mid信息
        self.hall_page.wait_element("头像").click()
        self.mid = self.hall_page.wait_element("idNumber").get_attribute("text")
        print "获取的mid为： %s" % self.mid
        self.start_step("调用接口封停账号")
        resultBanUser = PHPInterface.shutdown_user(int(self.mid), 1)
        if resultBanUser:
            print "封停账号成功"
        else:
            raise "封停账号失败"

    def run_test(self):
        # 关闭APP重新打开
        self.common.closedriver()
        self.luadriver = self.common.setupdriver()
        time.sleep(10)
        #寻找弹框并确认标题文本为：账号禁用
        t=self.hall_page.wait_element("账号禁用").get_attribute("text")
        self.assert_equal("公告框信息：", "账号禁用", t)
        #点击切换账号，切换成功
        self.hall_page.wait_element("切换账号").click()

    def post_test(self):
        self.start_step("调用接口解封账号")
        resultBanUser = PHPInterface.shutdown_user(self.mid, 0)
        if resultBanUser:
            print "解封账号成功"
        else:
            raise "解封账号失败"
        self.common.closedriver()

testdata=test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C302_DFCP_Login_Interface_AccountSignIn(TestCase):
    '''
    注册用户被封账号登录
    '''
    owner = "RealLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    # 用例超时时间，单位：分钟
    # 其他配置时间的地方，单位均为：秒
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(6)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
           self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"
        print "mid为： %s" % self.casedata['mid']
        self.start_step("调用接口封停账号")
        resultBanUser = PHPInterface.shutdown_user(int(self.casedata['mid']), 1)
        if resultBanUser:
            print "封停账号成功"
        else:
            raise "封停账号失败"
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        # self.common.closeactivitytest(self.luadriver)
        # self.start_step("获取Mid信息")
        # self.hall_page.wait_element("头像").click()
        # self.common.loginuser(self.casedata['user'], self.casedata['password'])
        # self.common.closeactivitytest(self.luadriver)
        # 关闭APP重新打开
        self.common.closedriver()
        self.luadriver = self.common.setupdriver()
        self.common.closeactivitytest(self.luadriver)

    def run_test(self):
        self.start_step("寻找弹框并确认标题文本为：账号禁用")
        time.sleep(30)
        self.hall_page.wait_element("头像").click()
        time.sleep(6)
        try:
            self.hall_page.wait_element("账号禁用")
            self.hall_page.screenshot("jinyong.png")
            self.start_step("切换其他账号")
            self.hall_page.wait_element("账号切换").click()
            time.sleep(2)
            self.setting_page.wait_element("手机号码").send_keys(self.casedata['user1'])
            time.sleep(1)
            self.setting_page.wait_element("密码").send_keys(self.casedata['password1'])
            time.sleep(1)
            self.setting_page.wait_element("确认登陆").click()
            time.sleep(10)
            self.hall_page.wait_element("同步标志")
        except:
            print "未出现封停提示"

    def post_test(self):
        self.start_step("调用接口解封账号")
        resultBanUser = PHPInterface.shutdown_user(int(self.casedata['mid']), 0)
        if resultBanUser:
            print "解封账号成功"
        else:
            raise "解封账号失败"
        self.common.closedriver()

testdata=test_datas.logindata2
@dataprovider.DataDrive(testdata)
class C306_DFCP_Login_Interface_Personinfo(TestCase):
    '''
    玩家是vip，点击个人资料，查看vip
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.sign_page = Sign_Page()
        self.personinfo_page = Personinfo_Page()
        # 设置成VIP
        PHPInterface.set_vip(self.casedata['mid'], 4)
        time.sleep(1)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivitytest(self.luadriver)
        self.hall_page.wait_element("头像").click()
        time.sleep(2)
        if self.personinfo_page.wait_element("账号ID").get_attribute('text') != self.casedata['cid']:
           self.common.loginuser(self.casedata['user'], self.casedata['password'])
        try:
            self.personinfo_page.wait_element("关闭").click()
        except:
            print "已关闭窗口"

    def run_test(self):
        self.start_step("进入头像页面")
        self.hall_page.wait_element("头像").click()
        self.personinfo_page.wait_element("VIP续期").get_attribute('text') == u"立即续费"

    def post_test(self):
        PHPInterface.set_vip(self.casedata['mid'], -1)
        self.common.closedriver()


testdata = test_datas.logindata2
class C312_DFCP_Login_Interface_Notice(TestCase):
    '''
    配置文本公告，登录游戏，查看显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.luadriver = self.common.setupdriver()
        self.hall_page = Hall_Page()
        self.backpack_page = Backpack_Page()
        self.personinfo_page = Personinfo_Page()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivitytest(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入物品箱页面")
        time.sleep(2)
        self.hall_page.wait_element("物品箱").click()
        time.sleep(2)
        self.hall_page.wait_element("兑奖记录").click()
        time.sleep(2)
        self.hall_page.screenshot('Backpack_record.png')
    def post_test(self):
        self.common.closedriver()


__qtaf_seq_tests__ = [C302_DFCP_Login_Interface_AccountSignIn]
if __name__ == '__main__':
    # C308_DFCP_Hall_Interface_Getrecordinfo = C308_DFCP_Hall_Interface_Getrecordinfo()
    # C308_DFCP_Hall_Interface_Getrecordinfo.debug_run()
    debug_run_all()
