#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
地方棋牌个人信息页面
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.personinfo_page import Personinfo_Page
from uilib.hall_page import Hall_Page
from common.common import Common

class C016_DFQP_PersonInfo1(TestCase):
    '''
    大厅进入个人信息页面
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.screenshot('C016_DFQP_PersonInfo1.png')
        time.sleep(1)
        self.personinfo_page.wait_element("关闭").click()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C017_DFQP_PersonInfo_Photo(TestCase):
    """
    默认展示本地头像
    """
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.screenshot('C017_DFQP_PersonInfoPhoto.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C018_DFQP_PersonInfo_EnterVIP(TestCase):
    """
    玩家不是vip,点击个人资料，查看VIP特权页面
    """
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.wait_element("了解VIP特权").click()
        time.sleep(3)
        self.personinfo_page.wait_element("VIP页签")
        self.personinfo_page.screenshot('C018_DFQP_EnterVIP.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C019_DFQP_PersonInfo_Pay(TestCase):
    """
    点击个人资料中充值按钮，查看充值H5界面显示
    """
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

        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.wait_element("使用充值卡").click()
        time.sleep(10)
        self.luadriver.find_elements_by_class_name("android.view.View")
        self.personinfo_page.screenshot( 'C019_DFQP_Pay.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C020_DFQP_PersonInfo_Photographer(TestCase):
    """
    默认展示本地头像，拍照设置头像
    """
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.screenshot('C020_DFQP_photographer1.png')
        self.personinfo_page.wait_element("头像logo").click()
        time.sleep(3)
        self.start_step("拍照修改头像")
        self.luadriver.find_element_by_id("android:id/text1").click()
        time.sleep(3)
        self.luadriver.keyevent(27)
        # self.luadriver.find_element_by_accessibility_id("拍照").click()
        time.sleep(10)
        try:
            #取消选中
           # self.luadriver.find_elements_by_class_name("android.widget.ImageView")[2].click()
            #选中图片
            self.luadriver.find_elements_by_class_name("android.widget.ImageView")[4].click()
        except:
            print "未找到元素1"
        try:
            self.luadriver.find_elements_by_class_name("android.widget.TextView")[1].click()
        except:
            print "未找到元素2"
        time.sleep(5)
        try:
            self.luadriver.find_element_by_id("com.android.gallery3d:id/head_select_right").click()
        except:
            print "未找到元素3"
        try:
            self.luadriver.find_element_by_id("com.sec.android.gallery3d:id/save").click()
        except:
            print "未找到元素3"
        time.sleep(5)
        self.personinfo_page.screenshot( 'C020_DFQP_photographer2.png')
        #重新登陆
        self.start_step("重新启动游戏，查看头像是否修改成功")
        self.common.closedriver()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)
        self.personinfo_page.screenshot('C020_DFQP_photographer3.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C021_DFQP_PersonInfo_Photoalter(TestCase):
    """
    上传本地图片，点击修改头像，上传本地图片
    """
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity(self.luadriver)

        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.screenshot('C021_DFQP_Photoalter1.png')
        self.personinfo_page.wait_element("头像logo").click()
        time.sleep(2)
        self.start_step("选择本地图片")
        self.luadriver.find_elements_by_class_name("android.widget.CheckedTextView")[1].click()
        # time.sleep(3)
        # self.luadriver.find_element_by_accessibility_id("从相册中选择").click()
        time.sleep(2)
        try:
            # self.luadriver.find_elements_by_class_name("android.widget.TextView")[0].click()
            self.luadriver.find_elements_by_class_name("android.widget.ImageView")[3].click()
            # self.luadriver.find_element_by_id("com.huawei.android.internal.app:id/hw_button_once").click()
        except:
            print "进入文件管理有问题"
            self.luadriver.keyevent(4)
        time.sleep(5)
        self.luadriver.find_elements_by_class_name("android.view.View")[1].click()
        # time.sleep(2)
        # self.luadriver.find_elements_by_class_name("android.widget.ImageView")[1].click()
        time.sleep(5)
        self.luadriver.find_element_by_id("com.android.gallery3d:id/head_select_right").click()
        time.sleep(5)
        self.personinfo_page.screenshot('C021_DFQP_Photoalter2.png')
        #重新登陆
        self.start_step("重新登陆查看头像")
        self.common.closedriver()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        time.sleep(10)
        self.common.closeactivity(self.luadriver)
        self.personinfo_page.screenshot('C021_DFQP_Photoalter3.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C022_DFQP_PersonInfo_Photocancel(TestCase):
    """
    点击修改头像，拍照，切换到对应界面拍照，点击取消
    """
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        time.sleep(10)
        self.common.closeactivity(self.luadriver)

        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.screenshot( 'C022_DFQP_Photocancel1.png')
        self.personinfo_page.wait_element("头像logo").click()
        time.sleep(3)
        self.luadriver.find_elements_by_class_name("android.widget.CheckedTextView")[0].click()
        time.sleep(3)
        self.luadriver.keyevent(27)
        # self.luadriver.find_element_by_accessibility_id("拍照").click()
        time.sleep(10)
        try:
            #取消选中
           # self.luadriver.find_elements_by_class_name("android.widget.ImageView")[2].click()
            #选中图片
            self.luadriver.find_elements_by_class_name("android.widget.ImageView")[4].click()
        except:
            print "未找到元素1"
        try:
            self.luadriver.find_elements_by_class_name("android.widget.TextView")[1].click()
        except:
            print "未找到元素2"
        time.sleep(5)
        #取消
        try:
            self.luadriver.find_element_by_id("com.android.gallery3d:id/head_select_left").click()
        except:
            print "未找到元素3"
        try:
            self.luadriver.find_element_by_id("com.sec.android.gallery3d:id/cancel").click()
        except:
            print "未找到元素3"
        time.sleep(2)
        self.luadriver.keyevent(4)
        self.personinfo_page.screenshot('C022_DFQP_Photocancel2.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C023_DFQP_PersonInfo_Photocancel(TestCase):
    """
    点击修改头像，从本地选择图片，切换到对应界面选择图片，点击取消
    """
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

        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.screenshot('C023_DFQP_Photocancel1.png')
        self.personinfo_page.wait_element("头像logo").click()
        time.sleep(3)
        self.start_step("选择本地图片")
        self.luadriver.find_elements_by_class_name("android.widget.CheckedTextView")[1].click()
        # time.sleep(3)
        # self.luadriver.find_element_by_accessibility_id("从相册中选择").click()
        time.sleep(2)
        try:
            # self.luadriver.find_elements_by_class_name("android.widget.TextView")[0].click()
            self.luadriver.find_elements_by_class_name("android.widget.ImageView")[3].click()
            # self.luadriver.find_element_by_id("com.huawei.android.internal.app:id/hw_button_once").click()
        except:
            print "进入文件管理有问题"
            self.luadriver.keyevent(4)
        time.sleep(5)
        self.luadriver.find_elements_by_class_name("android.view.View")[1].click()
        self.luadriver.find_element_by_accessibility_id("取消").click()
        time.sleep(5)
        self.personinfo_page.screenshot('C023_DFQP_Photocancel2.png')
    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C024_DFQP_PersonInfo_NicknameNull(TestCase):
    """
    点击修改昵称,修改昵称为空
    """
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

        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.wait_element("设置用户名").send_keys("")
        self.personinfo_page.wait_element("修改用户名").click()
        #点击页面其他元素，设置保存
        self.personinfo_page.wait_element("了解VIP特权").click()
        self.personinfo_page.screenshot( 'C024_DFQP_NicknameNull.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C025_DFQP_PersonInfo_NicknameLong(TestCase):
    """
    点击修改昵称,修改昵称过长
    """
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

        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.wait_element("设置用户名").send_keys("sdfdjsafjsdkfjsdajfsdkfklsdjflkdsjfldjsfljsdalfjsdlkjflkds")
        self.personinfo_page.wait_element("修改用户名").click()
        #点击页面其他元素，设置保存
        self.personinfo_page.wait_element("了解VIP特权").click()
        self.personinfo_page.screenshot('C025_DFQP_NicknameLong.png')
    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C026_DFQP_PersonInfo_NicknameSpecial(TestCase):
    """
    点击修改昵称,修改昵称含有屏蔽字、表情、特殊符号、空格
    """
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

        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.wait_element("设置用户名").send_keys("%^$% &haha")
        self.personinfo_page.wait_element("修改用户名").click()
        #点击页面其他元素，设置保存
        self.personinfo_page.wait_element("了解VIP特权").click()
        self.personinfo_page.screenshot( 'C026_DFQP_NicknameSpecial.png')
    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C027_DFQP_PersonInfo_NicknameAlter(TestCase):
    """
    点击修改昵称,修改昵称正常
    """
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

        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        nickname = self.common.random_str(5)
        print nickname
        self.personinfo_page.wait_element("设置用户名").send_keys(nickname)
        # self.personinfo_page.wait_element("设置用户名").send_keys(u"的说法就")
        self.personinfo_page.wait_element("修改用户名").click()
        #点击页面其他元素，设置保存
        self.personinfo_page.wait_element("了解VIP特权").click()
        self.personinfo_page.screenshot('C027_DFQP_NicknameAlter.png')
        nickname1 = self.personinfo_page.wait_element("设置用户名").get_attribute('text')
        print nickname1
        self.start_step("判断nickname是否一致")
        self.assert_equal("nickname", nickname1, nickname)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C028_DFQP_PersonInfo_Sex1(TestCase):
    """
    头像不是默认头像,修改性别为男、女
    """
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

        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.start_step("修改性别")
        print self.personinfo_page.wait_element("女").get_attribute('selected')
        if(self.personinfo_page.wait_element("女").get_attribute('selected')):
            self.personinfo_page.wait_element("男").click()
        else:
            self.personinfo_page.wait_element("女").click()
        time.sleep(1)
        if(self.personinfo_page.wait_element("女").get_attribute('selected')):
            a=1
        else:
            a=0
        print a
        # 重新登陆
        self.start_step("重启游戏查看性别")
        self.common.closedriver()
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        if(a==1):
            self.personinfo_page.wait_element("女").get_attribute('selected')
        else:
            self.personinfo_page.wait_element("男").get_attribute('selected')
        self.personinfo_page.screenshot( 'C028_DFQP_PersonInfo_Sex1.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C030_DFQP_PersonInfo_City(TestCase):
    """
    点击个人资料，修改城市信息
    """
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

        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.start_step("修改城市")
        self.personinfo_page.wait_element("城市").click()
        time.sleep(2)
        self.personinfo_page.screenshot( 'C030_DFQP_PersonInfo_City1.png')
        element1 = self.personinfo_page.wait_element("海南") #海南
        element2 = self.personinfo_page.wait_element("四川") # 四川
        self.common.swipeelement(element1,element2)
        #点击其他元素进行保存
        self.personinfo_page.wait_element("修改用户名").click()
        time.sleep(2)
        self.personinfo_page.screenshot('C030_DFQP_PersonInfo_City2.png')
        self.personinfo_page.wait_element("关闭").click()
        #重新登陆
        self.start_step("重新登陆查看头像")
        self.common.closedriver()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity(self.luadriver)
        time.sleep(2)
        self.personinfo_page.wait_element("头像").click()
        # self.luadriver.find_element_by_name("View_head").click()
        time.sleep(2)
        self.personinfo_page.screenshot( 'C030_DFQP_PersonInfo_City3.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C031_DFQP_PersonInfo_EnterVIPtab(TestCase):
    """
    玩家不是vip，点击个人资料，查看vip
    """
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

        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.wait_element("了解VIP特权").click()
        time.sleep(2)
        self.personinfo_page.screenshot('PersonInfo_EnterVIPtab.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C032_DFQP_PersonInfo_Money(TestCase):
    """
    玩家不是vip，点击个人资料，查看vip
    """
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

        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.screenshot('Money.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

# __qtaf_seq_tests__ = [C020_DFQP_PersonInfo_Photographer]
if __name__ == '__main__':
    # C027_DFQP_PersonInfo_NicknameAlter = C027_DFQP_PersonInfo_NicknameAlter()
    # C027_DFQP_PersonInfo_NicknameAlter.debug_run()
    debug_run_all()
