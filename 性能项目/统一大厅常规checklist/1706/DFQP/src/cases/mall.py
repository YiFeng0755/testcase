#!/usr/bin/env/ python
#-*-coding:utf-8-*-

'''
性能测试场景之商城
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from cfg.constantEnum import EnumSceneName,EnumSceneType
from runcenter.testcase import debug_run_all,TestCase
from uilib.mall_page import Mall_Page
from uilib.hall_page import Hall_Page
from com.common import Common

class PerTest_QIPAIHALL_Mall(TestCase):
    '''
    商城操作
    '''
    owner = "JessicZeng"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.mall_Page = Mall_Page()

    def run_test(self):
        '''
        测试步骤
        1、大厅点击商城入口
        2、点击第一金条购买item，关闭购买框
        3、滑动金条购买列表
        4、切换到银币购买列表
        5、滑动银币购买列表
        6、切换到道具列表
        7、执行购买第一个道具操作，打开购买弹框后取消购买操作
        8、滑动道具列表
        9、切换到VIP页
        10、返回大厅
        不同类型的商品列表，共用listView和Item
        '''
        self.hall_page.wait_element("同步标志")

        self.start_step("点击大厅商城入口")
        self.common.sendTagBroadcast(EnumSceneName.Mall,EnumSceneType.Start)

        try:
            #点击商城
            self.hall_page.get_element("商城",0).click()
            time.sleep(2)
            self.mall_Page.wait_element("同步标志")
            self.common.taskScreenShot("openMallPop.jpg")

            #购买金条（选择第一个item）并滑动金条列表
            self.start_step("购买金条")
            self.mall_Page.get_element("item0",0).click()
            self.mall_Page.wait_element("金条购买框Flag")
            self.common.taskScreenShot("buyGoldPop.jpg")
            self.mall_Page.get_element("金条购买框关闭",0).click()
            time.sleep(1)
            self.start_step("滑动金条列表")
            self.common.swipeList(self.mall_Page.get_element("物品列表"))

            #切换到银币页并滑动列表
            self.start_step("切换到银币Tab")
            self.mall_Page.get_element("银币Tab",0).click()
            time.sleep(2)
            self.common.taskScreenShot("silverView.jpg")
            self.start_step("滑动银币列表")
            self.common.swipeList(self.mall_Page.get_element("物品列表"))

            #切换到道具页面，并查看购买道具框，最后滑动列表
            self.start_step("切换到道具Tab")
            self.mall_Page.get_element("道具Tab",0).click()
            time.sleep(2)
            self.common.taskScreenShot("propView.jpg")
            self.start_step("购买道具")
            self.mall_Page.get_element("item0",0).click()
            self.mall_Page.wait_element("道具购买框Flag")
            self.common.taskScreenShot("buyPropPop.jpg")
            self.mall_Page.get_element("道具购买框关闭",0).click()
            time.sleep(1)
            self.start_step("滑动道具列表")
            self.common.swipeList(self.mall_Page.get_element("物品列表"))

            #切换到VIP
            self.start_step("切换到VIPTab")
            self.mall_Page.get_element("VIPTab",0).click()
            time.sleep(2)
            self.common.taskScreenShot("vipView.jpg")

            #关闭商城弹框
            self.mall_Page.get_element("商城关闭",0).click()



        except:
            self.common.platformLog("操作商城失败")

        finally:
            self.common.checkPopVisible(self.mall_Page)
            self.hall_page.wait_element("同步标志")

        time.sleep(5)
        self.common.sendTagBroadcast(EnumSceneName.Mall, EnumSceneType.Stop)


# __qtaf_seq_tests__ = [C30990_DFQP_PersonInfo_EnterVIP]
if __name__ == '__main__':
    # C027_DFQP_PersonInfo_NicknameAlter = C027_DFQP_PersonInfo_NicknameAlter()
    # C027_DFQP_PersonInfo_NicknameAlter.debug_run()
    debug_run_all()
