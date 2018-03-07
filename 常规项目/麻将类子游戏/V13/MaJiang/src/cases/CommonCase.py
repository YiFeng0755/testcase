#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.game_page import Game_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common
import common.Interface as PHPInterface

class CommonCase(TestCase):

    def pre_test(self):
    #初始化步骤
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.common = Common()
        self.start_step("初始化driver")
        self.driver = self.common.setupdriver()


        self.start_step("关闭弹框")
        self.common.closeactivity(self.driver)

    def click_change(self):
        if self.hall_page.element_is_exist("右三角"):
            self.hall_page.wait_element("右三角").click()
            time.sleep(1)
        return True

    def set_autoPerson(self,gameElement):
        name = gameElement.get_attribute("name")
        gameid = int(name[4:len(name)])
        # 获取gameid
        PHPInterface.set_robot_flag(gameid, 0, 0, 12, 0)
        #关闭机器人

    def open_autoPerson(self,gameElement):
        name = gameElement.get_attribute("name")
        gameid = int(name[4:len(name)])
        # 获取gameid
        PHPInterface.set_robot_flag(gameid, 0, 0, 12, 1)
        #打开机器人

    def inter_game(self,gameElement,isChange = False):
        game_id = gameElement.get_attribute("name")
        #得到game203，game2000
        self.start_step("点击游戏" + game_id)
        if isChange:
            self.click_change()
        gameElement.click()
        if self.game_page.game_is_download():
            # 游戏已经下载
            self.start_step("进入游戏房间")
            if not self.game_page.element_is_exist("广播按钮") or self.game_page.element_is_exist("玩法", 1):
            #判断点击场次上方的（标准场、叫分场、或者是金条场）
                self.game_page.click_game_play()
                #默认点击最左边的场次
            if self.hall_page.get_elements("场次名称") != None:
                ele = self.hall_page.get_elements("场次名称")
                ele[0].click()
                # 点击初级场，进入游戏
            else:
                self.assert_equal(game_id + "进入游戏房间失败", False, True)
                self.back_hall()
                return False
            return True
            # 说明子游戏下载成功，并且进入游戏房间成功
        else:
            self.assert_equal(game_id + "进入子游戏失败", False, True)
            return False
        if self.hall_page.element_is_exist("关闭框"):
            self.hall_page.wait_element("关闭框").click()

    def exit_gameroom(self):
    #退出游戏房间
        try:
            self.hall_page.wait_element("菜单").click()
            self.hall_page.wait_element("退出").click()
            if self.hall_page.element_is_exist("带他返回游戏大厅"):
                self.hall_page.wait_element("带他返回游戏大厅").click()
            while (self.hall_page.element_is_exist("预发布") != True):
                self.driver.back()
                time.sleep(10)
                # 等待牌局打完
        except:
            print "退出牌局失败"

    def back_hall(self):
    #返回游戏大厅
        if self.hall_page.wait_element("返回1") != None:
            self.hall_page.wait_element("返回1").click()

    def test_case(self, reconnect):
        game_list = self.game_page.get_game_list()
        #获取某一屏幕的所有子游戏
        reconnect(game_list)
        if self.click_change():
            game_list = self.game_page.get_game_list()
            reconnect(game_list,True)

    def set_coin(self):
        try:
            global mid
            mid = self.common.get_config_value("casecfg", "mid")
            self.start_step("设置银币数为10000")
            self.common.set_coin(mid=mid, value="20000")
            if self.hall_page.element_is_exist("预发布"):
                self.hall_page.wait_element("预发布").click()
                #重新刷新页面
                time.sleep(10)
            self.hall_page.wait_element("头像")
        except:
            self.assert_equal("设置金币失败",False,True)

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        self.common.closedriver()

