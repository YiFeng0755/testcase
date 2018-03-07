#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
房间内踢人操作
'''
import time,re
import json
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.backpack_page import Backpack_Page
from uilib.game_page import Game_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common
import common.Interface as PHPInterface

class kick_base(TestCase):
    '''
    房间内踢人脚本基类
    '''
    owner = "JessicZeng"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    global mid
    global kickCard_cnt

    #各游戏对应id   203：斗地主，20：干瞪眼，7：血流成河， 2002：双扣  23:拖三批（七人焖鸡、斗鸡）
    #              2601：葫芦岛麻将   2603：K十五  25：升级  3:斗牛
	#20:预发布环境有不能正常玩牌的子游戏，不进行测试
    #23、3:每局游戏时间太短不足以操作玩家头像
    global global_black_list
    global_black_list = [ "game20","game23","game3"]

    # 为True，本地调试时不执行关闭活动弹框逻辑
    global isDebug
    isDebug = False

    def pre_test(self):
        self.start_step("初始化环境")
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.backpack_page = Backpack_Page()
        self.start_step("初始化driver")
        global mid
        mid = self.common.get_config_value("casecfg", "mid")

        self.luadriver = self.common.setupdriver()

        if isDebug != True:
            self.common.closeactivity(self.luadriver)
        else :
            time.sleep(10)

    def wait_login_suc(self):
        '''等待大厅登录成功标志加载完成'''
        end_time = time.time() + 120
        while True:
            try:
                if self.hall_page.element_is_exist("登录成功标志",1) :
                    self.common.platformLog("大厅登录成功")
                    return True
                elif self.hall_page.element_is_exist("重连游戏",1):
                    self.hall_page.get_element("重连游戏").click()
                    time.sleep(2)
                elif self.hall_page.element_is_exist("重新登陆",1):
                    self.hall_page.get_element("重新登陆").click()
                    time.sleep(2)
            except:
                self.common.platformLog("等待大厅登录成功过程中，获取元素失败")
                return False
            if time.time() > end_time:
                self.common.platformLog("大厅未在指定时间内登录成功")
                return False

    def changeServer(self):
        '''
        子游戏返回列表后通过切换环境，来确保每次都重新登录  避免某些接口设置不生效
        默认从正式环境切换到当前测试环境
        :return:
        '''
        try:
            self.hall_page.wait_element("正式服").click()
            self.common.closeactivity(self.luadriver)
        except:
            print "切换到正式服失败"
        self.common.switchserver()
        self.common.closeactivity(self.luadriver)

    def set_PlayerData(self,VIPType, kickCnt):
        '''
        设置玩家VIP及踢人卡数量，由于有界面操作   只能放在进入大厅成功后调用
        :param VIPCnt: 是否有VIP
        :param kickCnt: 踢人卡张数  踢人卡id为36  None:则是不设置踢人卡数量
        :return:
        '''
        self.start_step("设置玩家数据")

        if PHPInterface.set_vip(mid, VIPType) == 0:
            self.common.platformLog("接口设置VIP信息失败")
            return False
        else:
            self.common.platformLog("设置VIP状态成功")


        #目前道具接口有问题，设置为0   会返回失败  当设置数量为0时，强制返回True
        status = False
        if PHPInterface.add_props(mid, 36, kickCnt) == 0 and kickCnt != 0:
            self.common.platformLog("设置踢人卡数量失败")
            status = False
        else :
            global kickCard_cnt
            kickCard_cnt = kickCnt
            status = True
        self.common.platformLog("测试开始前设置被测玩家初始数据", mid, VIPType, kickCnt,"设置VIP和踢人卡结果：",status)
        return status

    def check_player_data(self,VIPType, kickCnt):
        '''
        检测当前用户数据是否与设置一致，若不一致则切换测试环境来刷新用户数据
        :param VIPType:
        :param kickCnt:
        :return:
        '''
        need_change = False
        if (VIPType in [4,5,6] and self.hall_page.element_is_exist("vip标识",1)):#有VIP标识
            pass
        elif (VIPType == -1 and self.hall_page.element_not_exist("vip标识",1)):#无VIP标识
            pass
        else:
            need_change = True

        if need_change == False and kickCnt != self.get_KickCnt():
            need_change = True

        if need_change == True :
            self.changeServer()
            if self.wait_login_suc():
                self.common.platformLog("切换测试环境后，大厅登录成功")
                return True
            else :
                self.common.platformLog("切换测试环境后，大厅登录失败")
                return False
        else:
            self.common.platformLog("玩家VIP和踢人卡数量正确，不需切换环境")
            return True

    def wait_in_game(self):
        '''
        等待牌局开始，超过60s 则返回失败，停止后续测试操作
        :param gamePage  避免重复new
        :return: True:牌局中   False：未在牌局中
        '''
        gamePage = Game_Page()
        cnt = 0
        isIn = False
        while cnt < 30:
            if self.el_not_exist(gamePage,"房间标志"):
                isIn = False
                break;
            if self.el_not_exist(gamePage, "换桌") and self.el_not_exist(gamePage, "准备"):
                isIn = True
                print "牌局已经开始"
                break
            cnt += 1
            time.sleep(1)
        self.common.platformLog("牌局是否进行中：", isIn)
        return isIn

    def el_not_exist(self,page, el_name):
        '''
        判断元素不存在
        :param element:
        '''
        try:
            if (page.get_element(el_name) == None):
                return True
            else:
                return False
        except:
            return True

    def set_Robot(self, gameid, basechiptype=0, playmode=1, roomlevel=1, robotflag=0):
        #七人焖鸡默认的七人玩法，对应的playmod是3  其余游戏均为0
        if gameid == '23':
            playmode = 3
        return PHPInterface.set_robot_flag(gameid,basechiptype,playmode,roomlevel,robotflag)

    def get_KickCnt(self):
        '''
        :return: 踢人卡张数  默认为None  表示获取踢人卡失败
        '''
        self.start_step("获取玩家物品箱踢人卡数量")
        self.common.platformLog("开始获取踢人卡*************")
        kick_cnt = 0
        try:
            self.hall_page.get_element("物品箱").click()
            self.backpack_page.wait_element("物品箱同步标志")
            item_namesEl = self.backpack_page.get_elements("item名称")
            item_cntsEl = self.backpack_page.get_elements("item数量")
            # 获取两个元素列表成功
            index = 0
            for el in item_namesEl:
                if el.get_attribute('text') == "踢人卡":
                    kick_cnt = int(item_cntsEl[index].get_attribute('text'))
                    break
                index += 1
        except:
            self.common.platformLog("打开物品箱获取踢人卡数量失败")
        finally:
            self.common.checkPopVisible(self.luadriver, self.backpack_page)
            self.hall_page.wait_element("同步标志")
        self.common.platformLog("从物品箱获取到的踢人卡数量",kick_cnt)
        return kick_cnt

    def loop_GameList(self,testFunc, isNext ,VIPType ,kickCnt, def_black_list = None):
        game_list = self.game_page.get_game_list()
        for gameElement in game_list:
            try:

                gameId = gameElement.get_attribute("name")
                self.common.platformLog("当前测试子游戏：", gameId)

                #判断该子游戏是否是可测游戏
                if def_black_list != None:
                    black_list = def_black_list
                else:
                    black_list = global_black_list
                if black_list != None and gameId in black_list :
                    self.common.platformLog(gameId,"该子游戏不符合用例前置条件，不进行测试")
                    continue

                #若从子游戏返回大厅后登录大厅失败，结束测试
                if self.wait_login_suc():
                    self.common.platformLog("登录大厅成功")
                else:
                    self.assert_equal("登录大厅失败，停止后续所有测试步骤", True, False)
                    self.hall_page.screenshot("登录大厅失败.png")
                    break

                #根据条件设置玩家数据
                global kickCard_cnt
                if self.set_PlayerData(VIPType ,kickCnt) == False:
                    self.assert_equal(gameId + "设置玩家VIP信息失败", True, False)
                    continue
                else:
                    time.sleep(2)
                    self.hall_page.wait_element("可点击标志",2).click()
                    time.sleep(1)
                    if self.check_player_data(VIPType ,kickCnt) == False:
                        self.assert_equal(gameId + "玩家数据不匹配切换环境后，登录失败，退出该用例测试", True, False)
                        break

                if isNext and self.hall_page.element_is_exist("右三角", 3):
                    self.hall_page.get_element("右三角").click()
                    time.sleep(1)

                self.common.platformLog("点击大厅子游戏入口")
                time.sleep(1)
                gameElement.click()
                if (self.game_page.game_is_download() == False):
                    self.log_info("下载游戏ID：%s 失败" % gameId)
                    self.game_page.screenshot(gameId + "_下载子游戏失败.png")
                    try:
                        self.hall_page.wait_element("关闭对话框").click()
                    except:
                        self.common.platformLog("关闭弹框")
                    continue

                self.start_step("开启机器人")

                if self.set_Robot(re.search('\d+', gameId).group(), 0, 0, 12, 1):
                    self.common.platformLog("开始机器人成功")
                else:
                    self.assert_equal(gameId + "开启机器人失败", True, False)
                    return 0

                try:
                    self.start_step("点击入口进入房间")
                    if self.game_page.element_is_exist("新房间类型", 2):
                        gameType_Els = self.game_page.get_elements("新房间类型")
                        gameType_Els[0].click()
                    elif self.game_page.element_not_exist("广播",2):
                        gameType_tabEls = self.game_page.game_play_way()
                        gameType_tabEls[0][1].click()  # 确保进入的是普通场

                    #点击房间场次，进入房间
                    if self.game_page.element_is_exist("新初级场场次", 2):
                        self.game_page.get_element("新初级场场次").click()
                    elif self.game_page.element_is_exist("房间场次", 2):
                        self.game_page.get_element("房间场次").click()
                except:
                    self.assert_equal(gameId + "大厅进入房间失败", True, False)
                    self.game_page.screenshot(game_id + "_大厅进入房间失败" + ".png")

                try:
                    self.start_step("开始具体子游戏操作：" + gameId)
                    testFunc(gameId)
                except:
                    self.game_page.screenshot(game_id + "_房间内操作子游戏失败" + ".png")
                    self.assert_equal(gameId + "房间内操作子游戏失败", True, False)
            except:
                self.assert_equal(gameId + "子游戏循环操作失败", True, False)
            finally:
                while True:
                    if self.hall_page.element_is_exist("排行榜", 5):
                        break
                    self.luadriver.back()

    def run_test_base(self,stepFunc, VIPType,kickCnt, def_black_list = None):
        '''

        :param VIPType:  VIP类型
        :param kickCnt:  踢人卡数量
        :param stepFunc: 具体测试步骤方法
        :param def_black_list: 自定义子游戏黑名单
        :return:
        '''
        self.start_step("等待页面加载完成")
        # 若从子游戏返回大厅后登录大厅失败，结束测试
        if self.wait_login_suc():
            self.common.platformLog("run_test_base登录大厅成功")
        else:
            self.assert_equal("run_test_base登录大厅失败，停止后续所有测试步骤", True, False)
            self.hall_page.screenshot("登录大厅失败.png")
            return 0

        time.sleep(8)
        self.loop_GameList(stepFunc, False, VIPType, kickCnt, def_black_list)
        try:
            self.hall_page.wait_element("右三角").click()
            time.sleep(8)
            self.loop_GameList(stepFunc, True, VIPType, kickCnt, def_black_list)
        except:
            self.common.platformLog("没有右三角按钮")

    def post_test(self):
    #     '''
    #     测试用例执行完成后，清理测试环境
    #     设置VIP为过期状态，踢人卡数量为0
    #     '''
         self.start_step("清理测试环境")
         self.set_PlayerData(-1,0)
         self.common.set_coin(mid,'10000')
         self.common.closedriver()


