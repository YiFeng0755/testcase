# -*- coding:utf-8 -*-
'''
聊天--聊天记录
'''

from runcenter.enums import EnumPriority, EnumStatus
from runcenter.testcase import debug_run_all, TestCase
from uilib.hall_page import Hall_Page
from uilib.setting_page import Setting_Page
from uilib.game_page import Game_Page
from uilib.personinfo_page import Personinfo_Page
from common.common import Common
import common.Interface as PHPInterface
import time
from utils.loghelper import Logger

class C27519_ChatOpenWhenBegin(TestCase):
    '''
    聊天界面打开过程中牌局开始
    '''
    owner = "LukeJiang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    try_find_time = 5
    child_game_timeout = 5
    # game1500 鞍山麻将 -- 网络特么的有问题
    # game24 五狼腿 -- 网络特么的有问题
    # game23 托三批
    # 1502 三打一
    # game25 升级 -- 网络有问题
    # game2603 -- 五十k  -- 网络有问题
    excluded_game = ['game20', 'game2002', 'game1500', 'game1502', 'game24', 'game23', 'game25', 'game2603']
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

    def log_info(self, msg):
        self.log.info(msg)

    def _restart_app(self):
        # 重启游戏
        # driver quite
        self.common.closedriver()
        # recreate driver
        self.init()

    def pre_test(self):
        self.log = Logger().get_logger()
        self.log_info("TestCase: 聊天界面打开过程中牌局开始")
        self.init()
        # self.start_step("关闭活动")
        # self.common.closeactivity(self.luadriver)

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
        #self._restart_app()
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
            self.log_info("==== 准备进入子游戏: %s ====" % game_name)
            if game_name in self.excluded_game:#['game20', 'game2002']:
                continue

            r_v = PHPInterface.set_match_config(game=int(game_name.replace("game", "")), basechiptype=0, playmode=0,
                                                roomlevel=12+self.level,
                                                baseconfig="BASE_CHIPS=>100,HIGH_LIMIT=>-1,HIGH_LIMIT_EXIT=>-1,SERVICE_FEE=>10,ADDROBOTFLAG=>1,ROBOT_MAX_NUMBER=>2",
                                                extraconfig="")
            self.log_info("设置场次接口返回值:%s" % str(r_v))

            if self.enter_game_room(game_name, find_in_elements=False, level=self.level):
                # SB斗地主，进入房间没有准备按钮，聊天按钮不会变
                sb_ddz_chat = self.try_find_element("聊天", try_time=3, page_object=self.game_page)
                if sb_ddz_chat:
                    sb_ddz_chat.click()
                    self.game_page.screenshot('before_play_%s_game.png' % game_name)
                    record = self.try_find_element("聊天记录", try_time=1, page_object=self.game_page)
                    if record:
                        raise Exception("当前界面不应该存在聊天记录按钮")
                    self.luadriver.keyevent(4)
                    self.ready()
                    while 1:
                        start_chat = self.try_find_element("聊天", page_object=self.game_page)
                        if start_chat:
                            start_chat.click()
                            break
                        time.sleep(2)
                    self.game_page.screenshot('after_play_%s_game.png' % game_name)
                    record = self.game_page.wait_element("聊天记录", timesleep=1)
                    if not record:
                         raise Exception("当前界面应该存在聊天记录按钮")
                    self.luadriver.keyevent(4)
                    self.wait_for_gameover()
                    self.back_to_hall()

                else:
                    majiang_chat_btn = self.try_find_element("聊天1", try_time=3, page_object=self.game_page)
                    if majiang_chat_btn:
                        majiang_chat_btn.click()
                        self.game_page.screenshot('before_play_%s_game.png' % game_name)
                        record = self.try_find_element("聊天记录", try_time=1, page_object=self.game_page)
                        if record:
                            raise Exception("当前界面不应该存在聊天记录按钮")
                        self.luadriver.keyevent(4)
                        self.ready()
                        while 1:
                            start_chat = self.try_find_element("牌局开始时聊天按钮", page_object=self.game_page)
                            if start_chat:
                                start_chat.click()
                                record = self.try_find_element("聊天记录", page_object=self.game_page)
                                if record:
                                    self.game_page.screenshot('after_play_%s_game.png' % game_name)
                                    break
                            time.sleep(2)
                        self.luadriver.keyevent(4)
                        self.wait_for_gameover()
                        self.back_to_hall()

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
                self.log_info("游戏超时")
                self.back_to_hall()
                break
                #raise Exception("玩游戏超时")

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

    def ready(self):
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
                break
            if time.time() > end_time:
                raise Exception("等待大厅超时")
            time.sleep(1)
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

