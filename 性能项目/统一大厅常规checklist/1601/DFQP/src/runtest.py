# -*- coding: utf-8 -*-
'''
Created on 2017年3月13日
@author: AppleWang
'''
import os,datetime,time
import shutil
import sys
import utils.util as util
from utils.confighelper import ConfigHelper
import utils.constant as constant
from common.common import Common
from common.globalVars import singleGlobalVar
from runcenter.runner import TestRunner,TestCaseSettings
from runcenter.report import XMLTestReport,EmptyTestReport
from runcenter.testresult import StreamResult

class RunTest(object):
    '''批量执行测试用例，通过模块名来执行，如args=cases
    '''                  
    def __init__(self,device):
        self.device=device
        self.isDebug = False
    
    def runtest(self, args):
        '''
        args参数为数组类型
        '''                  
        test_conf = TestCaseSettings(args)
        #读配置
        config=ConfigHelper(constant.cfg_path)   
        report_formal=config.getValue('report','reportFormal')
        if report_formal=='XMLReport':
            runner = TestRunner(XMLTestReport(self.device))
        else:
            runner = TestRunner(EmptyTestReport(lambda tc: StreamResult()))
        print test_conf
        runner.run(test_conf)

    def initEnv(self):
        '''
        初始化整个测试环境
        创建driver，整个项目共用的driver
        删除文件(data文件和性能结果文件)
        获取启动完成时间
        启动性能采集apk
        关闭页面上的系统弹框和活动页面
        :return:
        '''
        self.common = Common()
        self.common.platformLog("runtest.initEnv 初始化整个测试环境")
        self.common.setupdriver()
        self.common.deletefile()
        self.common.getResumeTime()
        self.common.startCollectApp()
        if(self.isDebug):
            time.sleep(10)
        else:
            self.common.closeActivity()

    def clearEnv(self):
        self.common.platformLog("runtest.clearEnv 测试完成，清理测试环境")
        self.common.sendStopServiceBroad()
        self.common.closedriver()

if __name__ == '__main__':
    #获取device_name参数
    device = None
    try:
        device=str(sys.argv[1])
    except:
        print "no devicename"
    if device == None:
        cfg_path = os.sep.join([util.getrootpath(), 'cfg', 'cfg.ini'])
        config = ConfigHelper(cfg_path)
        device = config.getValue('appium', 'deviceName')
        cfgfiletmp = os.sep.join([util.getrootpath(),device,'cfg'])
        if os.path.exists(cfgfiletmp):
            pass
        else:
            os.makedirs(cfgfiletmp)
        shutil.copy(cfg_path, cfgfiletmp)
        cfgfile = os.sep.join([util.getrootpath(), device, 'cfg', 'cfg.ini'])
        logfile = os.sep.join([util.getrootpath(),device,'logs'])
        if os.path.exists(logfile):
            pass
        else:
            os.makedirs(logfile)
    else:
        #根据device写入配置
        cfgfile=os.sep.join([util.getrootpath(), device,'cfg','cfg.ini'])
        logfile=os.sep.join([util.getrootpath(), device,'logs'])
    constant.cfg_path=cfgfile
    constant.log_path=logfile
    config=ConfigHelper(constant.cfg_path) 
    cases=config.getValue('runtest','cases')
    cases=cases.split(',')
    print "#"*20
    print cases
    runtest=RunTest(device)
    runtest.initEnv()
    runtest.runtest(cases)
    runtest.clearEnv()