class C27491_KickPlayer_withKickCard(kick_base):
    '''
    牌局中使用踢人卡（非VIP）踢人,提示游戏进行中，无法将该玩家请出房间
    '''

    def pre_test(self):
        kick_base.pre_test(self)
        self.common.platformLog("C27491_KickPlayer_withKickCard开始测试#####")

    def test_step(self,game_id):
        '''
        牌局中使用踢人卡（非VIP）踢人,提示游戏进行中，无法将该玩家请出房间
        :return:
        '''
        self.start_step("点击进入房间")
        self.common.platformLog("C27491_KickPlayer_withKickCard开始测试#####----",game_id)
        self.common.set_coin(mid, 15000)
        if self.game_page.element_is_exist("房间标志", 60) :
            self.common.platformLog("60s进入房间成功")
            self.game_page.screenshot(game_id+"_进入房间成功.png")
        else :
            self.assert_equal("60s进入房间失败_",game_id)
            self.game_page.screenshot(game_id+"_进入房间失败.png")
            return 0

        #若有准备按钮，则点击准备按钮  只有斗地主是自动准备好的
        try:
            self.game_page.wait_element("准备", 3).click()
        except:
            self.common.platformLog("没有准备按钮")
        if kick_base.wait_in_game(self) :
            self.start_step("获取头像列表")
            try:
                headsEle = self.game_page.get_elements("头像frame")
            except:
                self.assert_equal(game_id + "牌局中获取玩家头像列表败", True, False)
                self.game_page.screenshot(game_id + "_获取玩家头像列表败.png")
                return 0
            try:
                if len(headsEle) > 1:
                    #进行踢人操作
                    self.start_step("进行踢人操作")
                    #斗地主 叫抢按钮会自动关闭弹框   等提示操作按钮出现后再进行操作
                    if game_id == "game203" :
                        if self.game_page.element_is_exist("操作面板",180) :
                            pass
                        else:
                            self.game_page.screenshot("斗地主牌局开始失败.png")
                            self.assert_equal("斗地主  180s未出现操作面板，测试失败   直接返回", True, False)
                            return 0
                    headsEle[1].click()
                    time.sleep(2)
                    self.game_page.screenshot(game_id + "_被踢玩家个人详情.png")
                    self.game_page.wait_element("踢人按钮",2).click()
                    try :
                        toastEl = self.game_page.wait_element("系统提示",3,0.1)
                        self.common.platformLog(toastEl.get_attribute('text'))
                        if "游戏进行中" in  toastEl.get_attribute('text') :
                            self.common.platformLog("C27491_KickPlayer_withKickCard_",game_id,"测试成功")
                    except:
                        self.assert_equal(game_id + " _牌局中踢人卡踢人提示不正确", True, False)
                        self.game_page.screenshot(game_id + "_踢人卡踢人提示不正确.png")

                else:
                    self.assert_equal(game_id + "参与牌局玩家数小于2", True, False)
                    self.game_page.screenshot(game_id + "_参与牌局玩家数小于2.png")
            except:
                self.assert_equal(game_id + " 牌局中使用踢人卡踢人失败", True, False)
                self.game_page.screenshot(game_id + "_踢人卡踢人失败.png")
        else:
            self.assert_equal("牌局指定时间内未开始测试失败",True,False)
            self.game_page.screenshot(game_id,"指定时间牌局为未开始.png")


    def run_test(self):
        kick_base.run_test_base(self, self.test_step, -1 ,3)

    def post_test(self):
        kick_base.post_test(self)


