#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
性能测试场景之兑换奖品
'''

import time
from runcenter.enums import EnumPriority,EnumStatus
from cfg.constantEnum import EnumSceneName,EnumSceneType
from runcenter.testcase import debug_run_all,TestCase
from uilib.exchange_page import Exchange_Page
from uilib.hall_page import Hall_Page
from common.common import Common

class PerTest_QIPAIHALL_Exchange(TestCase):
    '''
    兑换奖品场景
    '''
    owner = "JessicZeng"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 60

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.exchange_page = Exchange_Page()

    def run_test(self):
        '''
        测试用例
        '''
        self.hall_page.wait_element("同步标志")
        self.common.sendTagBroadcast(EnumSceneName.ExchangeRwd, EnumSceneType.Start)
        self.start_step("点击大厅兑换奖品入口")
        self.hall_page.wait_element("兑换奖品").click()
        try:
            self.exchange_page.wait_element("同步标志")
            self.common.taskScreenShot("openExchangePop.jpg")

            #循环点击tab
            self.start_step("循环点击tab，查看可兑换物品")
            tabs = self.exchange_page.get_elements("tabItem")
            for tab in tabs:
                tab.click()
                time.sleep(1)

            #显示兑换窗口
            try:
                self.start_step("查看兑换弹框，未实际兑换")
                self.exchange_page.get_element("兑换按钮").click()
                self.exchange_page.wait_element("兑换窗口同步标志")
                self.common.taskScreenShot("exchangeTips.jpg")
                time.sleep(1)
                self.exchange_page.get_element("兑换窗口关闭").click()
            except:
                self.common.platformLog("操作兑换对话框失败")

            #显示兑换记录
            self.start_step("查看兑换记录")
            self.exchange_page.get_element("兑奖记录").click()
            time.sleep(1)
            self.common.taskScreenShot("exchangeRecord.jpg")

            self.exchange_page.get_element("返回").click()
        except:
            self.common.platformLog("操作exchange对话框失败")
        finally:
            self.common.checkPopVisible(self.exchange_page)
            self.hall_page.wait_element("同步标志")

        time.sleep(2)
        self.common.sendTagBroadcast(EnumSceneName.ExchangeRwd, EnumSceneType.Stop)

# __qtaf_seq_tests__ = [C31107_DFQP_Setting_AboutUsSwitch]
if __name__ == '__main__':
    # C042_DFQP_Setting_floatBall = C042_DFQP_Setting_floatBall()
    PerTest_QIPAIHALL_Exchange.debug_run()
    debug_run_all()