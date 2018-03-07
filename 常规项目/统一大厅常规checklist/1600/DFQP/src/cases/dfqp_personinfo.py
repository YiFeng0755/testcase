#!/usr/bin/env python
#coding=utf-8
'''
个人资料
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from runcenter.testcase import debug_run_all,TestCase
from uilib.personinfo_page import Personinfo_Page
from uilib.hall_page import Hall_Page
from common.common import Common
from datacenter import dataprovider
import test_datas

class C30984_DFQP_Guestinfo(TestCase):
    '''
    游客玩家个人资料界面显示
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        self.start_step("初始化Luadriver")
        self.luadriver = self.common.setupdriver()
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.element_is_exist("账号ID")
        self.personinfo_page.screenshot('Guestinfo.png')
        time.sleep(3)
        self.personinfo_page.wait_element("关闭").click()
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()


class C30985_DFQP_Personinfo(TestCase):
    '''
    手机玩家个人资料界面显示
    '''
    owner = "MindyZhang"
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
        self.common.deletefile(self.luadriver)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver)
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        self.start_step("登陆账号")
        # self.common.loginuser(user_info['user'], user_info['password'])
        # self.common.closeactivity_switchserver(self.luadriver, "环境切换")
        # time.sleep(2)
        # self.start_step("进入头像页面")
        # self.personinfo_page.wait_element("头像").click()
        self.personinfo_page.screenshot('Personnfo.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.release_user(user_info['mid'])
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C30986_DFQP_PersonInfo_NicknameNull(TestCase):
    """
    点击修改昵称,修改为空字符、空格
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
        self.common.closeactivity_switchserver(self.luadriver)
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(5)
        self.personinfo_page.wait_element("设置用户名").send_keys("")
        time.sleep(3)
        self.personinfo_page.wait_element("修改用户名").click()
        #点击页面其他元素，设置保存
        self.personinfo_page.wait_element("了解VIP特权").click()
        self.personinfo_page.screenshot( 'NicknameNull.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C30986_DFQP_PersonInfo_NicknameLong(TestCase):
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
        self.common.closeactivity_switchserver(self.luadriver)
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
        self.personinfo_page.screenshot('NicknameLong.png')
    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        # self.common.deletefile(self.luadriver)
        self.common.closedriver()

class C30986_DFQP_PersonInfo_NicknameSpecial(TestCase):
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
        self.common.closeactivity_switchserver(self.luadriver)
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.wait_element("设置用户名").send_keys("%^$%&haha")
        self.personinfo_page.wait_element("修改用户名").click()
        #点击页面其他元素，设置保存
        self.personinfo_page.wait_element("了解VIP特权").click()
        self.personinfo_page.screenshot( 'NicknameSpecial.png')
    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C30986_DFQP_PersonInfo_NicknameAlter(TestCase):
    """
    点击修改昵称,修改昵称正常
    """
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeActivityBtn()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.start_step("设置用户名")
        nickname = self.common.random_str(5)
        print nickname
        self.personinfo_page.wait_element("设置用户名").send_keys(nickname)
        # self.personinfo_page.wait_element("设置用户名").send_keys(u"的就".encode("utf-8"))
        self.personinfo_page.wait_element("修改用户名").click()
        #点击页面其他元素，设置保存
        self.personinfo_page.wait_element("了解VIP特权").click()
        self.personinfo_page.screenshot('NicknameAlter.png')
        time.sleep(3)
        self.personinfo_page.wait_element("关闭").click()
        time.sleep(1)
        self.start_step("设置完成后，重启游戏")
        self.luadriver = self.common.restart()
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        nickname1 = self.personinfo_page.wait_element("设置用户名").get_attribute('text')
        print nickname1
        self.start_step("判断nickname是否一致")
        self.assert_equal("nickname", nickname1, nickname)

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C30987_DFQP_PersonInfo_Sex1(TestCase):
    """
    头像为自定义头像,修改性别
    """
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10
    def pre_test(self):
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver )
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.start_step("拍照修改为自定义头像")
        self.personinfo_page.wait_element("头像logo").click()
        time.sleep(3)
        self.start_step("拍照修改头像")
        self.luadriver.find_element_by_id("android:id/text1").click()
        time.sleep(3)
        self.luadriver.keyevent(27) #拍照
        time.sleep(10)
        try:
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

        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.start_step("修改性别")
        print self.personinfo_page.wait_element("女").get_attribute('selected')
        if(self.personinfo_page.wait_element("女").get_attribute('selected')):
            self.personinfo_page.wait_element("男").click()
        else:
            self.personinfo_page.wait_element("女").click()
        time.sleep(2)
        if(self.personinfo_page.wait_element("女").get_attribute('selected')):
            a=1
        else:
            a=0
        print a
        self.personinfo_page.wait_element("关闭").click()
        # 重新登陆
        self.start_step("重启游戏查看性别")
        self.common.restart()
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        if(a==1):
            self.personinfo_page.wait_element("女").get_attribute('selected')
        else:
            self.personinfo_page.wait_element("男").get_attribute('selected')
        self.personinfo_page.screenshot( 'Sex1.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C30988_DFQP_PersonInfo_Photographer(TestCase):
    """
    默认展示本地头像，拍照设置头像
    """
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 8
    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver )
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.screenshot('photographer1.png')
        self.personinfo_page.wait_element("头像logo").click()
        time.sleep(3)
        self.start_step("拍照修改头像")
        self.luadriver.find_element_by_id("text1").click()
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
        self.personinfo_page.screenshot( 'photographer2.png')
        #重新登陆
        self.start_step("重新启动游戏，查看头像是否修改成功")
        self.common.restart()
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        self.personinfo_page.screenshot('photographer3.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C30988_DFQP_PersonInfo_Photoalter2(TestCase):
    """
    上传本地图片，点击修改头像，上传本地图片
    """
    owner = "Lucyliu"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        #删除自动登陆文件,置为游客状态
        self.common = Common()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.deletefile(self.luadriver)
        # 每个用例都需要关闭活动，把这个放在初始化里面实现
        self.common.closeactivity_switchserver(self.luadriver )
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        self.start_step("进入头像页面")
        self.personinfo_page.wait_element("头像").click()
        time.sleep(2)
        self.personinfo_page.screenshot('Photoalter1.png')
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
        try:
            self.luadriver.find_element_by_id("com.android.gallery3d:id/head_select_right").click()
            time.sleep(5)
            self.personinfo_page.screenshot('Photoalter2.png')
            #重新登陆
            self.start_step("重新登陆查看头像")
            self.common.restart()
            self.start_step("进入头像页面")
            self.personinfo_page.wait_element("头像").click()
        except:
            print "选择截图失败"
        self.personinfo_page.screenshot('Photoalter3.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C30989_DFQP_PersonInfo_City(TestCase):
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
        self.common.closeactivity_switchserver(self.luadriver )
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
        self.personinfo_page.screenshot( 'City1.png')
        element1 = self.personinfo_page.wait_element("海南") #海南
        element2 = self.personinfo_page.wait_element("四川") # 四川
        self.common.swipeelement(element1,element2)
        #点击其他元素进行保存
        self.personinfo_page.wait_element("修改用户名").click()
        time.sleep(2)
        self.personinfo_page.screenshot('City2.png')
        self.personinfo_page.wait_element("关闭").click()
        #重新登陆
        self.start_step("重新登陆查看头像")
        self.common.closedriver()
        # 初始化Luadriver
        self.luadriver = self.common.setupdriver()
        self.common.closeactivity_switchserver(self.luadriver)
        time.sleep(2)
        self.personinfo_page.wait_element("头像").click()
        # self.luadriver.find_element_by_name("View_head").click()
        time.sleep(2)
        self.personinfo_page.screenshot( 'City3.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C30990_DFQP_PersonInfo_EnterVIP(TestCase):
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
        self.common.closeactivity_switchserver(self.luadriver )
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
        self.personinfo_page.screenshot('EnterVIP.png')

    def post_test(self):
        '''
        测试用例执行完成后，清理测试环境
        '''
        self.common.closedriver()

class C30992_DFQP_PersonInfo_Pay(TestCase):
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
        self.common.closeactivity_switchserver(self.luadriver )
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

__qtaf_seq_tests__ = [C30986_DFQP_PersonInfo_NicknameAlter]
if __name__ == '__main__':
    # C027_DFQP_PersonInfo_NicknameAlter = C027_DFQP_PersonInfo_NicknameAlter()
    # C027_DFQP_PersonInfo_NicknameAlter.debug_run()
    debug_run_all()