class C27491_KickPlayer_withVIP(kick_base):
    '''
    牌局中使用VIP踢人,提示 游戏进行中，无法将该玩家请出房间
    '''

    def pre_test(self):
        kick_base.pre_test(self)
        self.common.platformLog("C27491_KickPlayer_withVIP开始测试#####")

    def test_step(self,game_id):
        '''
        牌局中使用VIP踢人,提示 游戏进行中，无法将该玩家请出房间
        :return:
        '''
        self.common.platformLog("C27491_KickPlayer_withVIP开始具体测试步骤",game_id)
        self.common.set_coin(mid, 15000)
        if self.game_page.element_is_exist("房间标志", 60) :
            self.common.platformLog("60s进入房间成功")
            self.game_page.screenshot(game_id+"_进入房间成功.png")
        else :
            self.assert_equal("60s进入房间失败_",game_id)
            self.game_page.screenshot(game_id+"_进入房间失败.png")
            return 0

        #若有准备按钮，则点击准备按钮  只有斗地主是自动准备好的
        try:
            self.game_page.wait_element("准备", 2).click()
        except:
            pass
        if kick_base.wait_in_game(self) :
            try:
                headsEle = self.game_page.get_elements("头像frame")
            except:
                self.assert_equal(game_id + "牌局中获取玩家头像列表失败", True, False)
                self.game_page.screenshot(game_id + "_获取玩家头像列表失败.png")
                return 0
            try:
                if len(headsEle) > 1:
                    #进行踢人操作
                    # 斗地主 叫抢按钮会自动关闭弹框   等提示操作按钮出现后再进行操作
                    if game_id == "game203":
                        if self.game_page.element_is_exist("操作面板", 180):
                            pass
                        else:
                            self.game_page.screenshot("斗地主牌局开始失败.png")
                            self.assert_equal("斗地主  180s未出现操作面板，测试失败",True,False)
                            return 0
                    headsEle[1].click()
                    time.sleep(2)
                    self.game_page.screenshot(game_id + "_被踢玩家个人详情.png")
                    self.game_page.wait_element("踢人按钮").click()
                    try :
                        toastEl = self.game_page.wait_element("系统提示",3,0.1)
                        self.common.platformLog(toastEl.get_attribute('text'))
                        if "游戏进行中" in  toastEl.get_attribute('text') :
                            self.common.platformLog("C27491_KickPlayer_withVIP",game_id,"测试成功")
                    except:
                        self.assert_equal(game_id + " 牌局中VIP踢人提示不正确", True, False)
                        self.game_page.screenshot(game_id + "_VIP踢人提示不正确.png")

                else:
                    self.assert_equal(game_id + "参与牌局玩家数小于2", True, False)
                    self.game_page.screenshot(game_id + "_参与牌局玩家数小于2.png")
            except:
                self.assert_equal(game_id + " 牌局中使用VIP卡踢人失败", True, False)
                self.game_page.screenshot(game_id + "_使用VIP卡踢人失败.png")
        else:
            self.assert_equal("牌局指定时间内未开始测试失败",True,False)
            self.game_page.screenshot(game_id + "_牌局指定时间内未开始测试失败.png")

    def run_test(self):
        kick_base.run_test_base(self, self.test_step, 4, 0)

    def post_test(self):
        kick_base.post_test(self)

