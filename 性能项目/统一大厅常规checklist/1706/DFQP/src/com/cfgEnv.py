#!/usr/bin/env/ python
#-*-coding:utf-8-*-

'''
性能测试环境配置
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from cfg.constantEnum import EnumSceneName,EnumSceneType
from runcenter.testcase import TestCase
from uilib.hall_page import Hall_Page
from common import Common

class PerTest_INITENV(TestCase):
    '''
    初始化测试环境
    '''
    owner = "JessicZeng"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def run_test(self):
        '''
        初始化整个测试环境
        创建driver，整个项目共用的driver
        删除文件(data文件和性能结果文件)
        获取启动完成时间
        启动性能采集apk
        关闭页面上的系统弹框和活动页面
        关闭悬浮球
        :return:
        '''
        print "PerTest_INITENV**************"
        self.common = Common()
        self.common.platformLog("PerTest_INITENV 初始化整个测试环境")
        self.common.setupdriver()
        self.common.deletefile()
        self.common.getResumeTime()
        self.common.startCollectApp()
        self.common.closeActivity()
        self.common.closefloatBall()


class PerTest_CLEARENV(TestCase):
    '''
    测试完成，清理测试环境
    '''
    owner = "JessicZeng"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def run_test(self):
        print "PerTest_CLEARENV*************"
        self.common = Common()
        self.common.platformLog("PerTest_CLEARENV 测试完成，清理测试环境")
        self.common.sendStopServiceBroad()
        self.common.closedriver()