class C27218_Reconnect(CommonCase):
    '''
    玩家进入房间未准备，掉线重连
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        CommonCase.pre_test(self)

    def run_test(self):
        def reconnect(gameList,flag = False):
        #对某一屏幕的子游戏遍历操作
            for game in gameList:
                if self.inter_game(game,flag):
                    #获取到子游戏id，并且已经进入游戏房间
                    self.set_autoPerson(game)
                    #关闭机器人操作
                    time.sleep(2)
                    self.hall_page.wait_element("测试").click()
                    self.hall_page.wait_element("重连").click()
                    if self.hall_page.element_is_exist("关闭对话框"):
                        self.hall_page.element_is_exist("关闭对话框").click()
                    self.exit_gameroom()
                    #退出游戏
                    self.back_hall()
                    #退出游戏大厅
        self.test_case(reconnect)

    def post_test(self):
        CommonCase.post_test(self)

class C27212_ReadPlay_Reconnect(CommonCase):
    '''
    玩家已准备游戏未开始，网络波动
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        CommonCase.pre_test(self)

    def run_test(self):
        def reconnect(gameList,flag = False):
        #对某一屏幕的子游戏遍历操作
            for game in gameList:
                if self.inter_game(game,flag):
                # 获取到子游戏id，并且已经进入游戏房间
                    self.set_autoPerson(game)
                    #关闭机器人界面
                    time.sleep(2)
                    if self.hall_page.element_is_exist("准备"):
                        self.hall_page.wait_element("准备").click()
                    time.sleep(4)
                    try:
                        self.hall_page.screenshot("%s_cartoonScreen.png" % game.get_attribute("name"))
                        # 截出定庄动画图
                        self.hall_page.wait_element("测试").click()
                        self.hall_page.wait_element("重连").click()
                        self.hall_page.screenshot("%s_ watermarkScreen.png" % game.get_attribute("name"))
                        # 截出定庄动画图重连后的图
                        if (self.hall_page.element_is_exist("关闭对话框") == True):
                            self.hall_page.wait_element("关闭对话框").click()
                    except:
                            self.assert_equal(game.get_attribute("name")+"未进入到定庄界面中",False,True)
                    self.exit_gameroom()
                    # 退出游戏
                    self.back_hall()
                    # 退出游戏大厅
        self.test_case(reconnect)

    def post_test(self):
        CommonCase.post_test(self)

class C27218_Village_reconnect(CommonCase):
    '''
    定庄阶段掉线重连
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        CommonCase.pre_test(self)

    def run_test(self):
        def reconnect(gameList,flag = False):
        #对某一屏幕的子游戏遍历操作
            for game in gameList:
                if self.inter_game(game,flag):
                    #获取到子游戏id，并且已经进入游戏房间
                    self.open_autoPerson(game)
                    #打开机器人操作
                    try:
                        self.hall_page.wait_element("准备").click()
                        if (self.hall_page.element_is_exist("庄") == True):
                            self.hall_page.screenshot("%s_cartoonScreen.png" % game.get_attribute("name"))
                            # 截出定庄动画图
                            self.hall_page.wait_element("测试").click()
                            self.hall_page.wait_element("重连").click()
                            self.hall_page.screenshot("%s_ watermarkScreen.png" % game.get_attribute("name"))
                            # 截出定庄动画图重连后的图
                        if (self.hall_page.element_is_exist("关闭对话框") == True):
                            self.hall_page.wait_element("关闭对话框").click()
                    except:
                        self.assert_equal(game.get_attribute("name") + "定庄界面进入失败", False, True)
                        time.sleep(5)
                    try:
                        self.exit_gameroom()
                        #退出游戏
                        self.back_hall()
                        #退出游戏大厅
                    except:
                        self.assert_equal(game.get_attribute("name") + '游戏直接退出房间到游戏大厅',False,True)

        self.test_case(reconnect)

    def post_test(self):
        CommonCase.post_test(self)

class C27212_Gamelist_Noready_Reconnect(CommonCase):
    '''
    定庄阶段网络波动
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        CommonCase.pre_test(self)

    def run_test(self):
        def reconnect(gameList,flag = False):
        #对某一屏幕的子游戏遍历操作
            for game in gameList:
                if self.inter_game(game,flag):
                    #获取到子游戏id，并且已经进入游戏房间
                    self.open_autoPerson(game)
                    #打开机器人操作
                    try:
                        self.hall_page.wait_element("准备").click()
                        if (self.hall_page.element_is_exist("庄") == True):
                            self.hall_page.screenshot("%s_cartoonScreen.png" % game.get_attribute("name"))
                            # 截出定庄动画图
                            try:
                                self.hall_page.wait_element("测试").click()
                                self.hall_page.wait_element("重连").click()
                                self.hall_page.screenshot(
                                    "%s_ watermarkScreen.png" % game.get_attribute("name"))
                                # 截出定庄动画图重连后的图
                            except:
                                self.common.switchnetwork(self.driver, u"无网络")
                                time.sleep(3)
                                self.common.switchnetwork(self.driver, u"WIFI模式")
                                self.common.network_connect()
                                self.hall_page.screenshot("%s_reconnectScreen.png" % game.get_attribute("name"))
                        if (self.hall_page.element_is_exist("关闭对话框") == True):
                            self.hall_page.wait_element("关闭对话框").click()
                    except:
                        time.sleep(5)
                    try:
                        self.exit_gameroom()
                        #退出游戏
                        self.back_hall()
                        #退出游戏大厅
                    except:
                        self.assert_equal(game.get_attribute("name") + '游戏直接退出房间到游戏大厅')
        self.test_case(reconnect)

    def post_test(self):
        CommonCase.post_test(self)

