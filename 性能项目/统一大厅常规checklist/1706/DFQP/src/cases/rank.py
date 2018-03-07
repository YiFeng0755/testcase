#!/usr/bin/env/ python
#-*-coding:utf-8-*-

'''
性能测试场景之大厅排行榜
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from cfg.constantEnum import EnumDirection,EnumItemCount,EnumSceneName,EnumSceneType
from runcenter.testcase import debug_run_all,TestCase
from uilib.rank_page import Rank_Page
from uilib.hall_page import Hall_Page
from com.common import Common

class PerTest_QIPAIHALL_Rank(TestCase):
    '''
    排行榜操作
    '''
    owner = "JessicZeng"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    global rank_item_count
    rank_item_count = 4
    #一页显示item个数

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.rankPage = Rank_Page()

    def run_test(self):
        '''
        测试步骤
        排行榜内容会重置，当关闭或切换tab后回到默认位置  eg。关闭后再打开默认显示今日内容   切换到新tag后，list index变为0
        操作步骤：
        1、检测同步标志是否出现
        2、点击第一个item，操作加好友   然后关闭用户信息弹框回到排行榜页面
        3、点击第二个item，操作举报（不良头像，然后点击举报按钮）
        4、滑动列表到底
        5、切换到富豪榜，滑动一页数据
        6、切换到昨日排行榜，滑动昨日之富豪榜一页数据
        7、切换tab到昨日收益榜  滑动一页数据
        8、关闭弹框，返回大厅
        '''
        self.hall_page.wait_element("同步标志")

        #点击排行榜大厅入口，进入排行榜
        self.start_step("点击大厅排行榜入口")
        self.common.sendTagBroadcast(EnumSceneName.Rank,EnumSceneType.Start)

        try:
            self.hall_page.get_element("排行榜",0).click()
            time.sleep(2)
            self.rankPage.wait_element("同步标志")
            self.common.taskScreenShot("openRankPop.jpg")
            headEls = self.rankPage.get_elements("用户头像")
            # 查看排行第一的用户信息，并执行加好友操作
            if len(headEls) >= 1:
                self.start_step("查看rank1的用户信息，并加为好友")
                headEls[0].click()
                self.rankPage.wait_element("用户信息框同步标志")
                self.common.taskScreenShot("playerInfoPop.jpg")
                time.sleep(1)
                self.rankPage.get_element("加好友",0).click()
                time.sleep(1)
                self.rankPage.get_element("用户信息框关闭按钮",0).click()

            # 查看排行第二的用户信息，并执行举报操作
            if len(headEls) >= 2:
                self.start_step("查看rank2的用户信息，并执行查看举报弹框然后取消举报")
                headEls[1].click()
                self.rankPage.wait_element("用户信息框同步标志")
                time.sleep(1)
                self.rankPage.get_element("举报",0).click()
                time.sleep(1)
                self.common.taskScreenShot("reportOtherpop.jpg")
                self.rankPage.wait_element("色情昵称").click()
                time.sleep(1)
                self.rankPage.get_element("取消举报",0).click()

            # 滑动今日收益排行榜，并滑动到底
            self.start_step("滑动今日收益榜，并滑动到底")
            self.common.taskScreenShot("todayIncomeRank.jpg")
            self.swipeListView(True)

            # 切换到昨日富豪榜，并将列表滑动一页
            self.start_step("滑动一页昨日富豪榜")
            self.rankPage.get_element("日期",0).click()
            time.sleep(1)
            self.common.taskScreenShot("yesterdayRegalRank.jpg")
            # 当文字发生改变时，表示切换成功
            while self.rankPage.get_element("日期文字").get_attribute("text") == '昨日':
                None
                self.swipeListView(False)

            # 返回大厅
            self.rankPage.get_element("返回大厅",0).click()
        except:
            self.common.platformLog("排行榜操作失败")
        finally:
            self.common.checkPopVisible(self.rankPage)
            self.hall_page.wait_element("同步标志")

        time.sleep(5)
        self.common.sendTagBroadcast(EnumSceneName.Rank, EnumSceneType.Stop)

    def swipeListView(self,loop):
        '''
        滑动指定列表
        :param listName:  列表元素名
        :param itemName:  列表item元素名
        :param loop:  是否循环滑动到底
        :return:
        '''
        listView = None
        itemViews = None
        try:
            listView = self.rankPage.get_element("排行榜列表")
            # itemViews = self.rankPage.get_elements("排行榜item")
        except:
            self.common.platformLog("排行榜指定列表元素不存在，结束列表滑动测试")
            return

        cnt = 1
        while cnt < 10:
            # for item in itemViews:
            #     Common.printStr("item x y:",item.location["x"]," ",item.location["y"])
            # self.com.swipeList(listView)
            # if loop == False:
            #     break
            # itemViews = self.rankPage.get_elements("排行榜item")
            self.common.swipeList(listView)
            if loop == False:
                break
            cnt = cnt + 1
            time.sleep(0.2)
        time.sleep(1)
