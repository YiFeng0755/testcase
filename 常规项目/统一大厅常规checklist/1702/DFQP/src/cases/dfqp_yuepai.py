#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌约牌测试
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from appiumcenter.luadriver import LuaDriver
from uilib.personinfo_page import Personinfo_Page
from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page
from uilib.safebox_page import Safebox_Page
from common.common import Common
from common import Interface as PHPInterface
import re
import json
import test_datas
from datacenter import dataprovider

class C31190_DFQP_Yuepai_UI_Display(TestCase):
    '''
    约牌房界面显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(2)
        self.yuepai_page.screenshot('.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()


class C31191_DFQP_Yuepai_Tournament(TestCase):
    '''
    约牌房跳转邀请赛
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(3)
        self.yuepai_page.wait_element('+按钮').click()
        time.sleep(3)
        self.yuepai_page.screenshot('1.png')
        self.start_step('跳转至邀请赛界面')
        try:
            self.yuepai_page.get_element('邀请赛1').click()
            time.sleep(5)
        except:
            try:
                self.yuepai_page.wait_element('+按钮').click()
                time.sleep(3)
                self.yuepai_page.wait_element('邀请赛1').click()
            except:
                time.sleep(3)
        self.yuepai_page.screenshot('2.png')
        self.yuepai_page.wait_element("返回").click()
        time.sleep(3)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C31192_DFQP_Yuepai_CreateRoom_GameUninstalled(TestCase):
    '''
    未下载游戏创建约牌房
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        capabilities = {}
        capabilities['noReset'] = False
        capabilities['resetKeyboard'] = False
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(1)
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入积分房界面')
        self.yuepai_page.wait_element('积分房').click()
        time.sleep(4)
        self.start_step('点击开房')
        self.yuepai_page.wait_element('开房').click()
        time.sleep(4)
        self.yuepai_page.screenshot('1.png')
        self.start_step('点击确定')
        try:
            self.yuepai_page.wait_element('确定').click()
            time.sleep(40)
        except:
            print '未找到确定按钮'
        time.sleep(4)
        Flag = True
        while Flag:
            try:
                self.yuepai_page.wait_element('开房')
            except:
                Flag = False
        try:
            self.yuepai_page.wait_element('准备')
            self.yuepai_page.screenshot('3.png')
            print '成功创建房间'
        except:
            print '创建房间失败'
        time.sleep(10)
        self.start_step("退出约牌房")
        self.yuepai_page.wait_element("菜单键").click()
        time.sleep(3)
        self.yuepai_page.wait_element("退出键").click()
        time.sleep(4)
        self.yuepai_page.screenshot('exit.png')
        self.yuepai_page.wait_element("返回").click()
        time.sleep(3)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()


class C31198_DFQP_Yuepai_ScoreRoom_Display(TestCase):
    '''
    积分约牌房房间展示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        # global user_info,UserID
        # user_info = self.common.get_user()
        # print user_info
        # UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.yuepai_page = Yuepai_Page()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.common.closeactivity(self.luadriver)
        # self.hall_page.wait_element("头像").click()
        # time.sleep(5)
        # self.common.loginuser(user_info['user'], user_info['password'])
        # self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('进入约牌房界面')
        self.yuepai_page.wait_element('约牌').click()
        time.sleep(1)
        self.start_step('进入积分房界面')
        self.yuepai_page.wait_element('积分房').click()
        time.sleep(1)
        self.start_step('点击开房按钮')
        self.yuepai_page.wait_element('开房').click()
        time.sleep(1)
        self.start_step('点击确定')
        try:
            self.yuepai_page.wait_element('确定').click()
        except:
            print '未找到确定按钮'
        Flag = True
        while Flag:
            try:
                self.yuepai_page.wait_element('开房').click()
            except:
                Flag = False
        try:
            self.yuepai_page.wait_element('准备')
            print '成功创建积分房'
        except:
            print '创建积分房失败'
        time.sleep(3)
        self.start_step('点击菜单键')
        self.yuepai_page.wait_element('菜单键').click()
        time.sleep(3)
        self.yuepai_page.screenshot('1.png')
        self.yuepai_page.wait_element('斗地主icon').click()
        time.sleep(3)
        self.start_step('点击二维码按钮')
        self.yuepai_page.wait_element('二维码').click()
        time.sleep(3)
        self.yuepai_page.screenshot('2.png')
        self.yuepai_page.wait_element('斗地主icon').click()
        time.sleep(3)
        # self.start_step('点击更多按钮')
        # self.yuepai_page.wait_element('更多').click()
        # time.sleep(3)
        # self.yuepai_page.screenshot('3.png')
        self.yuepai_page.wait_element('斗地主icon').click()
        time.sleep(3)
        # self.start_step('点击邀请按钮')
        # self.yuepai_page.wait_element('邀请-积分房').click()
        # time.sleep(3)
        # self.yuepai_page.screenshot('4.png')
        # self.yuepai_page.wait_element('斗地主icon').click()
        # time.sleep(3)
        # self.start_step('点击详情按钮')
        # self.yuepai_page.wait_element('详情').click()
        # time.sleep(3)
        # self.yuepai_page.screenshot('5.png')
        # self.yuepai_page.wait_element('斗地主icon').click()
        # time.sleep(3)
        self.start_step('点击聊天按钮')
        self.yuepai_page.wait_element('聊天').click()
        time.sleep(3)
        self.yuepai_page.screenshot('6.png')
        self.yuepai_page.wait_element('斗地主icon').click()
        time.sleep(3)
        self.start_step('点击准备按钮')
        self.yuepai_page.wait_element('准备').click()
        time.sleep(3)
        self.yuepai_page.screenshot('7.png')
        self.start_step("退出约牌房")
        self.yuepai_page.wait_element("菜单键").click()
        time.sleep(3)
        self.yuepai_page.wait_element("退出键").click()
        time.sleep(4)
        self.yuepai_page.screenshot('exit.png')
        self.yuepai_page.wait_element("返回").click()
        time.sleep(3)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        try:
            # self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        # finally:
        #     self.common.release_user(UserID)


__qtaf_seq_tests__ = [C31198_DFQP_Yuepai_ScoreRoom_Display]
if __name__ == '__main__':
    debug_run_all()

