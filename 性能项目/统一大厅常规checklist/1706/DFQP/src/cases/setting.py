#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
性能测试场景之设置
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from cfg.constantEnum import EnumSceneName,EnumSceneType
from runcenter.testcase import debug_run_all,TestCase
from uilib.setting_page import Setting_Page
from uilib.hall_page import Hall_Page
from com.common import Common

class PerTest_QIPAIHALL_Setting(TestCase):
    '''
    设置界面显示
    '''
    owner = "JessicZeng"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 60

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.setting_page = Setting_Page()
        #通过xpath获取items，是完全返回  因此针对一页显示的item数进行操作
        self.helpItemCount = 5

    def run_test(self):
        '''
        测试用例
        操作步骤：
        1、关闭悬浮球（若已是关闭状态则先打开再关闭）
        2、静音关闭（若已是关闭状态则先打开再关闭）
        3、读牌打开（若已是打开状态则先关闭再打开）
        4、音效、音乐、聊天、震动、比赛围观打开（若已是打开状态则先关闭再打开）
        5、关于查看，四个标签操作步骤：关于--服务协议--隐私策略--版号申明  列表项均滑动  从版号申明往前一直到关于我们  然后点击返回按钮返回设置页面
        6、关于游戏帮助目前所打包不支持，暂不操作
        '''
        self.hall_page.wait_element("同步标志")
        self.common.sendTagBroadcast(EnumSceneName.Setting, EnumSceneType.Start)
        try:
            self.start_step("点击大厅设置入口")
            self.hall_page.get_element("设置").click()
            self.setting_page.wait_element("同步标志")
            self.common.taskScreenShot("openSettingPop.jpg")
            # 操作各切换按钮
            self.start_step("操作各切换按钮")
            self.common.switchBtn("浮动球开关", "浮动球状态", True)
            self.common.taskScreenShot("closeFloatBall.jpg")
            self.common.switchBtn("静音开关", "静音状态", True)
            self.common.switchBtn("读牌开关", "读牌状态", False)
            self.common.switchBtn("聊天开关", "聊天状态", False)
            self.common.switchBtn("震动开关", "震动状态", False)
            self.common.switchBtn("比赛围观开关", "比赛围观状态", False)

            # 查看关于弹框
            self.start_step("查看关于内容")
            self.setting_page.get_element("关于入口",0).click()
            self.setting_page.wait_element("关于同步标志")
            self.common.taskScreenShot("setting_about_pop.jpg")
            self.setting_page.get_element("关于我们").click()
            time.sleep(1)
            self.setting_page.get_element("服务协议").click()
            time.sleep(1)
            self.setting_page.get_element("隐私策略").click()
            time.sleep(1)
            self.setting_page.get_element("版本声明").click()
            time.sleep(1)
            self.setting_page.get_element("退出关于",0).click()

            #查看游戏帮忙
            self.start_step("查看游戏帮助")
            self.setting_page.get_element("游戏帮助入口").click()
            self.setting_page.wait_element("游戏帮助同步标志")
            self.common.taskScreenShot("setting_help_pop.jpg")
            tabList = self.setting_page.get_element("tab列表")
            tabItems = self.setting_page.get_elements("tabItem")
            self.start_step("切换tab，查看不同类型游戏帮助")
            for i in range(self.helpItemCount):
                if(tabItems[i] != None):
                    tabItems[i].click()
                    time.sleep(1)
            if(len(tabItems) > self.helpItemCount):
                self.start_step("滑动左侧tab列表")
                self.common.swipeList(tabList)
            self.setting_page.get_element("退出游戏帮助").click()

            # 退出设置弹框
            self.setting_page.get_element("退出设置",0).click()
        except:
            self.common.platformLog("设置页面操作失败")
        finally:
            self.common.checkPopVisible(self.setting_page)
            self.hall_page.wait_element("同步标志")

        time.sleep(5)
        self.common.sendTagBroadcast(EnumSceneName.Setting, EnumSceneType.Stop)




# __qtaf_seq_tests__ = [C31107_DFQP_Setting_AboutUsSwitch]
if __name__ == '__main__':
    # C042_DFQP_Setting_floatBall = C042_DFQP_Setting_floatBall()
    # C042_DFQP_Setting_floatBall.debug_run()
    debug_run_all()