class C27212_Gamelist_Shutdown_Process(CommonCase):
    '''
    定庄阶段关闭进程重连
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        CommonCase.pre_test(self)

    def run_test(self):
        def reconnect(gameList,flag = False):
        #对某一屏幕的子游戏遍历操作
            for game in gameList:
                print game.get_attribute("name")
                if self.inter_game(game,flag):
                    #获取到子游戏id，并且已经进入游戏房间
                    self.open_autoPerson(game)
                    #关闭机器人操作
                    time.sleep(2)
                    try:
                        self.hall_page.wait_element("准备").click()
                        self.hall_page.wait_element("庄")
                        while (self.hall_page.element_is_exist("庄") == True):
                            self.hall_page.screenshot("%s_cartoonScreen.png" % game.get_attribute("name"))
                            # 截出定庄动画图
                            try:
                                self.common.closedriver()
                                # 关闭进程
                                time.sleep(3)
                                self.start_step("初始化driver")
                                #重新加载游戏
                                self.luadriver = self.common.setupdriver()
                                self.common.closeactivity(self.luadriver)
                                #关闭活动界面
                                time.sleep(5)
                                self.hall_page.screenshot("%s_RightScreen.png" % game.get_attribute("name"))
                                self.inter_game(game,flag)
                                #进入房间
                                time.sleep(4)
                                ele1 = self.hall_page.get_elements("换桌xxx")
                                ele1[1].click()
                                #点击换桌按钮,退出结算界面
                            except:
                                self.assert_equal(game.get_attribute("name") + "关闭进程失败",False,True)
                    except:
                        self.assert_equal(game.get_attribute("name") + "定庄失败",False,True)
                    try:
                        self.exit_gameroom()
                        #退出游戏
                        self.back_hall()
                        #退出游戏大厅
                    except:
                        self.assert_equal(game.get_attribute("name")+ '游戏直接退出房间到游戏大厅',False,True)
        self.test_case(reconnect)

    def post_test(self):
        CommonCase.post_test(self)

class C27213_Lock_Screen(CommonCase):
    '''
    定庄阶段长时间切换后台/锁屏
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        CommonCase.pre_test(self)

    def run_test(self):
        def reconnect(gameList,flag = False):
        #对某一屏幕的子游戏遍历操作
            for game in gameList:
                if self.inter_game(game,flag):
                    #获取到子游戏id，并且已经进入游戏房间
                    self.open_autoPerson(game)
                    #打开机器人操作
                    time.sleep(2)
                    try:
                        self.hall_page.wait_element("准备").click()
                        self.hall_page.wait_element("庄")
                        self.hall_page.screenshot("%s_cartoonScreen.png" % game.get_attribute("name"))
                        # 截出定庄动画图
                        try:
                            self.log_info("home键")
                            self.driver.keyevent(3)  # home
                            self.game_page.screenshot("%s_being.png" % game.get_attribute("name"))
                            time.sleep(1)
                            self.start_step("解锁")
                            self.common.unlock()
                        except:
                            self.assert_equal(game.get_attribute("name") + "锁屏操作失败",False,True)
                    except:
                        self.assert_equal(game.get_attribute("name") + "定庄失败" , False,True)
                try:
                    self.exit_gameroom()
                    #退出游戏
                    self.back_hall()
                    #退出游戏大厅
                except:
                    self.assert_equal(game.get_attribute("name") + "未返回到游戏大厅",False,True)
        self.test_case(reconnect)

    def post_test(self):
        CommonCase.post_test(self)

