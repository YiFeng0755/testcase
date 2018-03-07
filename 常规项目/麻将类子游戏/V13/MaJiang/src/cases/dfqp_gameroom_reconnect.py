#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
游戏重连
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.game_page import Game_Page
from uilib.sign_page import Sign_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common

class C27215_Gamelist_Noready_Back(TestCase):
    '''
    玩家进入房间未准备，短时间切换后台
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动页面")
        self.common.closeactivity(self.luadriver)

    def noready_back(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i].get_attribute("name"))
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            self.game_page.wait_element("同步标志", 20)
            try:
                self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i].get_attribute("name"))
                elements = self.game_page.game_play_way()
                elements[0][1].click()
            except:
                self.log_info("当前子游戏初级场")
            self.log_info("进入游戏ID：%s 的房间" % game_list[i].get_attribute("name"))
            self.game_page.screenshot("%s_1.png" % game_list[i].get_attribute("name"))
            self.game_page.wait_element("房间场次").click()
            time.sleep(10)

            self.start_step("判断当前游戏是否准备，如果是，则继续玩游戏，否则，退出房间")
            self.yuepai_page.play_game()

            self.game_page.screenshot("%s_切换后台操作前.png" % game_list[i].get_attribute("name"))
            self.log_info("home键")
            self.luadriver.keyevent(3)  # home
            self.game_page.screenshot("%s_切换后台中.png" % game_list[i].get_attribute("name"))
            time.sleep(2)
            self.start_step("解锁")
            self.start_step("读配置,拉起游戏")
            self.common.unlock()
            time.sleep(4)
            self.game_page.screenshot("%s_切换后台恢复后.png" % game_list[i].get_attribute("name"))

            self.yuepai_page.wait_element("换桌")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("退出房间失败")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.noready_back()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.noready_back(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27215_Gamelist_Noready_Lock(TestCase):
    '''
    玩家进入房间未准备，短时间锁屏
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭活动页面")
        self.common.closeactivity(self.luadriver)

    def noready_lock(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i].get_attribute("name"))
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            self.game_page.wait_element("同步标志", 20)
            try:
                self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i].get_attribute("name"))
                elements = self.game_page.game_play_way()
                elements[0][1].click()
            except:
                self.log_info("当前子游戏初级场")
            self.log_info("进入游戏ID：%s 的房间" % game_list[i].get_attribute("name"))
            self.game_page.screenshot("%s_1.png" % game_list[i].get_attribute("name"))
            self.game_page.wait_element("房间场次").click()
            time.sleep(10)
            self.start_step("判断当前游戏是否准备，如果是，则继续玩游戏，否则，退出房间")
            self.yuepai_page.play_game()
            self.game_page.screenshot("%s_before.png" % game_list[i].get_attribute("name"))
            self.start_step("锁屏")
            self.luadriver.keyevent(26)  # 锁屏
            self.game_page.screenshot("%s_being.png" % game_list[i].get_attribute("name"))
            time.sleep(2)
            self.start_step("解锁")
            self.common.unlock()
            time.sleep(4)
            self.game_page.screenshot("%s_after.png" % game_list[i].get_attribute("name"))
            self.start_step("读配置,拉起游戏")
            self.yuepai_page.wait_element("换桌")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("退出房间失败")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.noready_lock()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.noready_lock(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27216_Gamelist_Noready_Back_Longtime(TestCase):
    '''
    玩家进入房间未准备，长时间切换后台
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 20

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        capabilities = {}
        capabilities['newCommandTimeout'] = 60*3
        self.luadriver = self.common.setupdriver(capabilities)
        self.common.closeactivity(self.luadriver)

    def noready_back_longtime(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            self.game_page.wait_element("同步标志", 20)
            try:
                self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i].get_attribute("name"))
                elements = self.game_page.game_play_way()
                elements[0][1].click()
            except:
                self.log_info("当前子游戏初级场")
            self.log_info("进入游戏ID：%s 的房间" % game_list[i].get_attribute("name"))
            self.game_page.screenshot("%s_1.png" % game_list[i].get_attribute("name"))
            self.game_page.wait_element("房间场次").click()
            time.sleep(10)
            self.start_step("判断当前游戏是否准备，如果是，则继续玩游戏，否则，退出房间")
            self.yuepai_page.play_game()
            self.game_page.screenshot("%s_before.png" % game_list[i].get_attribute("name"))
            self.luadriver.keyevent(3)  # home
            self.game_page.screenshot("%s_being.png" % game_list[i].get_attribute("name"))
            time.sleep(2*60)
            self.start_step("解锁")
            self.common.unlock()
            time.sleep(4)
            self.game_page.screenshot("%s_after.png" % game_list[i].get_attribute("name"))
            self.start_step("读配置,拉起游戏")
            self.yuepai_page.wait_element("换桌")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("退出房间失败")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.noready_back_longtime()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.noready_back_longtime(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27216_Gamelist_Noready_Lock_Longtime(TestCase):
    '''
    玩家进入房间未准备，长时间锁屏
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.sign_page = Sign_Page()
        self.start_step("初始化driver")
        capabilities = {}
        capabilities['newCommandTimeout'] = 60*3
        self.luadriver = self.common.setupdriver(capabilities)
        self.common.closeactivity(self.luadriver)

    def noready_lock_longtime(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            self.game_page.wait_element("同步标志", 20)
            try:
                self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i].get_attribute("name"))
                elements = self.game_page.game_play_way()
                elements[0][1].click()
            except:
                self.log_info("当前子游戏初级场")
            self.log_info("进入游戏ID：%s 的房间" % game_list[i].get_attribute("name"))
            self.game_page.screenshot("%s_1.png" % game_list[i].get_attribute("name"))
            self.game_page.wait_element("房间场次").click()
            time.sleep(10)
            self.start_step("判断当前游戏是否准备，如果是，则继续玩游戏，否则，退出房间")
            self.yuepai_page.play_game()
            self.game_page.screenshot("%s_before.png" % game_list[i].get_attribute("name"))
            self.start_step("锁屏")
            self.luadriver.keyevent(26)  # 锁屏
            self.game_page.screenshot("%s_being.png" % game_list[i].get_attribute("name"))
            time.sleep(2*60)
            self.start_step("解锁")
            self.common.unlock()
            time.sleep(4)
            self.game_page.screenshot("%s_after.png" % game_list[i].get_attribute("name"))
            self.start_step("读配置,拉起游戏")
            self.yuepai_page.wait_element("换桌")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("退出房间失败")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.noready_lock_longtime()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.noready_lock_longtime(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27212_Gamelist_Noready_Reconnect(TestCase):
    '''
    玩家进入房间未准备，网络波动
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.sign_page = Sign_Page()
        self.start_step("初始化driver")
        capabilities = {}
        capabilities['newCommandTimeout'] = 60*3
        self.luadriver = self.common.setupdriver(capabilities)
        self.common.closeactivity(self.luadriver)

    def noready_lock_longtime(self,is_next=False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if(self.game_page.game_is_download()==False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i].get_attribute("name"))
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            self.game_page.wait_element("同步标志", 20)
            try:
                self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i].get_attribute("name"))
                elements = self.game_page.game_play_way()
                elements[0][1].click()
            except:
                self.log_info("当前子游戏初级场")
            self.log_info("进入游戏ID：%s 的房间" % game_list[i].get_attribute("name"))
            self.game_page.screenshot("%s_1.png" % game_list[i].get_attribute("name"))
            self.game_page.wait_element("房间场次").click()
            time.sleep(10)
            self.start_step("判断当前游戏是否准备，如果是，则继续玩游戏，否则，退出房间")
            self.yuepai_page.play_game()
            self.game_page.screenshot("%s_before.png" % game_list[i].get_attribute("name"))
            # self.start_step("锁屏")
            # self.luadriver.keyevent(26)  # 锁屏
            try:
                self.hall_page.wait_element("测试按钮",6).click()
                self.game_page.wait_element("重连").click()
                time.sleep(3)
                self.game_page.screenshot("%s_being.png" % game_list[i].get_attribute("name"))
                time.sleep(4)
            except:
                self.common.switchnetwork(self.luadriver, u"无网络")
                self.game_page.screenshot("%s_being.png" % game_list[i].get_attribute("name"))
                self.common.switchnetwork(self.luadriver, u"WIFI模式")
                self.common.network_connect()
                self.common.closeActivityBtn()
            # time.sleep(2*60)
            # self.start_step("解锁")
            # self.common.unlock()
            self.game_page.screenshot("%s_after.png" % game_list[i].get_attribute("name"))
            self.yuepai_page.wait_element("换桌")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("退出房间失败")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("查看首屏子游戏列表")
        self.noready_lock_longtime()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("查看第二屏子游戏列表")
        self.noready_lock_longtime(is_next=True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()


__qtaf_seq_tests__ = [C27215_Gamelist_Noready_Back]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
