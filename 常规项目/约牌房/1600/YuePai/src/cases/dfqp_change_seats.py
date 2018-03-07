#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
换座
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.hall_page import Hall_Page
from uilib.yuepai_page import Yuepai_Page
from common.common import Common

class C61014_Huanzhuo_Appear(TestCase):
    '''
   查看房间内换座显示
    '''
    owner = "ShelleyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):

        self.common = Common()
        self.hall_page = Hall_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化driver")
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.common.closefloatBall()

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入约牌页面")
        self.hall_page.wait_element("约牌").click()
        self.start_step("创建免费记分房")
        self.yuepai_page.wait_element('记分房',20).click()
        time.sleep(6)
        self.start_step("获取左边游戏列表")
        elements = self.yuepai_page.game_list()
        self.log_info("记分房有个列表个数为：%d个" % len(elements))
        for i in range(0, len(elements)):
            elements[i].click()
            self.start_step("进入%s记分房" % elements[i].get_attribute("text"))
            self.yuepai_page.enter_room()
            try:
                self.yuepai_page.wait_element("换座位").click()
            except:
                self.log_info("无法换座位")
            self.yuepai_page.screenshot("%d.png" %i)
            self.yuepai_page.exit_yuepai_page()
            try:
                self.yuepai_page.wait_element('记分房').click()
            except:
                self.log_info("未返回到记分房页面")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

__qtaf_seq_tests__ = [C61014_Huanzhuo_Appear]
if __name__ == '__main__':
    # C039_DFQP_Activity = C039_DFQP_Activity()
    # C039_DFQP_Activity.debug_run()
    debug_run_all()