class C27214_ShortTime_Shift(CommonCase):
    '''
       定庄阶段短时间切换后台/锁屏
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        CommonCase.pre_test(self)

    def run_test(self):
        def reconnect(gameList, flag=False):
            # 对某一屏幕的子游戏遍历操作
            for game in gameList:
                if self.inter_game(game, flag):
                    # 获取到子游戏id，并且已经进入游戏房间
                    self.open_autoPerson(game)
                    # 打开机器人操作
                    time.sleep(2)
                    try:
                        self.hall_page.wait_element("准备").click()
                        self.hall_page.wait_element("庄")
                        if (self.hall_page.element_is_exist("庄") == True):
                            self.hall_page.screenshot("%s_cartoonScreen.png" % game.get_attribute("name"))
                            # 截出定庄动画图
                            try:
                                self.log_info("home键")
                                self.driver.keyevent(3)  # home
                                self.game_page.screenshot("%s_being.png" % game.get_attribute("name"))
                                time.sleep(1)
                                #1秒后解锁
                                self.start_step("解锁")
                                self.common.unlock()
                            except:
                                self.assert_equal(game.get_attribute("name") + "锁屏操作失败", False, True)
                    except:
                        self.assert_equal(game.get_attribute("name") + "定庄失败", False, True)
                try:
                    self.exit_gameroom()
                    # 退出游戏
                    self.back_hall()
                    # 退出游戏大厅
                except:
                    self.assert_equal(game.get_attribute("name") + "未返回到游戏大厅", False, True)

        self.test_case(reconnect)

    def post_test(self):
        CommonCase.post_test(self)

class C27215_PalyGame_ShortTime_Shift(CommonCase):
    '''
    发牌阶段短时间切换后台/锁屏
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        CommonCase.pre_test(self)

    def run_test(self):
        def reconnect(gameList, flag=False):
            # 对某一屏幕的子游戏遍历操作
            for game in gameList:
                self.set_coin()
                if self.inter_game(game, flag):
                    # 获取到子游戏id，并且已经进入游戏房间
                    self.open_autoPerson(game)
                    # 打开机器人操作
                    time.sleep(2)
                    try:
                        self.hall_page.wait_element("准备").click()
                        time.sleep(6)
                        self.hall_page.wait_element("东南西北")
                        try:
                            self.log_info("home键")
                            self.driver.keyevent(3)  # home
                            self.game_page.screenshot("%s_being.png" % game.get_attribute("name"))
                            time.sleep(1)
                            self.start_step("解锁")
                            self.common.unlock()
                        except:
                            self.assert_equal(game.get_attribute("name")+"短时间锁屏操作失败",False,True)
                    except:
                        self.assert_equal(game.get_attribute("name")+"麻将房间开局失败",False,True)
                try:
                    self.exit_gameroom()
                    # 退出游戏
                    self.back_hall()
                    # 退出游戏大厅
                except:
                    self.assert_equal(game.get_attribute("name") + "未返回到游戏大厅", False, True)

        self.test_case(reconnect)

    def post_test(self):
        CommonCase.post_test(self)

