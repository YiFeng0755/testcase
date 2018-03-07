# -*- coding:utf-8 -*-
'''
牌桌资料卡战绩、胜率显示
'''

from runcenter.enums import EnumPriority, EnumStatus
from runcenter.testcase import debug_run_all, TestCase
from uilib.hall_page import Hall_Page
from uilib.setting_page import Setting_Page
from uilib.game_page import Game_Page
from uilib.personinfo_page import Personinfo_Page
from common.common import Common
import time
import common.Interface as PHPInterface
from utils.loghelper import Logger

class C27411_ExitRoomLevel(TestCase):
    '''
    退出房间后再次查看战绩信息
    '''
    owner = "LukeJiang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    try_find_time = 5
    child_game_timeout = 10
    # game1500 鞍山麻将 -- 子游戏进不了 网络特么的有问题
    # game24 五狼腿 -- 子游戏进不了 网络特么的有问题
    # game23 托三批
    # 1502 三打一
    # game25 升级 -- 网络有问题
    # game2603 -- 五十k  -- 网络有问题
    excluded_game = ['game20', 'game2002', 'game1500', 'game1502', 'game24', 'game23', 'game25', 'game2603', 'game2001']
    level = 0

    def init(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()
        self.game_page = Game_Page()
        self.person_info_page = Personinfo_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        #self.start_step("关闭弹出框")
        #self.common.closeactivity(self.luadriver)
        time.sleep(30)
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.luadriver)
        self.wait_for_hallstable()
        self.kill_popup_windom()

    def pre_test(self):
        self.log = Logger().get_logger()
        self.log_info("退出房间后再次查看战绩信息")
        self.init()

    def run_test(self):
        self.common.switchserver()
        self.start_step("关闭弹出框")
        #self.common.closeactivity(self.luadriver)
        time.sleep(15)
        self.wait_for_hallstable()
        #self.start_step("关闭弹出框")
        #self.common.closeactivity(self.luadriver)
        self.kill_popup_windom()

        mid = self.common.get_mid()
        self.log_info("当前用户mid:%s" % str(mid))
        r_v = PHPInterface.set_coin(mid, 50000)
        self.log_info("设置用户 银币数 接口返回值:%s" % str(r_v))

        self.common.switchserver()
        self.start_step("关闭弹出框")
        time.sleep(15)
        self.wait_for_hallstable()
        #self.common.closeactivity(self.luadriver)
        self.kill_popup_windom()

        self.loop_current_page_game()

        self.log_info("第二页游戏")
        self.game_page.wait_element("右三角标", timesleep=1).click()

        self.loop_current_page_game()

    def loop_current_page_game(self):
        i = self.try_find_time
        game_list = []
        while i:
            game_list = self.game_page.get_game_list()
            if len(game_list) != 0:
                break
            i = i - 1
            time.sleep(1)
        if len(game_list) == 0:
            raise Exception("子游戏列表为空")
        for game in game_list:
            game_name = game.get_attribute('name')
            self.log_info("准备进入子游戏:%s" % game_name)
            if game_name in self.excluded_game:
                continue

            r_v = PHPInterface.set_match_config(game=int(game_name.replace("game", "")), basechiptype=0, playmode=0,
                                                roomlevel=12+self.level,
                                                baseconfig="BASE_CHIPS=>100,HIGH_LIMIT=>-1,HIGH_LIMIT_EXIT=>-1,SERVICE_FEE=>10,ADDROBOTFLAG=>1,ROBOT_MAX_NUMBER=>2",
                                                extraconfig="")
            self.log_info("设置场次接口返回值:%s" % str(r_v))

            if self.enter_game_room(game_name, find_in_elements=False, level=self.level):
                # 有准备的按准备
                self.log_info("有无准备按钮")
                i = self.try_find_time
                while i:
                    ready_btn = None
                    try:
                        ready_btn = self.hall_page.get_element("准备", timesleep=1)
                    except:
                        pass
                    if ready_btn:
                        ready_btn.click()
                        break
                    i = i - 1
                self.log_info("等待游戏结束")
                self.wait_for_gameover()
                #while 1:
                #    # 超时10分钟, 睡眠间隔2s
                #    ready_btn = self.game_page.wait_element("牌局结束标志", timeout=60 * 10, frequency=2)
                #    if ready_btn:
                #        self.log_info("牌局已结束")
                #        break
                end_time = time.time() + self.child_game_timeout * 60
                while 1:
                    head_frames = self.game_page.get_elements("头像frame", timesleep=1.5)
                    # print head_frames
                    if head_frames and len(head_frames) == 1:
                        head_frames[0].click()
                        time.sleep(1)
                        #self.game_page.screenshot('played_%s_info.png' % game_name)
                        break
                    if time.time() > end_time:
                        raise Exception("等待游戏头像超时")
                # 点击头像查看战绩和胜率
                zhanji = self.luadriver.find_lua_element_by_name("zhanji_value").get_attribute('text')
                self.log_info("玩游戏后战绩:%s" % zhanji)
                shenlv = self.luadriver.find_lua_element_by_name("shenglv_value").get_attribute('text')
                self.log_info("玩游戏后胜率:%s" % shenlv)

                # 回到场次界面
                self.luadriver.keyevent(4)
                self.luadriver.keyevent(4)
                time.sleep(4)

                # 再次进入房间
                level = "初级场" if self.level == 0 else "中级场" if self.level == 1 else "高级场"
                self.log_info("点击%s" % level)
                self.game_page.wait_element(level).click()

                # 等待头像出现并点击
                self.log_info("等待头像出现")
                end_time = time.time() + self.child_game_timeout * 60
                while 1:
                    head = self.try_find_element("头像frame", page_object=self.game_page)
                    #head = self.game_page.wait_element("头像frame", timesleep=1)
                    if head:
                        head.click()
                        break
                    if time.time() > end_time:
                        raise Exception("头像frame超时")

                #self.game_page.screenshot('enter_%s_info.png' % game_name)
                zhanji2 = self.luadriver.find_lua_element_by_name("zhanji_value").get_attribute('text')
                self.log_info("再次进入房间战绩:%s" % zhanji2)
                shenlv2 = self.luadriver.find_lua_element_by_name("shenglv_value").get_attribute('text')
                self.log_info("再次进入房间胜率:%s" % shenlv2)

                self.assert_equal("退出房间再次进入房间战绩与退出房间前显示的一致", zhanji2, zhanji)
                self.assert_equal("退出房间再次进入房间胜率与退出房间前显示的一致", shenlv2, shenlv)
                self.game_page.screenshot('enter_%s_info.png' % game_name)
                self.luadriver.keyevent(4)

                # 如果此时在打游戏 打完再退出
                # 如果此时在打游戏 打完再退出
                jdz_has_clicked = False
                ddz_qf_clicked = False
                while 1:
                    head_frames = self.game_page.get_elements("头像frame", timesleep=1.5)
                    self.log_info(str(head_frames))
                    if len(head_frames) <= 1:
                        break
                    else:
                        close_btn = self.try_find_element("关闭按钮", page_object=self.hall_page)
                        if close_btn:
                            close_btn.click()
                            self.log_info("牌局已结束")
                            break
                        share_btn = self.try_find_element("share_btn", find_in_elements=False)
                        if share_btn:
                            self.log_info("share_btn: 牌局已结束")
                            self.try_find_element("close_btn", find_in_elements=False, try_time=3).click()
                            break
                        if not jdz_has_clicked:
                            jdz = self.try_find_element("callLordBtn", find_in_elements=False)
                            if jdz:
                                jdz.click()
                                jdz_has_clicked = True
                                self.log_info("点击叫地主")
                                # 新斗地主，叫地主按钮会在一瞬间消失，此时点击准备按钮会跑在(0,0)位置
                                if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                                    self.log_info("点击叫地主, 存在退出按钮")
                                    self.luadriver.keyevent(4)
                        if not ddz_qf_clicked:
                            qf = self.try_find_element("叫抢场1分", page_object=self.game_page)
                            if qf:
                                qf.click()
                                self.log_info("点击抢分1分")
                                ddz_qf_clicked = True
                                if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                                    self.log_info("点击点击抢分1分, 存在退出按钮")
                                    self.luadriver.keyevent(4)
                #while 1:
                #    head_frames = self.game_page.get_elements("头像frame", timesleep=1.5)
                #    self.log_info(str(head_frames))
                #    if head_frames and len(head_frames) == 1:
                #        break
                # 退到大厅
                self.back_to_hall()

    def element_exists(self, name, find_in_elements=True, try_time=1, page_object=None, timesleep=0.5):
        time.sleep(timesleep)
        target_element = None
        i = try_time
        while i:
            try:
                if find_in_elements:
                    target_element = page_object.get_element(name, timesleep=1)  # self.luadriver.find_lua_element_by_name(target_gamename)
                else:
                    target_element = self.luadriver.find_lua_element_by_name(name)
            except:
                pass
            if target_element:
                break
            i = i - 1
        if target_element:
            return True
        return False

    def wait_for_gameover(self):
        self.log_info("等待游戏结束")
        end_time = time.time() + self.child_game_timeout * 60
        jdz_has_clicked = False
        ddz_qf_clicked = False
        end_tag_showed = False
        close_btn_showed = False
        while 1:
            # 超时10分钟, 睡眠间隔2s
            ddz_gameover = self.try_find_element("ddz_gameover", find_in_elements=False)
            # ready_btn = self.game_page.wait_element("牌局结束标志", timeout=60 * self.child_game_timeout, frequency=2)
            if ddz_gameover:
                end_tag_showed = True
                self.log_info("ddz_gameover: 牌局已结束")
            close_btn = self.try_find_element("关闭按钮", page_object=self.hall_page)
            if close_btn:
                close_btn.click()
                close_btn_showed = True
                self.log_info("关闭按钮: 牌局已结束")
            if end_tag_showed or close_btn_showed:
                break
            share_btn = self.try_find_element("share_btn", find_in_elements=False)
            if share_btn:
                self.log_info("share_btn: 牌局已结束")
                self.try_find_element("close_btn", find_in_elements=False, try_time=3).click()
                close_btn_showed = True
                break
            if not jdz_has_clicked:
                jdz = self.try_find_element("callLordBtn", find_in_elements=False)
                if jdz:
                    jdz.click()
                    # 新斗地主，叫地主按钮会在一瞬间消失，此时点击准备按钮会跑在(0,0)位置
                    if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                        self.log_info("点击叫地主, 存在退出按钮")
                        self.luadriver.keyevent(4)
                    jdz_has_clicked = True
                    self.log_info("点击叫地主")
            if not ddz_qf_clicked:
                qf = self.try_find_element("叫抢场1分", page_object=self.game_page)
                if qf:
                    qf.click()
                    self.log_info("点击抢分1分")
                    ddz_qf_clicked = True
                    if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                        self.log_info("点击叫抢场1分, 存在退出按钮")
                        self.luadriver.keyevent(4)
            if time.time() > end_time:
                raise Exception("玩游戏超时")

    def _restart_app(self):
        # 重启游戏
        # driver quite
        self.common.closedriver()
        # recreate driver
        self.init()

    def wait_for_hallstable(self):
        self.log_info("等待大厅稳定")
        end_time = time.time() + self.child_game_timeout * 60
        while 1:
            game_list = self.game_page.get_game_list()
            if len(game_list) != 0:
                if not self.try_find_element("splashScreen", find_in_elements=False):
                    break
            if time.time() > end_time:
                raise Exception("等待大厅超时")
            time.sleep(1)
        return True

    def log_info(self, msg):
        self.log.info(msg)

    def enter_game_room(self, target_gamename, find_in_elements=True, level=0, page_object=None):
        self.log_info("准备进入子游戏:%s" % target_gamename)
        # 在当前页中点击target子游戏
        child_game = None
        i = self.try_find_time
        while i:
            time.sleep(1)
            self.log_info("获取子游戏:%s" % target_gamename)
            try:
                if find_in_elements:
                    child_game = self.hall_page.get_element(target_gamename)  # self.luadriver.find_lua_element_by_name(target_gamename)
                else:
                    child_game = self.try_find_element(target_gamename, find_in_elements=False)#self.luadriver.find_lua_element_by_name(target_gamename)
            except:
                pass
            if child_game:
                break
            i = i - 1
        if child_game:
            self.log_info("点击子游戏:%s" % target_gamename)
            child_game.click()
        else:
            next_page = self.try_find_element("right_arrow", find_in_elements=False, try_time=self.try_find_time)#self.luadriver.find_lua_element_by_name("right_arrow")
            if next_page:
                next_page.click()
            time.sleep(1)
            if find_in_elements:
                child_game = self.hall_page.wait_element(target_gamename)
            else:
                child_game = self.try_find_element(target_gamename, find_in_elements=False)
            if child_game:
                child_game.click()

        if not child_game:
            raise Exception("获取不到子游戏")
        retry_btn = None
        try:
            retry_btn = self.game_page.get_element("重新获取1")
            self.luadriver.keyevent(4)
        except:
            pass
        if retry_btn:
            return False
        # 判断是否需要下载资源
        download_btn = None
        try:
            download_btn = self.game_page.get_element("资源下载-确定")
        except:
            pass
        room_showed = False
        if download_btn:
            download_btn.click()
            # 等待资源下载完成, 等待结束条件: 场次UI出现
            self.log_info("开始下载游戏")
            while 1:
                if self.element_exists("swf_view", find_in_elements=False):
                    break
                if self.element_exists("房间场次", find_in_elements=True, page_object=self.game_page):
                    room_showed = True
                    break
                time.sleep(1)
                #if self.game_page.wait_element("房间场次", timeout=60 * 10, frequency=1):
                    #break
        else:
            if not self.element_exists("swf_view", find_in_elements=False, try_time=self.try_find_time):
                room_showed = True

        if not room_showed:
            market_btns = self.try_find_elements("swf_view", find_in_elements=False, try_time=self.try_find_time)
            self.log_info("斗地主金银场次选择:%s" % str(market_btns))
            if len(market_btns) == 0:
                raise Exception("获取不到金银场次选择")
            market_btns[0].click()
            time.sleep(2)
            level_btns = self.game_page.wait_element("叫抢初级场").click()
            #self.log_info("斗地主初中高场次选择:%s" % str(level_btns))
            #if len(level_btns) == 0:
             #   raise Exception("获取不到初中高场次选择")
            #level_btns[0].click()
            return True
        else:
            level = "初级场" if level == 0 else "中级场" if level == 1 else "高级场"
            self.log_info("点击%s" % level)
            self.game_page.wait_element(level).click()
            return True

    def try_find_element(self, name, find_in_elements=True, try_time=1, page_object=None):
        target_element = None
        i = try_time
        while i:
            try:
                if find_in_elements:
                    target_element = page_object.get_element(name, timesleep=1)  # self.luadriver.find_lua_element_by_name(target_gamename)
                else:
                    target_element = self.luadriver.find_lua_element_by_name(name)
            except:
                pass
            if target_element:
                break
            i = i - 1
        return target_element

    def back_to_hall(self, back_time=4):
        self.log_info("返回到大厅")
        for i in range(back_time):
            self.luadriver.keyevent(4)
            time.sleep(0.5)
        while 1:
            if self.wait_for_hallstable() and not self.element_exists("title", find_in_elements=False, try_time=2):
                break
            else:
                self.luadriver.keyevent(4)
        return True

    def post_test(self):
        self.log_info("post test")
        #self.common.deletefile(self.luadriver)
        self.luadriver.quit()

    def kill_popup_windom(self, backtime=4):
        # 每日签到
        popup = self.try_find_element("signupTips1", find_in_elements=False, try_time=2)
        if popup:
            self.log_info("每日签到存在")
            sign = self.try_find_element("rewardIcon", find_in_elements=False, try_time=2)
            if sign:
                sign.click()
                time.sleep(3)
                self.try_find_element("closeBtn", find_in_elements=False, try_time=2).click()
        # 问卷调查 暂时没法标识
        # 无条件back 4次
        for i in range(backtime):
            self.luadriver.keyevent(4)
            time.sleep(0.5)
        # 新手礼包
        reward = self.try_find_element("login_money_anim", find_in_elements=False, try_time=2)
        if reward:
            t = self.try_find_element("领新手礼包", page_object=self.hall_page)
            if t:
                t.click()
        while 1:
            if not self.try_find_element("exitGameView", find_in_elements=False, try_time=2):
                break
            else:
                self.luadriver.keyevent(4)

