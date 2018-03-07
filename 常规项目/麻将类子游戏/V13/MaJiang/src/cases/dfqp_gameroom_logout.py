#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
房间内，物理键退出房间
'''
import time,re
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.game_page import Game_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common
import common.Interface as PHPInterface

'''
进行中提示：牌局还未结束，请打完再走（干瞪眼、斗地主、血流成河）
是否需要点击再显示结算弹框（干瞪眼、双扣：N   血流成河、斗地主：Y）
'''

class logout_base(TestCase):
    '''
    牌局开始后物理返回基类
    '''
    owner = "JessicZeng"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30

    global isDebug
    isDebug = False

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

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")

        global mid
        mid = self.common.get_config_value("casecfg", "mid")
        self.common.set_coin(mid, 10000)

        self.luadriver = self.common.setupdriver()
        if isDebug != True:
            self.common.closeactivity(self.luadriver)
        else :
            time.sleep(15)
        self.common.platformLog("开始设置游戏币")


    def loop_GameList(self,testFunc,isNext = False, black_list = None):
        self.common.platformLog("开始循环子游戏")
        game_list = self.game_page.get_game_list()
        for gameElement in game_list:
            try:

                gameId = gameElement.get_attribute("name")
                self.common.platformLog("当前测试子游戏：",gameId)
                if black_list != None and gameId in black_list :
                    self.common.platformLog(gameId,"该游戏玩牌异常，不进行测试")
                    continue
                self.common.platformLog("点击大厅子游戏入口")

                if self.hall_page.element_is_exist("登录成功标志", 90):
                    self.common.platformLog("登录大厅成功")
                else:
                    self.assert_equal("登录大厅失败", True, False)
                    self.hall_page.screenshot("登录大厅失败.png")
                    return 0

                time.sleep(1)
                if isNext and self.hall_page.element_is_exist("右三角",3):
                    self.hall_page.get_element("右三角").click()
                    time.sleep(1)

                gameElement.click()
                if (self.game_page.game_is_download() == False):
                    self.log_info("下载游戏ID：%s 失败" % gameId)
                    self.game_page.screenshot(gameId + "_open_failed.png")
                    try:
                        self.hall_page.wait_element("关闭对话框").click()
                    except:
                        self.common.platformLog("关闭弹框")
                    continue

                self.start_step("开启机器人")

                if self.set_Robot(re.search('\d+', gameId).group(), 0, 0, 12, 1) :
                    self.common.platformLog("开始机器人成功")
                else :
                    self.assert_equal(gameId + "开启机器人失败", True, False)
                    return 0

                # 适应斗地主新界面，进入房间
                try:
                    self.start_step("点击入口进入房间")
                    #选择房间类型
                    if self.game_page.element_is_exist("新房间类型", 2):
                        gameType_Els = self.game_page.get_elements("新房间类型")
                        gameType_Els[0].click()
                    elif self.game_page.element_not_exist("广播",2):
                        gameType_tabEls = self.game_page.game_play_way()
                        if gameType_tabEls != None and len(gameType_tabEls) > 0 :
                            gameType_tabEls[0][1].click()  # 确保进入的是普通场

                    #点击房间场次，进入房间
                    if self.game_page.element_is_exist("新初级场场次", 2):
                        self.game_page.get_element("新初级场场次").click()
                    elif self.game_page.element_is_exist("房间场次", 2):
                        self.game_page.get_element("房间场次").click()
                except:
                    self.assert_equal(gameId + "大厅进入房间失败", True, False)
                    self.game_page.screenshot(game_id + "大厅进入房间失败" + ".png")

                try:
                    self.start_step("开始具体子游戏操作：" + gameId)
                    testFunc(gameId)
                except:
                    self.game_page.screenshot(game_id + "房间内操作子游戏失败" + ".png")
                    self.assert_equal(gameId + "房间内操作子游戏失败", True, False)

            except:
                self.assert_equal(gameId + "子游戏循环操作失败", True, False)
            finally:
                while True:
                    if self.hall_page.element_is_exist("排行榜", 5):
                        break
                    self.luadriver.back()

    def run_test_base(self,stepFunc,black_list):
        '''

        :param VIPType:  VIP类型
        :param kickCnt:  踢人卡数量
        :param stepFunc: 具体测试步骤方法
        :return:
        '''
        self.start_step("等待页面加载完成")
        if self.hall_page.element_is_exist("登录成功标志", 90):
            self.common.platformLog("登录大厅成功")
        else:
            self.assert_equal("登录大厅失败", True, False)
            self.hall_page.screenshot("登录大厅失败.png")
            return 0
        time.sleep(8)
        self.loop_GameList(stepFunc,False, black_list)
        try:
            self.hall_page.wait_element("右三角").click()
            time.sleep(8)
            self.loop_GameList(stepFunc,True, black_list)
        except:
            self.common.platformLog("没有右三角按钮")

    def post_test(self):
        #     '''
        #     测试用例执行完成后，清理测试环境
        #     '''
        self.common.recover_user(mid)
        self.common.closedriver()



