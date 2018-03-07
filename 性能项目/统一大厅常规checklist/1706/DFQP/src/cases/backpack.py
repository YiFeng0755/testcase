#!/usr/bin/env/ python
#-*-coding:utf-8-*-

'''
性能测试场景之物品箱
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from cfg.constantEnum import EnumSceneName,EnumSceneType
from runcenter.testcase import debug_run_all,TestCase
from uilib.backpack_page import Backpack_Page
from uilib.hall_page import Hall_Page
from com.common import Common

class PerTest_QIPAIHALL_Backpack(TestCase):
    '''
    物品箱操作
    '''
    owner = "JessicZeng"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.backpack_Page = Backpack_Page()

    def run_test(self):
        '''
        测试步骤
        1、大厅点击物品箱入口
        2、点击兑换记录
        3、点击大厅同步标志，退出物品箱
        '''
        self.hall_page.wait_element("同步标志")

        #点击大厅物品箱入口
        self.start_step("点击大厅物品箱入口")
        self.common.sendTagBroadcast(EnumSceneName.Backpack,EnumSceneType.Start)

        try:
            #点击物品箱入口
            self.hall_page.get_element("物品箱",0).click()
            time.sleep(2)
            self.backpack_Page.wait_element("同步标志")
            self.common.taskScreenShot("openBackpackPop.jpg")

            #查看物品箱兑换记录
            self.start_step("查看物品箱兑换记录")
            self.backpack_Page.get_element("兑换记录按钮",0).click()
            self.backpack_Page.wait_element("兑换记录框同步标志")
            self.common.taskScreenShot("openBackpackPop.jpg")
            self.backpack_Page.get_element("兑换记录框关闭",0).click()
        except:
            print "操作物品箱失败"
        finally:
            self.common.checkPopVisible(self.backpack_Page)
            self.hall_page.wait_element("同步标志")

        time.sleep(5)
        self.common.sendTagBroadcast(EnumSceneName.Backpack, EnumSceneType.Stop)


# __qtaf_seq_tests__ = [C30990_DFQP_PersonInfo_EnterVIP]
if __name__ == '__main__':
    # C027_DFQP_PersonInfo_NicknameAlter = C027_DFQP_PersonInfo_NicknameAlter()
    # C027_DFQP_PersonInfo_NicknameAlter.debug_run()
    debug_run_all()