class C27412_RestartGameLevel(TestCase):
    '''
    重启游戏后再次查看战绩信息
    '''
    owner = "LukeJiang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    try_find_time = 5
    child_game_timeout = 10
    # game1500 鞍山麻将 -- 子游戏进不了 网络特么的有问题
    # game24 五狼腿 -- 子游戏进不了 网络特么的有问题
    # game23 托三批
    # 1502 三打一
    # game25 升级 -- 网络有问题
    # game2603 -- 五十k  -- 网络有问题
    excluded_game = ['game20', 'game2002', 'game1500', 'game1502', 'game24', 'game23', 'game25', 'game2603', 'game2001']
    level = 0

    def init(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()
        self.game_page = Game_Page()
        self.person_info_page = Personinfo_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.luadriver)

    def pre_test(self):
        self.log = Logger().get_logger()
        self.log_info("TestCase: 重启游戏后再次查看战绩信息")
        self.init()

    def run_test(self):
        self.common.switchserver()
        time.sleep(15)
        self.kill_popup_windom()

        mid = self.common.get_mid()
        self.log_info("当前用户mid:%s" % str(mid))
        r_v = PHPInterface.set_coin(mid, 50000)
        self.log_info("设置用户 银币数 接口返回值:%s" % str(r_v))

        self.common.switchserver()
        time.sleep(15)
        self.kill_popup_windom()

        self.loop_current_page_game()
        self.log_info("第二页游戏")
        self.game_page.wait_element("右三角标", timesleep=1).click()
        self.loop_current_page_game()

    def loop_current_page_game(self):
        i = self.try_find_time
        game_list = []
        while i:
            game_list = self.game_page.get_game_list()
            if len(game_list) != 0:
                break
            i = i - 1
            time.sleep(1)
        if len(game_list) == 0:
            raise Exception("子游戏列表为空")
        for game in game_list:
            game_name = game.get_attribute('name')
            self.log_info("准备进入子游戏:%s" % game_name)
            if game_name in self.excluded_game:
                continue

            r_v = PHPInterface.set_match_config(game=int(game_name.replace("game", "")), basechiptype=0, playmode=0,
                                                roomlevel=12+self.level,
                                                baseconfig="BASE_CHIPS=>100,HIGH_LIMIT=>505000,HIGH_LIMIT_EXIT=>505000,SERVICE_FEE=>10,ADDROBOTFLAG=>1,ROBOT_MAX_NUMBER=>2",
                                                extraconfig="")
            self.log_info("设置场次接口返回值:%s" % str(r_v))

            if self.enter_game_room(game_name, find_in_elements=False, level=self.level):
                # 有准备的按准备
                self.log_info("有无准备按钮")
                i = self.try_find_time
                while i:
                    ready_btn = None
                    try:
                        ready_btn = self.hall_page.get_element("准备", timesleep=1)
                    except:
                        pass
                    if ready_btn:
                        ready_btn.click()
                        break
                    i = i - 1
                self.log_info("等待游戏结束")
                self.wait_for_gameover()
                while 1:
                    head_frames = self.game_page.get_elements("头像frame", timesleep=1.5)
                    # print head_frames
                    if head_frames and len(head_frames) == 1:
                        head_frames[0].click()
                        time.sleep(1)
                        #self.game_page.screenshot('played_%s_info.png' % game_name)
                        break
                # 点击头像查看战绩和胜率
                zhanji = self.luadriver.find_lua_element_by_name("zhanji_value").get_attribute('text')
                self.log_info("玩游戏后战绩:%s" % zhanji)
                shenlv = self.luadriver.find_lua_element_by_name("shenglv_value").get_attribute('text')
                self.log_info("玩游戏后胜率:%s" % shenlv)

                # 重启游戏
                self.log_info("重启游戏")
                self._restart_app()
                self.kill_popup_windom()

                if not self.enter_game_room(game_name, find_in_elements=False, level=self.level):
                    raise Exception("重启游戏后进入子游戏:%s失败" % game_name)
                else:
                    # 等待头像出现并点击
                    self.log_info("等待头像出现")
                    while 1:
                        head = self.try_find_element("头像frame", page_object=self.game_page)
                        #head = self.game_page.wait_element("头像frame", timesleep=1)
                        if head:
                            head.click()
                            break
                    #self.game_page.screenshot('enter_%s_info.png' % game_name)
                    zhanji2 = self.luadriver.find_lua_element_by_name("zhanji_value").get_attribute('text')
                    self.log_info("重启游戏再次进入房间战绩:%s" % zhanji2)
                    shenlv2 = self.luadriver.find_lua_element_by_name("shenglv_value").get_attribute('text')
                    self.log_info("重启游戏再次进入房间胜率:%s" % shenlv2)

                    self.assert_equal("再次进入房间战绩与重启游戏前显示的一致", zhanji2, zhanji)
                    self.assert_equal("再次进入房间胜率与重启游戏前显示的一致", shenlv2, shenlv)
                    self.luadriver.keyevent(4)
                    # 如果此时在打游戏 打完再退出
                    # 如果此时在打游戏 打完再退出
                    jdz_has_clicked = False
                    ddz_qf_clicked = False
                    while 1:
                        head_frames = self.game_page.get_elements("头像frame", timesleep=1.5)
                        self.log_info(str(head_frames))
                        if len(head_frames) <= 1:
                            break
                        else:
                            close_btn = self.try_find_element("关闭按钮", page_object=self.hall_page)
                            if close_btn:
                                close_btn.click()
                                self.log_info("牌局已结束")
                                break
                            share_btn = self.try_find_element("share_btn", find_in_elements=False)
                            if share_btn:
                                self.log_info("share_btn: 牌局已结束")
                                self.try_find_element("close_btn", find_in_elements=False, try_time=3).click()
                                break
                            if not jdz_has_clicked:
                                jdz = self.try_find_element("callLordBtn", find_in_elements=False)
                                if jdz:
                                    jdz.click()
                                    jdz_has_clicked = True
                                    self.log_info("点击叫地主")
                                    # 新斗地主，叫地主按钮会在一瞬间消失，此时点击准备按钮会跑在(0,0)位置
                                    if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                                        self.log_info("点击叫地主, 存在退出按钮")
                                        self.luadriver.keyevent(4)
                            if not ddz_qf_clicked:
                                qf = self.try_find_element("叫抢场1分", page_object=self.game_page)
                                if qf:
                                    qf.click()
                                    self.log_info("点击抢分1分")
                                    ddz_qf_clicked = True
                                    if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                                        self.log_info("点击点击抢分1分, 存在退出按钮")
                                        self.luadriver.keyevent(4)
            # 退到大厅
            self.back_to_hall()

    def log_info(self, msg):
        self.log.info(msg)

    def enter_game_room(self, target_gamename, find_in_elements=True, level=0, page_object=None):
        self.log_info("准备进入子游戏:%s" % target_gamename)
        # 在当前页中点击target子游戏
        child_game = None
        i = self.try_find_time
        while i:
            time.sleep(1)
            self.log_info("获取子游戏:%s" % target_gamename)
            try:
                if find_in_elements:
                    child_game = self.hall_page.get_element(target_gamename)  # self.luadriver.find_lua_element_by_name(target_gamename)
                else:
                    child_game = self.try_find_element(target_gamename, find_in_elements=False)#self.luadriver.find_lua_element_by_name(target_gamename)
            except:
                pass
            if child_game:
                break
            i = i - 1
        if child_game:
            self.log_info("点击子游戏:%s" % target_gamename)
            child_game.click()
        else:
            next_page = self.try_find_element("right_arrow", find_in_elements=False, try_time=self.try_find_time)#self.luadriver.find_lua_element_by_name("right_arrow")
            if next_page:
                next_page.click()
            time.sleep(1)
            if find_in_elements:
                child_game = self.hall_page.wait_element(target_gamename)
            else:
                child_game = self.try_find_element(target_gamename, find_in_elements=False)
            if child_game:
                child_game.click()

        if not child_game:
            raise Exception("获取不到子游戏")
        retry_btn = None
        try:
            retry_btn = self.game_page.get_element("重新获取1")
            self.luadriver.keyevent(4)
        except:
            pass
        if retry_btn:
            return False
        # 判断是否需要下载资源
        download_btn = None
        try:
            download_btn = self.game_page.get_element("资源下载-确定")
        except:
            pass
        room_showed = False
        if download_btn:
            download_btn.click()
            # 等待资源下载完成, 等待结束条件: 场次UI出现
            self.log_info("开始下载游戏")
            while 1:
                if self.element_exists("swf_view", find_in_elements=False):
                    break
                if self.element_exists("房间场次", find_in_elements=True, page_object=self.game_page):
                    room_showed = True
                    break
                time.sleep(1)
                #if self.game_page.wait_element("房间场次", timeout=60 * 10, frequency=1):
                    #break
        else:
            if not self.element_exists("swf_view", find_in_elements=False, try_time=self.try_find_time):
                room_showed = True

        if not room_showed:
            market_btns = self.try_find_elements("swf_view", find_in_elements=False, try_time=self.try_find_time)
            self.log_info("斗地主金银场次选择:%s" % str(market_btns))
            if len(market_btns) == 0:
                raise Exception("获取不到金银场次选择")
            market_btns[0].click()
            time.sleep(2)
            level_btns = self.game_page.wait_element("叫抢初级场").click()
            #self.log_info("斗地主初中高场次选择:%s" % str(level_btns))
            #if len(level_btns) == 0:
             #   raise Exception("获取不到初中高场次选择")
            #level_btns[0].click()
            return True
        else:
            level = "初级场" if level == 0 else "中级场" if level == 1 else "高级场"
            self.log_info("点击%s" % level)
            self.game_page.wait_element(level).click()
            return True

    def try_find_element(self, name, find_in_elements=True, try_time=1, page_object=None):
        target_element = None
        i = try_time
        while i:
            try:
                if find_in_elements:
                    target_element = page_object.get_element(name, timesleep=1)  # self.luadriver.find_lua_element_by_name(target_gamename)
                else:
                    target_element = self.luadriver.find_lua_element_by_name(name)
            except:
                pass
            if target_element:
                break
            i = i - 1
        return target_element

    def _restart_app(self):
        # 重启游戏
        # driver quite
        self.common.closedriver()
        # recreate driver
        self.init()

    def post_test(self):
        self.log_info("post test")
        self.luadriver.quit()

    def element_exists(self, name, find_in_elements=True, try_time=1, page_object=None, timesleep=0.5):
        time.sleep(timesleep)
        target_element = None
        i = try_time
        while i:
            try:
                if find_in_elements:
                    target_element = page_object.get_element(name, timesleep=1)  # self.luadriver.find_lua_element_by_name(target_gamename)
                else:
                    target_element = self.luadriver.find_lua_element_by_name(name)
            except:
                pass
            if target_element:
                break
            i = i - 1
        if target_element:
            return True
        return False

    def wait_for_gameover(self):
        self.log_info("等待游戏结束")
        end_time = time.time() + self.child_game_timeout * 60
        jdz_has_clicked = False
        ddz_qf_clicked = False
        end_tag_showed = False
        close_btn_showed = False
        while 1:
            # 超时10分钟, 睡眠间隔2s
            ddz_gameover = self.try_find_element("ddz_gameover", find_in_elements=False)
            # ready_btn = self.game_page.wait_element("牌局结束标志", timeout=60 * self.child_game_timeout, frequency=2)
            if ddz_gameover:
                end_tag_showed = True
                self.log_info("ddz_gameover: 牌局已结束")
            close_btn = self.try_find_element("关闭按钮", page_object=self.hall_page)
            if close_btn:
                close_btn.click()
                close_btn_showed = True
                self.log_info("关闭按钮: 牌局已结束")
            if end_tag_showed or close_btn_showed:
                break
            share_btn = self.try_find_element("share_btn", find_in_elements=False)
            if share_btn:
                self.log_info("share_btn: 牌局已结束")
                self.try_find_element("close_btn", find_in_elements=False, try_time=3).click()
                close_btn_showed = True
                break
            if not jdz_has_clicked:
                jdz = self.try_find_element("callLordBtn", find_in_elements=False)
                if jdz:
                    jdz.click()
                    # 新斗地主，叫地主按钮会在一瞬间消失，此时点击准备按钮会跑在(0,0)位置
                    if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                        self.log_info("点击叫地主, 存在退出按钮")
                        self.luadriver.keyevent(4)
                    jdz_has_clicked = True
                    self.log_info("点击叫地主")
            if not ddz_qf_clicked:
                qf = self.try_find_element("叫抢场1分", page_object=self.game_page)
                if qf:
                    qf.click()
                    self.log_info("点击抢分1分")
                    ddz_qf_clicked = True
                    if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                        self.log_info("点击叫抢场1分, 存在退出按钮")
                        self.luadriver.keyevent(4)
            if time.time() > end_time:
                raise Exception("玩游戏超时")

    def back_to_hall(self, back_time=4):
        self.log_info("返回到大厅")
        for i in range(back_time):
            self.luadriver.keyevent(4)
            time.sleep(0.5)
        while 1:
            if self.wait_for_hallstable() and not self.element_exists("title", find_in_elements=False, try_time=2):
                break
            else:
                self.luadriver.keyevent(4)
        return True

    def wait_for_hallstable(self):
        self.log_info("等待大厅稳定")
        end_time = time.time() + self.child_game_timeout * 60
        while 1:
            game_list = self.game_page.get_game_list()
            if len(game_list) != 0:
                if not self.try_find_element("splashScreen", find_in_elements=False):
                    break
            if time.time() > end_time:
                raise Exception("等待大厅超时")
            time.sleep(1)
        return True

    def kill_popup_windom(self, backtime=4):
        # 每日签到
        popup = self.try_find_element("signupTips1", find_in_elements=False, try_time=2)
        if popup:
            self.log_info("每日签到存在")
            sign = self.try_find_element("rewardIcon", find_in_elements=False, try_time=2)
            if sign:
                sign.click()
                time.sleep(3)
                self.try_find_element("closeBtn", find_in_elements=False, try_time=2).click()
        # 问卷调查 暂时没法标识
        # 无条件back 4次
        for i in range(backtime):
            self.luadriver.keyevent(4)
            time.sleep(0.5)
        # 新手礼包
        reward = self.try_find_element("login_money_anim", find_in_elements=False, try_time=2)
        if reward:
            t = self.try_find_element("领新手礼包", page_object=self.hall_page)
            if t:
                t.click()
        while 1:
            if not self.try_find_element("exitGameView", find_in_elements=False, try_time=2):
                break
            else:
                self.luadriver.keyevent(4)

