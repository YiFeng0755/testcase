#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#Author: Lucyliu

'''
性能测试环境配置
'''
from runcenter.enums import EnumStatus, EnumPriority
from runcenter.testcase import TestCase
from com.common import Common

class PerTest_INITENV(TestCase):
    '''
    初始化整个测试环境
    创建driver，整个项目共用的driver
    获取启动完成时间
    启动性能采集apk
    关闭页面上的系统弹框和活动页面
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def run_test(self):
        print "PerTest_INITENV**************"
        self.common = Common()
        self.common.platformLog("PerTest_INITENV 初始化整个测试环境")
        self.common.setupdriver()
        self.common.deletefile()
        self.common.getResumeTime()
        self.common.startCollectApp()
        self.common.closeactivity()
        mid = self.common.get_mid()

class PerTest_CLEARENV(TestCase):
    '''
    测试完成，清理测试环境
    '''
    owner = "LucyLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def run_test(self):
        print "PostTest_CLEARENV*************"
        self.common = Common()
        self.common.platformLog("PerTest_CLEARENV 测试完成，清理测试环境")
        self.common.sendStopServiceBroad()
        self.common.closedriver()


