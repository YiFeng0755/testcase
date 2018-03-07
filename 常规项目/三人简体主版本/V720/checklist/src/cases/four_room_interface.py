#!/usr/bin/env python
# -*- coding:utf-8 -*- 
'''
四人场-四人场界面
'''
import time
from runcenter.enums import EnumStatus, EnumPriority
from runcenter.testcase import TestCase, debug_run_all
from common.common import Common
from uilib.game_page import Game_Page
from uilib.hall_page import Hall_Page
from common import Interface
from uilib.level_page import Level_Page

class D25771_FourRoom_Buy(TestCase):
    '''
    房间内快捷购买
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    # pending = True

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.log_info("金币数为5000")
        self.common.set_money(mid,5000)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去四人场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments = self.hall_page.get_elements("游戏列表")
            elments[3].click()
        self.start_step("进入房间")
        while self.level_page.element_is_exist("房间列表"):
            elments = self.level_page.get_elements("房间列表")
            print len(elments)
            self.common.swipeelement(elments[1], elments[3])
            self.level_page.wait_element("房间列表").click()
        while self.game_page.element_is_exist("购买金币") == False:
            self.common.swipeelement(elments[1], elments[3])
            self.level_page.wait_element("房间列表").click()
        self.start_step("查看金币支付页面")
        self.game_page.wait_element("购买金币",40).click()
        while self.game_page.element_is_exist("立即购买")==False:
            self.game_page.wait_element("购买金币").click()
        self.game_page.wait_element("立即购买",60).click()
        self.game_page.screenshot("金币购买界面.png")
        while self.game_page.element_is_exist("购买金币",1)==False:
            try:
                self.luadriver.keyevent(4)
            except:
                self.log_info("未出现支付页面")
        self.game_page.wait_element("关闭1").click()
        self.start_step("记牌器支付页面")
        if self.game_page.element_is_exist("记牌器"):
            self.game_page.wait_element("记牌器").click()
            time.sleep(4)
            self.game_page.get_elements("记牌器购买").click()
            self.game_page.wait_element("立即购买").click()
            self.game_page.screenshot("记牌器购买界面.png")
            self.game_page.wait_element("关闭1").click()
        else:
            self.log_info("未出现记牌器按钮")

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
        finally:
            self.common.closedriver()

class D25758_FourRoom_Displays(TestCase):
    '''
    金币不足
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg","mid")
        self.common.set_money(mid,1000)
        self.hall_page = Hall_Page()
        self.level_page = Level_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去四人场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments = self.hall_page.get_elements("游戏列表")
            elments[3].click()
        self.start_step("点击快速开始")
        self.level_page.wait_element("快速开始").click()
        self.level_page.screenshot("破产点击快速开始出现的界面.png")
        try:
            self.level_page.wait_element("关闭2").click()
        except:
            self.log_info("未出现此按钮")
        self.level_page.element_is_exist("立即购买")
        self.assert_equal("检查是否出现立即购买",self.level_page.wait_element("立即购买文本").get_attribute("text")=="立即购买")
        self.level_page.screenshot("立即购买")

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
            self.common.set_money(mid, 5000)
        finally:
            self.common.closedriver()

class D25759_FourRoom_Enter(TestCase):
    '''
    玩家金币不足
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    pending = True

    def pre_test(self):
        self.common = Common()
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_money(mid, 4000)
        self.hall_page = Hall_Page()
        self.level_page = Level_Page()
        self.game_page = Game_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去四人场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments = self.hall_page.get_elements("游戏列表")
            elments[3].click()
        elments = self.level_page.get_elements("房间列表")
        print len(elments)
        for j in range(len(elments)/2):
            self.start_step("点击第%s个房间" %(j+1))
            elments[j].click()
            try:
                self.level_page.wait_element("关闭2").click()
            except:
                self.log_info("未出现此按钮")
            self.game_page.element_is_exist("立即购买")
            self.assert_equal("检查是否出现立即购买", self.level_page.wait_element("立即购买文本").get_attribute("text") == "立即购买")
            self.game_page.screenshot("点击第%s个房间界面.png" %(j+1))
            self.hall_page.wait_element("关闭1").click()
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
            self.common.set_money(mid, 5000)
        finally:
            self.common.closedriver()

class D25760_FourRoom_Enter_ToomuchMoney(TestCase):
    '''
    金币过多
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    pending = True

    def pre_test(self):
        self.common = Common()
        global mid,money
        money = 1000001
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_money(mid, 1000001)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去四人场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[3].click()
        self.start_step("查看房间列表")
        self.hall_page.screenshot("查看房间列表.png")
        # while self.level_page.element_is_exist("房间列表"):
        #     elments = self.level_page.get_elements("房间列表")
        #     print len(elments)
        #     self.common.swipeelement(elments[1], elments[3])
        self.start_step("获取初级场底分")
        imageelement = self.game_page.wait_element("场次底分")
        chujichangdifen = self.common.image_text(imageelement)
        if chujichangdifen == '':
            chujichangdifen = '10'
        self.log_info("初级场底分:"+chujichangdifen)
        self.start_step("点击初级场房间")
        self.level_page.wait_element("房间列表").click()
        string = self.level_page.wait_element("金币超出文本").get_attribute("text")
        self.assert_equal("检查是否出现金币超出弹框",string.find("您的金币已超过本房间上限")!= -1)
        self.level_page.screenshot("金币超出.png")
        self.level_page.wait_element("去高级场").click()
        time.sleep(4)
        self.level_page.screenshot("高级场房间.png")
        image_element = self.game_page.wait_element("四人场房间底分")
        room = self.common.image_text(image_element)
        self.start_step("初级场底：%s，房间底分：%s，核对是否是高级场" %(chujichangdifen,room))
        if room.isdigit():
            self.assert_equal("进入了高级场",actual= int(room)>int(chujichangdifen))
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
            self.common.set_money(mid, 5000)
        finally:
            self.common.closedriver()