class C27524_ChatOpenBeforeFakeRoom(TestCase):
    '''
    牌局结束后未进入假房间情况下查看聊天
    '''
    owner = "LukeJiang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    try_find_time = 5
    child_game_timeout = 5
    # game1500 鞍山麻将 -- 网络特么的有问题
    # game24 五狼腿 -- 网络特么的有问题
    # game23 托三批
    # 1502 三打一
    # game25 升级 -- 网络有问题
    # game2603 -- 五十k  -- 网络有问题
    excluded_game = ['game20', 'game2002', 'game1500', 'game1502', 'game24', 'game23', 'game25', 'game2603']
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

    def _restart_app(self):
        # 重启游戏
        # driver quite
        self.common.closedriver()
        # recreate driver
        self.init()

    def pre_test(self):
        self.log = Logger().get_logger()
        self.log_info("TestCase: 牌局结束后未进入假房间情况下查看聊天")
        self.init()

    def log_info(self, msg):
        self.log.info(msg)

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
        #self._restart_app()
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
            self.log_info("====准备进入子游戏:%s====" % game_name)
            if game_name in self.excluded_game:#['game20', 'game2002']:
                continue

            r_v = PHPInterface.set_match_config(game=int(game_name.replace("game", "")), basechiptype=0, playmode=0,
                                                roomlevel=12+self.level,
                                                baseconfig="BASE_CHIPS=>100,HIGH_LIMIT=>-1,HIGH_LIMIT_EXIT=>-1,SERVICE_FEE=>10,ADDROBOTFLAG=>1,ROBOT_MAX_NUMBER=>2",
                                                extraconfig="")
            self.log_info("设置场次接口返回值:%s" % str(r_v))

            if self.enter_game_room(game_name, find_in_elements=False, level=self.level):
                self.ready()
                self.wait_for_gameover()
                sb_ddz_chat = self.try_find_element("聊天", try_time=3, page_object=self.game_page)
                if sb_ddz_chat:
                    sb_ddz_chat.click()
                else:
                    normal_chat = self.try_find_element("牌局开始时聊天按钮", try_time=3, page_object=self.game_page)
                    normal_chat.click()
                count = self._check_button_count()
                if count != 2:
                    raise Exception("当前页面聊天界面选项卡数量不是二个")
                self.game_page.screenshot("two_tab.png")
            self.back_to_hall()

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

    def ready(self):
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
                self.log_info("游戏超时")
                raise Exception("玩游戏超时")

    def _check_button_count(self):
        count = 0
        common_btn = None
        try:
            common_btn = self.luadriver.find_lua_element_by_name("commonTabBtn")
        except:
            pass
        face_btn = None
        try:
            face_btn = self.luadriver.find_lua_element_by_name("faceTabBtn")
        except:
            pass
        if common_btn:
            count = count + 1
        if face_btn:
            count = count + 1
        return count

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