class C27478_KickPlayer_checkCnt(kick_base):
    '''
    没有VIP有踢人卡时，牌局中查看其它玩家信息框显示的踢人卡数量
    '''
    def pre_test(self):
        kick_base.pre_test(self)
        self.common.platformLog("C27478_KickPlayer_checkCnt开始测试#####")

    def test_step(self,game_id):
        '''
        进入房间到用例所需的具体测试步骤
        :return:
        '''
        self.common.platformLog("C27478_KickPlayer_checkCnt开始具体执行步骤",game_id)
        self.common.set_coin(mid, 15000)

        if self.game_page.element_is_exist("房间标志", 60) :
            self.common.platformLog("60s进入房间成功")
            self.game_page.screenshot(game_id+"_进入房间成功.png")
        else :
            self.assert_equal("60s进入房间失败_",game_id)
            self.game_page.screenshot(game_id+"_进入房间失败.png")
            return 0
        #若有准备按钮，则点击准备按钮  只有斗地主是自动准备好的
        try:
            self.game_page.wait_element("准备", 2).click()
        except:
            pass
        if kick_base.wait_in_game(self) :
            try:
                headsEle = self.game_page.get_elements("头像frame")
            except:
                self.assert_equal(game_id + "牌局中获取其他玩家头像失败", True, False)
                self.game_page.screenshot(game_id + "_获取玩家头像失败.png")
                return 0
            try:
                if len(headsEle) > 1:
                    # 斗地主 叫抢按钮会自动关闭弹框   等提示操作按钮出现后再进行操作
                    if game_id == "game203":
                        if self.game_page.element_is_exist("操作面板", 180):
                            pass
                        else:
                            self.game_page.screenshot("斗地主牌局开始失败.png")
                            self.assert_equal("斗地主  180s未出现操作面板，测试失败",True, False)
                            return 0
                    headsEle[1].click()
                    if self.game_page.element_is_exist("踢人按钮",2):
                        cnt_txt = self.game_page.get_element("踢人文本").get_attribute('text')
                        self.common.platformLog("踢人按钮显示文本", cnt_txt,kickCard_cnt)
                        if int(re.search("\d+", cnt_txt).group()) == kickCard_cnt :
                            self.common.platformLog("C27478_KickPlayer_checkCnt",game_id,"测试成功")
                            self.game_page.screenshot(game_id + "_踢人卡数量正确.png")
                            self.luadriver.back()
                        else:
                            self.assert_equal("踢人卡数量不匹配，测试失败", True, False)
                            self.game_page.screenshot(game_id + "_踢人卡数量不匹配.png")
                    else:
                        self.assert_equal("玩家信息框打开失败", True, False)
                        self.game_page.screenshot(game_id + "_玩家信息框打开失败.png")
                else:
                    self.assert_equal("房间内参与牌局玩家数量少于1", True, False)
                    self.game_page.screenshot(game_id + "_参数牌局玩家过少.png")
            except:
                pass
        else:
            self.assert_equal("牌局指定时间内未开始测试失败",True,False)
            self.game_page.screenshot(game_id + "_牌局指定时间内未开始测试失败.png")

    def run_test(self):
        kick_base.run_test_base(self, self.test_step, -1, 2)

    def post_test(self):
        kick_base.post_test(self)


