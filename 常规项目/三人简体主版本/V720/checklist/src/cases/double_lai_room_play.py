#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
双癞子场--玩牌相关(正式/测试)
'''
import time
from runcenter.enums import EnumStatus, EnumPriority
from runcenter.testcase import TestCase, debug_run_all
from common.common import Common
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from uilib.level_page import Level_Page

class D25712_DoubleLaizi_Room_InAndOut(TestCase):
    '''
    房间内按钮跳转
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
        self.common.user_money(money=3000)


    def run_test(self):
        self.start_step("进入双癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
        self.start_step("点击初级场房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.game_page.wait_element("输赢封顶")
        self.game_page.screenshot("第一次进房间.png")
        self.start_step("点击退出键退出房间")
        i = 0
        while self.game_page.element_is_exist("退出"):
            self.game_page.wait_element("退出").click()
            i += 1
            self.log_info("点击退出次数：%s" %i )
        self.level_page.wait_element("同步标志")
        self.hall_page.screenshot("点击退出键退出房间.png")
        self.level_page.wait_element("房间列表").click()
        self.game_page.wait_element("输赢封顶")
        self.game_page.screenshot("第二次进房间.png")
        self.start_step("点击物理返回键退出房间")
        while self.game_page.element_is_exist("同步标志"):
            self.luadriver.keyevent(4)
            time.sleep(4)
            self.log_info("点击物理返回键" )
        self.level_page.wait_element("同步标志",30)
        self.hall_page.screenshot("物理返回键退出房间.png")
        self.level_page.wait_element("房间列表").click()
        self.game_page.wait_element("输赢封顶")
        self.game_page.screenshot("第三次进房间.png")
        self.start_step("点击开始按钮")
        self.game_page.wait_element("开始",30).click()
        self.hall_page.screenshot("点击开始按钮.png")
        i = 0
        while self.game_page.element_is_exist("退出"):
            self.game_page.wait_element("退出").click()
            i += 1
            self.log_info("点击退出次数：%s" %i )
            if i > 5:
                while self.game_page.element_is_exist("出牌", 2) == False:
                    list = ["抢地主", "叫地主", "不加倍"]
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

class D25713_DoubleLaizi_Sign_Display(TestCase):
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
        self.common.user_money(money=3000)

    def run_test(self):
        self.start_step("进入双癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
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
        if self.game_page.element_is_exist("机器人",1) == False:
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

class D25714_DoubleLaizi_Cards_Display(TestCase):
    '''
    底牌及倍数
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
        self.common.user_money(money=3000)

    def run_test(self):
        self.start_step("进入双癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
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
        self.game_page.screenshot("底牌及倍数.png")
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

class D25719_DoubleLaizi_MultiplyDouble(TestCase):
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
        self.start_step("设置金币")
        self.common.user_money(money=3000)

    def run_test(self):
        self.start_step("进入双癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
        self.start_step("进入房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.start_step("开始玩牌")
        while self.game_page.element_is_exist("开始"):
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
        # image_element = self.game_page.wait_element("双癞子场倍数")
        # beishu1 = self.common.image_text(image_element)
        self.game_page.screenshot("明牌前的倍数.png",sleeptime=0)
        try:
            self.game_page.wait_element("明牌X2", 20).click()
            # beishu2 = self.common.image_text(image_element)
            self.game_page.screenshot("明牌.png")
            # if beishu1.isdigit() and beishu2.isdigit():
            #     self.start_step("明牌前的倍数%s，之后的倍数%s" %(beishu1,beishu2))
            #     self.assert_equal("明牌加倍",actual=(beishu2/beishu1),expect=2)
        except:
            self.log_info("未出现明牌按钮")
        self.game_page.screenshot("明牌后的倍数.png")
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

class D25720_DoubleLaizi_Interaction(TestCase):
    '''
    玩家互动
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
        self.common.user_money(money=3000)

    def run_test(self):
        self.start_step("进入双癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
        self.start_step("进入房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.start_step("开始玩牌")
        while self.game_page.element_is_exist("开始"):
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
            # while self.game_page.element_is_exist("QQ分享"):
            #     self.game_page.screenshot("出现分享页面.png")
            #     self.luadriver.keyevent(4)
            #     break
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

class D25721_DoubleLaizi_Setting(TestCase):
    '''
    房间内设置
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
        self.common.user_money(money=3000)

    def run_test(self):
        self.start_step("进入双癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
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

class D25722_DoubleLaizi_Trustee_Display(TestCase):
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
        self.common.user_money(money=3000)

    def run_test(self):
        self.start_step("进去癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
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
            list = ["抢地主", "叫地主"]
            self.log_info("叫地主中")
            for name in list:
                try:
                    self.game_page.wait_element(name, 1).click()
                except:
                    self.log_info("未出现抢地主按钮")
            if self.game_page.element_is_exist("继续游戏", 1):
                break
        self.start_step("托管")
        if self.game_page.element_is_exist("机器人",2) == False:
            self.game_page.wait_element("托管").click()
            self.game_page.screenshot("手动托管.png")
            try:
                self.game_page.wait_element("点击取消托管").click()
                self.game_page.screenshot("取消托管.png")
            except:
                self.log_info("未出现取消托管按钮")
        while self.game_page.element_is_exist("点击取消托管") == False and self.game_page.element_is_exist("继续游戏") == False:
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

class D25728_DoubleLaizi_Account_Display(TestCase):
    '''
    房间内结算显示
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
        self.common.user_money(money=3000)

    def run_test(self):
        self.start_step("进入双癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
        self.start_step("进入房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.start_step("开始玩牌")
        while self.game_page.element_is_exist("开始"):
            self.game_page.wait_element("开始").click()
        self.game_page.screenshot("玩牌开始.png")
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

class D25733_DoubleLaizi_Network_Reconnect(TestCase):
    '''
    房间内玩牌断线重回
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
        self.start_step("设置金币")
        self.common.user_money(money=1000)

    def run_test(self):
        self.start_step("进入双癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
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
        # self.start_step("托管")
        # while self.game_page.element_is_exist("继续游戏",2) == False and self.game_page.element_is_exist("机器人",2) == False:
        #     self.game_page.wait_element("托管").click()
        self.start_step("重连")
        self.game_page.screenshot("断开网络前.png")
        self.common.switchnetwork(self.luadriver, u"无网络")
        self.game_page.screenshot("断开网络时.png")
        self.common.switchnetwork(self.luadriver, u"WIFI模式")
        self.common.network_connect()
        time.sleep(5)
        self.game_page.screenshot("重新连接网络.png")
        self.start_step("重新进入双癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
            if (self.game_page.element_is_exist("立即领取",1) or self.game_page.element_is_exist("立即购买",1)):
                self.game_page.screenshot("重新进入游戏时破产了.png")
                return
        self.game_page.screenshot("重新连接网络并进入双癞子场.png")
        while self.game_page.element_is_exist("继续游戏", 1) == False:
            time.sleep(1)
            self.log_info("正在游戏中")
            if self.game_page.element_is_exist("开始"):
                break
            if self.game_page.element_is_exist("立即购买",1):
                break
            if self.game_page.element_is_exist("机器人",1) == False:
                self.game_page.wait_element("托管").click()
        self.start_step("退出玩牌房间")
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
        finally:
            self.common.closedriver()

class D25731_DoubleLaizi_Broke_Display(TestCase):
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
        while self.game_page.element_is_exist("破产对话框",1)==False:
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
                    self.game_page.screenshot("双癞子场破产气泡.png")
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
        self.start_step("进入双癞子场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[1].click()
        self.start_step("进入房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        self.play_game()
        self.level_page.screenshot("结算包含气泡界面.png")
        # try:
        #     self.assert_equal("检查是否出现立即购买", self.level_page.wait_element("立即购买文本").get_attribute("text") == "立即购买")
        # except:
        #     self.log_info("未出现此按钮")
        self.start_step("退出玩牌房间")
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
        finally:
            self.common.closedriver()

__qtaf_seq_tests__ = [D25719_DoubleLaizi_MultiplyDouble]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()


