#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
牌桌显示
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common

class C70445_CreatScoreRoom(TestCase):
    '''
    创建麻将记分房
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌房界面")
        self.yuepai_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房',20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0, len(elements)):
            elements[i].click()
            self.start_step("进入%s记分房" % elements[i].get_attribute("text"))
            self.yuepai_page.enter_room()
            self.yuepai_page.screenshot("%d.png" %i)
            self.yuepai_page.exit_yuepai_page()
            try:
                self.yuepai_page.wait_element('记分房').click()
            except:
                self.log_info("未返回到记分房页面")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70446_Room_Status(TestCase):
    '''
    玩家进入房间后状态
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌房界面")
        self.yuepai_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房',20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0, len(elements)):
            elements[i].click()
            self.start_step("进入%s记分房" % elements[i].get_attribute("text"))
            self.yuepai_page.enter_room()
            self.yuepai_page.screenshot("%d.png" %i)
            try:
                self.yuepai_page.wait_element('准备',30)
                self.log_info('玩家进入房间后显示了准备按钮，而不是自动准备状态')
            except:
                self.log_info( '玩家进入房间后没显示准备按钮')
            self.yuepai_page.exit_yuepai_page()
            try:
                self.yuepai_page.wait_element('记分房').click()
            except:
                self.log_info("未返回到记分房页面")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70449SocreRoom_XialaMemu(TestCase):
    '''
    记分房内查看菜单下拉框按钮
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌房界面")
        self.yuepai_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房',20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0, len(elements)):
            elements[i].click()
            self.start_step("进入%s记分房" % elements[i].get_attribute("text"))
            self.yuepai_page.enter_room()
            self.yuepai_page.screenshot("%d.png" %i)
            try:
                self.yuepai_page.wait_element('准备',30)
                self.log_info('玩家进入房间后显示了准备按钮，而不是自动准备状态')
            except:
                self.log_info( '玩家进入房间后没显示准备按钮')
            self.startStep("点击下拉菜单按钮")
            self.yuepai_page.wait_element("菜单键").click()
            self.yuepai_page.screenshot('xialMenu_%d.png' %i)
            self.startStep("点击设置按钮")
            self.yuepai_page.wait_element("设置键").click()
            self.yuepai_page.screenshot('setting_%d.png' %i)
            self.startStep("关闭设置页面")
            self.yuepai_page.wait_element("关闭设置").click()
            self.startStep("点击下拉菜单按钮")
            self.yuepai_page.wait_element("菜单键").click()
            self.startStep("点击退出按钮")
            self.yuepai_page.wait_element("退出键").click()
            self.yuepai_page.screenshot('exitRoom_%d.png' %i)
            try:
                self.yuepai_page.wait_element('记分房').click()
            except:
                self.log_info("未返回到记分房页面")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70450_Erweima(TestCase):
    '''
    斗地主积分房二维码可正常打开、房间号显示正确
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌房界面")
        self.yuepai_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房',20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0, len(elements)):
            elements[i].click()
            self.start_step("进入%s记分房" % elements[i].get_attribute("text"))
            self.yuepai_page.enter_room()
            self.yuepai_page.screenshot("%d.png" %i)
            try:
                self.yuepai_page.wait_element('准备',30)
                self.log_info('玩家进入房间后显示了准备按钮，而不是自动准备状态')
            except:
                self.log_info( '玩家进入房间后没显示准备按钮')
            self.startStep("点击二维码")
            self.yuepai_page.wait_element("二维码").click()
            self.yuepai_page.screenshot('yuepaifangErweima_%d.png' %i)
            self.start_step("点击玩家头像以关闭二维码界面")
            self.yuepai_page.wait_element("头像").click()
            self.start_step("退出约牌房")
            self.yuepai_page.exit_yuepai_page()
            try:
                self.yuepai_page.wait_element('记分房').click()
            except:
                self.log_info("未返回到记分房页面")


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C70451_DFQP_Yuepaifang_microphone(TestCase):
    '''
    斗地主积分房内麦克风
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌房界面")
        self.yuepai_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房',20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0, len(elements)):
            elements[i].click()
            self.start_step("进入%s记分房" % elements[i].get_attribute("text"))
            self.yuepai_page.enter_room()
            self.yuepai_page.screenshot("%d.png" %i)
            try:
                self.yuepai_page.wait_element('准备',30)
                self.log_info('玩家进入房间后显示了准备按钮，而不是自动准备状态')
            except:
                self.log_info( '玩家进入房间后没显示准备按钮')
            self.startStep("点击二维码")
            self.yuepai_page.wait_element("斗地主房间麦克风").click()
            self.yuepai_page.screenshot("microphone_%d.png" %i)
            self.startStep("再次点击关闭麦克风")
            self.yuepai_page.wait_element("斗地主房间麦克风").click()
            self.yuepai_page.screenshot("microphone2_%d.png" %i)
            self.start_step("退出约牌房")
            self.yuepai_page.exit_yuepai_page()
            try:
                self.yuepai_page.wait_element('记分房').click()
            except:
                self.log_info("未返回到记分房页面")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()


class C70453_DFQP_Yuepaifang_Chat(TestCase):
    '''
    斗地主积分房聊天
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌房界面")
        self.yuepai_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房',20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0, len(elements)):
            elements[i].click()
            self.start_step("进入%s记分房" % elements[i].get_attribute("text"))
            self.yuepai_page.enter_room()
            self.yuepai_page.screenshot("%d.png" %i)
            try:
                self.yuepai_page.wait_element('准备',30)
                self.log_info('玩家进入房间后显示了准备按钮，而不是自动准备状态')
            except:
                self.log_info( '玩家进入房间后没显示准备按钮')
            self.startStep("点击聊天按钮")
            self.yuepai_page.wait_element("聊天").click()
            self.yuepai_page.screenshot('_%d_chat.png' %i)
            self.startStep("点击表情tab页")
            self.yuepai_page.wait_element("表情").click()
            self.startStep("常用表情tab页")
            self.yuepai_page.wait_element("常用表情").click()
            self.yuepai_page.screenshot('_%d_commonface.png' %i)
            self.startStep("vip表情tab页")
            self.yuepai_page.wait_element("vip表情").click()
            self.yuepai_page.screenshot('vipface_%d.png' %i)
            self.startStep("点击聊天记录tab页")
            self.yuepai_page.wait_element("聊天记录").click()
            self.yuepai_page.screenshot('_%d_chatrecord.png' %i)
            self.startStep("切回常用tab页")
            self.yuepai_page.wait_element("常用").click()
            self.yuepai_page.screenshot('_%d_common.png' %i)
            self.start_step("点击玩家头像以关闭聊天界面")
            self.yuepai_page.wait_element("头像").click()
            self.start_step("退出约牌房")
            self.yuepai_page.exit_yuepai_page()
            try:
                self.yuepai_page.wait_element('记分房').click()
            except:
                self.log_info("未返回到记分房页面")


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C70456_DFQP_Yuepaifang_InviteFriend(TestCase):
    '''
    斗地主积分房邀请界面
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌房界面")
        self.yuepai_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房',20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0, len(elements)):
            elements[i].click()
            self.start_step("进入%s记分房" % elements[i].get_attribute("text"))
            self.yuepai_page.enter_room()
            self.yuepai_page.screenshot("%d.png" %i)
            try:
                self.yuepai_page.wait_element('准备',30)
                self.log_info('玩家进入房间后显示了准备按钮，而不是自动准备状态')
            except:
                self.log_info( '玩家进入房间后没显示准备按钮')
            self.startStep("点击邀请按钮")
            self.yuepai_page.wait_element("邀请-积分房").click()
            self.yuepai_page.screenshot('_%d_invite.png' %i)
            self.start_step("点击玩家头像以关闭邀请界面")
            self.yuepai_page.wait_element("头像").click()
            self.start_step("退出约牌房")
            self.yuepai_page.exit_yuepai_page()
            try:
                self.yuepai_page.wait_element('记分房').click()
            except:
                self.log_info("未返回到记分房页面")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C70454_DFQP_Yuepaifang_Head(TestCase):
    '''
    斗地主积分房玩家头像，默认男/默认女/自定义
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌房界面")
        self.yuepai_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房',20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0, len(elements)):
            elements[i].click()
            self.start_step("进入%s记分房" % elements[i].get_attribute("text"))
            self.yuepai_page.enter_room()
            self.yuepai_page.screenshot("%d.png" %i)
            try:
                self.yuepai_page.wait_element('准备',30)
                self.log_info('玩家进入房间后显示了准备按钮，而不是自动准备状态')
            except:
                self.log_info( '玩家进入房间后没显示准备按钮')
            self.startStep("玩家默认头像显示")
            self.yuepai_page.screenshot('_%d_head.png' %i)
            self.yuepai_page.wait_element("头像").click()
            self.yuepai_page.screenshot('_%d_personalInfo.png' %i)
            self.start_step("点击玩家头像以关闭玩家信息界面")
            self.yuepai_page.wait_element("头像").click()
            self.start_step("退出约牌房")
            self.yuepai_page.exit_yuepai_page()
            try:
                self.yuepai_page.wait_element('记分房').click()
            except:
                self.log_info("未返回到记分房页面")


    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C70447_No_Appear(TestCase):
    '''
   进入房间内准备15分钟后未开始游戏，查看显示
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 23

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        capabilities = {}
        capabilities['newCommandTimeout'] = 16 * 60
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver(capabilities)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房', 20).click()
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.get_elements("记分房创建页面游戏列表")
        print elements
        print len(elements)
        for i in range(0, len(elements)):
            print elements[i].get_attribute("text")
            elements[i].click()
            self.yuepai_page.enter_room()
            self.yuepai_page.screenshot("01.png")
            time.sleep(15 * 60)
            self.yuepai_page.screenshot("02.png")
            self.start_step("退出房间")
            self.yuepai_page.is_exist_yuepairoom()
            break

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()


# __qtaf_seq_tests__ = [C032_DFQP_Backpack_Enterpack]
if __name__ == '__main__':

    debug_run_all()