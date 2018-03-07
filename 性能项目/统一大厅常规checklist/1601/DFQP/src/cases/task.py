#!usr/bin/env python
#-*-coding:utf-8-*-
'''
性能测试场景之签到及每日任务
'''
import time
from runcenter.enums import EnumStatus, EnumPriority
from cfg.constantEnum import EnumSceneName,EnumSceneType
from runcenter.testcase import TestCase
from common.common import Common
from uilib.hall_page import Hall_Page
from uilib.task_page import Task_Page


class PerTest_QIPAIHALL_Task(TestCase):
    '''
    任务场景
    '''
    owner = "JessicZeng"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 60

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.task_page = Task_Page()

    def run_test(self):
        '''
        任务场景测试步骤
        :return:
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击大厅任务入口")
        self.common.sendTagBroadcast(EnumSceneName.Task, EnumSceneType.Start)
        try:
            self.hall_page.wait_element("任务").click()
            self.task_page.wait_element("同步标志")
            self.task_page.get_element("每日签到tab").click()
            time.sleep(2)
            self.common.taskScreenShot("qiandaoView.jpg")

            #若今日签到按钮存在，则点击
            try:
                #若按钮存在并签到成功，会直接跳转到补签页面
                self.task_page.get_element("签到按钮").click()
                time.sleep(1)
            except:
                self.common.platformLog("今日签到按钮不存在or领取今日签到奖励失败")

            #查看购买补签卡界面
            self.start_step("购买补签卡界面")
            self.task_page.wait_element("获取补签卡").click()
            self.task_page.wait_element("补签卡购买框同步标志")
            self.common.taskScreenShot("buyBuqianPop.jpg")
            self.task_page.get_element("取消购买补签卡").click()
            time.sleep(1)

            #进行补签操作，目前没有实际进行补签操作  只是查看补签框
            # try:
            #     buItmes = self.task_page.get_elements("补签item")
            #     print "长度："+len(buItmes)
            #     if(buItmes != None and len(buItmes) > 0):
            #         buItmes[0].click()
            #         self.task_page.wait_element("补签对话框标志")
            #         time.sleep(1)
            #         self.task_page.get_element("关闭补签对话框").click()
            #     else:
            #         print "!! buItmes != null and len(buItmes) > 0"
            # except:
            #     print "没有可补签项，或执行补签操作失败"

            #查看每日任务列表，若列表可滑动则进行滑动操作
            self.start_step("查看每日任务界面")
            self.task_page.get_element("每日任务tab").click()
            try:
                listView = self.task_page.wait_element("taskList")
                self.common.taskScreenShot("taskView.jpg")
                taskItems = self.task_page.get_elements("taskItem")
                if (len(taskItems) > 4):
                    self.start_step("滑动每日任务列表")
                    self.common.swipeList(listView)
            except:
                self.common.platformLog("查看任务列表失败")

            #关闭每日任务弹框
            self.task_page.get_element("关闭按钮").click()
        except:
            self.common.platformLog("操作任务场景失败")
        finally:
            self.common.checkPopVisible(self.task_page)
            self.hall_page.wait_element("同步标志")

        time.sleep(2)
        self.common.sendTagBroadcast(EnumSceneName.Task, EnumSceneType.Stop)