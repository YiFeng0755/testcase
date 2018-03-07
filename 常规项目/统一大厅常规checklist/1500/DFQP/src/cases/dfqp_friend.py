#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
好友
'''
import time,test_datas
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.friend_page import Friend_Page
from uilib.hall_page import Hall_Page
from common.common import Common
from datacenter import dataprovider

class C61023_DFQP_Friend_Enter(TestCase):
    '''
    结交好友界面显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看结交好友tab")
        self.friend_page.wait_element("结交好友tab").click()
        time.sleep(1)
        self.friend_page.screenshot('.png')

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C61025_DFQP_Friend_ContactList(TestCase):
    '''
    通讯录无联系人时通过通讯录查找好友
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看结交好友tab")
        self.friend_page.wait_element("结交好友tab").click()
        time.sleep(1)
        self.start_step('查找通讯录好友')
        self.friend_page.wait_element('查找通讯录好友').click()
        time.sleep(1)
        self.friend_page.screenshot('1.png')
        self.start_step('点击返回键')
        self.friend_page.wait_element('返回').click()
        time.sleep(1)
        self.friend_page.screenshot('2.png')

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C61026_DFQP_Friend_Nearby(TestCase):
    '''
    通讯录无联系人时通过通讯录查找好友界面【点击查看】
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看结交好友tab")
        self.friend_page.wait_element("结交好友tab").click()
        time.sleep(1)
        self.start_step('查找通讯录好友')
        self.friend_page.wait_element('查找通讯录好友').click()
        time.sleep(1)
        self.start_step('点击查看')
        self.friend_page.wait_element('点击查看').click()
        time.sleep(2)
        self.friend_page.screenshot('1.png')
        self.friend_page.wait_element('头像').click()
        time.sleep(1)
        self.friend_page.wait_element('加好友').click()
        self.friend_page.screenshot('2.png')

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C61029_DFQP_Friend_WeChat(TestCase):
    '''
    有微信情况下，通过推荐微信好友添加好友
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看结交好友tab")
        self.friend_page.wait_element("结交好友tab").click()
        time.sleep(1)
        self.start_step('点击推荐微信好友')
        self.friend_page.wait_element('推荐微信好友').click()
        time.sleep(2)
        self.friend_page.screenshot('.png')
        self.luadriver.keyevent(4)

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C61030_DFQP_Friend_LocateTimeout(TestCase):
    '''
    未授权，通过定位添加好友，提示定位超时
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        time.sleep(5)
        flag = True
        while flag :
            try:
                self.luadriver.find_elements_by_class_name("android.widget.Button")[0].click()
                print '点击了拒绝按钮'
                flag = False
            except:
                print "未出现按钮"
        self.common.closeactivity_switchserver(self.luadriver, "预发布")

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看结交好友tab")
        self.friend_page.wait_element("结交好友tab").click()
        time.sleep(1)
        self.friend_page.wait_element('发现身边玩家').click()
        time.sleep(20)
        self.friend_page.screenshot('.png')

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C61031_DFQP_Friend_AddById(TestCase):
    '''
    通过输入id添加好友
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        global user_info, UserID
        user_info = self.common.get_user()
        UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看结交好友tab")
        self.friend_page.wait_element("结交好友tab").click()
        time.sleep(1)
        self.friend_page.wait_element('搜索').click()
        time.sleep(1)
        self.friend_page.screenshot('1.png')
        self.friend_page.wait_element('通过ID搜索好友').send_keys('100111767')
        self.friend_page.wait_element('搜索').click()
        time.sleep(1)
        self.friend_page.screenshot('2.png')
        self.friend_page.wait_element('头像').click()
        time.sleep(1)
        self.friend_page.screenshot('3.png')
        self.luadriver.keyevent(4)
        self.friend_page.wait_element('通过ID搜索好友').send_keys('10085')
        self.friend_page.wait_element('搜索').click()
        time.sleep(1)
        self.friend_page.screenshot('4.png')
        self.friend_page.wait_element('头像').click()
        time.sleep(1)
        self.friend_page.screenshot('5.png')
        self.luadriver.keyevent(4)
        self.friend_page.wait_element('加好友').click()
        self.friend_page.screenshot('6.png')
        self.friend_page.wait_element('通过ID搜索好友').send_keys('100009024')
        self.friend_page.wait_element('搜索').click()
        time.sleep(1)
        self.friend_page.screenshot('7.png')
        self.friend_page.wait_element('头像').click()
        time.sleep(1)
        self.friend_page.screenshot('8.png')
        self.friend_page.wait_element('加好友/发送消息').click()
        time.sleep(1)
        self.friend_page.screenshot('9.png')
        self.luadriver.keyevent(4)
        self.friend_page.wait_element('通过ID搜索好友').send_keys('111111111')
        self.friend_page.wait_element('搜索').click()
        self.friend_page.screenshot('10.png')

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C61033_DFQP_Friend_HasFriends(TestCase):
    '''
    有好友时好友界面显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        global user_info, UserID
        user_info = self.common.get_user()
        UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(1)
        self.friend_page.screenshot('1.png')
        self.friend_page.wait_element('头像').click()
        time.sleep(1)
        self.friend_page.screenshot('2.png')

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C61035_DFQP_Friend_SingleFriendSendMessage(TestCase):
    '''
    有好友时好友界面显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        global user_info, UserID
        user_info = self.common.get_user()
        UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(2)
        elements = self.friend_page.get_elements('头像')
        print elements
        elements[2].click()
        time.sleep(1)
        self.friend_page.wait_element('语音/键盘').click()
        time.sleep(1)
        self.friend_page.wait_element('按住说话').click()
        time.sleep(1)
        self.friend_page.screenshot('1.png')
        self.friend_page.wait_element('语音/键盘').click()
        self.friend_page.wait_element('输入框').send_keys('abc123!@#')
        self.friend_page.wait_element('输入框').click()
        #self.luadriver.keyevent(4)
        self.friend_page.wait_element('发送').click()
        self.friend_page.screenshot('2.png')

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C61036_DFQP_Friend_LookUpInformation(TestCase):
    '''
    单个好友聊天界面 查看资料
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        global user_info, UserID
        user_info = self.common.get_user()
        UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(2)
        elements = self.friend_page.get_elements('头像')
        print elements
        elements[2].click()
        time.sleep(1)
        self.friend_page.wait_element('查看右上图标').click()
        self.friend_page.wait_element('查看详细资料').click()
        time.sleep(1)
        self.friend_page.screenshot('1.png')
        self.luadriver.keyevent(4)
        self.friend_page.wait_element('输入框').send_keys('abc123!@#')
        self.friend_page.wait_element('输入框').click()
        #self.luadriver.keyevent(4)
        self.friend_page.wait_element('发送').click()
        time.sleep(2)
        elements1 = self.friend_page.get_elements('头像')
        elements1[-1].click()
        time.sleep(1)
        self.friend_page.screenshot('2.png')

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C61038_DFQP_Friend_SingleFriendYuepaiRoom(TestCase):
    '''
    单个好友聊天跳转到约牌房
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        global user_info, UserID
        user_info = self.common.get_user()
        UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(2)
        elements = self.friend_page.get_elements('头像')
        print elements
        elements[2].click()
        time.sleep(1)
        self.friend_page.wait_element('发送').click()
        time.sleep(1)
        self.friend_page.wait_element('约牌').click()
        time.sleep(1)
        self.friend_page.screenshot('.png')

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C61039_DFQP_Friend_GroupChat(TestCase):
    '''
    创建群聊
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        global user_info, UserID
        user_info = self.common.get_user()
        UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(2)
        elements = self.friend_page.get_elements('头像')
        print elements
        elements[1].click()
        time.sleep(1)
        self.friend_page.wait_element('查看右上图标').click()
        time.sleep(1)
        self.friend_page.wait_element('发起群聊').click()
        time.sleep(2)
        self.friend_page.screenshot('1.png')
        elements[1].click()
        time.sleep(1)
        self.friend_page.screenshot('2.png')
        self.luadriver.keyevent(4)
        time.sleep(1)
        self.luadriver.keyevent(4)
        time.sleep(1)
        self.luadriver.keyevent(4)
        time.sleep(1)
        self.friend_page.wait_element('创建群聊').click()
        time.sleep(1)
        elements = self.friend_page.get_elements('选择')
        elements[1].click()
        elements[2].click()
        time.sleep(1)
        self.friend_page.wait_element('确认').click()
        time.sleep(2)
        self.friend_page.screenshot('3.png')

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C61040_DFQP_Friend_GroupChatDisplay(TestCase):
    '''
    多人聊天界面显示
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global user_info, UserID
        user_info = self.common.get_user()
        UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(2)
        self.friend_page.wait_element('创建群聊').click()
        time.sleep(1)
        elements = self.friend_page.get_elements('选择')
        elements[1].click()
        elements[2].click()
        time.sleep(1)
        self.friend_page.wait_element('确认').click()
        time.sleep(2)
        self.friend_page.screenshot('1.png')
        self.friend_page.wait_element('发送').click()
        time.sleep(1)
        self.friend_page.screenshot('2.png')
        self.friend_page.wait_element('查看右上图标').click()
        time.sleep(1)
        self.friend_page.wait_element('查看右上图标').click()
        time.sleep(2)
        self.friend_page.screenshot('3.png')
        elements1 = self.friend_page.get_elements('头像')
        elements1[-4].click()
        time.sleep(1)
        self.friend_page.screenshot('4.png')
        self.luadriver.keyevent(4)
        time.sleep(1)
        elements1[-6].click()
        time.sleep(1)
        self.friend_page.screenshot('5.png')
        self.friend_page.wait_element('加好友/发送消息').click()
        time.sleep(1)
        self.friend_page.screenshot('6.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C61041_DFQP_Friend_GroupChatDisplay(TestCase):
    '''
    群聊发送及接收语音、文本聊天信息
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global user_info, UserID
        user_info = self.common.get_user()
        UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(2)
        self.friend_page.wait_element('创建群聊').click()
        time.sleep(1)
        elements = self.friend_page.get_elements('选择')
        elements[1].click()
        elements[2].click()
        time.sleep(1)
        self.friend_page.wait_element('确认').click()
        time.sleep(2)
        #后续long_press添加后再补上语音聊天代码
        self.friend_page.wait_element('输入框').send_keys('abc123!@#')
        self.friend_page.wait_element('输入框').click()
        #self.luadriver.keyevent(4)
        self.friend_page.wait_element('发送').click()
        time.sleep(1)
        self.friend_page.screenshot('.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C75741_DFQP_Friend_GroupChatNameModify(TestCase):
    '''
    群聊界面修改群名称
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global user_info, UserID
        user_info = self.common.get_user()
        UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(2)
        self.friend_page.wait_element('创建群聊').click()
        time.sleep(1)
        elements = self.friend_page.get_elements('选择')
        elements[1].click()
        elements[2].click()
        time.sleep(1)
        self.friend_page.wait_element('确认').click()
        time.sleep(2)
        self.friend_page.wait_element('查看右上图标').click()
        time.sleep(1)
        self.friend_page.wait_element('修改群名称').click()
        time.sleep(1)
        self.friend_page.wait_element('群名称输入框').send_keys('群聊abc^_^')
        time.sleep(1)
        self.luadriver.keyevent(4)
        time.sleep(1)
        self.friend_page.screenshot('.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C75742_DFQP_Friend_AddGroupMembers(TestCase):
    '''
    群聊天界面添加群成员
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global user_info, UserID
        user_info = self.common.get_user()
        UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(2)
        self.friend_page.wait_element('创建群聊').click()
        time.sleep(1)
        elements = self.friend_page.get_elements('选择')
        elements[1].click()
        elements[2].click()
        time.sleep(1)
        self.friend_page.wait_element('确认').click()
        time.sleep(2)
        self.friend_page.wait_element('查看右上图标').click()
        time.sleep(1)
        elements1 = self.friend_page.get_elements('头像')
        self.start_step('点击添加按钮')
        elements1[-3].click()#点击添加按钮
        time.sleep(2)
        self.friend_page.screenshot('1.png')
        elements1[1].click()
        time.sleep(1)
        self.friend_page.screenshot('2.png')
        self.luadriver.keyevent(4)
        elements[3].click()
        time.sleep(1)
        self.friend_page.wait_element('确认').click()
        time.sleep(2)
        self.friend_page.screenshot('3.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C75742_DFQP_Friend_DeleteGroupMembers(TestCase):
    '''
    群聊天界面删除群成员
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global user_info, UserID
        user_info = self.common.get_user()
        UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(2)
        self.friend_page.wait_element('创建群聊').click()
        time.sleep(1)
        elements = self.friend_page.get_elements('选择')
        elements[1].click()
        elements[2].click()
        time.sleep(1)
        self.friend_page.wait_element('确认').click()
        time.sleep(2)
        self.friend_page.wait_element('查看右上图标').click()
        time.sleep(1)
        elements1 = self.friend_page.get_elements('头像')
        self.start_step('点击删除按钮')
        print elements1
        elements1[-1].click()  # 点击删除按钮
        print (elements1[-1])
        time.sleep(1)
        self.friend_page.screenshot('4.png')
        elements1[1].click()
        time.sleep(1)
        self.friend_page.screenshot('5.png')
        self.luadriver.keyevent(4)
        elements[1].click()
        time.sleep(1)
        self.friend_page.wait_element('确认').click()
        time.sleep(1)
        self.friend_page.wait_element('温馨提示-确认').click()
        time.sleep(1)
        self.friend_page.screenshot('6.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C75743_DFQP_Friend_EmptyChatRecord(TestCase):
    '''
    群聊天界面清空聊天
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global user_info, UserID
        user_info = self.common.get_user()
        UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(2)
        self.friend_page.wait_element('创建群聊').click()
        time.sleep(1)
        elements = self.friend_page.get_elements('选择')
        elements[1].click()
        elements[2].click()
        time.sleep(1)
        self.friend_page.wait_element('确认').click()
        time.sleep(2)
        i = 0
        while i < 3 :
            i += 1
            self.friend_page.wait_element('输入框').send_keys('abc123!@#')
            self.friend_page.wait_element('输入框').click()
            self.friend_page.wait_element('发送').click()
            time.sleep(1)
        self.friend_page.screenshot('1.png')
        self.friend_page.wait_element('查看右上图标').click()
        time.sleep(1)
        self.friend_page.wait_element('查看右上图标').click()
        self.friend_page.wait_element('清空聊天').click()
        self.luadriver.keyevent(4)
        time.sleep(1)
        self.friend_page.screenshot('2.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)

class C75744_DFQP_Friend_DissolveGroupChat(TestCase):
    '''
    群聊天界面解散群聊
    '''
    owner = "YoungLiu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        self.common = Common()
        global user_info, UserID
        user_info = self.common.get_user()
        UserID = user_info.get('mid')
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        self.common.closeactivity_switchserver(self.luadriver, "预发布")
        self.hall_page.wait_element("头像").click()
        time.sleep(5)
        self.common.loginuser(user_info['user'], user_info['password'])
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(2)
        self.start_step("查看好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(2)
        self.friend_page.wait_element('创建群聊').click()
        time.sleep(1)
        elements = self.friend_page.get_elements('选择')
        elements[1].click()
        elements[2].click()
        time.sleep(1)
        self.friend_page.wait_element('确认').click()
        time.sleep(2)
        self.friend_page.screenshot('1.png')
        self.friend_page.wait_element('查看右上图标').click()
        time.sleep(1)
        self.friend_page.wait_element('查看右上图标').click()
        self.friend_page.wait_element('解散群聊').click()
        self.friend_page.wait_element('温馨提示-确认').click()
        time.sleep(1)
        self.friend_page.screenshot('2.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            print 'Closedriver failed'
        finally:
            self.common.release_user(UserID)


# __qtaf_seq_tests__ = [ C31089_DFQP_Friend_Addfriend ]
if __name__ == '__main__':
    C75742_DFQP_Friend_AddGroupMembers = C75742_DFQP_Friend_AddGroupMembers()
    C75742_DFQP_Friend_AddGroupMembers.debug_run()
    #debug_run_all()