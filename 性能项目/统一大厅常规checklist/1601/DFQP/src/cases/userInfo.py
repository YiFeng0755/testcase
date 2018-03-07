#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
性能测试场景之个人信息框
'''
import time
from runcenter.enums import EnumPriority,EnumStatus
from cfg.constantEnum import EnumSceneName,EnumSceneType
from runcenter.testcase import debug_run_all,TestCase
from uilib.personinfo_page import Personinfo_Page
from uilib.hall_page import Hall_Page
from common.common import Common


#目前问题：不能切换城市、账号不是可设置项
class PerTest_QIPAIHALL_Userinfo(TestCase):
    '''
    玩家个人信息框操作
    '''
    owner = "JessicZeng"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 5
    def pre_test(self):
        self.common = Common()
        self.hall_page = Hall_Page()
        self.personinfo_page = Personinfo_Page()

    def run_test(self):
        '''
        操作步骤：
        1、点击大厅个人信息框入口
        2、修改昵称
        3、修改性别
        4、修改城市
        5、查看VIP特权，然后返回个人信息框
        6、切换账号（可能造成前后两次结果有差异主要是切换账号后可能有签到框）
        7、结束测试
        :return:
        '''
        self.hall_page.wait_element("同步标志")
        self.start_step("点击大厅玩家信息框入口")
        self.common.sendTagBroadcast(EnumSceneName.UserInfo,EnumSceneType.Start)
        try:
            self.hall_page.wait_element("打开个人信息框")
            self.hall_page.wait_element("头像").click()
            time.sleep(2)
            self.personinfo_page.wait_element("同步标志")
            time.sleep(1)
            self.common.taskScreenShot('openUserInfo_pop.jpg')

            #设置用户昵称,修改后点击其他地方来保存修改
            self.start_step("修改昵称")
            nickName = self.common.random_str(6)
            self.personinfo_page.wait_element("设置用户名").send_keys(nickName)
            self.personinfo_page.wait_element("同步标志").click()
            self.common.taskScreenShot('modifyNick.jpg')

            #修改玩家性别，女改男，男改女  get_attribute('selected')
            self.start_step("修改性别")
            enGirl = self.personinfo_page.wait_element("女")
            if (enGirl.get_attribute('selected')):
                self.common.platformLog("点击性别男")
                self.personinfo_page.wait_element("男").click()
            else:
                self.common.platformLog("点击性别女")
                self.personinfo_page.wait_element("女").click()
            self.common.taskScreenShot('modifySex.jpg')

            #修改城市，海南和四川来回切换  若当前为四川则切换为海南  反之亦然
            self.start_step("修改城市")
            cityNameStr = self.personinfo_page.get_element("城市").get_attribute('text')
            self.personinfo_page.wait_element("城市").click()
            element1 = self.personinfo_page.wait_element("海南")  # 海南
            element2 = self.personinfo_page.wait_element("四川")  # 四川
            if cityNameStr.find('四川') != -1 :
                self.common.moveElement(element1, element2)
            else:
                self.common.moveElement(element2, element1)
            time.sleep(2)
            self.personinfo_page.wait_element("同步标志").click()
            self.common.taskScreenShot('modifyCity.jpg')

            #查看VIP特权
            self.start_step("查看VIP特权")
            self.personinfo_page.get_element("了解VIP特权").click()
            time.sleep(2)
            self.common.taskScreenShot('VIPPrivilege.jpg')
            try:
                self.personinfo_page.wait_element("特权同步标志")
                self.personinfo_page.wait_element("返回个人资料").click()
            except:
                self.common.platformLog("VIP特权页面显示失败，结束玩家信息框测试")

            self.personinfo_page.get_element("关闭").click()
            #切换账号，用已有账号登录  登录成功后会直接返回大厅并切换账号
            # time.sleep(2)
            # self.start_step("切换账号")
            # try:
            #     self.personinfo_page.get_element("切换账号").click()
            #     self.personinfo_page.wait_element("继续登录").click()
            #     self.personinfo_page.wait_element("登录框title")
            #     self.personinfo_page.wait_element("账号").send_keys("18676676262")
            #     self.personinfo_page.wait_element("密码").send_keys("zrf.870208")
            #     self.personinfo_page.wait_element("确认登录").click()
            #     self.hall_page.wait_element("同步标志")
            # except:
            #     print "切换账号失败,直接退回到大厅"
            #     while (self.personinfo_page.is_exist("同步标志")):
            #         self.common.closePop()
            # finally:
            #     self.common.closeActivity()
        except:
            self.common.platformLog("操作个人信息框失败")
        finally:
            self.common.checkPopVisible(self.personinfo_page)
            self.hall_page.wait_element("同步标志")

        time.sleep(2)
        self.common.sendTagBroadcast(EnumSceneName.UserInfo, EnumSceneType.Stop)

# __qtaf_seq_tests__ = [C30990_DFQP_PersonInfo_EnterVIP]
if __name__ == '__main__':
    # C027_DFQP_PersonInfo_NicknameAlter = C027_DFQP_PersonInfo_NicknameAlter()
    # C027_DFQP_PersonInfo_NicknameAlter.debug_run()
    debug_run_all()
