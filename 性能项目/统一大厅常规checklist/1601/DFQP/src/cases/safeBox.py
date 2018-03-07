#!/usr/bin/env/ python
#-*-coding:utf-8-*-

'''
性能测试场景之保险箱
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from cfg.constantEnum import EnumSceneName,EnumSceneType
from runcenter.testcase import debug_run_all,TestCase
from uilib.safebox_page import Safebox_Page
from uilib.hall_page import Hall_Page
from common.common import Common

class PerTest_QIPAIHALL_SafeBox(TestCase):
    '''
    保险箱操作
    '''
    owner = "JessicZeng"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.safeBox_Page = Safebox_Page()

    def run_test(self):
        '''
        测试步骤
        1、大厅点击保险箱入口   每次进入都会先金进入银币tab，不用再单独天机银币tab
        3、点击金币保险箱
        4、退出
        '''
        self.hall_page.wait_element("同步标志")

        self.start_step("点击大厅保险箱入口")
        self.common.sendTagBroadcast(EnumSceneName.SafeBox,EnumSceneType.Start)

        try:
            #点击物品箱入口
            self.hall_page.get_element("保险箱").click()
            time.sleep(2)
            self.safeBox_Page.wait_element("同步标志")
            self.common.taskScreenShot("silverSafebox.jpg")

            #操作金币保险箱
            self.start_step("操作金条保险箱")
            self.safeBox_Page.get_element("金条tab").click()
            time.sleep(1)
            self.common.taskScreenShot("goldSafebox.jpg")
        except:
            self.common.platformLog("操作保险箱失败")

        finally:
            self.common.checkPopVisible(self.safeBox_Page)
            self.hall_page.wait_element("同步标志")

        time.sleep(2)
        self.common.sendTagBroadcast(EnumSceneName.SafeBox, EnumSceneType.Stop)


# __qtaf_seq_tests__ = [C30990_DFQP_PersonInfo_EnterVIP]
if __name__ == '__main__':
    # C027_DFQP_PersonInfo_NicknameAlter = C027_DFQP_PersonInfo_NicknameAlter()
    # C027_DFQP_PersonInfo_NicknameAlter.debug_run()
    debug_run_all()