class C27477_KickPlayer_checkCnt(kick_base):
    '''
    VIP和踢人卡均无时，牌局中查看其它玩家信息框显示的踢人卡数量，点击后跳转到支付弹框
    '''
    def pre_test(self):
        kick_base.pre_test(self)
        self.common.platformLog("C27477_KickPlayer_checkCnt开始测试#####")

    def test_step(self,game_id):
        '''
        进入房间到用例所需的具体测试步骤
        :return:
        '''
        self.common.platformLog("C27477_KickPlayer_checkCnt开始具体测试步骤",game_id)
        self.common.set_coin(mid, 15000)

        if self.game_page.element_is_exist("房间标志", 60) :
            self.common.platformLog("60s进入房间成功")
            self.game_page.screenshot(game_id+"_进入房间成功.png")
        else :
            self.assert_equal("60s进入房间失败_",game_id)
            self.game_page.screenshot(game_id+"_进入房间失败.png")
            return 0
        #若有准备按钮，则点击准备按钮  只有斗地主是自动准备好的
        try:
            self.game_page.wait_element("准备", 2).click()
        except:
            pass
        if kick_base.wait_in_game(self):
            try:
                headsEle = self.game_page.get_elements("头像frame")
            except:
                self.assert_equal(game_id + "牌局中获取其他玩家头像失败", True, False)
                self.game_page.screenshot(game_id + "_获取头像列表失败.png")
                return 0
            try:
                if len(headsEle) > 1:
                    # 斗地主 叫抢按钮会自动关闭弹框   等提示操作按钮出现后再进行操作
                    if game_id == "game203":
                        if self.game_page.element_is_exist("操作面板", 180):
                            pass
                        else:
                            self.game_page.screenshot("斗地主牌局开始失败.png")
                            self.assert_equal("斗地主  180s未出现操作面板，测试失败",True, False)
                            return 0
                    headsEle[1].click()
                    if self.game_page.element_is_exist("踢人按钮",2):
                        cnt_txt = self.game_page.get_element("踢人文本").get_attribute('text')
                        self.common.platformLog("踢人按钮显示文本",cnt_txt,kickCard_cnt)
                        if int(re.search("\d+", cnt_txt).group()) == kickCard_cnt:
                            self.game_page.screenshot(game_id + "_踢人卡数量正确.png")
                            self.game_page.get_element("踢人按钮").click()
                            if self.game_page.element_is_exist("支付框标志",2):
                                self.game_page.screenshot(game_id + "_显示支付弹框.png")
                                self.common.platformLog("C27477_KickPlayer_checkCnt",game_id,"测试成功")
                            self.luadriver.back()
                        else:
                            self.assert_equal("踢人卡数量不匹配，测试失败", True, False)
                            self.game_page.screenshot(game_id + "_踢人卡数量不匹配.png")
                    else:
                        self.assert_equal("玩家信息框打开失败", True, False)
                        self.game_page.screenshot(game_id + "_玩家信息框打开失败.png")
                else:
                    self.assert_equal("房间内获取玩家头像数量少于等于", True, False)
                    self.game_page.screenshot(game_id + "_参与牌局玩家过少.png")
            except:
                pass
        else:
            self.assert_equal("牌局指定时间内未开始测试失败",True,False)
            self.game_page.screenshot(game_id + "牌局指定时间内未开始测试失败.png")

    def run_test(self):
        kick_base.run_test_base(self, self.test_step, -1, 0 )

    def post_test(self):
        kick_base.post_test(self)