class C27525_ChatOpenAfterFakeRoom(TestCase):
    '''
    牌局结束后进入假房间情况下查看聊天
    '''
    owner = "LukeJiang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    try_find_time = 5
    child_game_timeout = 5
    # game1500 鞍山麻将 -- 网络特么的有问题
    # game24 五狼腿 -- 网络特么的有问题
    # game23 托三批
    # 1502 三打一
    # game25 升级 -- 网络有问题
    # game2603 -- 五十k  -- 网络有问题
    # game203 -- 斗地主
    # 棋牌类没有准备按钮， 并且游戏结束后会自动跳出界面，忽略棋牌类游戏
    excluded_game = ['game20', 'game2002', 'game1500', 'game1502', 'game24', 'game23', 'game25', 'game2603', 'game203']
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

    def _restart_app(self):
        # 重启游戏
        # driver quite
        self.common.closedriver()
        # recreate driver
        self.init()

    def pre_test(self):
        self.log = Logger().get_logger()
        self.log_info("TestCase: 牌局结束后进入假房间情况下查看聊天")
        self.init()

    def log_info(self, msg):
        self.log.info(msg)

    def run_test(self):
        self.common.switchserver()
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.luadriver)

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
            self.log_info("====准备进入子游戏:%s====" % game_name)
            if game_name in self.excluded_game:#['game20', 'game2002']:
                continue

            r_v = PHPInterface.set_match_config(game=int(game_name.replace("game", "")), basechiptype=0, playmode=0,
                                                roomlevel=12+self.level,
                                                baseconfig="BASE_CHIPS=>100,HIGH_LIMIT=>-1,HIGH_LIMIT_EXIT=>-1,SERVICE_FEE=>10,ADDROBOTFLAG=>1,ROBOT_MAX_NUMBER=>2",
                                                extraconfig="")
            self.log_info("设置场次接口返回值:%s" % str(r_v))

            if self.enter_game_room(game_name, find_in_elements=False, level=self.level):
                self.ready()
                self.wait_for_gameover()
                # 打开聊天
                self.game_page.wait_element("牌局开始时聊天按钮").click()
                # 等待假房间
                while 1:
                    head_frames = self.game_page.get_elements("头像frame", timesleep=1.5)
                    self.log_info(str(head_frames))
                    if head_frames and len(head_frames) == 1:
                        break
                count = self._check_button_count()
                if count != 2:
                    raise Exception("当前页面聊天界面选项卡数量不是二个")
                self.luadriver.keyevent(4)

                # 玩第二局
                self.ready()
                self.wait_for_gameover()
                # 等待假房间
                while 1:
                    head_frames = self.game_page.get_elements("头像frame", timesleep=1.5)
                    self.log_info(str(head_frames))
                    if head_frames and len(head_frames) == 1:
                        break
                self.game_page.wait_element("聊天1").click()
                time.sleep(1)
                count = self._check_button_count()
                if count != 2:
                    raise Exception("当前页面聊天界面选项卡数量不是二个")
                self.game_page.screenshot("%s_two_tab.png" % game_name)
            self.back_to_hall()

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

    def ready(self):
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
                self.log_info("游戏超时")
                raise Exception("玩游戏超时")

    def _check_button_count(self):
        count = 0
        common_btn = None
        try:
            common_btn = self.luadriver.find_lua_element_by_name("commonTabBtn")
        except:
            pass
        face_btn = None
        try:
            face_btn = self.luadriver.find_lua_element_by_name("faceTabBtn")
        except:
            pass
        if common_btn:
            count = count + 1
        if face_btn:
            count = count + 1
        return count


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

