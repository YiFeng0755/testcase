# -*- coding: utf-8 -*-
'''
Created on 2017年3月13日
@author: AppleWang
'''
import os
import shutil
import sys
import utils.util as util
from utils.confighelper import ConfigHelper
import utils.constant as constant
from runcenter.runner import TestRunner, TestCaseSettings
from runcenter.report import XMLTestReport, EmptyTestReport
from runcenter.testresult import StreamResult


class RunTest(object):
    '''批量执行测试用例，通过模块名来执行，如args=cases
    '''

    def __init__(self, device):
        self.device = device

    def runtest(self, args):
        '''
        args参数为数组类型
        '''
        test_conf = TestCaseSettings(args)
        #         print 'test_conf:',test_conf
        # 读配置
        config = ConfigHelper(constant.cfg_path)
        print constant.cfg_path
        report_formal = config.getValue('report', 'reportFormal')
        if report_formal == 'XMLReport':
            # if self.device == None:
            #     runner = TestRunner(XMLTestReport('cases'))
            # else:
            runner = TestRunner(XMLTestReport(self.device))
        else:
            runner = TestRunner(EmptyTestReport(lambda tc: StreamResult()))
        runner.run(test_conf)


if __name__ == '__main__':
    # 获取device_name参数
    device = None
    try:
        device = str(sys.argv[1])
    except:
        print "no devicename"
    if device == None:
        cfg_path = os.sep.join([util.getrootpath(), 'cfg', 'cfg.ini'])
        config = ConfigHelper(cfg_path)
        device = config.getValue('appium', 'deviceName')
        cfgfiletmp = os.sep.join([util.getrootpath(), device, 'cfg'])
        if os.path.exists(cfgfiletmp):
            pass
        else:
            os.makedirs(cfgfiletmp)
        shutil.copy(cfg_path, cfgfiletmp)
        cfgfile = os.sep.join([util.getrootpath(), device, 'cfg', 'cfg.ini'])
        logfile = os.sep.join([util.getrootpath(), device, 'logs'])
        if os.path.exists(logfile):
            pass
        else:
            os.makedirs(logfile)
            # use_cfg = config.getValue('casecfg', 'user_cfg')
    else:
        # 根据device写入配置
        cfgfile = os.sep.join([util.getrootpath(), device, 'cfg', 'cfg.ini'])
        logfile = os.sep.join([util.getrootpath(), device, 'logs'])
        config1 = ConfigHelper(cfgfile)
        use_cfg = config1.getValue('casecfg', 'user_cfg')
        if use_cfg != "undefined":
            constant.user_cfg = use_cfg
            print use_cfg
    constant.cfg_path = cfgfile
    constant.log_path = logfile
    # print constant.user_cfg
    config = ConfigHelper(constant.cfg_path)
    # 执行初始化用例
    init_cases = 'cases.initialize'
    if (len(init_cases) != 0):
        # cases+=init_cases
        init_cases = init_cases.split(',')
        runtest = RunTest(device)
        runner = TestRunner(EmptyTestReport(lambda tc: StreamResult()))
        test_conf = TestCaseSettings(init_cases)
        runner.run(test_conf)
    # 执行功能用例
    cases = config.getValue('runtest', 'cases')
    cases = cases.split(',')
    runtest = RunTest(device)
    runtest.runtest(cases)