class C27413_EnterOtherGameLevel(TestCase):
    '''
    进入其他游戏玩牌之后再次查看战绩信息
    '''
    owner = "LukeJiang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 40
    try_find_time = 5
    child_game_timeout = 5
    # game1500 鞍山麻将 -- 网络特么的有问题
    # game24 五狼腿 -- 网络特么的有问题
    # game23 托三批
    # 1502 三打一
    # game25 升级 -- 网络有问题
    excluded_game = ['game20', 'game2002', 'game1500', 'game1502', 'game24', 'game23', 'game25']
    level = 0

    def pre_test(self):
        self.log = Logger().get_logger()
        self.log_info("TestCase: 进入其他游戏玩牌之后再次查看战绩信息")
        self.init()

    def run_test(self):
        self.common.switchserver()
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.luadriver)
        time.sleep(15)
        self.kill_popup_windom()

        mid = self.common.get_mid()
        self.log_info("当前用户mid:%s" % str(mid))
        r_v = PHPInterface.set_coin(mid, 50000)
        self.log_info("设置用户 银币数 接口返回值:%s" % str(r_v))

        self.common.switchserver()
        time.sleep(20)
        self.kill_popup_windom()

        self.loop_current_page_game()
        self.log_info("第二页游戏")
        self.game_page.wait_element("右三角标", timesleep=1).click()
        self.loop_current_page_game()

    def loop_current_page_game(self):
        i = self.try_find_time
        game_list = []
        while i:
            game_list = self.game_page.get_game_list()
            if len(game_list) != 0:
                break
            i = i - 1
            time.sleep(1)
        if len(game_list) == 0:
            raise Exception("子游戏列表为空")

        for game in game_list:
            game_name = game.get_attribute('name')
            self.log_info("====准备进入子游戏:%s====" % game_name)
            if game_name in self.excluded_game:#['game20', 'game2002']:
                continue

            r_v = PHPInterface.set_match_config(game=int(game_name.replace("game", "")), basechiptype=0, playmode=0,
                                                roomlevel=12+self.level,
                                                baseconfig="BASE_CHIPS=>100,HIGH_LIMIT=>-1,HIGH_LIMIT_EXIT=>-1,SERVICE_FEE=>10,ADDROBOTFLAG=>1,ROBOT_MAX_NUMBER=>2",
                                                extraconfig="")
            self.log_info("设置场次接口返回值:%s" % str(r_v))

            if self.enter_game_room(game_name, find_in_elements=False, level=self.level):
                # 有准备的按准备
                self.log_info("有无准备按钮")
                i = self.try_find_time
                while i:
                    ready_btn = None
                    try:
                        ready_btn = self.game_page.get_element("准备", timesleep=1)
                    except:
                        pass
                    if ready_btn:
                        self.log_info("点击准备按钮")
                        ready_btn.click()
                        # 新斗地主，准备按钮会在一瞬间消失，此时点击准备按钮会跑在(0,0)位置
                        if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                            self.log_info("点击准备按钮, 存在退出按钮")
                            self.luadriver.keyevent(4)
                        break
                    i = i - 1
                self.log_info("等待游戏结束")
                end_time = time.time() + self.child_game_timeout * 60
                jdz_has_clicked = False
                ddz_qf_clicked = False
                end_tag_showed = False
                close_btn_showed = False
                while 1:
                    # 超时10分钟, 睡眠间隔2s
                    ddz_gameover = self.try_find_element("ddz_gameover", find_in_elements=False)
                    #ready_btn = self.game_page.wait_element("牌局结束标志", timeout=60 * self.child_game_timeout, frequency=2)
                    if ddz_gameover:
                        end_tag_showed = True
                        self.log_info("ddz_gameover: 牌局已结束")
                    close_btn = self.try_find_element("关闭按钮", page_object=self.hall_page)
                    if close_btn:
                        close_btn.click()
                        close_btn_showed = True
                        self.log_info("关闭按钮: 牌局已结束")
                    if end_tag_showed or close_btn_showed:
                        break
                    share_btn = self.try_find_element("share_btn", find_in_elements=False)
                    if share_btn:
                        self.log_info("share_btn: 牌局已结束")
                        self.try_find_element("close_btn", find_in_elements=False, try_time=3).click()
                        close_btn_showed = True
                        break
                    if not jdz_has_clicked:
                        jdz = self.try_find_element("callLordBtn", find_in_elements=False)
                        if jdz:
                            jdz.click()
                            # 新斗地主，叫地主按钮会在一瞬间消失，此时点击准备按钮会跑在(0,0)位置
                            if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                                self.log_info("点击叫地主, 存在退出按钮")
                                self.luadriver.keyevent(4)
                            jdz_has_clicked = True
                            self.log_info("点击叫地主")
                    if not ddz_qf_clicked:
                        qf = self.try_find_element("叫抢场1分", page_object=self.game_page)
                        if qf:
                            qf.click()
                            self.log_info("点击抢分1分")
                            ddz_qf_clicked = True
                            if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                                self.log_info("点击叫抢场1分, 存在退出按钮")
                                self.luadriver.keyevent(4)
                    if time.time() > end_time:
                        raise Exception("玩游戏超时")
                #while 1:
                    #head_frames = self.game_page.get_elements("头像frame", timesleep=1)
                    # print head_frames
                    #if head_frames and len(head_frames) == 1:
                    #    head_frames[0].click()
                    #    time.sleep(1)
                    #    self.game_page.screenshot('played_%s_info.png' % game_name)
                    #    break
                # 点击头像查看战绩和胜率
                while 1:
                    head_frames = self.game_page.get_elements("头像frame", timesleep=1)
                    self.log_info("头像:%s" % str(head_frames))
                    if len(head_frames):
                        if self.try_find_element("readyBtn", find_in_elements=False):
                            if len(head_frames) != 1:
                                continue
                        if head_frames:
                            head_frames[0].click()
                            time.sleep(0.5)
                            break
                zhanji = self.luadriver.find_lua_element_by_name("zhanji_value").get_attribute('text')
                self.log_info("玩游戏后战绩:%s" % zhanji)
                shenlv = self.luadriver.find_lua_element_by_name("shenglv_value").get_attribute('text')
                self.log_info("玩游戏后胜率:%s" % shenlv)

                # 退到大厅
                #self.luadriver.keyevent(4)
                #time.sleep(1)
                #self.luadriver.keyevent(4)
                #time.sleep(1)
                #self.luadriver.keyevent(4)
                #self.wait_for_hallstable()
                self.back_to_hall()

                # 选择另一个子游戏
                another_game = self.get_another_different_game(game_name)
                self.log_info("进入另一个子游戏玩:%s" % another_game)
                self.back_to_hall()
                if not another_game:
                    raise Exception("找不到可用的另一个子游戏")
                if not self.enter_game_room(another_game, find_in_elements=False, level=self.level):
                    raise Exception("进入另一子游戏:%s失败" % game_name)
                else:
                    # 有准备的按准备
                    self.log_info("有无准备按钮")
                    i = self.try_find_time
                    while i:
                        ready_btn = None
                        try:
                            ready_btn = self.game_page.get_element("准备", timesleep=1)
                        except:
                            pass
                        if ready_btn:
                            ready_btn.click()
                            # 新斗地主，准备按钮会在一瞬间消失，此时点击准备按钮会跑在(0,0)位置
                            if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                                self.log_info("点击准备按钮, 存在退出按钮")
                                self.luadriver.keyevent(4)
                            break
                        i = i - 1

                    self.log_info("等待游戏结束")
                    end_time = time.time() + self.child_game_timeout * 60
                    jdz_has_clicked = False
                    ddz_qf_clicked = False
                    end_tag_showed = False
                    close_btn_showed = False
                    while 1:
                        # 超时10分钟, 睡眠间隔2s
                        ddz_gameover = self.try_find_element("ddz_gameover", find_in_elements=False)
                        # ready_btn = self.game_page.wait_element("牌局结束标志", timeout=60 * self.child_game_timeout, frequency=2)
                        if ddz_gameover:
                            end_tag_showed = True
                            self.log_info("ddz_gameover: 牌局已结束")
                        close_btn = self.try_find_element("关闭按钮", page_object=self.hall_page)
                        if close_btn:
                            close_btn.click()
                            close_btn_showed = True
                            self.log_info("关闭按钮: 牌局已结束")
                        if end_tag_showed or close_btn_showed:
                            break
                        share_btn = self.try_find_element("share_btn", find_in_elements=False)
                        if share_btn:
                            self.log_info("share_btn: 牌局已结束")
                            self.try_find_element("close_btn", find_in_elements=False, try_time=3).click()
                            break
                        if not jdz_has_clicked:
                            jdz = self.try_find_element("callLordBtn", find_in_elements=False)
                            if jdz:
                                jdz.click()
                                # 新斗地主，叫地主按钮会在一瞬间消失，此时点击准备按钮会跑在(0,0)位置
                                if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                                    self.log_info("点击叫地主, 存在退出按钮")
                                    self.luadriver.keyevent(4)
                                jdz_has_clicked = True
                                self.log_info("点击叫地主")
                        if not ddz_qf_clicked:
                            qf = self.try_find_element("叫抢场1分", page_object=self.game_page)
                            if qf:
                                qf.click()
                                self.log_info("点击抢分1分")
                                ddz_qf_clicked = True
                                if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                                    self.log_info("点击点击抢分1分, 存在退出按钮")
                                    self.luadriver.keyevent(4)
                        if time.time() > end_time:
                            raise Exception("玩游戏超时")

                    self.game_page.screenshot('enter_another_%s_info.png' % another_game)
                    # 退到大厅
                    #self.game_page.wait_element("房间内菜单", timesleep=1).click()
                    #self.game_page.wait_element("退出", timesleep=1).click()
                    #self.luadriver.keyevent(4)
                    #self.wait_for_hallstable()
                    self.back_to_hall()

                    # 进入上一个子游戏
                    if not self.enter_game_room(game_name, find_in_elements=False, level=self.level):
                        raise Exception("重新进入上一个子游戏:%s失败" % game_name)
                    else:
                        # 等待头像出现并点击
                        self.log_info("等待头像出现")
                        while 1:
                            #head = self.game_page.wait_element("头像frame", timesleep=1, timeout=self.child_game_timeout*60)
                            heads = self.game_page.get_elements("头像frame", timesleep=1)
                            self.log_info("头像:%s" % str(heads))
                            if self.try_find_element("readyBtn", find_in_elements=False):
                                if len(heads) != 1:
                                    continue
                            if heads:
                                heads[0].click()
                                time.sleep(0.5)
                                break
                        self.game_page.screenshot('enter_again_%s_info.png' % game_name)
                        zhanji2 = self.luadriver.find_lua_element_by_name("zhanji_value").get_attribute('text')
                        self.log_info("玩另一子游戏后再次进入前房间战绩:%s" % zhanji2)
                        shenlv2 = self.luadriver.find_lua_element_by_name("shenglv_value").get_attribute('text')
                        self.log_info("玩另一子游戏后再次进入前房间胜率:%s" % shenlv2)
                        self.assert_equal("玩另一子游戏后再次进入前房间胜率一致", zhanji2, zhanji)
                        self.assert_equal("玩另一子游戏后再次进入前房间胜率一致", shenlv2, shenlv)
                        self.luadriver.keyevent(4)

                        # 如果此时在打游戏 打完再退出
                        end_time = time.time() + self.child_game_timeout * 60
                        jdz_has_clicked = False
                        ddz_qf_clicked = False
                        while 1:
                            head_frames = self.game_page.get_elements("头像frame", timesleep=1.5)
                            self.log_info(str(head_frames))
                            if len(head_frames) <= 1:
                                break
                            else:
                                close_btn = self.try_find_element("关闭按钮", page_object=self.hall_page)
                                if close_btn:
                                    close_btn.click()
                                    self.log_info("牌局已结束")
                                    break
                                share_btn = self.try_find_element("share_btn", find_in_elements=False)
                                if share_btn:
                                    self.log_info("share_btn: 牌局已结束")
                                    self.try_find_element("close_btn", find_in_elements=False, try_time=3).click()
                                    break
                                if not jdz_has_clicked:
                                    jdz = self.try_find_element("callLordBtn", find_in_elements=False)
                                    if jdz:
                                        jdz.click()
                                        jdz_has_clicked = True
                                        self.log_info("点击叫地主")
                                        # 新斗地主，叫地主按钮会在一瞬间消失，此时点击准备按钮会跑在(0,0)位置
                                        if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                                            self.log_info("点击叫地主, 存在退出按钮")
                                            self.luadriver.keyevent(4)
                                if not ddz_qf_clicked:
                                    qf = self.try_find_element("叫抢场1分", page_object=self.game_page)
                                    if qf:
                                        qf.click()
                                        self.log_info("点击抢分1分")
                                        ddz_qf_clicked = True
                                        if self.element_exists("退出", page_object=self.game_page, timesleep=1):
                                            self.log_info("点击点击抢分1分, 存在退出按钮")
                                            self.luadriver.keyevent(4)

                                if time.time() > end_time:
                                    raise Exception("玩游戏超时")

                        # 对于斗地主，打完后会自动跳出这种SB行为
                        #if self.element_exists("叫抢初级场", page_object=self.game_page, try_time=self.try_find_time):
                        #    self.luadriver.keyevent(4)
                        #    self.luadriver.keyevent(4)
                        #else:
                        #   # 退到大厅
                        #    self.game_page.wait_element("房间内菜单", timesleep=1).click()
                        #    self.game_page.wait_element("退出", timesleep=1).click()
                        #    self.luadriver.keyevent(4)
                        #self.wait_for_hallstable()
                        self.back_to_hall()

    def init(self):
        #PHPInterface.set_env(PHPInterface.TEST_ENV)
        self.common = Common()
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()
        self.game_page = Game_Page()
        self.person_info_page = Personinfo_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.luadriver)

    def log_info(self, msg):
        self.log.info(msg)

    def enter_game_room(self, target_gamename, find_in_elements=True, level=0, page_object=None):
        self.log_info("准备进入子游戏:%s" % target_gamename)
        # 在当前页中点击target子游戏
        child_game = None
        i = self.try_find_time
        while i:
            time.sleep(1)
            self.log_info("获取子游戏:%s" % target_gamename)
            try:
                if find_in_elements:
                    child_game = self.hall_page.get_element(target_gamename)  # self.luadriver.find_lua_element_by_name(target_gamename)
                else:
                    child_game = self.try_find_element(target_gamename, find_in_elements=False)#self.luadriver.find_lua_element_by_name(target_gamename)
            except:
                pass
            if child_game:
                break
            i = i - 1
        if child_game:
            self.log_info("点击子游戏:%s" % target_gamename)
            child_game.click()
        else:
            next_page = self.try_find_element("right_arrow", find_in_elements=False, try_time=self.try_find_time)#self.luadriver.find_lua_element_by_name("right_arrow")
            if next_page:
                next_page.click()
            time.sleep(1)
            if find_in_elements:
                child_game = self.hall_page.wait_element(target_gamename)
            else:
                child_game = self.try_find_element(target_gamename, find_in_elements=False)
            if child_game:
                child_game.click()

        if not child_game:
            raise Exception("获取不到子游戏")
        retry_btn = None
        try:
            retry_btn = self.game_page.get_element("重新获取1")
            self.luadriver.keyevent(4)
        except:
            pass
        if retry_btn:
            return False
        # 判断是否需要下载资源
        download_btn = None
        try:
            download_btn = self.game_page.get_element("资源下载-确定")
        except:
            pass
        room_showed = False
        if download_btn:
            download_btn.click()
            # 等待资源下载完成, 等待结束条件: 场次UI出现
            self.log_info("开始下载游戏")
            while 1:
                if self.element_exists("swf_view", find_in_elements=False):
                    break
                if self.element_exists("房间场次", find_in_elements=True, page_object=self.game_page):
                    room_showed = True
                    break
                time.sleep(1)
                #if self.game_page.wait_element("房间场次", timeout=60 * 10, frequency=1):
                    #break
        else:
            if not self.element_exists("swf_view", find_in_elements=False, try_time=self.try_find_time):
                room_showed = True

        if not room_showed:
            market_btns = self.try_find_elements("swf_view", find_in_elements=False, try_time=self.try_find_time)
            self.log_info("斗地主金银场次选择:%s" % str(market_btns))
            if len(market_btns) == 0:
                raise Exception("获取不到金银场次选择")
            market_btns[0].click()
            time.sleep(2)
            level_btns = self.game_page.wait_element("叫抢初级场").click()
            #self.log_info("斗地主初中高场次选择:%s" % str(level_btns))
            #if len(level_btns) == 0:
             #   raise Exception("获取不到初中高场次选择")
            #level_btns[0].click()
            return True
        else:
            level = "初级场" if level == 0 else "中级场" if level == 1 else "高级场"
            # 点击初级场
            self.log_info("点击%s" % level)
            self.game_page.wait_element(level).click()

            return True

    def try_find_element(self, name, find_in_elements=True, try_time=1, page_object=None):
        target_element = None
        i = try_time
        while i:
            try:
                if find_in_elements:
                    target_element = page_object.get_element(name, timesleep=1)  # self.luadriver.find_lua_element_by_name(target_gamename)
                else:
                    target_element = self.luadriver.find_lua_element_by_name(name)
            except:
                pass
            if target_element:
                break
            i = i - 1
        return target_element

    def _restart_app(self):
        # 重启游戏
        # driver quite
        self.common.closedriver()
        # recreate driver
        self.init()

    def play_game(self):
        # 等待准备按钮
        self.log_info("等待准备按钮出现")
        while 1:
            ready_btn = self.hall_page.wait_element("准备", timesleep=1)
            if ready_btn:
                ready_btn.click()
                break

        # 接下来就是等自己打完牌
        self.log_info("等待关闭按钮出现")
        while 1:
            # 超时10分钟, 睡眠间隔2s
            close_btn = self.game_page.wait_element("麻将退出按钮", timeout=60*10, frequency=2)
            if close_btn:
                ss = self.game_page.get_elements("换桌xx", timesleep=1)
                self.log_info(str(ss))
                if ss and len(ss) != 0:
                    ss[1].click()
                    break

    def get_another_different_game(self, cur_game):

        def _current_page_game_list():
            i = self.try_find_time
            game_list = []
            while i:
                game_list = self.game_page.get_game_list()
                if len(game_list) != 0:
                    break
                i = i - 1
                time.sleep(1)
            return game_list

        def _scrap_a_available_game(g_list):
            target_game = None
            for game in g_list:
                game_name = game.get_attribute('name')
                # 第一层判断
                if not game_name in self.excluded_game and game_name != cur_game:
                    # 点击之后不会出现网络问题
                    #child_game = self.luadriver.find_lua_element_by_name(game_name)
                    child_game = self.try_find_element(game_name, find_in_elements=False, try_time=self.try_find_time)
                    child_game.click()
                    retry_btn = None
                    try:
                        retry_btn = self.game_page.get_element("重新获取1")
                        self.luadriver.keyevent(4)
                    except:
                        self.luadriver.keyevent(4)
                    if retry_btn:
                        continue
                    else:
                        target_game = game_name
                        break
            return target_game

        game_list = _current_page_game_list()
        t = _scrap_a_available_game(game_list)
        if not t:
            # 先点右三角
            if self.element_exists('right_arrow', find_in_elements=False, try_time=3):
                self.luadriver.find_lua_element_by_name('right_arrow').click()
                time.sleep(1)
                t = _scrap_a_available_game(_current_page_game_list())
            else:
                self.luadriver.find_lua_element_by_name('left_arrow').click()
                time.sleep(1)
                t = _scrap_a_available_game(_current_page_game_list())
        return t

    def element_exists(self, name, find_in_elements=True, try_time=1, page_object=None, timesleep=0.5):
        time.sleep(timesleep)
        target_element = None
        i = try_time
        while i:
            try:
                if find_in_elements:
                    target_element = page_object.get_element(name, timesleep=1)  # self.luadriver.find_lua_element_by_name(target_gamename)
                else:
                    target_element = self.luadriver.find_lua_element_by_name(name)
            except:
                pass
            if target_element:
                break
            i = i - 1
        if target_element:
            return True
        return False

    def try_find_element(self, name, find_in_elements=True, try_time=1, page_object=None):
        target_element = None
        i = try_time
        while i:
            try:
                if find_in_elements:
                    target_element = page_object.get_element(name, timesleep=1)  # self.luadriver.find_lua_element_by_name(target_gamename)
                else:
                    target_element = self.luadriver.find_lua_element_by_name(name)
            except:
                pass
            if target_element:
                break
            i = i - 1
        return target_element

    def try_find_elements(self, name, find_in_elements=True, try_time=1, page_object=None):
        target_elements = []
        i = try_time
        while i:
            try:
                if find_in_elements:
                    target_elements = page_object.get_elements(name, timesleep=1)  # self.luadriver.find_lua_element_by_name(target_gamename)
                else:
                    target_elements = self.luadriver.find_lua_elements_by_name(name)
            except:
                pass
            if target_elements:
                break
            i = i - 1
        return target_elements if target_elements != None else []

    def wait_for_hallstable(self):
        self.log_info("等待大厅稳定")
        end_time = time.time() + self.child_game_timeout * 60
        while 1:
            game_list = self.game_page.get_game_list()
            if len(game_list) != 0:
                break
            if time.time() > end_time:
                raise Exception("等待大厅超时")
            time.sleep(1)
        return True

    def back_to_hall(self, back_time=4):
        self.log_info("返回到大厅")
        for i in range(back_time):
            self.luadriver.keyevent(4)
            time.sleep(0.5)
        while 1:
            if self.wait_for_hallstable() and not self.element_exists("title", find_in_elements=False, try_time=2):
                break
            else:
                self.luadriver.keyevent(4)
        return True

    def post_test(self):
        self.log_info("post test")
        #self.common.deletefile(self.luadriver)
        self.luadriver.quit()

    def kill_popup_windom(self, backtime=4):
        # 每日签到
        popup = self.try_find_element("signupTips1", find_in_elements=False, try_time=2)
        if popup:
            self.log_info("每日签到存在")
            sign = self.try_find_element("rewardIcon", find_in_elements=False, try_time=2)
            if sign:
                sign.click()
                time.sleep(3)
                self.try_find_element("closeBtn", find_in_elements=False, try_time=2).click()
        # 问卷调查 暂时没法标识
        # 无条件back 4次
        for i in range(backtime):
            self.luadriver.keyevent(4)
            time.sleep(0.5)
        # 新手礼包
        reward = self.try_find_element("login_money_anim", find_in_elements=False, try_time=2)
        if reward:
            t = self.try_find_element("领新手礼包", page_object=self.hall_page)
            if t:
                t.click()
        while 1:
            if not self.try_find_element("exitGameView", find_in_elements=False, try_time=2):
                break
            else:
                self.luadriver.keyevent(4)

#__qtaf_seq_tests__ = [C27411_ExitRoomLevel, C27412_RestartGameLevel, C27413_EnterOtherGameLevel]

if __name__ == '__main__':
    debug_run_all()
