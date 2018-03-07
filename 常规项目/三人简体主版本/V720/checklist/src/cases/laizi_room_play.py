#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
癞子场-玩牌相关（正式/测试）
'''
import time
from runcenter.enums import EnumStatus, EnumPriority
from runcenter.testcase import TestCase, debug_run_all

from common import Interface
from common.common import Common
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.level_page import Level_Page

class D25688_LaiziRoom_InAndOut(TestCase):
    '''
    金币足够进入房间
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 20
    # pending = True

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()
        self.common.user_money(money=1000)

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
            self.game_page.wait_element("切换按钮").click()
            elments = self.game_page.get_elements("切换玩法")
            elments[0].click()
            # self.level_page.wait_element("快速开始").click()
        self.start_step("点击初级场房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.game_page.wait_element("倍数说明")
        self.game_page.screenshot("第一次进房间.png")
        self.start_step("点击退出键退出房间")
        i = 0
        while self.game_page.element_is_exist("退出",1):
            self.game_page.wait_element("退出").click()
            i += 1
            self.log_info("点击退出次数：%s" %i )
        self.level_page.wait_element("同步标志")
        self.hall_page.screenshot("点击退出键退出房间.png")
        self.level_page.wait_element("房间列表").click()
        self.game_page.wait_element("倍数说明")
        self.game_page.screenshot("第二次进房间.png")
        self.start_step("点击物理返回键退出房间")
        while self.game_page.element_is_exist("同步标志",1):
            self.luadriver.keyevent(4)
            time.sleep(4)
            self.log_info("点击物理返回键" )
        self.level_page.wait_element("同步标志",30)
        self.hall_page.screenshot("物理返回键退出房间.png")
        self.level_page.wait_element("房间列表").click()
        self.game_page.wait_element("倍数说明")
        self.game_page.screenshot("第三次进房间.png")
        self.start_step("点击开始按钮")
        self.game_page.wait_element("开始",30).click()
        self.hall_page.screenshot("点击开始按钮.png")
        i = 0
        while self.game_page.element_is_exist("退出",1):
            self.game_page.wait_element("退出").click()
            i += 1
            self.log_info("点击退出次数：%s" % i)
            if i > 5:
                while self.game_page.element_is_exist("出牌", 1) == False:
                    list = ["抢地主", "叫地主", "不加倍", "加倍"]
                    self.log_info("叫地主中")
                    for name in list:
                        try:
                            self.game_page.wait_element(name, 1).click()
                        except:
                            self.log_info("未出现抢地主按钮")
                    if self.game_page.element_is_exist("继续游戏", 1):
                        break
                self.start_step("托管")
                if self.game_page.element_is_exist("机器人") == False:
                    self.game_page.wait_element("托管").click()
                while self.game_page.element_is_exist("继续游戏", 1) == False:
                    time.sleep(1)
                    self.log_info("正在游戏中")
                self.start_step("退出玩牌房间")
                self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
        finally:
            self.common.closedriver()

class D25689_LaiziRoom_Sign_Display(TestCase):
    '''
    房间内身份标志显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    # pending = True

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()
        self.common.user_money(money=1000)

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
            self.game_page.wait_element("切换按钮").click()
            elments = self.game_page.get_elements("切换玩法")
            elments[0].click()
            # self.level_page.wait_element("快速开始").click()
        self.start_step("点击初级场房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.start_step("开始玩牌")
        self.game_page.wait_element("开始").click()
        starttime = time.time()
        while self.game_page.element_is_exist("正在配桌中"):
            time.sleep(1)
            self.log_info("正在配桌中,等待")
            endtime = time.time()
            time.sleep(3)
            try:
                self.game_page.wait_element("换桌").click()
            except:
                self.log_info("换桌失败")
            if (endtime - starttime) / 60 > self.timeout - 5:
                self.game_page.is_in_gameroom(self.luadriver)
                self.log_info("等待超时")
                return
        self.start_step("叫地主")
        while self.game_page.element_is_exist("出牌", 1) == False:
            list = ["抢地主", "叫地主", "不加倍"]
            self.log_info("叫地主中")
            for name in list:
                try:
                    self.game_page.wait_element(name, 1).click()
                except:
                    self.log_info("未出现抢地主按钮")
            if self.game_page.element_is_exist("继续游戏", 1):
                break
        self.game_page.element_is_exist("农民地主标志",20)
        self.game_page.screenshot("农民地主标志.png")
        self.start_step("托管")
        if self.game_page.element_is_exist("机器人") == False:
            self.game_page.wait_element("托管").click()
        while self.game_page.element_is_exist("继续游戏", 1) == False:
            time.sleep(1)
            self.log_info("正在游戏中")
        self.start_step("退出玩牌房间")
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
        finally:
            self.common.closedriver()

class D25692_LaiziRoom_MultiplyDouble(TestCase):
    '''
    明牌加倍
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    # pending = True

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()
        self.common.user_money(money=1000)

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
            self.game_page.wait_element("切换按钮").click()
            elments = self.game_page.get_elements("切换玩法")
            elments[0].click()
            # self.level_page.wait_element("快速开始").click()
        self.start_step("点击初级场房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.start_step("开始玩牌")
        self.game_page.wait_element("开始").click()
        starttime = time.time()
        while self.game_page.element_is_exist("正在配桌中"):
            time.sleep(1)
            self.log_info("正在配桌中,等待")
            endtime = time.time()
            time.sleep(3)
            try:
                self.game_page.wait_element("换桌").click()
            except:
                self.log_info("换桌失败")
            if (endtime - starttime) / 60 > self.timeout - 5:
                self.game_page.is_in_gameroom(self.luadriver)
                self.log_info("等待超时")
                return
        self.start_step("叫地主")
        while self.game_page.element_is_exist("出牌", 1) == False:
            list = ["抢地主", "叫地主","加倍"]
            self.log_info("叫地主中")
            for name in list:
                try:
                    self.game_page.wait_element(name, 1).click()
                except:
                    self.log_info("未出现抢地主按钮")
            if self.game_page.element_is_exist("继续游戏", 1):
                break
        try:
            self.game_page.wait_element("明牌X2").click()
            self.game_page.screenshot("明牌.png")
        except:
            self.log_info("未出现明牌按钮")
        self.start_step("托管")
        if self.game_page.element_is_exist("机器人") == False:
            self.game_page.wait_element("托管").click()
        while self.game_page.element_is_exist("继续游戏", 1) == False:
            time.sleep(1)
            self.log_info("正在游戏中")
        self.game_page.screenshot("结算界面.png")
        self.start_step("退出玩牌房间")
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
        finally:
            self.common.closedriver()

class D25693_LaiziRoom_Interaction(TestCase):
    '''
    房间内玩家互动
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    # pending = True

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()
        self.common.user_money(money=1000)

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
            self.game_page.wait_element("切换按钮").click()
            elments = self.game_page.get_elements("切换玩法")
            elments[0].click()
            # self.level_page.wait_element("快速开始").click()
        self.start_step("点击初级场房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.start_step("开始玩牌")
        while self.game_page.element_is_exist("开始",1):
            self.game_page.wait_element("开始").click()
        self.start_step("叫地主")
        while self.game_page.element_is_exist("出牌", 1) == False:
            list = ["抢地主", "叫地主","加倍"]
            self.log_info("叫地主中")
            for name in list:
                try:
                    self.game_page.wait_element(name, 1).click()
                except:
                    self.log_info("未出现抢地主按钮")
        self.start_step("查看玩家信息")
        head_elements = self.game_page.get_elements("玩家头像")
        for i in range(1):
            head_elements[i].click()
            time.sleep(2)
            self.start_step("添加第%s个玩家为好友" %(i+1))
            self.game_page.wait_element("添加好友").click()
            self.game_page.screenshot("添加好友%s.png" %(i+1),sleeptime=0)
            head_elements[i].click()
            self.game_page.wait_element("发送表情").click()
            self.game_page.screenshot("发送表情%s.png" %(i+1),sleeptime=0)
            self.game_page.screenshot("发送表情%s_1.png" %(i+1),sleeptime=0)
            head_elements[i].click()
            self.game_page.wait_element("举报").click()
            self.game_page.wait_element("举报信息").click()
            self.game_page.screenshot("举报信息%s.png" %(i+1),sleeptime=0)
            self.game_page.wait_element("确定").click()
            self.game_page.screenshot("确定举报%s.png" %(i+1),sleeptime=3)
            # while self.game_page.element_is_exist("继续游戏", 1):
            #     break
            # while self.game_page.element_is_exist("QQ分享", 1):
            #     self.game_page.screenshot("出现分享页面.png")
            #     self.luadriver.keyevent(4)
            #     break
        self.start_step("托管")
        if self.game_page.element_is_exist("机器人",1) == False:
            self.game_page.wait_element("托管").click()
        while self.game_page.element_is_exist("继续游戏", 1) == False:
            time.sleep(1)
            self.log_info("正在游戏中")
        self.game_page.screenshot("结算界面.png")
        self.start_step("退出玩牌房间")
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
        finally:
            self.common.closedriver()

class D25694_LaiziRoom_Setting(TestCase):
    '''
    房间内设置
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    # pending = True

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()
        self.common.user_money(money=1000)

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
            self.game_page.wait_element("切换按钮").click()
            elments = self.game_page.get_elements("切换玩法")
            elments[0].click()
            # self.level_page.wait_element("快速开始").click()
        self.start_step("点击初级场房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.start_step("开始玩牌")
        self.game_page.wait_element("开始").click()
        self.start_step("叫地主")
        while self.game_page.element_is_exist("出牌", 1) == False:
            list = ["抢地主", "叫地主","加倍"]
            self.log_info("叫地主中")
            for name in list:
                try:
                    self.game_page.wait_element(name, 1).click()
                except:
                    self.log_info("未出现抢地主按钮")
            if self.game_page.element_is_exist("继续游戏", 1):
                break
        self.start_step("设置屏蔽聊天，查看设置结果")
        self.game_page.wait_element("设置").click()
        self.game_page.wait_element("屏蔽聊天").click()
        booltext = self.game_page.wait_element("屏蔽聊天").get_attribute('selected')
        self.game_page.wait_element("设置").click()
        self.game_page.wait_element("聊天").click()
        self.game_page.wait_element("常用语聊天列表").click()
        self.game_page.wait_element("聊天").click()
        self.game_page.wait_element("常用语聊天列表").click()
        if booltext =='false':
            self.start_step("设置为非屏蔽聊天后的效果")
            self.game_page.screenshot("设置为非屏蔽聊天后截图.png")
        else:
            self.start_step("设置为屏蔽聊天后的效果")
            self.game_page.screenshot("设置为屏蔽聊天后截图.png")
            self.start_step("恢复")
            self.game_page.wait_element("设置").click()
            self.game_page.wait_element("屏蔽聊天").click()
            self.game_page.wait_element("设置").click()
        self.start_step("设置屏蔽连发表情，查看设置结果")
        self.game_page.wait_element("设置").click()
        self.game_page.wait_element("屏蔽连发表情").click()
        booltext1 = self.game_page.wait_element("屏蔽连发表情").get_attribute('selected')
        self.game_page.wait_element("设置").click()
        self.game_page.wait_element("玩家头像").click()
        self.game_page.wait_element("连发十次互动表情").click()
        if booltext1 =='false':
            # self.start_step("设置为非屏蔽连发表情后的效果")
            self.game_page.screenshot("设置为非屏蔽连发表情后截图.png",sleeptime=0)
        else:
            # self.start_step("设置为屏蔽连发表情后的效果")
            self.game_page.screenshot("设置为屏蔽连发表情后截图.png", sleeptime=0)
            self.start_step("恢复")
            self.game_page.wait_element("设置").click()
            self.game_page.wait_element("设置").click()
            self.game_page.wait_element("屏蔽连发表情").click()
            self.game_page.wait_element("设置").click()
        self.start_step("托管")
        if self.game_page.element_is_exist("机器人") == False:
            self.game_page.wait_element("托管").click()
        while self.game_page.element_is_exist("继续游戏", 1) == False:
            time.sleep(1)
            self.log_info("正在游戏中")
        self.game_page.screenshot("结算界面.png")
        self.start_step("退出玩牌房间")
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
        finally:
            self.common.closedriver()

class D25695and25696_LaiziRoom_Trustee_Display(TestCase):
    '''
    托管/托管状态
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    # pending = True

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()
        self.common.user_money(money=1000)

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
            self.game_page.wait_element("切换按钮").click()
            elments = self.game_page.get_elements("切换玩法")
            elments[0].click()
            # self.level_page.wait_element("快速开始").click()
        self.start_step("点击初级场房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.start_step("开始玩牌")
        self.game_page.wait_element("开始").click()
        starttime = time.time()
        while self.game_page.element_is_exist("正在配桌中"):
            time.sleep(1)
            self.log_info("正在配桌中,等待")
            endtime = time.time()
            time.sleep(3)
            try:
                self.game_page.wait_element("换桌").click()
            except:
                self.log_info("换桌失败")
            if (endtime - starttime) / 60 > self.timeout - 5:
                self.game_page.is_in_gameroom(self.luadriver)
                self.log_info("等待超时")
                return
        self.start_step("叫地主")
        while self.game_page.element_is_exist("出牌", 2) == False:
            list = ["抢地主", "叫地主","加倍"]
            self.log_info("叫地主中")
            for name in list:
                try:
                    self.game_page.wait_element(name, 1).click()
                except:
                    self.log_info("未出现抢地主按钮")
            if self.game_page.element_is_exist("继续游戏", 1):
                break
        try:
            self.game_page.wait_element("明牌X2", 20).click()
            self.game_page.screenshot("明牌.png")
        except:
            self.log_info("未出现明牌按钮")
        self.game_page.screenshot("底牌及倍数.png")
        self.start_step("托管")
        if self.game_page.element_is_exist("机器人") == False:
            self.game_page.wait_element("托管").click()
            self.game_page.screenshot("手动托管.png")
        try:
            self.game_page.wait_element("点击取消托管").click()
            self.game_page.screenshot("取消托管.png")
        except:
            self.log_info("未出现取消托管按钮")
        if self.game_page.element_is_exist("点击取消托管") == False:
            time.sleep(1)
        self.game_page.screenshot("自动托管.png")
        while self.game_page.element_is_exist("继续游戏", 1) == False:
            time.sleep(1)
            self.log_info("正在游戏中")
        self.start_step("退出玩牌房间")
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
        finally:
            self.common.closedriver()

class D25701_LaiziRoom_Account_Display(TestCase):
    '''
    房间内结算显示
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    pending = True

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()
        self.common.user_money(money=1000)

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
            self.game_page.wait_element("切换按钮").click()
            elments = self.game_page.get_elements("切换玩法")
            elments[0].click()
            # self.level_page.wait_element("快速开始").click()
        self.start_step("点击初级场房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.start_step("开始玩牌")
        self.game_page.wait_element("开始").click()
        starttime = time.time()
        while self.game_page.element_is_exist("正在配桌中"):
            time.sleep(1)
            self.log_info("正在配桌中,等待")
            endtime = time.time()
            time.sleep(3)
            try:
                self.game_page.wait_element("换桌").click()
            except:
                self.log_info("换桌失败")
            if (endtime - starttime) / 60 > self.timeout - 5:
                self.game_page.is_in_gameroom(self.luadriver)
                self.log_info("等待超时")
                return
        self.start_step("叫地主")
        while self.game_page.element_is_exist("出牌", 1) == False:
            list = ["抢地主", "叫地主","加倍"]
            self.log_info("叫地主中")
            for name in list:
                try:
                    self.game_page.wait_element(name, 1).click()
                except:
                    self.log_info("未出现抢地主按钮")
            if self.game_page.element_is_exist("继续游戏", 1):
                break
        self.start_step("托管")
        if self.game_page.element_is_exist("机器人") == False:
            self.game_page.wait_element("托管").click()
        while self.game_page.element_is_exist("继续游戏", 1) == False:
            time.sleep(1)
            self.log_info("正在游戏中")
        self.game_page.screenshot("结算界面.png")
        self.start_step("退出玩牌房间")
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
        finally:
            self.common.closedriver()

class D25706_LaiziRoom_Network_Reconnect(TestCase):
    '''
    房间内玩牌断线重回
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    # pending = True

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()
        self.common.user_money(money=1000)

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
            self.game_page.wait_element("切换按钮").click()
            elments = self.game_page.get_elements("切换玩法")
            elments[0].click()
            # self.level_page.wait_element("快速开始").click()
        self.start_step("进入房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.start_step("开始玩牌")
        self.game_page.wait_element("开始").click()
        starttime = time.time()
        while self.game_page.element_is_exist("正在配桌中"):
            time.sleep(1)
            self.log_info("正在配桌中,等待")
            endtime = time.time()
            time.sleep(3)
            try:
                self.game_page.wait_element("换桌").click()
            except:
                self.log_info("换桌失败")
            if (endtime - starttime) / 60 > self.timeout - 5:
                self.game_page.is_in_gameroom(self.luadriver)
                self.log_info("等待超时")
                return
        self.start_step("叫地主")
        while self.game_page.element_is_exist("出牌", 1) == False:
            list = ["抢地主", "叫地主","加倍"]
            self.log_info("叫地主中")
            for name in list:
                try:
                    self.game_page.wait_element(name, 1).click()
                except:
                    self.log_info("未出现抢地主按钮")
            if self.game_page.element_is_exist("继续游戏", 1):
                break
        self.start_step("重连")
        self.game_page.screenshot("断开网络前.png")
        self.start_step("断开网络")
        self.common.switchnetwork(self.luadriver, u"无网络")
        self.game_page.screenshot("断开网络时.png")
        self.start_step("重新连接网络")
        self.common.switchnetwork(self.luadriver, u"WIFI模式")
        self.common.network_connect()
        time.sleep(5)
        self.game_page.screenshot("重新连接网络.png")
        self.start_step("重新进入癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
            try:
                self.game_page.wait_element("切换按钮").click()
                elments = self.game_page.get_elements("切换玩法")
                elments[0].click()
                # self.level_page.wait_element("快速开始").click()
            except:
                self.log_info("已进入房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
            if (self.game_page.element_is_exist("立即领取", 1) or self.game_page.element_is_exist("立即购买", 1)):
                self.game_page.screenshot("重新进入游戏时破产了.png")
                return
        self.game_page.screenshot("重新连接网络并进入癞子场.png")
        while self.game_page.element_is_exist("继续游戏", 1) == False:
            time.sleep(1)
            self.log_info("正在游戏中")
            if self.game_page.element_is_exist("开始", 1):
                break
            if self.game_page.element_is_exist("立即购买", 1):
                break
            if self.game_page.element_is_exist("机器人", 1) == False:
                self.game_page.wait_element("托管").click()
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
        finally:
            self.common.closedriver()

class D25690_LaiziRoom_Cards_Display(TestCase):
    '''
    底牌及倍数
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    pending = True

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()
        self.common.user_money(money=1000)

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
            self.game_page.wait_element("切换按钮").click()
            elments = self.game_page.get_elements("切换玩法")
            elments[0].click()
            # self.level_page.wait_element("快速开始").click()
        self.start_step("点击初级场房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.start_step("开始玩牌")
        self.game_page.wait_element("开始").click()
        starttime = time.time()
        while self.game_page.element_is_exist("正在配桌中"):
            time.sleep(1)
            self.log_info("正在配桌中,等待")
            endtime = time.time()
            time.sleep(3)
            try:
                self.game_page.wait_element("换桌").click()
            except:
                self.log_info("换桌失败")
            if (endtime - starttime) / 60 > self.timeout - 5:
                self.game_page.is_in_gameroom(self.luadriver)
                self.log_info("等待超时")
                return
        self.start_step("叫地主")
        while self.game_page.element_is_exist("出牌", 1) == False:
            list = ["抢地主", "叫地主", "不加倍"]
            self.log_info("叫地主中")
            for name in list:
                try:
                    self.game_page.wait_element(name, 1).click()
                except:
                    self.log_info("未出现抢地主按钮")
        self.game_page.screenshot("房间底牌和倍数展示.png")
        image_element = self.game_page.wait_element("房间内倍数")
        beishutext = self.common.image_text(image_element)
        self.start_step("房间内倍数展示%s" % beishutext)
        if beishutext.isdigit():
            self.assert_equal("房间内倍数展示", actual=int(beishutext)>=3)
        self.start_step("托管")
        if self.game_page.element_is_exist("机器人") == False:
            self.game_page.wait_element("托管").click()
        while self.game_page.element_is_exist("继续游戏", 1) == False:
            time.sleep(1)
            self.log_info("正在游戏中")
        self.start_step("退出玩牌房间")
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
        finally:
            self.common.closedriver()

class D25704_LaiziRoom_Broke_Display(TestCase):
    '''
    结算触发封顶或破产
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    # pending = True

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()
        self.common.user_money(money=3000)

    def play_game(self):
        self.start_step("开始玩牌")
        i = 1
        while self.game_page.element_is_exist("破产对话框")==False:
            while self.game_page.element_is_exist("开始"):
                self.game_page.wait_element("开始").click()
            while self.game_page.element_is_exist("继续游戏"):
                self.game_page.wait_element("继续游戏").click()
            self.start_step("开始玩第%s场牌" %i)
            starttime = time.time()
            while self.game_page.element_is_exist("正在配桌中",1):
                time.sleep(1)
                self.log_info("正在配桌中,等待")
                endtime = time.time()
                time.sleep(3)
                try:
                    self.game_page.wait_element("换桌").click()
                except:
                    self.log_info("换桌失败")
                if (endtime - starttime) / 60 > self.timeout - 5:
                    self.game_page.is_in_gameroom(self.luadriver)
                    self.log_info("等待超时")
                    return
            while self.game_page.element_is_exist("出牌",1)==False:
                list = ["抢地主", "叫地主", "加倍"]
                self.log_info("叫地主中")
                for name in list:
                    try:
                        self.game_page.wait_element(name, 1).click()
                    except:
                        self.log_info("未出现抢地主按钮")
                try:
                    self.game_page.wait_element("明牌X2",2).click()
                except:
                    self.log_info("未出现明牌按钮")
                if self.game_page.element_is_exist("继续游戏", 1):
                    break
            if self.game_page.element_is_exist("机器人") == False:
                self.game_page.wait_element("托管").click()
            self.game_page.screenshot("第%s次托管玩牌.png" %i)
            while self.game_page.element_is_exist("继续游戏", 1) == False:
                time.sleep(1)
                self.log_info("正在游戏中")
            while self.game_page.element_is_exist("继续游戏", 1):
                self.game_page.screenshot("第%s次玩牌结算.png" % i)
                while self.game_page.element_is_exist("QQ分享",1):
                        self.luadriver.keyevent(4)
                while self.game_page.element_is_exist("破产气泡"):
                    self.game_page.screenshot("癞子场破产气泡.png")
                    return
                try:
                    string = "赢取达到携带金币上限"
                    string in self.game_page.wait_element("赢取达到携带金币上限").get_attribute("text")
                    self.game_page.screenshot("赢取达到携带金币上限气泡.png")
                    return
                except:
                    self.log_info("未出现气泡")
                self.game_page.wait_element("继续游戏").click()
            while self.game_page.element_is_exist("去底倍场",1):
                self.game_page.screenshot("第%s次玩牌提示去底倍场.png" %i)
                self.game_page.wait_element("去底倍场").click()
            i += 1

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
            self.game_page.wait_element("切换按钮").click()
            elments = self.game_page.get_elements("切换玩法")
            elments[0].click()
            # self.level_page.wait_element("快速开始").click()
        self.start_step("点击初级场房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.play_game()
        self.level_page.screenshot("破产界面.png")
        try:
            self.assert_equal("检查是否出现立即购买", self.level_page.wait_element("立即购买文本").get_attribute("text") == "立即购买")
        except:
            self.log_info("未出现此按钮")
        self.start_step("退出玩牌房间")
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
        finally:
            self.common.closedriver()


# __qtaf_seq_tests__ = [D25704_LaiziRoom_Broke_Display]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()


