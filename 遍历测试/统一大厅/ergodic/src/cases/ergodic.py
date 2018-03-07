#!/usr/bin/python
# -*- coding:utf-8 -*-
import os,shutil,time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from common.common import Common
from uilib.hall_page import Hall_Page
from common.ergodic_util import dumpfile,get_btn_list_json,get_btn_list_ini,save_btn_list,click_btn,add_to_btn_black,filter_BtnBlackClicked
from utils.confighelper import ConfigHelper
import utils.constant as constant

cfg_path = constant.cfg_path
print 'cfg_path:%s'%cfg_path
serial = cfg_path.split('/')[-3]
config = ConfigHelper('./%s/cfg/cfg.ini'%serial)

class ERGODIC(TestCase):
    '''
    遍历
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 666

    def pre_test(self):
        current_path = os.getcwd()
        print 'current path:%s' % current_path
        self.start_step('删除上一次任务留下的状态文件')
        if os.path.exists('./%s/cfg/btn.ini'%serial):
            os.remove('./%s/cfg/btn.ini'%serial)
            print '删除./%s/cfg/btn.ini文件'%serial
        if os.path.exists('./%s/cfg/btn_black.json'%serial):
            os.remove('./%s/cfg/btn_black.json'%serial)
            print '删除./%s/cfg/btn_black.json文件'%serial
        if os.path.exists('./%s/cfg/btn_clicked.json'%serial):
            os.remove('./%s/cfg/btn_clicked.json'%serial)
            print '删除./%s/cfg/btn_clicked.json文件'%serial
        if os.path.exists('./%s/cfg/NoNeedBackPath.json'%serial):
            os.remove('./%s/cfg/NoNeedBackPath.json'%serial)
            print '删除./%s/cfg/NoNeedBackPath.json文件'%serial
        if os.path.exists('./%s/hall'%serial):
            shutil.rmtree('./%s/hall'%serial)
            print '删除./%s/hall文件夹'%serial
        self.common = Common()
        self.hall_page = Hall_Page()
        self.start_step("初始化环境")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)




    def run_test(self):

        self.start_step("等待页面加载完成")

        self.hall_page.wait_element("同步标志")
        self.start_step('开始遍历')
        path = './%s/hall/'%serial
        print '当前路径：' + path
        dumpfile(path,self.luadriver)
        btn_list = get_btn_list_json(path)
        btn_black = [  # 大厅
            'sendStripsBtn', 'test', 'prepublish', 'online', 'hall', 'Button_match',


            # 关闭、返回按钮
            'Button_return', 'returnBtn', 'close', 'closeBtn', 'backBtn', 'back', 'Button_close',
            'cityInfoArea',
            #其它
            'friendBtn'
        ]
        add_to_btn_black(btn_black)
        clickable_btn = filter_BtnBlackClicked(btn_list)
        print '当前路径下的可点击按钮clickable_btn=%s' % clickable_btn
        save_btn_list(path, clickable_btn)
        driver = self.luadriver
        driver.keyevent(4)
        dumpfile('./%s/hall/backwards/'%serial,driver)
        driver.keyevent(4)
        btn = clickable_btn[0]

        click_btn(driver,path,btn)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.start_step('遍历结束')
        self.common.closedriver()

if __name__ == '__main__':
    debug_run_all()
