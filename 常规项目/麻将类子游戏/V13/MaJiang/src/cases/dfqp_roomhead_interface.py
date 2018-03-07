#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
牌桌头像
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.game_page import Game_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common
import common.Interface as PHPInterface

class C27390_Room_DefaultHead(TestCase):
    '''
    头像为默认的男女头像，进入牌局中查看头像显示
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.personinfo_page =Personinfo_Page()
        self.game_page=Game_Page()
        self.yuepai_page =Yuepai_Page()
        # 初始化Luadriver
        self.mid = self.common.get_config_value("casecfg", "mid")
        PHPInterface.reset_img(self.mid)
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def see_head(self,is_next = False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if (self.game_page.game_is_download() == False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                self.log_info("进入游戏ID：%s 的房间" % game_list[i].get_attribute("name"))
                try:
                    self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i])
                    elements = self.game_page.game_play_way()
                    elements[0][1].click()
                except:
                    self.log_info("当前子游戏初级场")
                self.game_page.wait_element("房间场次").click()
                self.game_page.screenshot("%s_head.png" % game_list[i].get_attribute("name"))
            except:
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")


    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("头像").click()
        self.personinfo_page.screenshot("pre_change_head.png")
        if self.personinfo_page.wait_element("女").is_selected()==True and self.personinfo_page.wait_element("男").is_selected()==False:
            print "选择项为女"
            self.personinfo_page.wait_element("男").click()
        elif self.personinfo_page.wait_element("男").is_selected()==True and self.personinfo_page.wait_element("女").is_selected()==False:
            print "选择项为男"
            self.personinfo_page.wait_element("女").click()
        elif self.personinfo_page.wait_element("男").is_selected()==False and self.personinfo_page.wait_element("女").is_selected()==False:
            print "选择项为隐藏"
            self.personinfo_page.wait_element("女").click()
        self.personinfo_page.screenshot("after_change_head.png")
        self.luadriver.keyevent(4)
        self.start_step("进入子游戏查看头像")
        self.start_step("获取首屏子游戏列表")
        self.see_head()
        while (self.hall_page.element_is_exist("同步标志") == False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("获取第二页的子游戏")
        self.see_head(is_next=True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C27391_Room_Head_Alter(TestCase):
    '''
    头像为修改过的头像，进入牌局中查看头像显示
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.personinfo_page =Personinfo_Page()
        self.game_page=Game_Page()
        self.yuepai_page =Yuepai_Page()
        self.start_step("初始化头像，设置为默认值")
        self.mid = self.common.get_config_value("casecfg", "mid")
        PHPInterface.reset_img(self.mid)
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

    def see_head(self,is_next = False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if (self.game_page.game_is_download() == False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                self.log_info("进入游戏ID：%s 的房间" % game_list[i].get_attribute("name"))
                try:
                    self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i])
                    elements = self.game_page.game_play_way()
                    elements[0][1].click()
                except:
                    self.log_info("当前子游戏初级场")
                self.game_page.wait_element("房间场次").click()
                self.game_page.screenshot("%s_head.png" % game_list[i].get_attribute("name"))
            except:
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")


    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("头像").click()
        self.personinfo_page.screenshot("pre_change_head.png")
        # self.start_step("拍照修改为自定义头像")
        # self.personinfo_page.wait_element("头像logo").click()
        # self.start_step("拍照修改头像")
        # self.luadriver.find_element_by_id("android:id/text1").click()
        # self.luadriver.keyevent(27) #拍照
        # time.sleep(10)
        # try:
        #     self.luadriver.find_elements_by_class_name("android.widget.ImageView")[4].click()
        # except:
        #     print "未找到元素1"
        # try:
        #     self.luadriver.find_elements_by_class_name("android.widget.TextView")[1].click()
        # except:
        #     print "未找到元素2"
        # time.sleep(5)
        # try:
        #     self.luadriver.find_element_by_id("com.android.gallery3d:id/head_select_right").click()
        # except:
        #     print "未找到元素3"
        # try:
        #     self.luadriver.find_element_by_id("com.sec.android.gallery3d:id/save").click()
        # except:
        #     print "未找到元素3"
        # time.sleep(5)
        if self.personinfo_page.wait_element("女").is_selected() == True and self.personinfo_page.wait_element(
                "男").is_selected() == False:
            print "选择项为女"
            self.personinfo_page.wait_element("男").click()
        elif self.personinfo_page.wait_element("男").is_selected() == True and self.personinfo_page.wait_element(
                "女").is_selected() == False:
            print "选择项为男"
            self.personinfo_page.wait_element("女").click()
        elif self.personinfo_page.wait_element("男").is_selected() == False and self.personinfo_page.wait_element(
                "女").is_selected() == False:
            print "选择项为隐藏"
            self.personinfo_page.wait_element("女").click()
        self.personinfo_page.screenshot("after_change_head.png")
        self.luadriver.keyevent(4)
        self.start_step("进入子游戏查看头像")
        self.start_step("获取首屏子游戏列表")
        self.see_head()
        while (self.hall_page.element_is_exist("同步标志") == False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("获取第二页的子游戏")
        self.see_head(is_next=True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C27391and27396_Vip_RoomHead(TestCase):
    '''
    普通房间界面查看vip玩家头像和昵称显示
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.personinfo_page =Personinfo_Page()
        self.game_page=Game_Page()
        self.yuepai_page =Yuepai_Page()
        # 初始化Luadriver
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.mid=self.common.get_config_value("casecfg", "mid")
        self.common.recover_user(self.mid)
        PHPInterface.set_vip(self.mid,5)

    def see_head(self,is_next = False):
        game_list = self.game_page.get_game_list()
        for i in range(len(game_list)):
            self.start_step("进入子游戏:%s" % game_list[i].get_attribute("name"))
            game_list[i].click()
            if (self.game_page.game_is_download() == False):
                self.log_info("下载游戏ID：%s 失败" % game_list[i])
                self.game_page.screenshot("%s_downfail.png" % game_list[i])
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    print "关闭弹框"
                continue
            try:
                self.game_page.wait_element("同步标志", 20)
                self.log_info("进入游戏ID：%s 的房间" % game_list[i].get_attribute("name"))
                try:
                    self.log_info("进入游戏ID：%s 的第一个玩法" % game_list[i])
                    elements = self.game_page.game_play_way()
                    elements[0][1].click()
                except:
                    self.log_info("当前子游戏初级场")
                self.game_page.wait_element("房间场次").click()
                time.sleep(3)
                self.game_page.screenshot("%s_head.png" % game_list[i].get_attribute("name"))
            except:
                try:
                    self.hall_page.wait_element("关闭对话框").click()
                except:
                    self.log_info("未找到元素")
            try:
                self.start_step("退出房间")
                self.yuepai_page.is_exist_yuepairoom()
                self.game_page.wait_element("返回1").click()
                if is_next == True:
                    self.log_info("is_next为True则表示遍历的是第二页的子游戏")
                    try:
                        self.game_page.wait_element("右三角标").click()
                    except:
                        self.log_info("当前为第二页")
            except:
                self.log_info("未找到元素")

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("进入子游戏查看头像")
        self.start_step("获取首屏子游戏列表")
        self.see_head()
        while (self.hall_page.element_is_exist("同步标志") == False):
            self.game_page.wait_element("返回1").click()
        self.start_step("点击大厅第二页")
        if (self.game_page.element_is_exist("右三角标") == True):
            self.game_page.wait_element("右三角标").click()
        else:
            self.game_page.wait_element("左三角标").click()
        self.start_step("获取第二页的子游戏")
        self.see_head(is_next=True)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.recover_user(self.mid)
        self.common.closedriver()

__qtaf_seq_tests__=[C27391and27396_Vip_RoomHead]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
