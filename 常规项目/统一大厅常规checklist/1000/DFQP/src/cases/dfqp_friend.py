#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌好友页面测试
'''
import time,test_datas
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.friend_page import Friend_Page
from uilib.hall_page import Hall_Page
from common.common import Common

class C060_DFQP_Friend_Enter(TestCase):
    '''
    大厅好友模块---切换各tab页
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入好友页面")
        self.hall_page.wait_element("好友").click()
        time.sleep(3)
        self.start_step("切换消息tab")
        self.friend_page.wait_element("消息tab").click()
        time.sleep(5)
        self.start_step("切换好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(5)
        self.start_step("查看认识的人")
        self.friend_page.wait_element("认识的人").click()
        time.sleep(2)
        self.start_step("查看附近的人")
        self.friend_page.wait_element("附近的人").click()
        time.sleep(5)
        self.start_step("查看好友排行")
        self.friend_page.wait_element("好友排行").click()
        time.sleep(5)
        self.start_step("查找好友")
        self.friend_page.wait_element("查找好友").click()
        time.sleep(2)
        # self.friend_page.wait_element("关闭按钮").click()

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C061_DFQP_Friend_Frindinfo(TestCase):
    '''
    玩家有好友,点击好友排行查看
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入好友页面")
        self.hall_page.wait_element("好友").click()
        time.sleep(3)
        self.start_step("点击查看第一个好友资料")
        self.friend_page.wait_element("好友资料").click()
        time.sleep(5)
        self.start_step("点击进入会话模块")
        self.friend_page.wait_element("会话按钮").click()
        time.sleep(2)
        self.friend_page.wait_element("查看右上图标").click()
        time.sleep(2)
        self.friend_page.wait_element("查看详细资料").click()
        time.sleep(2)
        self.friend_page.screenshot('Friend_Frindinfo.png')
        time.sleep(2)
        self.friend_page.wait_element("关闭按钮").click()

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C062_DFQP_Friend_message(TestCase):
    '''
    点击好友排行界面好友聊天按钮，查看显示
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入好友页面")
        self.hall_page.wait_element("好友").click()
        time.sleep(5)
        self.start_step("点击查看第一个好友资料")
        self.friend_page.wait_element("好友资料").click()
        time.sleep(10)
        self.start_step("点击进入会话模块")
        self.friend_page.wait_element("会话按钮").click()
        time.sleep(2)
        self.friend_page.wait_element("查看右上图标").click()
        time.sleep(2)
        self.friend_page.wait_element("清空聊天记录").click()
        time.sleep(2)
        self.start_step("输入文本")
        massage = self.common.random_str(6)
        self.friend_page.wait_element("输入框").send_keys(massage)
        self.friend_page.wait_element("输入框").click()
        time.sleep(2)
        self.luadriver.keyevent(4)
        self.friend_page.wait_element("发送").click()
        time.sleep(2)
        self.friend_page.wait_element("消息页面返回").click()
        time.sleep(2)
        self.friend_page.screenshot('_Friend_message.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C063_DFQP_Friend_TabKnow(TestCase):
    '''
    认识的人,查看界面显示
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入好友页面")
        self.hall_page.wait_element("好友").click()
        time.sleep(3)
        self.start_step("查看认识的人")
        self.friend_page.wait_element("认识的人").click()
        time.sleep(2)
        self.friend_page.screenshot('Friend_TabKnow.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C064_DFQP_Friend_Tosee(TestCase):
    '''
    情况2：通讯录有玩家,点击【去看看】
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入好友页面")
        self.hall_page.wait_element("好友").click()
        time.sleep(3)
        self.start_step("查看认识的人")
        self.friend_page.wait_element("认识的人").click()
        time.sleep(2)
        try:
            self.friend_page.wait_element("去看看").click()
            time.sleep(15)
        except:
            self.friend_page.wait_element("+好友").click()
            time.sleep(2)
            self.friend_page.wait_element("换一个").click()
            time.sleep(2)
        self.friend_page.screenshot('Friend_Tosee.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C065_DFQP_Friend_TabNearby(TestCase):
    '''
    附近的人
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入好友页面")
        self.hall_page.wait_element("好友").click()
        time.sleep(3)
        self.start_step("查看附近的人")
        self.friend_page.wait_element("附近的人").click()
        self.friend_page.screenshot('Friend_TabNearby.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C066_DFQP_Friend_Addnearby(TestCase):
    '''
    附近的人附近有玩家,点击【看看哪些人在玩】
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入好友页面")
        self.hall_page.wait_element("好友").click()
        time.sleep(3)
        self.start_step("查看附近的人")
        self.friend_page.wait_element("附近的人").click()
        time.sleep(5)
        try:
            self.start_step("看看附近哪些人在玩")
            self.friend_page.wait_element("看看哪些人在玩").click()
            time.sleep(5)
        except:
            self.start_step("加列表第2个好友")
            self.friend_page.wait_element("+附近的好友2").click()
            time.sleep(2)

        self.friend_page.screenshot('Friend_Addnearby.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C067_DFQP_Friend_Clearadd(TestCase):
    '''
    点击 清除地理位置
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入好友页面")
        self.hall_page.wait_element("好友").click()
        time.sleep(3)
        self.start_step("查看附近的人")
        self.friend_page.wait_element("附近的人").click()
        time.sleep(3)
        try:
            self.start_step("看看附近哪些人在玩")
            self.friend_page.wait_element("看看哪些人在玩").click()
            time.sleep(5)
        except:
            self.start_step("加列表第2个好友")
            try:
                self.friend_page.wait_element("+附近的好友2").click()
            except:
                print "没有附近的好友"
            time.sleep(2)
        time.sleep(2)
        self.start_step("清除地理位置")
        self.friend_page.wait_element("清除地理位置").click()
        time.sleep(5)
        self.friend_page.wait_element("取消清除").click()
        time.sleep(2)
        self.friend_page.wait_element("清除地理位置").click()
        time.sleep(2)
        self.friend_page.wait_element("确定清除").click()
        time.sleep(2)
        self.friend_page.screenshot('Friend_Clearadd.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C068_DFQP_Friend_Addfriend1(TestCase):
    '''
    消息列表，加好友信息选择【同意】
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入好友模块")
        self.hall_page.wait_element("好友").click()
        time.sleep(3)
        self.start_step("切换消息tab")
        self.friend_page.wait_element("消息tab").click()
        time.sleep(3)
        self.start_step("查看好友请求")
        try:
            self.start_step("同意")
            time.sleep(2)
        except:
            self.start_step("没有好友请求")
        self.friend_page.screenshot('Friend_Addfriend1.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C069_DFQP_Friend_Addfriend2(TestCase):
    '''
    消息列表，加好友信息选择【拒绝】
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入好友模块")
        self.hall_page.wait_element("好友").click()
        time.sleep(3)
        self.start_step("切换消息tab")
        self.friend_page.wait_element("消息tab").click()
        time.sleep(3)
        self.start_step("查看好友请求")
        try:
            self.start_step("拒绝")
            time.sleep(2)
        except:
            self.start_step("没有好友请求")
        self.friend_page.screenshot('Friend_Addfriend2.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C070_DFQP_Friend_Messageinfo(TestCase):
    '''
    正常打开聊天玩家个人资料卡
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入好友页面")
        self.hall_page.wait_element("好友").click()
        time.sleep(10)
        self.start_step("点击查看第一个好友资料")
        self.friend_page.wait_element("好友资料").click()
        time.sleep(10)
        self.start_step("点击进入会话模块")
        self.friend_page.wait_element("会话").click()
        time.sleep(2)
        self.friend_page.wait_element("查看右上图标").click()
        time.sleep(2)
        self.friend_page.wait_element("查看详细资料").click()
        time.sleep(2)
        self.friend_page.screenshot('Friend_Messageinfo.png')
        time.sleep(2)
        self.friend_page.wait_element("关闭按钮").click()

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C072_DFQP_Friend_messageclear(TestCase):
    '''
    好友聊天界面，点击右上角图标选择【清空聊天记录】
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入好友页面")
        self.hall_page.wait_element("好友").click()
        time.sleep(3)
        self.start_step("点击查看第一个好友资料")
        self.friend_page.wait_element("好友资料").click()
        time.sleep(5)
        self.start_step("点击进入会话模块")
        self.friend_page.wait_element("会话").click()
        time.sleep(2)
        self.friend_page.wait_element("查看右上图标").click()
        time.sleep(2)
        self.friend_page.wait_element("清空聊天记录").click()
        time.sleep(2)
        self.friend_page.screenshot('Friend_messageclear.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C073_DFQP_Friend_message(TestCase):
    '''
    消息列表，点击查看好友聊天信息
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.start_step("进入好友页面")
        self.hall_page.wait_element("好友").click()
        time.sleep(3)
        self.start_step("消息tab")
        self.friend_page.wait_element("消息tab").click()
        time.sleep(2)
        self.friend_page.screenshot('Friend_message.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()


# __qtaf_seq_tests__ = [ C062_DFQP_Friend_message ]
if __name__ == '__main__':
    # C061_DFQP_Friend_Frindinfo = C061_DFQP_Friend_Frindinfo()
    # C061_DFQP_Friend_Frindinfo.debug_run()
    debug_run_all()