class C27488_KickPlayer_VIPExpired(kick_base):
    '''
    在牌局中玩家VIP刚好过期，通过VIP表情查看VIP状态是否修改成功
    '''
    global chatBtn_ElNames_dict
    chatBtn_ElNames_dict = {"game7":"房间内聊天1", "game2601":"房间内聊天2"}

    def pre_test(self):
        kick_base.pre_test(self)
        self.common.platformLog("C27488_KickPlayer_VIPExpired开始测试####")

    def test_step(self,game_id):
        '''
        1.玩家是VIP，进入房间游戏开始后通过后把玩家的VIP设置为过期
        2.玩家在牌局中点击聊天按钮，切到VIP表情，发送一个VIP表情后查看玩家头像显示
        :return:
        '''
        self.common.platformLog("C27488_KickPlayer_VIPExpired开始具体测试步骤",game_id)
        self.common.set_coin(mid, 15000)

        if self.game_page.element_is_exist("房间标志", 60) :
            self.common.platformLog("60s进入房间成功")
            self.game_page.screenshot(game_id+"_进入房间成功.png")
        else :
            self.assert_equal("60s进入房间失败_",game_id)
            self.game_page.screenshot(game_id+"_进入房间失败.png")
            return 0

        #若有准备按钮，则点击准备按钮  只有斗地主是自动准备好的
        try:
            self.game_page.wait_element("准备", 2).click()
        except:
            pass
        if kick_base.wait_in_game(self):
            try:
                if PHPInterface.set_vip(mid,-1) :
                    self.common.platformLog("设置VIP过期成功")
                    # 斗地主 叫抢按钮会自动关闭弹框   等提示操作按钮出现后再进行操作
                    if game_id == "game203":
                        if self.game_page.element_is_exist("操作面板", 180):
                            self.common.platformLog("操作面板出现")
                            pass
                        else:
                            self.game_page.screenshot("斗地主牌局开始失败.png")
                            self.assert_equal("斗地主  180s未出现操作面板，测试失败",True, False)
                            return 0

                    # 使用VIP表情
                    chatBtn_name = "聊天"
                    if chatBtn_ElNames_dict != None and game_id in chatBtn_ElNames_dict:
                        chatBtn_name = chatBtn_ElNames_dict[game_id]

                    self.yuepai_page.wait_element(chatBtn_name, 2).click()
                    time.sleep(2)
                    self.yuepai_page.wait_element("表情", 2).click()
                    self.yuepai_page.wait_element("vip表情", 2).click()
                    self.yuepai_page.wait_element("VIPFaceItem", 2).click()

                    # 查看个人头像VIP标识
                    headsEle = self.game_page.get_elements("头像frame")

                    headsEle[0].click()
                    if self.game_page.element_is_exist("自己信息框VIP标识"):
                        self.assert_equal("VIP设置过期后，消失失败", True, False)
                        self.game_page.screenshot(game_id + "_VIP标识消失失败" + ".png")
                        return 0
                    else:
                        self.common.platformLog("自己VIP标志消失，结果正确")
                        self.game_page.screenshot(game_id + "_VIP消失" + ".png")

                    # 关闭个人信息框
                    if self.game_page.element_is_exist("信息框同步标志", 1):
                        self.luadriver.back()

                    # 再次打开聊天表情项，查看能否使用VIP表情
                    self.yuepai_page.get_element("聊天").click()
                    time.sleep(2)
                    self.yuepai_page.wait_element("表情", 2).click()
                    self.yuepai_page.wait_element("vip表情", 2).click()
                    if self.yuepai_page.element_is_exist("立即成为VIP"):
                        self.common.platformLog("C27488_KickPlayer_VIPExpired",game_id,"测试成功")
                        self.game_page.screenshot(game_id + "_显示成为VIP按钮" + ".png")
                    else:
                        self.assert_equal("VIP设置过期后，VIP表情失效失败", True, False)
                        self.game_page.screenshot(game_id + "_VIP表情未失效" + ".png")
                else :
                    self.assert_equal("设置VIP过期信息失败，结束测试", True, False)
            except:
                self.assert_equal("VIP过期状态检测，失败", True, False)
                self.game_page.screenshot(game_id + "_VIP过期状态失败" + ".png")
        else:
            self.assert_equal("牌局指定时间内未开始测试失败",True,False)
            self.game_page.screenshot(game_id + "牌局指定时间内未开始测试失败" + ".png")

    def run_test(self):
        #2601：葫芦岛麻将显示取消托管按钮时会遮住表情按钮   但是目前取消托管按钮无法获取元素
        #2603:K105  按照测试用例描述的测试步骤  VIP并不会失效
        def_black_list = ["game20","game23","game3", "game2601","game2603"]
        kick_base.run_test_base(self, self.test_step , 4, 0, def_black_list)

    def post_test(self):
        kick_base.post_test(self)


if __name__ == '__main__':
     # debug_run_all()
     C27488_KickPlayer_VIPExpired().debug_run()