class C27526_ChatTabShow(TestCase):
    '''
    聊天记录tab界面显示
    '''
    owner = "LukeJiang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 30
    try_find_time = 5
    child_game_timeout = 5
    # game1500 鞍山麻将 -- 网络特么的有问题
    # game24 五狼腿 -- 网络特么的有问题
    # game23 托三批
    # 1502 三打一
    # game25 升级 -- 网络有问题
    # game2603 -- 五十k  -- 网络有问题
    # game203 -- 斗地主
    # 棋牌类没有准备按钮， 并且游戏结束后会自动跳出界面，忽略棋牌类游戏
    excluded_game = ['game20', 'game2002', 'game1500', 'game1502', 'game24', 'game23', 'game25', 'game2603']
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

    def _restart_app(self):
        # 重启游戏
        # driver quite
        self.common.closedriver()
        # recreate driver
        self.init()

    def pre_test(self):
        self.log = Logger().get_logger()
        self.log_info("TestCase: 聊天记录tab界面显示")
        self.init()

    def log_info(self, msg):
        self.log.info(msg)

    def run_test(self):
        self.common.switchserver()
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.luadriver)

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
            self.log_info("====准备进入子游戏:%s====" % game_name)
            if game_name in self.excluded_game:#['game20', 'game2002']:
                continue

            r_v = PHPInterface.set_match_config(game=int(game_name.replace("game", "")), basechiptype=0, playmode=0,
                                                roomlevel=12+self.level,
                                                baseconfig="BASE_CHIPS=>100,HIGH_LIMIT=>-1,HIGH_LIMIT_EXIT=>-1,SERVICE_FEE=>10,ADDROBOTFLAG=>1,ROBOT_MAX_NUMBER=>2",
                                                extraconfig="")
            self.log_info("设置场次接口返回值:%s" % str(r_v))

            if self.enter_game_room(game_name, find_in_elements=False, level=self.level):
                self.ready()
                while 1:
                    # 游戏开始即换桌按钮不见
                    change_table_btn = None
                    try:
                        change_table_btn = self.game_page.get_element("换桌", timesleep=1)
                    except:
                        pass
                    if not change_table_btn:
                        c = self.try_find_element("牌局开始时聊天按钮", page_object=self.game_page, try_time=3)
                        if c:
                            c.click()
                            break
                        else:
                            c = self.try_find_element("聊天", page_object=self.game_page, try_time=3)
                            if c:
                                c.click()
                                break

                self.game_page.wait_element("聊天记录", timesleep=1).click()
                # 检查输入文本，发送按钮和聊天内容
                input_text = None
                try:
                    input_text = self.luadriver.find_lua_element_by_name("input")
                except:
                    pass
                if not input_text:
                    raise Exception("当前界面没有输入文本")
                send_btn = None
                try:
                    send_btn = self.luadriver.find_lua_element_by_name("send")
                except:
                    pass
                if not send_btn:
                    raise Exception("当前页面没有发送按钮")
                main_view = None
                try:
                    main_view = self.luadriver.find_lua_element_by_name("recordView")
                except:
                    pass
                if not main_view:
                    raise Exception("当前页面没有聊天内容")

                # 检查输入框内容
                input_text_ele = self.game_page.wait_element("聊天输入框")
                input_text = input_text_ele.get_attribute('text')
                self.log_info(input_text)
                self.assert_equal("检查输入框:", input_text, "请在这里输入文字")

                # 检查输入中英数字
                target_text = "8L我"  # 8L&YhE-
                self.game_page.wait_element("聊天输入").send_keys(target_text.decode('utf-8'))
                self.game_page.screenshot('set_input_text.png')

                input_text = self.game_page.wait_element("聊天输入框", timesleep=1).get_attribute('text')
                self.log_info(input_text)
                self.assert_equal("检查输入框:", input_text, "8L&YhE-")
                self.luadriver.keyevent(4)
                self.wait_for_gameover()

            self.back_to_hall()

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

    def ready(self):
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
                self.log_info("游戏超时")
                raise Exception("玩游戏超时")

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