class C27216_PalyGame_LongTime_Shift(CommonCase):
    '''
    发牌阶段长时间切换后台/锁屏
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        CommonCase.pre_test(self)

    def run_test(self):
        def reconnect(gameList, flag=False):
            # 对某一屏幕的子游戏遍历操作
            for game in gameList:
                    self.set_coin()
                    if self.inter_game(game, flag):
                        # 获取到子游戏id，并且已经进入游戏房间
                        self.open_autoPerson(game)
                        # 打开机器人操作
                        time.sleep(2)
                        try:
                            self.hall_page.wait_element("准备").click()
                            time.sleep(6)
                            self.hall_page.wait_element("东南西北")
                            self.hall_page.screenshot("%s_cartoonScreen.png" % game.get_attribute("name"))
                            # 截出刚开始发牌动画图
                            self.log_info("home键")
                            self.driver.keyevent(3)  # home
                            self.game_page.screenshot("%s_being.png" % game.get_attribute("name"))
                            time.sleep(1)
                            self.start_step("解锁")
                            self.common.unlock()
                            #重新拉起游戏配置
                            # if self.hall_page.element_is_exist("带他返回游戏大厅"):
                            #     self.log_info("返回键")
                            #     self.driver.keyevent(4) #返回键
                        except:
                            self.assert_equal(game.get_attribute("name")+"短时间锁屏操作失败",False,True)
                    # except:
                    #     self.assert_equal(game.get_attribute("name")+"麻将房间开局失败",False,True)
                    try:
                        self.exit_gameroom()
                        # 退出游戏
                        self.back_hall()
                        # 退出游戏大厅
                    except:
                        self.assert_equal(game.get_attribute("name") + "未返回到游戏大厅", False, True)
        self.test_case(reconnect)

    def post_test(self):
        CommonCase.post_test(self)

class C27217_GameOver_Surface(CommonCase):
    '''
    结算时断网重连
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        CommonCase.pre_test(self)

    def run_test(self):
        def reconnect(gameList, flag=False):
            # 对某一屏幕的子游戏遍历操作
            for game in gameList:
                if self.inter_game(game, flag):
                    # 获取到子游戏id，并且已经进入游戏房间
                    self.open_autoPerson(game)
                    # 打开机器人操作
                    time.sleep(2)
                    self.hall_page.wait_element("准备").click()
                    try:
                        while(self.hall_page.wait_element("你输了") != True):
                            time.sleep(5)
                        self.hall_page.screenshot("%s_结算界面" % game.get_attribute("name"))
                        #截出结算界面
                        self.hall_page.wait_element("测试").click()
                        self.hall_page.wait_element("重连").click()
                        if self.hall_page.element_is_exist("关闭对话框"):
                            self.hall_page.element_is_exist("关闭对话框").click()
                    except:
                        self.assert_equal(game.get_attribute("name")+"进入结算界面失败",False,True)
                try:
                    self.exit_gameroom()
                    # 退出游戏
                    self.back_hall()
                    # 退出游戏大厅
                except:
                    self.assert_equal(game.get_attribute("name") + "未返回到游戏大厅", False, True)
        self.test_case(reconnect)

    def post_test(self):
        CommonCase.post_test(self)