class D25763_FourRoom_Cards_Display(TestCase):
    '''
    房间内底牌及倍数显示是否正常
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    pending = True

    def pre_test(self):
        self.common = Common()
        self.start_step("设置金币数为30001")
        global mid,money
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_money(mid,30001)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进入四人场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments = self.hall_page.get_elements("游戏列表")
            elments[3].click()
        self.start_step("查看房间列表")
        elments = self.level_page.get_elements("房间列表")
        self.start_step("进入房间")
        difenlist = {'1': '10', '2': '50', '3': '100'}
        for j in range(len(elments) / 2):
            if j < 3:
                self.start_step("进入第%s个房间" % (j + 1))
                elments[j].click()
                time.sleep(5)
                self.game_page.wait_element("四人场房间底分")
                self.game_page.screenshot("第%s个房间底分为%s.png" % ((j+1),difenlist[str(j+1)]))
                image_element = self.game_page.wait_element("四人场房间底分")
                beishutext = self.common.image_text(image_element)
                # if beishutext.isdigit():
                #     self.assert_equal("底分展示",actual=beishutext,expect=difenlist[str(j+1)])
                while self.game_page.element_is_exist("退出"):
                    self.game_page.wait_element("退出").click()
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
            self.common.set_money(mid, 5000)
        finally:
            self.common.closedriver()

class D25768_FourRoom_Talk_Display(TestCase):
    '''
    房间内聊天
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    # pending = True

    def pre_test(self):
        self.common = Common()
        self.start_step("设置金币数为100000")
        global mid,money
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_money(mid,100000)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去四人场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments = self.hall_page.get_elements("游戏列表")
            elments[3].click()
        self.start_step("进入房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        while self.game_page.element_is_exist("常用语聊天列表") == False:
            self.game_page.wait_element("聊天").click()
        self.game_page.wait_element("常用语聊天列表").click()
        self.game_page.screenshot("常用语聊天.png",sleeptime=0)
        while self.game_page.element_is_exist("常用表情tab") == False:
            try:
                self.game_page.wait_element("聊天").click()
            except:
                self.log_info("未找到聊天按钮")
        self.game_page.wait_element("常用表情tab").click()
        self.game_page.wait_element("表情1").click()
        self.game_page.screenshot("常表情聊天.png",sleeptime=0)
        while self.game_page.element_is_exist("常用语tab") == False:
            self.game_page.wait_element("聊天").click()
        self.game_page.wait_element("常用语tab").click()
        text = self.common.random_str(5)
        self.game_page.wait_element("输入聊天信息").send_keys(text)
        self.game_page.wait_element("输入聊天信息").click()
        self.game_page.wait_element("发送").click()
        self.game_page.screenshot("发送自定义信息.png")
        self.start_step("退出玩牌房间")
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
            self.common.set_money(mid, 5000)
        finally:
            self.common.closedriver()

class D25770_FourRoom_Money_Display(TestCase):
    '''
    金币和元宝信息显示正常
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        global mid,money
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_money("mid",value="5000")
        money = Interface.get_money(mid)
        self.log_info("金币数：%s" %money)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进入四人场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments = self.hall_page.get_elements("游戏列表")
            elments[3].click()
        self.start_step("进入房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        time.sleep(5)
        self.game_page.screenshot("金币元宝显示.png")
        image_element = self.game_page.wait_element("购买金币")
        text = self.common.image_text(image_element)
        self.log_info("text:"+text)
        self.start_step("接口获取的金币数目为：%s，界面获取的金币数目为：%s，核对是否一致" %(money,text))
        # if text.isdigit():
        #     self.assert_equal("金币数是否一致",actual=text,expect=money)
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
            self.common.set_money(mid, 5000)
        finally:
            self.common.closedriver()

class D25774_FourRoom_Change_Table(TestCase):
    '''
    换桌
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        global mid,money
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_money(mid, 5000)
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.level_page = Level_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进去四人场")
        while self.hall_page.element_is_exist("游戏列表"):
            elments1 = self.hall_page.get_elements("游戏列表")
            elments1[3].click()
        self.start_step("进入房间")
        while self.level_page.element_is_exist("房间列表"):
            self.level_page.wait_element("房间列表").click()
        time.sleep(6)
        self.game_page.wait_element("换桌").click()
        self.level_page.screenshot("换桌.png")
        self.level_page.screenshot("换桌1.png")
        self.start_step("退出玩牌房间")
        self.game_page.is_in_gameroom(self.luadriver)

    def post_test(self):
        try:
            self.game_page.is_in_gameroom(self.luadriver)
            self.common.set_money(mid, 5000)
        finally:
            self.common.closedriver()


# __qtaf_seq_tests__ = [D25770_FourRoom_Money_Display]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()


