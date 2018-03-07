#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
结算
'''
import time,re
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from common.common import Common
from uilib.hall_page import Hall_Page
from uilib.game_page import Game_Page
from uilib.yuepai_page import Yuepai_Page
import common.Interface as PHPInterface

class C27416_PersonalInfomation(TestCase):
    '''
    结算时个人信息弹框关闭情况
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化环境")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('获取mid')
        self.hall_page.wait_element('测试按钮').click()
        element = self.luadriver.find_lua_element_by_name('uid')
        text = element.get_attribute('text')
        global mid
        mid = int(re.search('\d+', text).group())
        print mid
        self.hall_page.wait_element('关闭测试页面').click()
        self.hall_page.wait_element('葫芦岛麻将').click()
        try:
            self.game_page.wait_element('资源下载-确定').click()
        except:
            print '游戏已下载'
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 1)
        Flag = True
        while Flag:
            try:
                self.hall_page.wait_element('场次名称')
                Flag = False
            except:
                pass
            time.sleep(1)
        self.hall_page.wait_element('场次名称').click()
        time.sleep(5)
        self.hall_page.wait_element('准备').click()
        time.sleep(5)
        Eles = self.game_page.get_elements('游戏内头像')
        Ele_ymax = Eles[0]
        for Ele in Eles:
            if int(Ele.location['y']) > int(Ele_ymax.location['y']):
                Ele_ymax = Ele
        Ele_ymax.click()
        time.sleep(2)
        self.hall_page.screenshot('游戏内头像.png')
        Flag = True
        while Flag :
            try:
                self.game_page.wait_element('game2601换桌')
                Flag = False
            except:
                print '玩牌中'
            time.sleep(2)
        self.hall_page.screenshot('结算页面弹出.png')
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 0)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.set_coin(mid,10000)
        self.common.closedriver()

class C27434_FriendInvitation(TestCase):#暂时不能写
    '''
    结算时邀请好友弹框关闭情况
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.yuepai_page = Yuepai_Page()
        self.start_step("初始化环境")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('获取mid')
        self.hall_page.wait_element('测试按钮').click()
        element = self.luadriver.find_lua_element_by_name('uid')
        text = element.get_attribute('text')
        global mid
        mid = int(re.search('\d+', text).group())
        print mid
        self.hall_page.wait_element('关闭测试页面').click()
        self.start_step('进入约牌')
        self.hall_page.wait_element('约牌').click()
        time.sleep(4)
        self.start_step('进入记分房')
        self.yuepai_page.wait_element('记分房').click()
        elements = self.yuepai_page.get_elements('子游戏')
        for element in elements:
            if element.get_attribute('text') == '斗地主':
                element.click()
        try:
            self.yuepai_page.wait_element('确定').click()
        except:
            print '已下载'
        PHPInterface.set_robot_flag(0, 0, 0, 12, 1)
        Flag = True
        while Flag:
            try:
                self.yuepai_page.wait_element('百分比')
            except:
                Flag = False
            time.sleep(2)
        self.start_step('点击开房')
        self.yuepai_page.wait_element('开房').click()
        time.sleep(5)
        try:
            self.yuepai_page.wait_element('准备').click()
        except:
            print '已准备'
        time.sleep(5)
        self.yuepai_page.wait_element('+邀请').click()
        time.sleep(2)
        self.hall_page.screenshot('1.png')
        Flag = True
        while Flag:
            try:
                self.game_page.wait_element('game20结算框标志')
                Flag = False
            except:
                print '玩牌中'
            time.sleep(2)
        self.hall_page.screenshot('2.png')
        PHPInterface.set_robot_flag(0, 0, 0, 12, 0)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.set_coin(mid,10000)
        self.common.closedriver()

class C27416_FriendFrame(TestCase):
    '''
    结算时加好友弹框关闭情况
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化环境")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('获取mid')
        self.hall_page.wait_element('测试按钮').click()
        element = self.luadriver.find_lua_element_by_name('uid')
        text = element.get_attribute('text')
        global mid
        mid = int(re.search('\d+', text).group())
        print mid
        self.hall_page.wait_element('关闭测试页面').click()
        self.hall_page.wait_element('葫芦岛麻将').click()
        try:
            self.game_page.wait_element('资源下载-确定').click()
        except:
            print '游戏已下载'
        PHPInterface.set_robot_flag(2601,0,0,12,1)
        Flag = True
        while Flag:
            try:
                self.hall_page.wait_element('场次名称')
                Flag = False
            except:
                pass
            time.sleep(1)
        self.hall_page.wait_element('场次名称').click()
        time.sleep(5)
        self.hall_page.wait_element('准备').click()
        time.sleep(5)
        Eles = self.game_page.get_elements('游戏内头像')
        Ele_ymin = Eles[0]
        for Ele in Eles:
            if int(Ele.location['y']) < int(Ele_ymin.location['y']):
                Ele_ymin = Ele
        Ele_ymin.click()
        time.sleep(2)
        self.hall_page.screenshot('游戏内其他玩家头像.png')
        Flag = True
        while Flag :
            try:
                self.game_page.wait_element('game2601换桌')
                Flag = False
            except:
                print '玩牌中'
            time.sleep(2)
        self.hall_page.screenshot('结算页面弹出.png')
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 0)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.set_coin(mid,10000)
        self.common.closedriver()

