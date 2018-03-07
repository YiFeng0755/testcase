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

class C31072_DFQP_Friend_Enter(TestCase):
    '''
    查看好友界面显示
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
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        self.start_step("切换好友tab")
        self.friend_page.wait_element("好友tab").click()
        self.start_step("查看结交好友tab")
        self.friend_page.wait_element("结交好友tab").click()
        self.start_step("切换消息tab")
        self.friend_page.wait_element("消息tab").click()

    def post_test(self):
        #测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C31074_DFQP_Friend_Frindinfo(TestCase):
    '''
    玩家有好友,点击好友排行查看
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        # self.hall_page.wait_element("头像").click()
        # time.sleep(5)
        # self.common.loginuser(user_info['user'], user_info['password'])
        # self.common.closeactivity_switchserver(self.luadriver, "切换环境")

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        self.start_step("切换好友tab")
        self.friend_page.wait_element("好友tab").click()
        self.start_step("点击查看第一个好友资料")
        self.friend_page.wait_element("好友资料").click()
        self.friend_page.wait_element("查看右上图标").click()
        self.friend_page.wait_element("查看详细资料").click()
        time.sleep(2)
        self.friend_page.screenshot('Friend_Frindinfo.png')
        time.sleep(2)
        self.friend_page.wait_element("聊天页面返回").click()

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        # user_util.release_account(user_info['mid'])
        try:
            # self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        # finally:
        #     self.common.release_user(user_info['mid'])