class C27566_logOut_gameOver(logout_base):
    '''
    牌局结束出现结算提示时，点击物理键返回  若有详情按钮则先点开详情按钮（斗地主、血流成河）
    '''
    # 牌局结束时是否有结算框详情按钮  203：斗地主，20：干瞪眼，7：血流成河， 2002：双扣
    global has_detailBtn_dic
    has_detailBtn_dic = {"game203": True,  "game7": True, }

    # 20:预发布环境有不能正常玩牌的子游戏，不进行测试
    # 23:没有结算界面，游戏异常
    # 25:游戏异常
    # 3： 没有结算界面
    global black_list
    black_list = ["game23", "game20","game25", "game3"]

    global backHallEl_name_dict
    backHallEl_name_dict = {}


    def pre_test(self):
        logout_base.pre_test(self)
        self.common.platformLog("C27566_logOut_gameOver开始测试####")

    def test_step(self, game_id):
        '''
       点击进入房间，并且在牌局开始后点击物理键返回大厅
       :return:
       '''
        self.common.platformLog("C27566_logOut_gameOver开始具体测试步骤",game_id)
        self.common.set_coin(mid, 15000)

        if self.game_page.element_is_exist("房间标志", 60) :
            self.common.platformLog("60s进入房间成功")
            self.game_page.screenshot(game_id+"_进入房间成功.png")
        else :
            self.assert_equal("60s进入房间失败_",game_id)
            self.game_page.screenshot(game_id+"_进入房间失败.png")
            return 0
        # 若有准备按钮，则点击准备按钮  只有斗地主是自动准备好的
        try:
            self.game_page.wait_element("准备", 3).click()
        except:
            pass

        if logout_base.wait_in_game(self):
            # 有结算框详情按钮,则先点击详情按钮  然后再物理退出
            flagEl_wait = 240
            if game_id in has_detailBtn_dic  and   has_detailBtn_dic[game_id]:
                if self.game_page.element_is_exist(game_id + "详情按钮", flagEl_wait):
                    self.game_page.get_element(game_id + "详情按钮").click()
                    flagEl_wait = 2
                else:
                    self.game_page.screenshot(game_id + " 显示详情按钮失败" + ".png")
                    self.assert_equal(game_id + " 240s详情按钮未显示", True, False)
                    return 0

            # 等待结算框标志，然后返回游戏
            if self.game_page.element_is_exist(game_id + "结算框标志", flagEl_wait):
                # 斗地主直接返回大厅，结算界面直接返回场次界面  但是其他游戏只是关闭结算弹框
                self.luadriver.back()

                if self.game_page.element_is_exist("菜单键", 2):
                    self.game_page.get_element("菜单键").click()
                    self.game_page.wait_element("退出", 2).click()

                #兼容斗地主新界面
                backHallEl_name = "返回1"
                if game_id in backHallEl_name_dict and backHallEl_name_dict[game_id] != None :
                    backHallEl_name = backHallEl_name_dict[game_id]
                if self.game_page.element_is_exist(backHallEl_name, 2):
                    self.game_page.screenshot(game_id + "room_back_gamelist_succes" + ".png")
                    self.game_page.get_element(backHallEl_name).click()
                else:
                    self.game_page.screenshot(game_id + "room_back_gamelist_fail" + ".png")
                    self.assert_equal("房间返回场次列表失败", True, False)
                    return 0

                if self.hall_page.element_is_exist("排行榜", 2):
                    self.game_page.screenshot(game_id + "gamlist_back_hall_succes" + ".png")
                    self.assert_equal("牌局结束物理返回测试成功", True, True)
                else:
                    self.game_page.screenshot(game_id + "gamlist_back_hall_fail" + ".png")
                    self.assert_equal("场次列表返回大厅失败", True, False)
            else:
                self.assert_equal("90秒等待游戏显示结算框失败", True, False)
                self.game_page.screenshot(game_id + "_show_gameOverDlg_fail" + ".png")
        else:
            self.assert_equal("牌局开始失败"+game_id, True, False)

    def run_test(self):
        logout_base.run_test_base(self, self.test_step,black_list)

    def post_test(self):
        logout_base.post_test(self)

class C27565_logOut_inGame(logout_base):
    '''
    子游戏房间，准备牌局开始打牌后，点击手机物理返回键，查看界面显示
    '''

    # 20:预发布环境有不能正常玩牌的子游戏，不进行测试
    # 23:没有结算界面
    global black_list_27565
    black_list_27565 = ["game20","game25"]


    def pre_test(self):
        logout_base.pre_test(self)
        self.common.platformLog("C27565_logOut_inGame开始测试####")

    def test_step(self, game_id):
        '''
       点击进入房间，并且在牌局开始后点击物理键返回大厅
       :return:
       '''
        self.common.platformLog("C27565_logOut_inGame开始具体测试步骤",game_id)
        self.common.set_coin(mid, 15000)

        if self.game_page.element_is_exist("房间标志", 60) :
            self.common.platformLog("60s进入房间成功")
            self.game_page.screenshot(game_id+"_进入房间成功.png")
        else :
            self.assert_equal("60s进入房间失败_",game_id)
            self.game_page.screenshot(game_id+"_进入房间失败.png")
            return 0
        # 若有准备按钮，则点击准备按钮  只有斗地主是自动准备好的
        try:
            self.game_page.wait_element("准备", 3).click()
        except:
            pass

        if logout_base.wait_in_game(self):

            #游戏开始后，点击物理返回键返回大厅
            self.luadriver.back()
            try:
                toastEl = self.game_page.wait_element("系统提示", 3, 0.1)
                self.common.platformLog(toastEl.get_attribute('text'))
                if "还未结束" in toastEl.get_attribute('text'):
                    self.common.platformLog("C27565_logOut_inGame",game_id,"测试成功")
            except:
                self.assert_equal(game_id + " 牌局开始后物理返回失败", True, False)
                self.game_page.screenshot(game_id + "_logout_inGame_failed.png")


    def run_test(self):
        logout_base.run_test_base(self, self.test_step,black_list_27565)

    def post_test(self):
        logout_base.post_test(self)

if __name__ == '__main__':
# C27566_logOut_gameOver().debug_run()
#     C27566_logOut_gameOver().debug_run()
    debug_run_all()