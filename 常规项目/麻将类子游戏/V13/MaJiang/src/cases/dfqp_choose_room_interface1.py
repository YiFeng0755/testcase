#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
选房间入场1
'''
import json
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from utils import constant
from utils.confighelper import ConfigHelper

from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common
from  uilib.game_page import Game_Page
from uilib.safebox_page import Safebox_Page
import test_datas
from datacenter import dataprovider
import common.Interface as PHPInterface

class C27360_ChooseRoom_ZeroMoneyEnter(TestCase):
    '''
    携带0银币且保险箱存款为0，点击游戏位进入选场界面
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()

        self.start_step("获取用户mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("设置银币数为0")
        self.common.set_coin(mid=mid, value="0")

        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange = False):
            game_list = self.game_page.get_game_list()
            for i in range(len(game_list)):
                # 大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()
                self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                time.sleep(2)
                game_list[i].click()
                if (self.game_page.element_is_exist("重新获取") == True):
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击重新获取")
                    self.game_page.wait_element("重新获取").click()
                else:
                    self.game_page.game_is_download()
                    print "进入子游戏%s选场界面" % game_list[i].get_attribute("name")
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    try:
                        time.sleep(3)
                        self.game_page.wait_element("返回1").click()
                    except:
                        print "选场界面获取返回键失败"
                        continue

        self.start_step("大厅第一页子游戏")
        traversal_gameList(self, False)
        time.sleep(2)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏")
        traversal_gameList(self, True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27373_ChooseRoom_NotEnoughEnter(TestCase):
    '''
    携带银币不足中级场下限，保险箱有钱，点击中级场，提示取钱，取钱后可入场
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()

        self.start_step("获取用户mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("设置银币数为1000000")
        self.common.set_coin(mid=mid, value="1000000")

        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        # 从保险箱取出银币
        def outFromSafebox(self):
            # self.start_step('进入保险箱页面')
            # self.hall_page.wait_element('保险箱').click()
            time.sleep(3)
            self.start_step("从保险箱取出银币")
            # self.safebox_page.wait_element("银币保险箱").click()
            # time.sleep(3)
            # self.safebox_page.wait_element("取出").click()
            time.sleep(3)
            try:
                self.safebox_page.wait_element("取出").click()
                time.sleep(3)
            except:
                print "无此按钮"
            self.start_step("拖动滑动条")
            self.common.swipeelement(self.safebox_page.wait_element("滚动条"),
                                     self.safebox_page.wait_element("增加金条/银条数目"))
            time.sleep(8)
            try:
                self.safebox_page.wait_element('确定---保险箱').click()
                time.sleep(5)
                self.safebox_page.screenshot('addSuccess.png')
            except:
                self.safebox_page.screenshot('addFail.png')
            self.start_step("点击屏幕任意一处关闭保险箱")
            self.hall_page.wait_element("头像").click()

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange = False):
            game_list = self.game_page.get_game_list()
            print len(game_list)
            for i in range(len(game_list)):
                # 大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()

                self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                time.sleep(2)
                game_list[i].click()
                if (self.game_page.element_is_exist("重新获取")):
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击重新获取")
                    self.game_page.wait_element("重新获取").click()
                    # continue

                else:
                    self.game_page.game_is_download()
                    time.sleep(3)
                    roomlevel = self.game_page.get_elements("房间场次")
                    if len(roomlevel) == 1:
                        print "该子游戏没有中级场"
                        continue

                    # 获取场次配置信息
                    self.start_step("获取游戏ID: %s场次配置信息" % game_list[i].get_attribute("name"))
                    # 获取到gameid
                    gameid_name = game_list[i].get_attribute("name")
                    gameid = int(gameid_name[4:len(gameid_name)])
                    #get_levelconfig(gameid, 0, 0, 13)，参数一表game id ,参数二表底注类型，0代表银币，参数三表玩法类型，0代表标准玩法，参数四表场次类型，13表中级场
                    gamecfg1 = PHPInterface.get_levelconfig(gameid, 0, 0, 13)
                    try:
                        low_limit1 = gamecfg1.get('values', {'LOW_LIMIT': None}).get('LOW_LIMIT')
                        print "游戏ID: %s 中级场下限是%d" % (game_list[i].get_attribute("name"), low_limit1)
                    except:
                        print "获取游戏ID: %s场次配置信息失败" % game_list[i].get_attribute("name")
                        self.game_page.wait_element("返回1").click()
                        continue

                    # 获取用户信息
                    result_userinfo = PHPInterface.get_user_info(mid)
                    myuser_info = json.loads(result_userinfo)
                    coin = myuser_info.get('result', {'coin': None}).get('coin')
                    # print "用户银币数为：%s" % coin

                    # 使保险箱有钱
                    if coin > 20000:
                        PHPInterface.deposit_safebox(mid, coin - 20000, 0)
                    else:
                        print "用户银币数未超过两万"

                    # 设置玩家携带银币数 < 中级场下限
                    # if (coin >= low_limit1):
                    self.common.set_coin(mid, low_limit1 - 1000)
                    self.common.switchserver()
                    self.common.closeactivity(self.luadriver)

                    #给玩家设置指定银币数目时进行了重新加载，回到了大厅，得重新点击游戏位
                    if (isChange and self.game_page.element_is_exist("右三角标")):
                        self.game_page.wait_element("右三角标").click()

                    self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                    time.sleep(2)
                    game_list[i].click()
                    self.game_page.game_is_download()
                    print "进入子游戏选场界面"
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    # roomlevel = self.game_page.get_elements("房间场次")
                    self.start_step("点击中级场")
                    time.sleep(2)
                    roomlevel[1].click()
                    time.sleep(3)
                    self.game_page.screenshot("middleroombefore_%s.png" % game_list[i].get_attribute("name"))

                    if(self.game_page.element_is_exist("取钱入场")):
                        self.start_step("点击取钱入场按钮")
                        self.game_page.wait_element("取钱入场").click()

                    elif(self.game_page.element_is_exist("打开保险箱")):
                        self.start_step("点击打开保险箱按钮")
                        self.game_page.wait_element("打开保险箱").click()
                        outFromSafebox(self)
                        self.start_step("保险箱取出银币后再次点击中级场")
                        roomlevel[1].click()
                    time.sleep(5)
                    self.game_page.screenshot("middleroomafter_%s.png" % game_list[i].get_attribute("name"))

                    self.start_step("退出房间")
                    # self.game_page.wait_element("房间内菜单").click()
                    # self.game_page.wait_element("退出").click()
                    # self.start_step("退出子游戏%s到大厅界面" % game_list[i].get_attribute("name"))
                    # self.game_page.wait_element("返回1").click()

                    # 若进入房间子游戏开局了，则等待游戏结束，物理键返回到选场界面
                    while (self.hall_page.element_is_exist("预发布") != True):
                        time.sleep(10)
                        self.luadriver.back()
                    time.sleep(3)
                    self.game_page.wait_element("返回1").click()

        self.start_step("大厅第一页子游戏")
        traversal_gameList(self, False)
        time.sleep(2)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏")
        traversal_gameList(self, True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.set_safeBoxMoney(mid, 0, 0)
        self.common.closedriver()

class C27374_ChooseRoom_NotEnoughEnter(TestCase):
    '''
    携带银币不足中级场下限，保险箱有钱，点击中级场，提示取钱可入场，关闭提示弹框
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()

        self.start_step("获取用户mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("设置银币数为1000000")
        self.common.set_coin(mid=mid, value="1000000")

        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange = False):
            game_list = self.game_page.get_game_list()
            for i in range(len(game_list)):
                # 大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()

                self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                time.sleep(2)
                game_list[i].click()
                if (self.game_page.element_is_exist("重新获取")):
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击重新获取")
                    self.game_page.wait_element("重新获取").click()

                else:
                    self.game_page.game_is_download()
                    roomlevel = self.game_page.get_elements("房间场次")
                    if len(roomlevel) == 1:
                        print "该子游戏没有中级场"
                        continue

                    # 获取场次配置信息
                    self.start_step("获取游戏ID: %s场次配置信息" % game_list[i].get_attribute("name"))
                    # 获取到gameid
                    gameid_name = game_list[i].get_attribute("name")
                    gameid = int(gameid_name[4:len(gameid_name)])
                    gamecfg1 = PHPInterface.get_levelconfig(gameid, 0, 0, 13)
                    try:
                        low_limit1 = gamecfg1.get('values', {'LOW_LIMIT': None}).get('LOW_LIMIT')
                        print "游戏ID: %s 中级场下限是%d" % (game_list[i].get_attribute("name"), low_limit1)
                    except:
                        print "获取游戏ID: %s场次配置信息失败" % game_list[i].get_attribute("name")
                        continue

                    # 获取用户信息
                    result_userinfo = PHPInterface.get_user_info(mid)
                    myuser_info = json.loads(result_userinfo)
                    coin = myuser_info.get('result', {'coin': None}).get('coin')
                    # print "用户银币数为：%s" % coin

                    #银币存入保险箱
                    if coin > 20000:
                        PHPInterface.deposit_safebox(mid, coin - 20000, 0)
                    else:
                        print "用户银币数未超过两万"

                    # 设置玩家携带银币数 < 中级场下限
                    # if (coin >= low_limit1):
                    self.common.set_coin(mid, low_limit1 - 1000)
                    self.common.switchserver()
                    self.common.closeactivity(self.luadriver)

                    # 给玩家设置指定银币数目时进行了重新加载，回到了大厅，得重新点击游戏位
                    if (isChange and self.game_page.element_is_exist("右三角标")):
                        self.game_page.wait_element("右三角标").click()

                    self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                    time.sleep(2)
                    game_list[i].click()
                    self.game_page.game_is_download()

                    print "进入子游戏选场界面"
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击中级场")
                    roomlevel[1].click()
                    self.game_page.screenshot("middleroom.png")
                    if (self.game_page.element_is_exist("关闭从保险箱取钱弹框")):
                        self.start_step("点击X关闭从保险箱取钱提示弹框")
                        self.game_page.wait_element("关闭从保险箱取钱弹框").click()

                    elif (self.game_page.element_is_exist("关闭取钱入场弹框")):
                        self.start_step("点击X关闭取钱入场提示弹框")
                        self.game_page.wait_element("关闭取钱入场弹框").click()

                    #将银币取出，避免退出到大厅时弹出破产提示框覆盖大厅游戏位
                    time.sleep(3)
                    money_dict = PHPInterface.get_safebox(mid)
                    if money_dict["safebox"] != 0:
                         PHPInterface.withdraw_safebox(mid, money_dict["safebox"], 0)

                    self.start_step("从子游戏选场界面退出到大厅")
                    try:
                        self.game_page.wait_element("返回1").click()
                    except:
                        # self.log_info("退出子游戏到大厅界面")
                        print "选场界面获取返回键失败"
                        continue

        self.start_step("大厅第一页子游戏")
        traversal_gameList(self, False)
        time.sleep(2)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏")
        traversal_gameList(self, True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.set_safeBoxMoney(mid, 0, 0)
        self.common.closedriver()

class C27375_ChooseRoom_NotEnoughEnter(TestCase):
    '''
    携带银币小于入场下限但未破产，保险箱没钱，点击入场，弹出商城购买提示
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()

        self.start_step("获取用户mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        # 将保险箱银币全部取出，使保险箱银币数为0
        self.start_step("将保险箱银币数设置为0")
        money_dict = PHPInterface.get_safebox(mid)
        if money_dict["safebox"] != 0:
            PHPInterface.withdraw_safebox(mid, money_dict["safebox"], 0)

        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange = False):
            game_list = self.game_page.get_game_list()
            for i  in range(len(game_list)):
                # 大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()

                self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                time.sleep(2)
                game_list[i].click()
                if (self.game_page.element_is_exist("重新获取")):
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击重新获取")
                    self.game_page.wait_element("重新获取").click()

                else:
                    self.game_page.game_is_download()

                    # 获取场次配置信息
                    self.start_step("获取游戏ID: %s中级场场次配置信息" % game_list[i].get_attribute("name"))
                    # 获取到gameid
                    gameid_name = game_list[i].get_attribute("name")
                    gameid = int(gameid_name[4:len(gameid_name)])
                    gamecfg0 = PHPInterface.get_levelconfig(gameid, 0, 0, 12)
                    gamecfg1 = PHPInterface.get_levelconfig(gameid, 0, 0, 13)
                    try:
                        low_limit0 = gamecfg0.get('values', {'LOW_LIMIT': None}).get('LOW_LIMIT')
                        print "游戏ID: %s 初级场下限是%d" % (game_list[i].get_attribute("name"), low_limit0)
                        low_limit1 = gamecfg1.get('values', {'LOW_LIMIT': None}).get('LOW_LIMIT')
                        print "游戏ID: %s 中级场下限是%d" % (game_list[i].get_attribute("name"), low_limit1)
                        backrupt_limit = gamecfg0.get('values', {'BANKRUPT_LIMIT': None}).get('BANKRUPT_LIMIT')
                        print "游戏ID: %s 的破产金额是%d" % (game_list[i].get_attribute("name"), backrupt_limit)
                    except:
                        print "获取游戏ID: %s场次配置信息失败" % game_list[i].get_attribute("name")
                        continue

                    # #获取玩家携带银币数
                    # result_userinfo = PHPInterface.get_user_info(mid)
                    # myuser_info = json.loads(result_userinfo)
                    # coin = myuser_info.get('result', {'coin': None}).get('coin')
                    # print "用户银币数为：%s" % coin

                    #如果初级场下限 == 子游戏破产金，则后续不遍历初级场， 设置玩家携带银币　< 中级场下限
                    # if (low_limit0 == backrupt_limit):
                    if (low_limit0 == backrupt_limit and low_limit1 > backrupt_limit):
                        self.common.set_coin(mid, low_limit1 - 1)
                        self.common.switchserver()
                        self.common.closeactivity(self.luadriver)
                    # 如果初级场下限 > 子游戏破产金，初级场也需遍历， 设置玩家携带银币　< 初级级场下限
                    elif (low_limit0 > backrupt_limit):
                        self.common.set_coin(mid, low_limit0 - 1)
                        self.common.switchserver()
                        self.common.closeactivity(self.luadriver)
                    #处理麻将通用框架的初级、中级、破产都为3000的问题
                    elif (low_limit0 == backrupt_limit and low_limit1 == backrupt_limit):
                        print "游戏配置问题，该子游戏的初级场、中级场、破产金三者值相同"
                        self.game_page.wait_element("返回1").click()
                        continue

                    # 给玩家设置指定银币数目后进行了重新加载，回到了大厅，得重新点击游戏位
                    if (isChange and self.game_page.element_is_exist("右三角标")):
                        self.game_page.wait_element("右三角标").click()

                    self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                    time.sleep(2)
                    game_list[i].click()
                    self.game_page.game_is_download()

                    print "进入游戏ID: %s选场界面" % game_list[i].get_attribute("name")
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))

                    # 选场界面点击快速开始入场
                    self.start_step("点击快速开始按钮")
                    self.game_page.wait_element("快速开始").click()
                    self.game_page.screenshot(".png")
                    time.sleep(2)
                    self.start_step("退出游戏ID：%s房间 到选场界面" % game_list[i].get_attribute("name"))
                    # self.game_page.wait_element("房间内菜单").click()
                    # self.game_page.wait_element("退出").click()
                    while (self.hall_page.element_is_exist("预发布") != True):
                        self.luadriver.back()
                        time.sleep(10)

                    #遍历符合要求的房间（未破产且玩家携带银币 < 房间下限）
                    roomlevel = self.game_page.get_elements("房间场次")
                    self.start_step("点击游戏ID: %s 符合要求的各个场次" % game_list[i].get_attribute("name"))

                    #初级场下限 == 破产线 ，则不遍历初级场
                    if (low_limit0 == backrupt_limit):
                        if len(roomlevel) == 1:
                            print "没有符合要求的场次"
                        else:
                            for j in range(1, len(roomlevel)):
                                self.start_step("点击游戏ID: %s 场次%d" % (game_list[i].get_attribute("name"), j))
                                if (j >= 4):
                                    self.common.swipeelement(roomlevel[3], roomlevel[1])
                                time.sleep(2)
                                roomlevel[j].click()
                                time.sleep(3)
                                self.game_page.screenshot("middleroom_%s.png" % game_list[i].get_attribute("name"))

                                try:
                                    self.start_step("关闭商城页面")
                                    self.game_page.wait_element("关闭商城页面").click()
                                except:
                                    print "进入该场次房间失败"

                        self.start_step("退出子游戏%s到大厅界面" % game_list[i].get_attribute("name"))
                        try:
                            time.sleep(2)
                            self.game_page.wait_element("返回1").click()
                        except:
                            print "选场界面获取返回键失败"
                            continue

                    # 初级场下限 > 破产线 ，则遍历初级场
                    elif (low_limit0 > backrupt_limit):
                        for j in range(len(roomlevel)):
                            self.start_step("点击游戏ID: %s 场次%d" % (game_list[i].get_attribute("name"), j))
                            if (j >= 4):
                                self.common.swipeelement(roomlevel[3], roomlevel[1])
                            time.sleep(2)
                            roomlevel[j].click()
                            time.sleep(3)
                            self.game_page.screenshot("middleroom_%s.png" % game_list[i].get_attribute("name"))
                            try:
                                self.start_step("关闭商城页面")
                                self.game_page.wait_element("关闭商城页面").click()
                            except:
                                print "进入该场次房间失败"

                        self.start_step("退出子游戏%s到大厅界面" % game_list[i].get_attribute("name"))
                        try:
                            time.sleep(2)
                            self.game_page.wait_element("返回1").click()
                        except:
                            print "选场界面获取返回键失败"
                            continue

        self.start_step("大厅第一页子游戏")
        traversal_gameList(self, False)
        time.sleep(2)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏")
        traversal_gameList(self, True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27376_ChooseRoom_NotEnoughEnter(TestCase):
    '''
    破产线<携带银币<中级入场下限，点击进入各个场次
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()

        self.start_step("获取用户mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("设置银币数为10000")
        self.common.set_coin(mid=mid, value="10000")

        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange = False):
            game_list = self.game_page.get_game_list()
            for i in range(len(game_list)):
                # 大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()

                self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                time.sleep(2)
                game_list[i].click()
                if (self.game_page.element_is_exist("重新获取")):
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击重新获取")
                    self.game_page.wait_element("重新获取").click()
                else:
                    self.game_page.game_is_download()
                    # 获取场次配置信息
                    self.start_step("获取游戏ID: %s中级场场次配置信息" % game_list[i].get_attribute("name"))
                    # 获取到gameid
                    gameid_name = game_list[i].get_attribute("name")
                    gameid = int(gameid_name[4:len(gameid_name)])
                    gamecfg1 = PHPInterface.get_levelconfig(gameid, 0, 0, 13)
                    try:
                        low_limit1 = gamecfg1.get('values', {'LOW_LIMIT': None}).get('LOW_LIMIT')
                        print "游戏ID: %s 中级场下限是%d" % (game_list[i].get_attribute("name"), low_limit1)
                        backrupt_limit = gamecfg1.get('values', {'BANKRUPT_LIMIT': None}).get('BANKRUPT_LIMIT')
                        print "游戏ID: %s 的破产金额是%d" % (game_list[i].get_attribute("name"), backrupt_limit)
                    except:
                        print "获取游戏ID: %s场次配置信息失败" % game_list[i].get_attribute("name")
                        continue

                    # 获取玩家携带银币数
                    # money_dict = PHPInterface.get_safebox(mid)
                    result_userinfo = PHPInterface.get_user_info(mid)
                    myuser_info = json.loads(result_userinfo)
                    coin = myuser_info.get('result', {'coin': None}).get('coin')
                    # print "用户银币数为：%s" % coin

                   #设置玩家携带银币数为：破产线 < 玩家携带　< 中级场下限
                    if (low_limit1 == backrupt_limit):
                        print "该子游戏中级场下限等于破产金额"
                        self.game_page.wait_element("返回1").click()
                        continue
                    elif (coin >= low_limit1):
                        self.common.set_coin(mid, low_limit1 - 1)
                        self.common.switchserver()
                        self.common.closeactivity(self.luadriver)

                    # 给玩家设置指定银币数目后进行了重新加载，回到了大厅，得重新点击游戏位
                    if (isChange and self.game_page.element_is_exist("右三角标")):
                        self.game_page.wait_element("右三角标").click()

                    self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                    time.sleep(2)
                    game_list[i].click()
                    self.game_page.game_is_download()

                    print "进入游戏ID: %s选场界面" % game_list[i].get_attribute("name")
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))

                    # 选场界面点击快速开始入场
                    # self.start_step("点击快速开始按钮")
                    # self.game_page.wait_element("快速开始").click()
                    # self.game_page.screenshot(".png")
                    # time.sleep(2)
                    # try:
                    #     self.start_step("退出游戏ID：%s房间 到选场界面" % game_list[i].get_attribute("name"))
                    #     self.game_page.wait_element("房间内菜单").click()
                    #     self.game_page.wait_element("退出").click()
                    # except:
                    #     print "未进入房间"

                    roomlevel = self.game_page.get_elements("房间场次")
                    # print len(roomlevel)
                    self.start_step("点击游戏ID: %s 的各个场次" % game_list[i].get_attribute("name"))

                    for j in range(len(roomlevel)):
                        self.start_step("点击游戏ID: %s 场次%d" % (game_list[i].get_attribute("name"), j))
                        if (j >= 4):
                            self.common.swipeelement(roomlevel[3], roomlevel[1])
                        time.sleep(2)
                        roomlevel[j].click()
                        # print roomlevel[j].location['x'], roomlevel[j].location['y']
                        time.sleep(3)
                        self.game_page.screenshot("middleroombefore_%s.png" % game_list[i].get_attribute("name"))

                        # 进入房间后的各种情况处理
                        # 玩家携带银币足够进入该场次游戏房间
                        if (self.game_page.element_is_exist("房间内菜单")):
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()

                        # 携带银币不足场次下限，保险箱没钱，进入房间会弹出商城购买页面
                        elif (self.game_page.element_is_exist("关闭商城页面")):
                            print "玩家携带银币不足场次下限，保险箱没钱, 商城购买后可入场"
                            self.start_step("关闭商城页面")
                            self.game_page.wait_element("关闭商城页面").click()

                        # 携带银币不足场次下限，保险箱有钱，进入房间会提示取钱，取钱后进入该场次房间
                        elif (self.game_page.element_is_exist("取钱入场")):
                            print "玩家携带银币不足场次下限，保险箱有钱, 取钱后可入场"
                            self.start_step("取钱入场")
                            self.game_page.wait_element("取钱入场").click()
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()

                        else:
                            print "进入该场次房间失败"

                    self.start_step("退出子游戏%s到大厅界面" % game_list[i].get_attribute("name"))
                    while (self.hall_page.element_is_exist("预发布") != True):
                        time.sleep(10)
                        self.luadriver.back()

                    self.game_page.wait_element("返回1").click()

        self.start_step("大厅第一页子游戏")
        traversal_gameList(self, False)
        time.sleep(2)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏")
        traversal_gameList(self, True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27377_ChooseRoom_NotEnoughEnter(TestCase):
    '''
    初级场上限　> 携带银币 > 中级场下限 ，点击进入各个场次
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

        global mid
        mid = self.common.get_config_value("casecfg", "mid")

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange = False):
            game_list = self.game_page.get_game_list()
            # game_list = []
            # game_list.append(self.luadriver.find_lua_element_by_name("game203"))
            for i in range(len(game_list)):
                # 大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()

                self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                time.sleep(2)
                game_list[i].click()
                if (self.game_page.element_is_exist("重新获取")):
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击重新获取")
                    self.game_page.wait_element("重新获取").click()
                else:
                    self.game_page.game_is_download()
                    #获取场次配置信息
                    self.start_step("获取游戏ID: %s场次配置信息" % game_list[i].get_attribute("name"))
                    # 获取到gameid
                    gameid_name = game_list[i].get_attribute("name")
                    gameid = int(gameid_name[4:len(gameid_name)])

                    gamecfg0 = PHPInterface.get_levelconfig(gameid, 0, 0, 12)
                    gamecfg1 = PHPInterface.get_levelconfig(gameid, 0, 0, 13)
                    try:
                        high_limit0 = gamecfg0.get('values', {'HIGH_LIMIT': None}).get('HIGH_LIMIT')
                        print "游戏ID: %s 初级场上限是%d" % (game_list[i].get_attribute("name"), high_limit0)
                        low_limit1 = gamecfg1.get('values', {'LOW_LIMIT': None}).get('LOW_LIMIT')
                        print "游戏ID: %s 中级场下限是%d" % (game_list[i].get_attribute("name"), low_limit1)
                    except:
                        print "获取游戏ID: %s场次配置信息失败" % game_list[i].get_attribute("name")
                        continue

                    #高级场下限小于等于初级场上限
                    if (high_limit0 != -1 and high_limit0 <= low_limit1):
                        self.game_page.wait_element("返回1").click()
                        continue

                    # 获取用户银币数
                    result_userinfo = PHPInterface.get_user_info(mid)
                    myuser_info = json.loads(result_userinfo)
                    coin = myuser_info.get('result', {'coin': None}).get('coin')
                    print "用户银币数为：%s" % coin

                    # 将用户银币数设置为：初级场上限　> 携带银币 > 中级场下限
                    self.common.set_coin(mid, low_limit1 + 1)
                    self.common.switchserver()
                    self.common.closeactivity(self.luadriver)

                    # 给玩家设置指定银币数目后进行了重新加载，回到了大厅，得重新点击游戏位
                    if (isChange and self.game_page.element_is_exist("右三角标")):
                        self.game_page.wait_element("右三角标").click()

                    self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                    time.sleep(2)
                    game_list[i].click()
                    self.game_page.game_is_download()

                    print "进入子游戏选场界面"
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    roomlevel = self.game_page.get_elements("房间场次")
                    for j in range(len(roomlevel)):
                        self.start_step("点击游戏ID: %s 场次%d" % (game_list[i].get_attribute("name"), j))
                        if (j >= 4):
                            self.common.swipeelement(roomlevel[3], roomlevel[1])
                        time.sleep(2)
                        roomlevel[j].click()
                        self.game_page.screenshot("middleroom_%s.png" % game_list[i].get_attribute("name"))
                        # print roomlevel[j].location['x'], roomlevel[j].location['y'], roomlevel[j].size['width'], roomlevel[j].size['height']

                        # 进入房间后的各种情况处理
                        # 玩家携带银币可以直接进入该场次游戏房间
                        if (self.game_page.element_is_exist("房间内菜单")):
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()

                        #玩家携带银币太多，高过场次上限，存钱后入场
                        elif (self.game_page.element_is_exist("存钱入场")):
                            print "玩家携带银币太多，高过场次上限，存钱后可入场"
                            self.start_step("存钱入场")
                            self.game_page.wait_element("存钱入场").click()
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()

                        # 携带银币不足场次下限，保险箱有钱，进入房间会提示取钱，取钱后进入该场次房间
                        elif (self.game_page.element_is_exist("取钱入场")):
                            print "玩家携带银币不足场次下限，保险箱有钱, 取钱后可入场"
                            self.start_step("取钱入场")
                            self.game_page.wait_element("取钱入场").click()
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()

                        # 携带银币不足场次下限，保险箱没钱，进入房间会弹出商城购买页面
                        elif (self.game_page.element_is_exist("关闭商城页面")):
                            print "玩家携带银币不足场次下限"
                            self.start_step("关闭商城页面")
                            self.game_page.wait_element("关闭商城页面").click()

                        else:
                            print "未找到该场次元素"

                        # self.start_step("退出房间")
                        # self.yuepai_page.is_exist_yuepairoom()
                        # self.common.closeActivityBtn()
                        # if self.hall_page.element_is_exist("返回1") == True:
                        #     self.hall_page.wait_element("返回1").click()
                    self.start_step("退出子游戏%s到大厅界面" % game_list[i].get_attribute("name"))
                    while (self.hall_page.element_is_exist("预发布") != True):
                        time.sleep(10)
                        self.luadriver.back()

                    self.game_page.wait_element("返回1").click()

        self.start_step("大厅第一页子游戏")
        traversal_gameList(self, False)
        time.sleep(2)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏")
        traversal_gameList(self, True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27378_ChooseRoom_NotEnoughEnter(TestCase):
    '''
    携带银币  = 初级场上限，点击进入各个场次
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

        global mid
        mid = self.common.get_config_value("casecfg", "mid")

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange = False):
            game_list = self.game_page.get_game_list()
            for i in range(len(game_list)):
                # 大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()

                self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                time.sleep(2)
                game_list[i].click()
                if (self.game_page.element_is_exist("重新获取")):
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击重新获取")
                    self.game_page.wait_element("重新获取").click()
                else:
                    self.game_page.game_is_download()
                    #获取场次配置信息
                    self.start_step("获取游戏ID: %s场次配置信息" % game_list[i].get_attribute("name"))
                    # 获取到gameid
                    gameid_name = game_list[i].get_attribute("name")
                    gameid = int(gameid_name[4:len(gameid_name)])
                    gamecfg0 = PHPInterface.get_levelconfig(gameid, 0, 0, 12)
                    try:
                        high_limit0 = gamecfg0.get('values', {'HIGH_LIMIT': None}).get('HIGH_LIMIT')
                        print "游戏ID: %s 初级场场次上限是%d" % (game_list[i].get_attribute("name"), high_limit0)
                    except:
                        print "获取游戏ID: %s场次配置信息失败" % game_list[i].get_attribute("name")
                        continue

                    # # 获取玩家信息
                    # result_userinfo = PHPInterface.get_user_info(mid)
                    # myuser_info = json.loads(result_userinfo)
                    # coin = myuser_info.get('result', {'coin': None}).get('coin')
                    # print "用户银币数为：%s" % coin

                    # 设置玩家携带银币数 == 初级场上限
                    # 如果子游戏初级场上限是-1 ，表无上限，则设置玩家携带银币数为500万
                    if (high_limit0 == -1):
                        self.common.set_coin(mid, 5000000)
                        self.common.switchserver()
                        self.common.closeactivity(self.luadriver)
                    # elif (coin != high_limit0):
                    else:
                        self.common.set_coin(mid, high_limit0)
                        self.common.switchserver()
                        self.common.closeactivity(self.luadriver)

                    # 给玩家设置指定银币数目后进行了重新加载，回到了大厅，得重新点击游戏位
                    if (isChange and self.game_page.element_is_exist("右三角标")):
                        self.game_page.wait_element("右三角标").click()

                    self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                    time.sleep(2)
                    game_list[i].click()
                    self.game_page.game_is_download()

                    print "进入子游戏选场界面"
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    roomlevel = self.game_page.get_elements("房间场次")
                    for j in range(len(roomlevel)):
                        self.start_step("点击游戏ID: %s 场次%d" % (game_list[i].get_attribute("name"), j))
                        time.sleep(3)
                        roomlevel[j].click()
                        self.game_page.screenshot("middleroom.png")
                        # print roomlevel[j].location('x'), roomlevel[j].location('x'), roomlevel[j].size('width'), roomlevel[j].size('height')

                        #进入房间后的各种情况处理
                        # 玩家携带银币足够进入该场次游戏房间
                        if (self.game_page.element_is_exist("房间内菜单")):
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()

                        # 携带银币不足场次下限，保险箱没钱，进入房间会弹出商城购买页面
                        if (self.game_page.element_is_exist("关闭商城页面")):
                            print "玩家携带银币不足场次下限，保险箱没钱, 商城购买后可入场"
                            self.start_step("关闭商城页面")
                            self.game_page.wait_element("关闭商城页面").click()
                            # self.game_page.screenshot("middleroom2.png")

                        # 携带银币不足场次下限，保险箱有钱，进入房间会提示取钱，取钱后进入该场次房间
                        elif (self.game_page.element_is_exist("取钱入场")):
                            print "玩家携带银币不足场次下限，保险箱有钱, 取钱后可入场"
                            self.start_step("取钱入场")
                            self.game_page.wait_element("取钱入场").click()
                            # self.game_page.screenshot("middleroom2.png")
                            # self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()
                        else:
                            print "进入该场次房间失败"

                    self.start_step("退出子游戏%s到大厅界面" % game_list[i].get_attribute("name"))
                    while (self.hall_page.element_is_exist("预发布") != True):
                        self.luadriver.back()
                        time.sleep(10)
                    self.game_page.wait_element("返回1").click()


        self.start_step("大厅第一页子游戏")
        traversal_gameList(self, False)
        time.sleep(2)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏")
        traversal_gameList(self, True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27379_ChooseRoom_NotEnoughEnter(TestCase):
    '''
    初级场上限　< 携带银币 < 高级场下限 ，点击进入各个场次
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

        global mid
        mid = self.common.get_config_value("casecfg", "mid")

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange = False):
            game_list = self.game_page.get_game_list()
            # game_list = []
            # game_list.append(self.luadriver.find_lua_element_by_name("game203"))
            for i in range(len(game_list)):
                # 大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()

                self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                time.sleep(3)
                game_list[i].click()
                if (self.game_page.element_is_exist("重新获取")):
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击重新获取")
                    self.game_page.wait_element("重新获取").click()
                else:
                    self.game_page.game_is_download()
                    #获取场次配置信息
                    self.start_step("获取游戏ID: %s场次配置信息" % game_list[i].get_attribute("name"))
                    # 获取到gameid
                    gameid_name = game_list[i].get_attribute("name")
                    gameid = int(gameid_name[4:len(gameid_name)])

                    gamecfg0 = PHPInterface.get_levelconfig(gameid, 0, 0, 12)
                    gamecfg2 = PHPInterface.get_levelconfig(gameid, 0, 0, 14)
                    try:
                        high_limit0 = gamecfg0.get('values', {'HIGH_LIMIT': None}).get('HIGH_LIMIT')
                        print "游戏ID: %s 初级场上限是%d" % (game_list[i].get_attribute("name"), high_limit0)
                        low_limit2 = gamecfg2.get('values', {'LOW_LIMIT': None}).get('LOW_LIMIT')
                        print "游戏ID: %s 高级场下限是%d" % (game_list[i].get_attribute("name"), low_limit2)
                    except:
                        print "获取游戏ID: %s场次配置信息失败" % game_list[i].get_attribute("name")
                        self.game_page.wait_element("返回1").click()
                        continue

                    # 获取用户银币数
                    # result_userinfo = PHPInterface.get_user_info(mid)
                    # myuser_info = json.loads(result_userinfo)
                    # coin = myuser_info.get('result', {'coin': None}).get('coin')
                    # print "用户银币数为：%s" % coin

                    # if high_limit0 == -1:

                    # 将用户银币数设置为： 初级场上限　< 携带银币 < 高级场下限
                    self.common.set_coin(mid, low_limit2 - 1)
                    self.common.switchserver()
                    self.common.closeactivity(self.luadriver)

                    # 给玩家设置指定银币数目后进行了重新加载，回到了大厅，得重新点击游戏位
                    if (isChange and self.game_page.element_is_exist("右三角标")):
                        self.game_page.wait_element("右三角标").click()
                    self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                    time.sleep(3)
                    game_list[i].click()
                    self.game_page.game_is_download()

                    print "进入子游戏选场界面"
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    roomlevel = self.game_page.get_elements("房间场次")
                    for j in range(len(roomlevel)):
                        self.start_step("点击游戏ID: %s 场次%d" % (game_list[i].get_attribute("name"), j))
                        if (j >= 4):
                            self.common.swipeelement(roomlevel[3], roomlevel[1])
                        time.sleep(3)
                        roomlevel[j].click()
                        self.game_page.screenshot("middleroom_%s.png" % game_list[i].get_attribute("name"))
                        # print roomlevel[j].location['x'], roomlevel[j].location['y'], roomlevel[j].size['width'], roomlevel[j].size['height']

                        # 进入房间后的各种情况处理
                        #玩家携带银币太多，高过场次上限，存钱后入场
                        if (self.game_page.element_is_exist("存钱入场")):
                            print "玩家携带银币太多，高过场次上限，存钱后可入场"
                            self.start_step("存钱入场")
                            self.game_page.wait_element("存钱入场").click()
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()

                        # 携带银币不足场次下限，保险箱有钱，进入房间会提示取钱，关闭提示取钱弹框
                        elif (self.game_page.element_is_exist("取钱入场")):
                            print "玩家携带银币不足场次下限，保险箱有钱, 取钱后可入场"
                            self.start_step("关闭取钱入场提示弹框")
                            self.game_page.wait_element("关闭取钱入场弹框").click()

                        # 携带银币不足场次下限，保险箱没钱，进入房间会弹出商城购买页面
                        elif (self.game_page.element_is_exist("关闭商城页面")):
                            print "玩家携带银币不足场次下限"
                            self.start_step("关闭商城页面")
                            self.game_page.wait_element("关闭商城页面").click()

                        # 玩家携带银币可以直接进入该场次游戏房间
                        elif (self.game_page.element_is_exist("房间内菜单")):
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()
                        else:
                            print "未找到该场次元素"

                    self.start_step("退出子游戏%s到大厅界面" % game_list[i].get_attribute("name"))
                    while (self.hall_page.element_is_exist("预发布") != True):
                        time.sleep(10)
                        self.luadriver.back()

                    self.game_page.wait_element("返回1").click()

        self.start_step("大厅第一页子游戏")
        traversal_gameList(self, False)
        time.sleep(2)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏")
        traversal_gameList(self, True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27380_ChooseRoom_NotEnoughEnter(TestCase):
    '''
    中级场上限 > 携带银币 > 高级场下限，点击进入各个场次
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

        global mid
        mid = self.common.get_config_value("casecfg", "mid")

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange = False):
            game_list = self.game_page.get_game_list()
            for i in range(len(game_list)):
                # 大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()

                self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                time.sleep(2)
                game_list[i].click()
                if (self.game_page.element_is_exist("重新获取")):
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击重新获取")
                    self.game_page.wait_element("重新获取").click()
                else:
                    self.game_page.game_is_download()
                    #获取场次配置信息
                    self.start_step("获取游戏ID: %s场次配置信息" % game_list[i].get_attribute("name"))
                    # 获取到gameid
                    gameid_name = game_list[i].get_attribute("name")
                    gameid = int(gameid_name[4:len(gameid_name)])

                    gamecfg1 = PHPInterface.get_levelconfig(gameid, 0, 0, 13)
                    gamecfg2 = PHPInterface.get_levelconfig(gameid, 0, 0, 14)
                    try:
                        high_limit1 = gamecfg1.get('values', {'HIGH_LIMIT': None}).get('HIGH_LIMIT')
                        print "游戏ID: %s 中级场上限是%d" % (game_list[i].get_attribute("name"), high_limit1)
                        low_limit2 = gamecfg2.get('values', {'LOW_LIMIT': None}).get('LOW_LIMIT')
                        print "游戏ID: %s 高级场下限是%d" % (game_list[i].get_attribute("name"), low_limit2)
                    except:
                        print "获取游戏ID: %s场次配置信息失败" % game_list[i].get_attribute("name")
                        self.game_page.wait_element("返回1").click()
                        continue

                    # # 获取用户银币数
                    # result_userinfo = PHPInterface.get_user_info(mid)
                    # myuser_info = json.loads(result_userinfo)
                    # coin = myuser_info.get('result', {'coin': None}).get('coin')
                    # print "用户银币数为：%s" % coin

                    # 将用户银币数设置为: 中级场上限 > 携带银币 > 高级场下限
                    self.common.set_coin(mid, low_limit2 + 1000)
                    self.common.switchserver()
                    self.common.closeactivity(self.luadriver)

                    # 给玩家设置指定银币数目后进行了重新加载，回到了大厅，得重新点击游戏位
                    if (isChange and self.game_page.element_is_exist("右三角标")):
                        self.game_page.wait_element("右三角标").click()
                    self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                    time.sleep(2)
                    game_list[i].click()
                    self.game_page.game_is_download()

                    print "进入子游戏选场界面"
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    roomlevel = self.game_page.get_elements("房间场次")
                    for j in range(len(roomlevel)):
                        self.start_step("点击游戏ID: %s 场次%d" % (game_list[i].get_attribute("name"), j))
                        if (j >= 4):
                            self.common.swipeelement(roomlevel[3], roomlevel[1])
                        time.sleep(2)
                        roomlevel[j].click()
                        self.game_page.screenshot("middleroom_%s.png" % game_list[i].get_attribute("name"))
                        # print roomlevel[j].location['x'], roomlevel[j].location['y'], roomlevel[j].size['width'], roomlevel[j].size['height']

                        # 进入房间后的各种情况处理
                        #玩家携带银币太多，高过场次上限，存钱后入场
                        if (self.game_page.element_is_exist("存钱入场")):
                            print "玩家携带银币太多，高过场次上限，存钱后可入场"
                            self.start_step("存钱入场")
                            self.game_page.wait_element("存钱入场").click()
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()

                        # 携带银币不足场次下限，保险箱有钱，进入房间会提示取钱，取钱后进入该场次房间
                        elif (self.game_page.element_is_exist("取钱入场")):
                            print "玩家携带银币不足场次下限，保险箱有钱, 取钱后可入场"
                            self.start_step("取钱入场")
                            self.game_page.wait_element("取钱入场").click()
                            # self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()

                        # 携带银币不足场次下限，保险箱没钱，进入房间会弹出商城购买页面
                        elif (self.game_page.element_is_exist("关闭商城页面")):
                            print "玩家携带银币不足场次下限"
                            self.start_step("关闭商城页面")
                            self.game_page.wait_element("关闭商城页面").click()

                        # 玩家携带银币可以直接进入该场次游戏房间
                        elif (self.game_page.element_is_exist("房间内菜单")):
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()
                        else:
                            print "未找到该场次元素"

                    self.start_step("退出子游戏%s到大厅界面" % game_list[i].get_attribute("name"))
                    while (self.hall_page.element_is_exist("预发布") != True):
                        time.sleep(10)
                        self.luadriver.back()
                    self.game_page.wait_element("返回1").click()

        self.start_step("大厅第一页子游戏")
        traversal_gameList(self, False)
        time.sleep(2)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏")
        traversal_gameList(self, True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27381_ChooseRoom_NotEnoughEnter(TestCase):
    '''
    携带银币  = 中级场上限，点击进入各个场次
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.safebox_page = Safebox_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

        global mid
        mid = self.common.get_config_value("casecfg", "mid")

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange = False):
            game_list = self.game_page.get_game_list()
            # game_list = []
            # game_list.append(self.luadriver.find_lua_element_by_name("game203"))
            for i in range(len(game_list)):
                # 大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()

                self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                time.sleep(2)
                game_list[i].click()
                if (self.game_page.element_is_exist("重新获取")):
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击重新获取")
                    self.game_page.wait_element("重新获取").click()
                else:
                    self.game_page.game_is_download()
                    #获取场次配置信息
                    self.start_step("获取游戏ID: %s场次配置信息" % game_list[i].get_attribute("name"))
                    # 获取到gameid
                    gameid_name = game_list[i].get_attribute("name")
                    gameid = int(gameid_name[4:len(gameid_name)])

                    gamecfg1 = PHPInterface.get_levelconfig(gameid, 0, 0, 13)
                    try:
                        high_limit1 = gamecfg1.get('values', {'HIGH_LIMIT': None}).get('HIGH_LIMIT')
                        print "游戏ID: %s 中级场上限是%d" % (game_list[i].get_attribute("name"), high_limit1)
                    except:
                        print "获取游戏ID: %s场次配置信息失败" % game_list[i].get_attribute("name")
                        self.game_page.wait_element("返回1").click()
                        continue

                    # 获取用户信息
                    result_userinfo = PHPInterface.get_user_info(mid)
                    myuser_info = json.loads(result_userinfo)
                    coin = myuser_info.get('result', {'coin': None}).get('coin')
                    # print "用户银币数为：%s" % coin

                    # 设置玩家携带银币数 = 中级场上限
                    #如果中级场上限为-1，表无上限，将玩家携带银币数是设为500万
                    if (high_limit1 == -1):
                        self.common.set_coin(mid, "5000000")
                        self.common.switchserver()
                        self.common.closeactivity(self.luadriver)

                    elif (coin != high_limit1):
                        self.common.set_coin(mid, high_limit1)
                        self.common.switchserver()
                        self.common.closeactivity(self.luadriver)

                    # 给玩家设置指定银币数目后进行了重新加载，回到了大厅，得重新点击游戏位
                    if (isChange and self.game_page.element_is_exist("右三角标")):
                        self.game_page.wait_element("右三角标").click()
                    self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                    time.sleep(2)
                    game_list[i].click()
                    self.game_page.game_is_download()

                    print "进入子游戏选场界面"
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    roomlevel = self.game_page.get_elements("房间场次")
                    for j in range(len(roomlevel)):
                        self.start_step("点击游戏ID: %s 场次%d" % (game_list[i].get_attribute("name"), j))
                        if (j >= 4):
                            self.common.swipeelement(roomlevel[3], roomlevel[1])
                        time.sleep(2)
                        roomlevel[j].click()
                        self.game_page.screenshot("middleroom_%s.png" % game_list[i].get_attribute("name"))
                        # print roomlevel[j].location['x'], roomlevel[j].location['y'], roomlevel[j].size['width'], roomlevel[j].size['height']

                        # 进入房间后的各种情况处理
                        #玩家携带银币太多，高过场次上限，存钱后入场
                        if (self.game_page.element_is_exist("存钱入场")):
                            print "玩家携带银币太多，高过场次上限，存钱后可入场"
                            self.start_step("存钱入场")
                            self.game_page.wait_element("存钱入场").click()
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()

                        # 携带银币不足场次下限，保险箱有钱，进入房间会提示取钱，取钱后进入该场次房间
                        elif (self.game_page.element_is_exist("取钱入场")):
                            print "玩家携带银币不足场次下限，保险箱有钱, 取钱后可入场"
                            self.start_step("取钱入场")
                            self.game_page.wait_element("取钱入场").click()
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()

                        # 携带银币不足场次下限，保险箱没钱，进入房间会弹出商城购买页面
                        elif (self.game_page.element_is_exist("关闭商城页面")):
                            print "玩家携带银币不足场次下限"
                            self.start_step("关闭商城页面")
                            self.game_page.wait_element("关闭商城页面").click()

                        # 玩家携带银币可以直接进入该场次游戏房间
                        elif (self.game_page.element_is_exist("房间内菜单")):
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()
                        else:
                            print "进入该场次房间失败"

                    self.start_step("退出子游戏%s到大厅界面" % game_list[i].get_attribute("name"))
                    while (self.hall_page.element_is_exist("预发布") != True):
                        time.sleep(10)
                        self.luadriver.back()
                    self.game_page.wait_element("返回1").click()

        self.start_step("大厅第一页子游戏")
        traversal_gameList(self, False)
        time.sleep(2)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏")
        traversal_gameList(self, True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27382_ChooseRoom_NotEnoughEnter(TestCase):
    '''
    携带银币  > 中级场上限，点击进入各个场次
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.safebox_page = Safebox_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

        global mid
        mid = self.common.get_config_value("casecfg", "mid")

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange = False):
            game_list = self.game_page.get_game_list()
            for i in range(len(game_list)):
                # 大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()

                self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                time.sleep(2)
                game_list[i].click()
                if (self.game_page.element_is_exist("重新获取")):
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    self.start_step("点击重新获取")
                    self.game_page.wait_element("重新获取").click()
                else:
                    self.game_page.game_is_download()
                    #获取场次配置信息
                    self.start_step("获取游戏ID: %s场次配置信息" % game_list[i].get_attribute("name"))
                    # 获取到gameid
                    gameid_name = game_list[i].get_attribute("name")
                    gameid = int(gameid_name[4:len(gameid_name)])

                    gamecfg1 = PHPInterface.get_levelconfig(gameid, 0, 0, 13)
                    try:
                        high_limit1 = gamecfg1.get('values', {'HIGH_LIMIT': None}).get('HIGH_LIMIT')
                        print "游戏ID: %s 中级场上限是%d" % (game_list[i].get_attribute("name"), high_limit1)
                    except:
                        print "获取游戏ID: %s场次配置信息失败" % game_list[i].get_attribute("name")
                        self.game_page.wait_element("返回1").click()
                        continue

                    # 获取用户银币数
                    result_userinfo = PHPInterface.get_user_info(mid)
                    myuser_info = json.loads(result_userinfo)
                    coin = myuser_info.get('result', {'coin': None}).get('coin')
                    # print "用户银币数为：%s" % coin

                    # 设置玩家携带银币数 > 中级场上限
                    #如果中级场上限为-1，表无上限，将玩家携带银币数是设为100万
                    if (high_limit1 == -1):
                        self.common.set_coin(mid, "1000000")
                        self.common.switchserver()
                        self.common.closeactivity(self.luadriver)

                    elif (coin <= high_limit1):
                        self.common.set_coin(mid, high_limit1 + 1000)
                        self.common.switchserver()
                        self.common.closeactivity(self.luadriver)

                    # 给玩家设置指定银币数目后进行了重新加载，回到了大厅，得重新点击游戏位
                    if (isChange and self.game_page.element_is_exist("右三角标")):
                        self.game_page.wait_element("右三角标").click()
                    self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                    time.sleep(2)
                    game_list[i].click()
                    self.game_page.game_is_download()

                    print "进入子游戏选场界面"
                    self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                    roomlevel = self.game_page.get_elements("房间场次")
                    for j in range(len(roomlevel)):
                        self.start_step("点击游戏ID: %s 场次%d" % (game_list[i].get_attribute("name"), j))
                        if (j >= 4):
                           self.common.swipeelement(roomlevel[3], roomlevel[1])
                        time.sleep(2)
                        roomlevel[j].click()
                        self.game_page.screenshot("middleroom_%s.png" % game_list[i].get_attribute("name"))
                        # print roomlevel[j].location['x'], roomlevel[j].location['y'], roomlevel[j].size['width'], roomlevel[j].size['height']

                        # 进入房间后的各种情况处理
                        #玩家携带银币太多，高过场次上限，存钱后入场
                        if (self.game_page.element_is_exist("存钱入场")):
                            print "玩家携带银币太多，高过场次上限，存钱后可入场"
                            self.start_step("存钱入场")
                            self.game_page.wait_element("存钱入场").click()
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()

                        # 携带银币不足场次下限，保险箱有钱，进入房间会提示取钱，取钱后进入该场次房间
                        elif (self.game_page.element_is_exist("取钱入场")):
                            print "玩家携带银币不足场次下限，保险箱有钱, 取钱后可入场"
                            self.start_step("取钱入场")
                            self.game_page.wait_element("取钱入场").click()
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()


                        # 携带银币不足场次下限，保险箱没钱，进入房间会弹出商城购买页面
                        elif (self.game_page.element_is_exist("关闭商城页面")):
                            print "玩家携带银币不足场次下限"
                            self.start_step("关闭商城页面")
                            self.game_page.wait_element("关闭商城页面").click()

                        # 玩家携带银币可以直接进入该场次游戏房间
                        elif (self.game_page.element_is_exist("房间内菜单")):
                            self.start_step("退出该场次游戏房间")
                            # self.game_page.wait_element("房间内菜单").click()
                            # self.game_page.wait_element("退出").click()
                            while (self.hall_page.element_is_exist("预发布") != True):
                                time.sleep(10)
                                self.luadriver.back()
                        else:
                            print "进入该场次房间失败"

                    self.start_step("退出子游戏%s到大厅界面" % game_list[i].get_attribute("name"))
                    while (self.hall_page.element_is_exist("预发布") != True):
                        time.sleep(10)
                        self.luadriver.back()
                    self.game_page.wait_element("返回1").click()

        self.start_step("大厅第一页子游戏")
        traversal_gameList(self, False)
        time.sleep(2)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏")
        traversal_gameList(self, True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

class C27384_ChooseRoom_TravelAfterEnter(TestCase):
    '''
    先遍历大厅的其他子游戏后，再进入在测子游戏房间
    '''
    owner = "StephanieHuang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.game_page = Game_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

        self.start_step("获取用户mid")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.start_step("设置银币数为10000")
        self.common.set_coin(mid = mid, value = "10000")

        self.start_step("重新加载，使设置的银币数生效")
        self.common.switchserver()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")

        # 遍历大厅每一页的子游戏列表
        def traversal_gameList(self, isChange=False):
            game_list = self.game_page.get_game_list()
            for i in range(len(game_list)):
                # 大厅每一页的子游戏在从选场界面退出到大厅时，都会退出到第一页
                if (isChange and self.game_page.element_is_exist("右三角标")):
                    self.game_page.wait_element("右三角标").click()
                if (game_list[i].get_attribute("name") != "game5400"):
                    self.start_step("点击大厅游戏ID: %s" % game_list[i].get_attribute("name"))
                    time.sleep(2)
                    game_list[i].click()
                    if self.game_page.element_is_exist("重新获取"):
                        self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                        self.start_step("点击重新获取")
                        # ele = self.game_page.get_elements("重新获取")
                        # print ele[0].location['x'], ele[0].location['y'],ele[0].size['width']，ele[0].size['height']，

                        self.game_page.wait_element("重新获取").click()
                    else:
                        self.game_page.game_is_download()
                        print "进入子游戏%s选场界面" % game_list[i].get_attribute("name")
                        self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                        self.game_page.wait_element("返回1").click()

        # 先进入在测版本的其他子游戏
        self.start_step("大厅第一页子游戏，除在测子游戏")
        traversal_gameList(self, False)
        time.sleep(2)
        self.game_page.wait_element("右三角标").click()
        self.start_step("大厅第二页子游戏，除在测子游戏")
        traversal_gameList(self, True)

        # 再进入在测游戏
        time.sleep(2)
        self.game_page.wait_element("左三角标").click()
        game_list = self.game_page.get_game_list()
        self.start_step("点击斗地主")
        for i in range(len(game_list)):
            #此处需要根据被测子游戏修改gameid
            if (game_list[i].get_attribute("name") == "game203"):
                game_list[i].click()
                self.game_page.game_is_download()
                time.sleep(3)
                self.game_page.screenshot("%s.png" % game_list[i].get_attribute("name"))
                roomlevel = self.game_page.get_elements("房间场次")
                self.start_step("点击初级场")
                roomlevel[0].click()
                time.sleep(3)
                self.game_page.screenshot("room.png")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(mid)
        self.common.closedriver()

__qtaf_seq_tests__ = [C27360_ChooseRoom_ZeroMoneyEnter]
if __name__ == '__main__':

    # C27360_ChooseRoom_ZeroMoneyEnter().debug_run()
    # C27373_ChooseRoom_NotEnoughEnter().debug_run()
    # C27374_ChooseRoom_NotEnoughEnter().debug_run()
    # C27375_ChooseRoom_NotEnoughEnter().debug_run()
    # C27376_ChooseRoom_NotEnoughEnter().debug_run()
    C27377_ChooseRoom_NotEnoughEnter().debug_run()
    # C27378_ChooseRoom_NotEnoughEnter().debug_run()
    # C27379_ChooseRoom_NotEnoughEnter().debug_run()
    # C27380_ChooseRoom_NotEnoughEnter().debug_run()
    # C27381_ChooseRoom_NotEnoughEnter().debug_run()
    # C27382_ChooseRoom_NotEnoughEnter().debug_run()
    # C27384_ChooseRoom_TravelAfterEnter().debug_run()
    # debug_run_all()