class C27657_Settlement_OneMoreGame(TestCase):
    '''
    结算界面点击继续（再来一局）
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化环境")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('获取mid')
        self.hall_page.wait_element('测试按钮').click()
        element = self.luadriver.find_lua_element_by_name('uid')
        text = element.get_attribute('text')
        global mid
        mid = int(re.search('\d+', text).group())
        print mid
        self.hall_page.wait_element('关闭测试页面').click()
        self.hall_page.wait_element('葫芦岛麻将').click()
        try:
            self.game_page.wait_element('资源下载-确定').click()
        except:
            print '游戏已下载'
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 1)
        Flag = True
        while Flag:
            try:
                self.hall_page.wait_element('场次名称')
                Flag = False
            except:
                pass
            time.sleep(1)
        self.hall_page.wait_element('场次名称').click()
        time.sleep(5)
        self.hall_page.wait_element('准备').click()
        time.sleep(2)
        self.hall_page.screenshot('进入房间.png')
        Flag = True
        while Flag:
            try:
                self.game_page.wait_element('game2601继续')
                Flag = False
            except:
                print '玩牌中'
            time.sleep(2)
        self.hall_page.screenshot('结算页面.png')
        self.game_page.wait_element('game2601继续').click()
        time.sleep(2)
        self.hall_page.screenshot('结算界面弹出后点击继续.png')
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 0)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.set_coin(mid,10000)
        self.common.closedriver()

class C27658_Settlement_Changetable(TestCase):
    '''
    结算界面点击换桌
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化环境")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('获取mid')
        self.hall_page.wait_element('测试按钮').click()
        element = self.luadriver.find_lua_element_by_name('uid')
        text = element.get_attribute('text')
        global mid
        mid = int(re.search('\d+', text).group())
        print mid
        self.hall_page.wait_element('关闭测试页面').click()
        self.hall_page.wait_element('葫芦岛麻将').click()
        try:
            self.game_page.wait_element('资源下载-确定').click()
        except:
            print '游戏已下载'
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 1)
        Flag = True
        while Flag:
            try:
                self.hall_page.wait_element('场次名称')
                Flag = False
            except:
                pass
            time.sleep(1)
        self.hall_page.wait_element('场次名称').click()
        time.sleep(5)
        self.hall_page.wait_element('准备').click()
        time.sleep(2)
        self.hall_page.screenshot('进入房间.png')
        Flag = True
        while Flag:
            try:
                self.game_page.wait_element('game2601换桌')
                Flag = False
            except:
                print '玩牌中'
            time.sleep(2)
        self.hall_page.screenshot('结算页面.png')
        self.game_page.wait_element('game2601换桌').click()
        time.sleep(2)
        self.hall_page.screenshot('结算页面弹出后点击换桌.png')
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 0)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.set_coin(mid,10000)
        self.common.closedriver()

