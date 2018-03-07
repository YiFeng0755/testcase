# -*- coding:utf-8 -*-
'''
牌桌资料卡显示
'''

from runcenter.enums import EnumPriority, EnumStatus
from runcenter.testcase import debug_run_all, TestCase
from uilib.hall_page import Hall_Page
from uilib.setting_page import Setting_Page
from uilib.game_page import Game_Page
from uilib.personinfo_page import Personinfo_Page
from common.common import Common
import utils.image_util as image_util
import time
from utils.loghelper import Logger

class C27406_PersonInfoCard(TestCase):
    '''
    查看玩家自己资料卡界面显示
    '''
    owner = "LukeJiang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15
    try_find_time = 5
    child_game_timeout = 10
    # game1500 鞍山麻将 -- 网络特么的有问题
    # game24 五狼腿 -- 网络特么的有问题
    # game23 托三批
    # 1502 三打一
    # game25 升级 -- 网络有问题
    # game2603 -- 五十k  -- 网络有问题
    # game2001 -- 飞小鸡麻将 -- 网络有问题
    # game203 -- 斗地主
    # 棋牌类没有准备按钮， 并且游戏结束后会自动跳出界面，忽略棋牌类游戏
    excluded_game = ['game20', 'game2002', 'game1500', 'game1502', 'game24', 'game23', 'game25', 'game2603', 'game2001']
    # 产次
    level = 0


    def pre_test(self):
        self.crop_image_map = {'person_head_image_name': 'person_head_image.png',
                               'person_agenda_icon_name': 'person_agenda_icon.png',
                               'in_game_person_head_image_name': 'in_game_head_image.png',
                               'in_game_person_agenda_icon_name': 'in_game_person_agenda_icon.png'
                               }
        self.info_image = {
            'hall_info': 'hall_person_info.png',
            'game_info': 'game_person_info.png'
        }
        self.log = Logger().get_logger()
        self.common = Common()
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()
        self.game_page = Game_Page()
        self.person_info_page = Personinfo_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()

    def init(self):
        time.sleep(30)
        self.start_step("关闭弹出框")
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.init()
        self.common.switchserver()
        time.sleep(15)
        self.wait_for_hallstable()
        #self.start_step("关闭弹出框")
        #self.common.closeactivity(self.luadriver)
        self.kill_popup_windom()

        self.hall_page.wait_element("头像").click()
        self.game_page.screenshot('hall_person_info.png')

        person_head_image = self.person_info_page.wait_element("头像截图")
        self.log_info("大厅个人信息头像: %s     %s" % (person_head_image.size, person_head_image.location))

        #print head_image.size
        #print head_image.location

        self.log_info("裁剪大厅个人头像")
        self.luadriver.get_screenshot_as_file(self.info_image['hall_info'])
        #screen_img_name = '../%s/report/screenshot/%s_hall_person_info.png' % (self.luadriver.capabilities['deviceName'], self.__class__.__name__)
        screen_img_name = self.info_image['hall_info']
        #person_head_image_name = 'person_head_image.png'
        person_head_image_name = self.crop_image_map['person_head_image_name']
        region = (int(person_head_image.location['x']), int(person_head_image.location['y']),
                  int(person_head_image.location['x'] + person_head_image.size["width"]),
                  int(person_head_image.location['y'] + person_head_image.size["height"]))

        image_util.crop(screen_img_name, person_head_image_name, region)

        # ID
        user_id = self.setting_page.wait_element("账号ID").get_attribute('text')
        self.log_info("大厅账号ID: %s" % user_id)

        # 性别
        agenda = 's'
        if self.person_info_page.wait_element("男").is_selected():
            agenda = 'm'
        elif self.person_info_page.wait_element("女").is_selected():
            agenda = 'w'
        self.log_info("大厅性别: %s" % agenda)

        # 男和秘密的性别icon都是显示的男
        agenda_icon_name = 'girlIcon' if agenda == 'w' else 'boyIcon'

        agenda_icon_ele = self.luadriver.find_lua_element_by_name(agenda_icon_name)
        self.log_info("大厅性别icon: %s     %s" % (agenda_icon_ele.size, agenda_icon_ele.location))

        self.log_info("裁剪大厅性别图像")
        # 截取性别icon
        region = (int(agenda_icon_ele.location['x']), int(agenda_icon_ele.location['y']),
                  int(agenda_icon_ele.location['x'] + agenda_icon_ele.size["width"]),
                  int(agenda_icon_ele.location['y'] + agenda_icon_ele.size["height"]))
        #person_agenda_icon_name = 'person_agenda_icon.png'
        person_agenda_icon_name = self.crop_image_map['person_agenda_icon_name']
        image_util.crop(screen_img_name, person_agenda_icon_name, region)

        # 昵称
        nick_name = self.person_info_page.wait_element("设置用户名").get_attribute('text')
        self.log_info("大厅呢称: %s" % nick_name)

        # 银币数量
        silver_coin = self.luadriver.find_lua_element_by_name("moneyNumText").get_attribute('text')
        self.log_info("大厅银币数量: %s" % silver_coin)

        # 金条数量
        gold = self.luadriver.find_lua_element_by_name("crystalNumText").get_attribute('text')
        self.log_info("大厅金条数量: %s" % gold)

        # 兑
        dui = self.luadriver.find_lua_element_by_name("diamondNumText").get_attribute('text')
        self.log_info("大厅兑换券数量: %s" % dui)

        # 等级称号
        level = self.luadriver.find_lua_element_by_name("chenghaoLevel").get_attribute('text')
        self.log_info("大厅等级称号: %s" % level)

        # 战线/胜率在个人资料页没有显示，后台也查不到，暂不比较

        # 查看物品箱有多少物品
        self.luadriver.keyevent(4)
        self.hall_page.wait_element("物品箱", timesleep=1).click()
        # 等待右侧物品滑出
        while 1:
            box = self.try_find_element("Text_tittle", find_in_elements=False)
            if box:
                break
            time.sleep(1)
        # 查看物品箱
        box = self.try_find_element("Text11", find_in_elements=False, try_time=4)
        if box:
            if '空空如也' in str(box.get_attribute('text')):
                self.log_info("物品箱是空的")

        # 按下back键
        self.luadriver.keyevent(4)

        self.loop_current_page_game(dui, user_id, level, nick_name, person_agenda_icon_name, person_head_image_name, silver_coin)
        self.log_info("第二页游戏")
        self.game_page.wait_element("右三角标", timesleep=1).click()
        self.loop_current_page_game(dui, user_id, level, nick_name, person_agenda_icon_name, person_head_image_name, silver_coin)

    def loop_current_page_game(self, dui, user_id, level, nick_name, person_agenda_icon_name, person_head_image_name, silver_coin):
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
            if self.enter_game_room(game_name, find_in_elements=False, level=self.level):

                # 等待头像出现并点击
                self.log_info("等待头像出现")
                while 1:
                    head = self.game_page.wait_element("头像frame", timesleep=1, timeout=5 * 60, frequency=1)
                    if head:
                        head.click()
                        break
                        # 截个图
                #self.game_page.screenshot('game_person_info.png')
                self.luadriver.get_screenshot_as_file(self.info_image['game_info'])

                # 裁剪头像区域图片
                in_game_head_image = self.person_info_page.wait_element("准备游戏头像")
                self.log_info("牌局个人信息头像: %s     %s" % (in_game_head_image.size, in_game_head_image.location))
                # print in_game_head_image.size
                # print in_game_head_image.location
                self.log_info("裁剪牌局个人信息头像")
                #screen_img_name = '../%s/report/screenshot/%s_game_person_info.png' % (self.luadriver.capabilities['deviceName'], self.class.name)
                screen_img_name = self.info_image['game_info']
                # in_game_person_head_image_name = 'in_game_head_image.png'
                in_game_person_head_image_name = self.crop_image_map['in_game_person_head_image_name']
                region = (int(in_game_head_image.location['x']), int(in_game_head_image.location['y']),
                          int(in_game_head_image.location['x'] + in_game_head_image.size["width"]),
                          int(in_game_head_image.location['y'] + in_game_head_image.size["height"]))

                image_util.crop(screen_img_name, in_game_person_head_image_name, region)

                # 检测头像
                similarity = image_util.cal_simi(person_head_image_name, in_game_person_head_image_name)
                self.log_info("头像相似度: %s" % similarity)
                assert similarity * 100 >= 20

                head_id = self.game_page.wait_element("牌局头像ID").get_attribute('text')
                self.log_info("牌局头像ID: %s" % head_id)

                # 检测id
                self.assert_equal("检测用户id是否一致", user_id, head_id.strip('ID').strip())

                # 检测性别
                # screen_img_name = 'in_game_person_info.png'
                # self.luadriver.get_screenshot_as_file(screen_img_name)
                agenda_icon_ele = self.luadriver.find_lua_element_by_name("gender_icon")
                self.log_info("牌局性别图像: %s     %s" % (agenda_icon_ele.size, agenda_icon_ele.location))

                self.log_info("裁剪牌局性别图像")
                # 截取性别icon
                region = (int(agenda_icon_ele.location['x']), int(agenda_icon_ele.location['y']),
                          int(agenda_icon_ele.location['x'] + agenda_icon_ele.size["width"]),
                          int(agenda_icon_ele.location['y'] + agenda_icon_ele.size["height"]))
                # in_game_person_agenda_icon_name = 'in_game_person_agenda_icon.png'
                in_game_person_agenda_icon_name = self.crop_image_map['in_game_person_agenda_icon_name']
                image_util.crop(screen_img_name, in_game_person_agenda_icon_name, region)

                similarity = image_util.cal_simi(person_agenda_icon_name, in_game_person_agenda_icon_name)
                self.log_info("性别图片相似度: %s" % similarity)
                assert similarity * 100 >= 50

                name = self.luadriver.find_lua_element_by_name("name_value").get_attribute('text')
                self.log_info("牌局用户呢称: %s" % name)
                self.assert_equal("检测用户呢称是否一致", name, nick_name)

                silver = self.luadriver.find_lua_element_by_name("total_money_value").get_attribute('text')
                self.log_info("牌局银币数量: %s" % silver)
                self.assert_equal("检测银币是否一致", silver_coin, silver)

                dui2 = self.luadriver.find_lua_element_by_name("diamondCount").get_attribute('text')
                self.log_info("牌局兑换券数量: %s" % dui2)
                self.assert_equal("检测兑换券是否一致", dui, dui2)

                level2 = self.luadriver.find_lua_element_by_name("level_name").get_attribute('text')
                self.log_info("牌局用户等级: %s" % level2)
                self.assert_equal("检测等级是否一致", level.split('(')[0], level2.replace(' ', ''))
                self.game_page.screenshot("%s.png" % game_name)
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
                if not self.try_find_element("splashScreen", find_in_elements=False):
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
        # 如果当前页面是在游戏中，则等待游戏结束

        while 1:
            if self.wait_for_hallstable() and not self.element_exists("title", find_in_elements=False, try_time=2):
                break
            else:
                self.luadriver.keyevent(4)
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

    def log_info(self, msg):
        self.log.info(msg)

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

    def post_test(self):
        # 删除裁剪的图片
        import os
        for k, v in self.crop_image_map.items():
            self.log_info("删除:%s" % v)
            try:
                os.remove(v)
            except Exception, e:
                pass
        for k, v in self.info_image.items():
            self.log_info("删除:%s" % v)
            try:
                os.remove(v)
            except Exception, e:
                pass
        #self.common.deletefile(self.luadriver)

        self.luadriver.quit()


if __name__ == '__main__':
    debug_run_all()