class C27217_GameOver_CloseProcess(CommonCase):
    '''
    结算时关闭进程重连
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        CommonCase.pre_test(self)

    def run_test(self):
        def reconnect(gameList, flag=False):
            # 对某一屏幕的子游戏遍历操作
            for game in gameList:
                if self.inter_game(game, flag):
                    # 获取到子游戏id，并且已经进入游戏房间
                    self.open_autoPerson(game)
                    # 打开机器人操作
                    time.sleep(2)
                    self.hall_page.wait_element("准备").click()
                    try:
                        while(self.hall_page.wait_element("你输了") != True):
                            time.sleep(5)
                        #等待进入结算界面
                        self.hall_page.screenshot("%s_结算界面" % game.get_attribute("name"))
                        #截出结算界面
                        try:
                            self.common.closedriver()
                            # 关闭进程
                            time.sleep(3)
                            self.start_step("初始化driver")
                            # 重新加载游戏
                            self.luadriver = self.common.setupdriver()
                            self.common.closeactivity(self.luadriver)
                            # 关闭活动界面
                            time.sleep(5)
                            self.hall_page.screenshot("%s_RightScreen.png" % game.get_attribute("name"))
                            self.inter_game(game, flag)
                            # 进入房间
                            time.sleep(4)
                            if self.hall_page.element_is_exist("关闭对话框"):
                                self.hall_page.element_is_exist("关闭对话框").click()
                            # 点击关闭按钮,退出结算界面
                        except:
                            self.assert_equal(game.get_attribute("name") + "关闭进程失败", False, True)
                    except:
                        self.assert_equal(game.get_attribute("name")+"进入结算界面失败",False,True)
                try:
                    self.exit_gameroom()
                    # 退出游戏
                    self.back_hall()
                    # 退出游戏大厅
                except:
                    self.assert_equal(game.get_attribute("name") + "未返回到游戏大厅", False, True)
        self.test_case(reconnect)

    def post_test(self):
        CommonCase.post_test(self)

class C27217_InterGame_NoNet(CommonCase):
    '''
    房间中玩牌时断开网络查看界面显示
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        CommonCase.pre_test(self)

    def run_test(self):
        def reconnect(gameList, flag=False):
            # 对某一屏幕的子游戏遍历操作
            for game in gameList:
                if self.inter_game(game, flag):
                    # 获取到子游戏id，并且已经进入游戏房间
                    self.open_autoPerson(game)
                    # 打开机器人操作
                    time.sleep(2)
                    self.hall_page.wait_element("准备").click()
                    try:
                        while(self.hall_page.wait_element("你输了") != True):
                            time.sleep(5)
                        #等待进入结算界面
                        self.hall_page.screenshot("%s_结算界面" % game.get_attribute("name"))
                        #截出结算界面
                        try:
                            self.common.closedriver()
                            # 关闭进程
                            time.sleep(3)
                            self.start_step("初始化driver")
                            # 重新加载游戏
                            self.luadriver = self.common.setupdriver()
                            self.common.closeactivity(self.luadriver)
                            # 关闭活动界面
                            time.sleep(5)
                            self.hall_page.screenshot("%s_RightScreen.png" % game.get_attribute("name"))
                            self.inter_game(game, flag)
                            # 进入房间
                            time.sleep(4)
                            if self.hall_page.element_is_exist("关闭对话框"):
                                self.hall_page.element_is_exist("关闭对话框").click()
                            # 点击关闭按钮,退出结算界面
                        except:
                            self.assert_equal(game.get_attribute("name") + "关闭进程失败", False, True)
                    except:
                        self.assert_equal(game.get_attribute("name")+"进入结算界面失败",False,True)
                try:
                    self.exit_gameroom()
                    # 退出游戏
                    self.back_hall()
                    # 退出游戏大厅
                except:
                    self.assert_equal(game.get_attribute("name") + "未返回到游戏大厅", False, True)
        self.test_case(reconnect)

    def post_test(self):
        CommonCase.post_test(self)

__qtaf_seq_tests__ = [C27215_PalyGame_ShortTime_Shift]
if __name__ == '__main__':
    debug_run_all()