class C27659_Settlement_Changetable(TestCase):
    '''
    结算动画未播放完成的时候点击继续、换桌
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化环境")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('获取mid')
        self.hall_page.wait_element('测试按钮').click()
        element = self.luadriver.find_lua_element_by_name('uid')
        text = element.get_attribute('text')
        global mid
        mid = int(re.search('\d+', text).group())
        print mid
        self.hall_page.wait_element('关闭测试页面').click()
        self.hall_page.wait_element('葫芦岛麻将').click()
        try:
            self.game_page.wait_element('资源下载-确定').click()
        except:
            print '游戏已下载'
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 1)
        Flag = True
        while Flag:
            try:
                self.hall_page.wait_element('场次名称')
                Flag = False
            except:
                pass
            time.sleep(1)
        self.hall_page.wait_element('场次名称').click()
        time.sleep(5)
        self.hall_page.wait_element('准备').click()
        time.sleep(2)
        self.hall_page.screenshot('进入房间.png')
        Flag = True
        while Flag:
            try:
                self.game_page.wait_element('game2601换桌')
                Flag = False
            except:
                print '玩牌中'
            time.sleep(2)
        self.hall_page.screenshot('结算页面.png')
        self.game_page.wait_element('game2601换桌').click()
        time.sleep(2)
        self.hall_page.screenshot('结算页面弹出后点击换桌.png')
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 0)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.set_coin(mid,10000)
        self.common.closedriver()

class C27660_Settlement_Close(TestCase):
    '''
    关闭结算界面
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化环境")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('获取mid')
        self.hall_page.wait_element('测试按钮').click()
        element = self.luadriver.find_lua_element_by_name('uid')
        text = element.get_attribute('text')
        global mid
        mid = int(re.search('\d+', text).group())
        print mid
        self.hall_page.wait_element('关闭测试页面').click()
        self.hall_page.wait_element('葫芦岛麻将').click()
        try:
            self.game_page.wait_element('资源下载-确定').click()
        except:
            print '游戏已下载'
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 1)
        Flag = True
        while Flag:
            try:
                self.hall_page.wait_element('场次名称')
                Flag = False
            except:
                pass
            time.sleep(1)
        self.hall_page.wait_element('场次名称').click()
        time.sleep(5)
        self.hall_page.wait_element('准备').click()
        time.sleep(2)
        self.hall_page.screenshot('进入房间.png')
        Flag = True
        while Flag:
            try:
                self.game_page.wait_element('game2601换桌')
                Flag = False
            except:
                print '玩牌中'
            time.sleep(2)
        self.hall_page.screenshot('结算页面.png')
        self.game_page.wait_element('game2601关闭').click()
        time.sleep(2)
        self.hall_page.screenshot('关闭结算页面.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.set_coin(mid,10000)
        self.common.closedriver()

class C27661_Settlement_CloseAndChangetable(TestCase):
    '''
    关闭结算界面，查看准备、换桌
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化环境")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('获取mid')
        self.hall_page.wait_element('测试按钮').click()
        element = self.luadriver.find_lua_element_by_name('uid')
        text = element.get_attribute('text')
        global mid
        mid = int(re.search('\d+', text).group())
        print mid
        self.hall_page.wait_element('关闭测试页面').click()
        self.hall_page.wait_element('葫芦岛麻将').click()
        try:
            self.game_page.wait_element('资源下载-确定').click()
        except:
            print '游戏已下载'
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 1)
        Flag = True
        while Flag:
            try:
                self.hall_page.wait_element('场次名称')
                Flag = False
            except:
                pass
            time.sleep(1)
        self.hall_page.wait_element('场次名称').click()
        time.sleep(5)
        self.hall_page.wait_element('准备').click()
        time.sleep(2)
        self.hall_page.screenshot('进入房间.png')
        Flag = True
        while Flag:
            try:
                self.game_page.wait_element('game2601换桌')
                Flag = False
            except:
                print '玩牌中'
            time.sleep(2)
        self.hall_page.screenshot('结算页面.png')
        self.game_page.wait_element('game2601关闭').click()
        time.sleep(2)
        self.hall_page.screenshot('关闭结算页面.png')
        self.game_page.wait_element('换桌').click()
        time.sleep(1)
        self.hall_page.screenshot('点击换桌.png')
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 1)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.set_coin(mid,10000)
        self.common.closedriver()

class C27662_Settlement_ClickBtnBeyondSettlementUI(TestCase):
    '''
    点击结算界面全部任何地方，查看显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化环境")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('获取mid')
        self.hall_page.wait_element('测试按钮').click()
        element = self.luadriver.find_lua_element_by_name('uid')
        text = element.get_attribute('text')
        global mid
        mid = int(re.search('\d+', text).group())
        print mid
        self.hall_page.wait_element('关闭测试页面').click()
        self.hall_page.wait_element('葫芦岛麻将').click()
        try:
            self.game_page.wait_element('资源下载-确定').click()
        except:
            print '游戏已下载'
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 1)
        Flag = True
        while Flag:
            try:
                self.hall_page.wait_element('场次名称')
                Flag = False
            except:
                pass
            time.sleep(1)
        self.hall_page.wait_element('场次名称').click()
        time.sleep(5)
        self.hall_page.wait_element('准备').click()
        time.sleep(2)
        self.hall_page.screenshot('进入房间.png')
        Flag = True
        while Flag:
            try:
                self.game_page.wait_element('game2601换桌')
                Flag = False
            except:
                print '玩牌中'
            time.sleep(2)
        self.hall_page.screenshot('结算页面.png')
        self.game_page.wait_element('游戏内头像').click()
        time.sleep(2)
        self.hall_page.screenshot('结算页面点击头像后.png')
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 0)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.set_coin(mid,10000)
        self.common.closedriver()