class C31077_DFQP_Friend_message(TestCase):
    '''
    好友聊天
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        # self.hall_page.wait_element("头像").click()
        # time.sleep(5)
        # self.common.loginuser(user_info['user'], user_info['password'])
        # self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        time.sleep(1)
        self.hall_page.wait_element("同步标志")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(5)
        self.start_step("切换好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(3)
        self.start_step("点击查看第一个好友资料")
        self.friend_page.wait_element("好友资料").click()
        time.sleep(2)
        self.start_step("输入文本")
        massage = self.common.random_str(6)
        self.friend_page.wait_element("输入框").send_keys(massage)
        self.friend_page.wait_element("输入框").click()
        time.sleep(2)
        self.luadriver.keyevent(4)
        self.friend_page.wait_element("发送").click()
        time.sleep(2)
        self.friend_page.screenshot('_Friend_message.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        try:
            # self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        # finally:
        #     self.common.release_user(user_info['mid'])

class C31076_DFQP_Friend_Delete(TestCase):
    '''
    删除玩家
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        # self.hall_page.wait_element("头像").click()
        # time.sleep(5)
        # self.common.loginuser(user_info['user'], user_info['password'])
        # self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(5)
        self.start_step("切换好友tab")
        self.friend_page.get_element("好友tab").click()
        time.sleep(3)
        self.start_step("点击查看第一个好友资料")
        self.friend_page.wait_element("好友资料").click()
        time.sleep(2)
        self.friend_page.wait_element("查看右上图标").click()
        time.sleep(2)
        self.friend_page.wait_element("查看详细资料").click()
        time.sleep(2)
        self.friend_page.wait_element("删除好友").click()
        time.sleep(2)
        self.friend_page.wait_element("删除好友-确定").click()
        time.sleep(2)
        self.friend_page.screenshot('deletefriend.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        try:
            # self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        # finally:
        #     self.common.release_user(user_info['mid'])

class C31079_DFQP_Friend_TabKnow(TestCase):
    '''
    认识的人,查看界面显示
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        # self.hall_page.wait_element("头像").click()
        # time.sleep(5)
        # self.common.loginuser(user_info['user'], user_info['password'])
        # self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(5)
        self.start_step("查看结交好友tab")
        self.friend_page.wait_element("结交好友tab").click()
        time.sleep(2)
        self.start_step("查找通讯录好友")
        self.friend_page.wait_element("查找通讯录好友").click()
        time.sleep(2)
        self.friend_page.screenshot('search.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        try:
            # self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        # finally:
        #     self.common.release_user(user_info['mid'])

class C31081_DFQP_Friend_Tosee(TestCase):
    '''
    	手机通讯录无玩家点击“去看看”
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
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(5)
        self.start_step("查看结交好友tab")
        self.friend_page.wait_element("结交好友tab").click()
        time.sleep(2)
        self.friend_page.wait_element("查找通讯录好友").click()
        time.sleep(3)
        try:
            self.luadriver.find_element_by_name("允许").click()
        except:
            print "未出现按钮"
        time.sleep(3)
        self.friend_page.wait_element("点击查看").click()
        time.sleep(15)
        self.friend_page.screenshot('Friend_Tosee.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C31083_DFQP_Friend_TabNearby(TestCase):
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
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(5)
        self.start_step("查看结交好友tab")
        self.friend_page.wait_element("结交好友tab").click()
        self.friend_page.screenshot('Friend_TabNearby.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C31084_DFQP_Friend_Addnearby(TestCase):
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
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(5)
        self.start_step("查看结交好友tab")
        self.friend_page.wait_element("结交好友tab").click()
        time.sleep(3)
        self.start_step("查看附近的人")
        self.friend_page.wait_element("发现身边玩家").click()
        time.sleep(5)
        try:
            self.start_step("加列表第2个好友")
            self.friend_page.wait_element("+附近的好友2").click()
            time.sleep(2)
        except:
            print "添加好友失败"
        self.friend_page.screenshot('Friend_Addnearby.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C31087_DFQP_Friend_Addfriend1(TestCase):
    '''
    查找好友界面显示
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
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(5)
        self.start_step("查看结交好友tab")
        self.friend_page.wait_element("结交好友tab").click()
        time.sleep(3)
        self.friend_page.screenshot('Friend_Addfriend1.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C31088_DFQP_Friend_Addfrienderror(TestCase):
    '''
    输入不正确id查找好友
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
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(5)
        self.start_step("查看结交好友tab")
        self.friend_page.wait_element("结交好友tab").click()
        time.sleep(3)
        self.friend_page.wait_element("通过ID搜索好友").send_keys("")
        self.friend_page.wait_element("通过ID搜索好友").click()
        time.sleep(2)
        self.friend_page.wait_element("搜索").click()
        time.sleep(2)
        self.friend_page.wait_element("搜索").click()
        time.sleep(10)
        self.friend_page.screenshot('Addfrienderror.png')


    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        self.common.closedriver()

class C31089_DFQP_Friend_Addfriend(TestCase):
    '''
    	输入正确id查找好友
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        global user_info,cid
        user_info = self.common.get_user()
        print user_info
        cid = user_info['cid']
        self.common.release_user(user_info['mid'])
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(5)
        self.start_step("查看结交好友tab")
        self.friend_page.wait_element("结交好友tab").click()
        time.sleep(3)
        # print user_info['cid']
        self.start_step("同意添加好友")
        try:
            self.friend_page.wait_element("同意").click()
            time.sleep(3)
        except:
            self.log_info("无好友申请")
        self.friend_page.wait_element("通过ID搜索好友").send_keys(cid)
        self.friend_page.wait_element("通过ID搜索好友").click()
        time.sleep(2)
        self.friend_page.wait_element("搜索").click()
        time.sleep(2)
        self.friend_page.wait_element("搜索").click()
        time.sleep(2)
        try:
            self.friend_page.wait_element("加好友").click()
            time.sleep(10)
        except:
            self.log_info("未找到好友")
        self.friend_page.screenshot('Addfriend.png')

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        try:
            # self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        # finally:
        #     self.common.release_user(user_info['mid'])

class C31096_DFQP_Friend_Messageinfo(TestCase):
    '''
    	查看聊天界面好友资料
    '''
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5

    def pre_test(self):
        self.common = Common()
        # global user_info
        # user_info = self.common.get_user()
        # print user_info
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.friend_page = Friend_Page()
        self.hall_page = Hall_Page()
        # self.hall_page.wait_element("头像").click()
        # time.sleep(5)
        # self.common.loginuser(user_info['user'], user_info['password'])
        # self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入消息页面")
        self.hall_page.wait_element("消息").click()
        time.sleep(6)
        self.start_step("切换好友tab")
        self.friend_page.wait_element("好友tab").click()
        time.sleep(3)
        self.start_step("点击查看第一个好友资料")
        self.friend_page.wait_element("好友资料").click()
        time.sleep(2)
        self.friend_page.wait_element("查看右上图标").click()
        time.sleep(2)
        self.friend_page.wait_element("查看详细资料").click()
        time.sleep(2)
        self.friend_page.screenshot('Friend_Frindinfo.png')
        time.sleep(2)
        self.friend_page.wait_element("聊天页面返回").click()

    def post_test(self):
        # 测试用例执行完成后，清理测试环境
        try:
            # self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        # finally:
        #     self.common.release_user(user_info['mid'])


__qtaf_seq_tests__ = [ C31089_DFQP_Friend_Addfriend ]
if __name__ == '__main__':
    # C061_DFQP_Friend_Frindinfo = C061_DFQP_Friend_Frindinfo()
    # C061_DFQP_Friend_Frindinfo.debug_run()
    debug_run_all()