class C27535_ChatRecordRefresh(TestCase):
    '''
    聊天记录刷新
    '''
    owner = "LukeJiang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 60
    try_find_time = 5
    child_game_timeout = 5
    # game1500 鞍山麻将 -- 网络特么的有问题
    # game24 五狼腿 -- 网络特么的有问题
    # game23 托三批
    # 1502 三打一
    # game25 升级 -- 网络有问题
    # game2603 -- 五十k  -- 网络有问题
    # game203 -- 斗地主
    # 棋牌类没有准备按钮， 并且游戏结束后会自动跳出界面，忽略棋牌类游戏
    excluded_game = ['game20', 'game2002', 'game1500', 'game1502', 'game24', 'game23', 'game25', 'game2603']
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

    def _restart_app(self):
        # 重启游戏
        # driver quite
        self.common.closedriver()
        # recreate driver
        self.init()

    def pre_test(self):
        self.log = Logger().get_logger()
        self.log_info("TestCase: 聊天记录刷新")
        self.init()

    def log_info(self, msg):
        self.log.info(msg)

    def run_test(self):
        self.common.switchserver()
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.luadriver)

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

    def _is_in_tray(self):
        is_in_tray = True
        chat_btn = None
        sb_ddz_chat_btn = None
        try:
            chat_btn = self.try_find_element("牌局开始时聊天按钮", page_object=self.game_page)
            if not chat_btn:
                sb_ddz_chat_btn = self.try_find_element("聊天", page_object=self.game_page)
            #chat_btn = self.game_page.get_element("牌局开始时聊天按钮", timesleep=1)
            #sb_ddz_chat_btn = self.game_page.get_element("聊天", timesleep=1)
        except:
            pass
        if chat_btn or sb_ddz_chat_btn:
            if chat_btn:
                chat_btn.click()
            if sb_ddz_chat_btn:
                sb_ddz_chat_btn.click()
            chat_record = None
            try:
                chat_record = self.game_page.get_element("聊天记录")
            except:
                pass
            if chat_record:
                self.luadriver.keyevent(4)
                is_in_tray = False
        return is_in_tray

    def _cancel_tray(self):
        menu = self.try_find_element("房间内菜单", page_object=self.game_page)
        if menu:
            menu.click()
        tray = self.try_find_element("托管", page_object=self.game_page)
        if tray:
            tray.click()

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
                                                extraconfig="OUT_CARD_TIMEOUT=>300,OPERATION_TIMEOUT=>300,OUT_TIME=>300,OPERATION_TIME=>300")
            self.log_info("设置场次接口返回值:%s" % str(r_v))

            if self.enter_game_room(game_name, find_in_elements=False, level=self.level):
                self.ready()
                i = 1
                current_tab_is_chat = False
                current_chat_list = []
                while 1:
                    # 如果是在托管
                    self.log_info("判断是否在托管中")
                    if self._is_in_tray():
                        self.log_info("在托管中")
                        self._cancel_tray()
                    else:
                        self.log_info("不在托管中")
                    try:
                        time.sleep(0.5)
                        c = self.try_find_element("牌局开始时聊天按钮", page_object=self.game_page)
                        if c:
                            c.click()
                        else:
                            c = self.try_find_element("聊天", page_object=self.game_page)
                            if c:
                                c.click()
                        #self.game_page.get_element("牌局开始时聊天按钮", timesleep=0.5).click()
                        #self.game_page.get_element("聊天", timesleep=0.5).click()
                        if current_tab_is_chat:
                            self.game_page.get_element("聊天输入", timesleep=0.5).send_keys(i)
                            self.game_page.get_element("聊天发送").click()
                            self.log_info("发送%s" % str(i))
                            i = i + 1
                        else:
                            self.game_page.get_element("聊天记录", timesleep=0.5).click()
                            self.game_page.get_element("聊天输入", timesleep=0.5).send_keys(i)
                            self.game_page.get_element("聊天发送").click()
                            self.log_info("发送%s" % str(i))
                            current_tab_is_chat = True
                            i = i + 1
                    except:
                        pass
                    if i == 5:
                        if self._is_in_tray():
                            self.log_info("在托管中")
                            self._cancel_tray()
                        try:
                            self.game_page.get_element("牌局开始时聊天按钮", timesleep=1).click()
                        except:
                            pass
                        chat_record_list = self.game_page.get_elements("聊天记录列表", timesleep=1)
                        self.game_page.screenshot('chat_record_list_%s.png' % game_name)
                        index = 1
                        for c in chat_record_list[0:4]:
                            tx = c.get_attribute('text')
                            current_chat_list.append(tx)
                            self.log_info("第%s条聊天记录:%s" % (str(index), tx))
                            index = index + 1
                        break
                self.assert_equal("检测聊天记录", current_chat_list, [u'1', u'2', u'3', u'4'])

            self.wait_for_gameover()
            r_v = PHPInterface.set_match_config(game=int(game_name.replace("game", "")), basechiptype=0, playmode=0,
                                                roomlevel=13,
                                                baseconfig="BASE_CHIPS=>100,HIGH_LIMIT=>-1,HIGH_LIMIT_EXIT=>-1,SERVICE_FEE=>10,ADDROBOTFLAG=>1,ROBOT_MAX_NUMBER=>2",
                                                extraconfig="OUT_CARD_TIMEOUT=>15,OPERATION_TIMEOUT=>15,OUT_TIME=>15,OPERATION_TIME=>15")
            self.log_info("设置场次接口返回值:%s" % str(r_v))

            self.back_to_hall()

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

    def ready(self):
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
                self.log_info("游戏超时")
                raise Exception("玩游戏超时")


    def post_test(self):
        self.log_info("post test")
        r_v = PHPInterface.set_match_config(game=2000, basechiptype=0, playmode=0, roomlevel=12,
                                            baseconfig="BASE_CHIPS=>1,HIGH_LIMIT=>-1,HIGH_LIMIT_EXIT=>-1,SERVICE_FEE=>10,ADDROBOTFLAG=>1,ROBOT_MAX_NUMBER=>2",
                                            extraconfig="OUT_CARD_TIMEOUT=>9,OPERATION_TIMEOUT=>9,OUT_TIME=>9,OPERATION_TIME=>9")
        self.log_info("恢复场次接口返回值:%s" % str(r_v))
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

if __name__ == '__main__':
    debug_run_all()