class C27663_Settlement_ShareWithWechatUninstall(TestCase):
    '''
    无微信情况下点击分享
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.game_page = Game_Page()
        self.start_step("初始化环境")
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step('获取mid')
        self.hall_page.wait_element('测试按钮').click()
        element = self.luadriver.find_lua_element_by_name('uid')
        text = element.get_attribute('text')
        global mid
        mid = int(re.search('\d+', text).group())
        print mid
        self.hall_page.wait_element('关闭测试页面').click()
        self.hall_page.wait_element('葫芦岛麻将').click()
        try:
            self.game_page.wait_element('资源下载-确定').click()
        except:
            print '游戏已下载'
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 1)
        Flag = True
        while Flag:
            try:
                self.hall_page.wait_element('场次名称')
                Flag = False
            except:
                pass
            time.sleep(1)
        self.hall_page.wait_element('场次名称').click()
        time.sleep(5)
        self.hall_page.wait_element('准备').click()
        time.sleep(2)
        self.hall_page.screenshot('进入房间.png')
        Flag = True
        while Flag:
            try:
                self.game_page.wait_element('game2601换桌')
                Flag = False
            except:
                print '玩牌中'
            time.sleep(2)
        self.hall_page.screenshot('结算页面.png')
        self.game_page.wait_element('game2601分享').click()
        time.sleep(1)
        self.hall_page.screenshot('点击分享.png')
        self.game_page.wait_element('分享到朋友圈').click()
        self.hall_page.screenshot('点击分享到朋友圈.png')
        PHPInterface.set_robot_flag(2601, 0, 0, 12, 0)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.set_coin(mid, 10000)
        self.common.closedriver()

if __name__ == '__main__':
    C27434_FriendInvitation().debug_run()









