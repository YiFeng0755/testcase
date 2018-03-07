#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Author: MindyZhang
'''
比赛
'''
import time
import test_datas
from runcenter.enums import EnumStatus,EnumPriority
from runcenter.testcase import TestCase,debug_run_all
from appiumcenter.luadriver import LuaDriver
from common.common import Common
from uilib.hall_page import Hall_Page
from uilib.match_page import Match_Page
from uilib.personinfo_page import Personinfo_Page
from uilib.game_page import Game_Page
from datacenter import dataprovider
import common.Interface as PHPInterface

class C31263_DFQP_Match_CreateInvitational(TestCase):
    '''
    大厅比赛场---创建邀请赛
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        global coin,totalmoney,safebox_crystal
        self.common = Common()
        self.hall_page = Hall_Page()
        self.match_page = Match_Page()
        self.personinfo_page = Personinfo_Page()
        global user_info
        user_info = self.common.get_user()
        print user_info
        #初始化luadriver
        print ("pre_test")
        self.luadriver = self.common.setupdriver()
        # PHPInterface.set_env(env=PHPInterface.PRE_REPUBLISH_ENV)
        self.common.closeactivityprepublish(self.luadriver) #关闭活动弹框
        time.sleep(15)

        self.start_step("获取用户ID信息")
        self.match_page.wait_element("头像").click()
        time.sleep(3)
        cid = self.personinfo_page.wait_element("账号ID").get_attribute('text')
        print "获取的用户cid为：%s" % cid
        if(cid != user_info['cid']):
            self.common.loginuser(user_info['user'],user_info['password'])
            time.sleep(10)
            if(self.match_page.is_exist("关闭")==True):
                self.match_page.wait_element("关闭").click()
                time.sleep(3)
        else:
            self.match_page.wait_element("关闭").click()
            time.sleep(3)
        cid1 = user_info['cid']
        mid = PHPInterface.get_mid(cid1, region=1)
        print "用户mid为：%s" % mid
        time.sleep(5)
        self.start_step("获取用户银币信息")
        dict = PHPInterface.get_user_info(mid)
        coin = eval(dict).get('result',{'coin':None}).get('coin')
        print "用户银币数为：%s" % coin
        crystal = eval(dict).get('result',{'crystal':None}).get('crystal')
        print "用户金条数为：%s" % crystal
        time.sleep(5)
        self.start_step("获取用户保险箱存款信息")
        safebox_info = PHPInterface.get_safebox(mid)
        safebox_money = safebox_info.get('safebox')
        print "保险箱银币存款为：%s" % safebox_money
        safebox_crystal = safebox_info.get('crystalsafebox')
        print "保险箱金条存款为：%s" % safebox_crystal
        totalmoney = safebox_info.get('totalmoney')
        print "用户银币总数量为：%s" % totalmoney
        time.sleep(10)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.start_step("点击比赛场按钮")
        self.hall_page.wait_element("比赛场").click()
        time.sleep(10)
        self.start_step("点击邀请赛")
        self.match_page.wait_element("比赛场-邀请赛").click()
        time.sleep(10)
        self.start_step("创建邀请赛")
        self.match_page.wait_element("创建邀请赛").click()
        time.sleep(3)
        self.match_page.wait_element("完成创建").click()
        time.sleep(3)
        self.match_page.screenshot("3.png")
        time.sleep(3)
        # 现金不足
        if(coin <53000):
            # 现金不足，存款足够
            if(totalmoney >= 53000):
                self.match_page.wait_element("notNow").click()
                time.sleep(3)
                self.match_page.screenshot("4.png")
                time.sleep(3)
                self.match_page.wait_element("确定").click()
                time.sleep(3)
                self.match_page.screenshot("5.png")
                time.sleep(3)
                self.match_page.wait_element("关闭").click()
                time.sleep(3)
                self.match_page.wait_element("箭头返回").click()
            #现金不足，存款不足
            elif(totalmoney < 53000):
                self.match_page.wait_element("现在充值").click()
                time.sleep(3)
                self.match_page.screenshot("5.png")
                time.sleep(3)
                self.match_page.wait_element("关闭").click()
                time.sleep(3)
                self.match_page.wait_element("箭头返回").click()
        #现金足够
        else:
            self.match_page.wait_element("确定").click()
            time.sleep(3)
            self.match_page.screenshot("5.png")
            time.sleep(3)
            self.match_page.wait_element("关闭").click()
            time.sleep(3)
            self.match_page.wait_element("箭头返回").click()

        self.match_page.wait_element("箭头返回").click()
        time.sleep(3)
        self.match_page.wait_element("返回").click()
        time.sleep(3)
        self.hall_page.wait_element("同步标志")
    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['mid'])

class C31264_DFQP_Match_MyMatch(TestCase):
    '''
    大厅比赛场---查看我创建的邀请赛
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 15

    def pre_test(self):
        global coin, totalmoney, safebox_crystal
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        # 初始化luadriver
        print ("pre_test")
        self.luadriver = self.common.setupdriver()
        # PHPInterface.set_env(env=PHPInterface.PRE_REPUBLISH_ENV)
        self.common.closeactivityprepublish(self.luadriver)  # 关闭活动弹框
        time.sleep(15)
        self.hall_page = Hall_Page()
        self.match_page = Match_Page()
        self.personinfo_page = Personinfo_Page()
        self.start_step("获取用户ID信息")
        self.match_page.wait_element("头像").click()
        time.sleep(3)
        cid = self.personinfo_page.wait_element("账号ID").get_attribute('text')
        print "获取的用户cid为：%s" % cid
        if (cid != user_info['cid']):
            self.common.loginuser(user_info['user'], user_info['password'])
            time.sleep(10)
            self.common.closeActivityBtn()
            # if (self.match_page.is_exist("关闭") == True):
            #     self.match_page.wait_element("关闭").click()
            #     time.sleep(3)
        else:
            self.match_page.wait_element("关闭").click()
            time.sleep(3)
        cid1 = user_info['cid']
        mid = PHPInterface.get_mid(cid1, region=1)
        print "用户mid为：%s" % mid

        self.start_step("获取用户银币信息")
        dict = PHPInterface.get_user_info(mid)
        coin = eval(dict).get('result', {'coin': None}).get('coin')
        print "用户银币数为：%s" % coin
        if(coin < 53000):
            PHPInterface.add_money(mid,(53000-coin))
            self.common.closeactivityprepublish(self.luadriver)
            time.sleep(10)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.start_step("点击比赛场按钮")
        self.hall_page.wait_element("比赛场").click()
        time.sleep(3)
        self.start_step("点击邀请赛")
        self.match_page.wait_element("比赛场-邀请赛").click()
        time.sleep(5)
        self.start_step("创建邀请赛")
        self.match_page.wait_element("创建邀请赛").click()
        time.sleep(5)
        self.match_page.wait_element("完成创建").click()
        time.sleep(3)
        self.match_page.screenshot("1.png")
        time.sleep(3)
        self.match_page.wait_element("确定").click()
        time.sleep(3)
        self.match_page.screenshot("2.png")
        time.sleep(3)
        self.match_page.wait_element("关闭").click()
        time.sleep(3)
        print ("邀请赛创建成功")
        self.match_page.wait_element("箭头返回").click()
        time.sleep(3)
        self.start_step("查看我创建的邀请赛")
        self.match_page.wait_element("我创建的邀请赛").click()
        time.sleep(3)
        self.match_page.screenshot("3.png")
        time.sleep(3)
        self.match_page.wait_element("邀请好友/领取退还奖品").click()
        time.sleep(3)
        if(self.match_page.is_exist("微信邀请")==True):
            self.start_step("微信邀请好友")
            try:
                self.start_step("微信邀请好友")
                self.match_page.wait_element("微信邀请").click()
                time.sleep(3)
                self.match_page.screenshot("4.png")
                # time.sleep(3)
                # self.luadriver.keyevent(4)
                time.sleep(2)
                self.luadriver.keyevent(4)
            except:
                print "微信邀请好友失败"
            self.start_step("QQ邀请好友")
            time.sleep(2)
            self.start_step("QQ邀请好友")
            self.match_page.wait_element("QQ邀请").click()
            time.sleep(3)
            self.match_page.screenshot("5.png")
            time.sleep(2)
            self.match_page.wait_element("立即邀请").click()
            time.sleep(2)
            self.match_page.screenshot("6.png")
            while(self.match_page.is_exist("面对面扫码")==False):
                time.sleep(2)
                self.luadriver.keyevent(4)
                self.match_page.screenshot("61.png")
            time.sleep(2)
            self.start_step("面对面扫码")
            self.match_page.wait_element("面对面扫码").click()
            time.sleep(3)
            self.match_page.screenshot("7.png")
            time.sleep(2)
            self.luadriver.keyevent(4)
            time.sleep(2)
            self.luadriver.keyevent(4)
            time.sleep(2)
        else:
            print ("领取退还奖品")
            self.match_page.screenshot("8.png")
        self.match_page.wait_element("箭头返回").click()
        time.sleep(3)
        self.match_page.wait_element("箭头返回").click()
        time.sleep(3)
        self.match_page.wait_element("返回").click()
        time.sleep(3)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''

        self.common.closedriver()

class C31265_DFQP_Match_MyInvolved(TestCase):
    '''
    大厅比赛场---查看我报名的邀请赛
    '''
    owner = "MindyZhang"
    status = EnumStatus.Design
    priority = EnumPriority.High
    timeout = 10

    def pre_test(self):
        global coin, totalmoney, safebox_crystal
        self.common = Common()
        global user_info
        user_info = self.common.get_user()
        print user_info
        # 初始化luadriver
        # print ("pre_test")
        self.luadriver = self.common.setupdriver()
        # PHPInterface.set_env(env=PHPInterface.PRE_REPUBLISH_ENV)
        self.common.closeactivityprepublish(self.luadriver)  # 关闭活动弹框
        time.sleep(15)
        self.hall_page = Hall_Page()
        self.match_page = Match_Page()
        self.personinfo_page = Personinfo_Page()
        self.game_page = Game_Page()
        self.start_step("获取用户ID信息")
        self.match_page.wait_element("头像").click()
        time.sleep(3)
        cid = self.personinfo_page.wait_element("账号ID").get_attribute('text')
        print "获取的用户cid为：%s" % cid
        if (cid != user_info['cid']):
            self.common.loginuser(user_info['user'], user_info['password'])
            time.sleep(10)
            if (self.match_page.is_exist("关闭") == True):
                self.match_page.wait_element("关闭").click()
                time.sleep(3)
        else:
            self.match_page.wait_element("关闭").click()
            time.sleep(3)
        cid1 = user_info['cid']
        mid = PHPInterface.get_mid(int(cid1), region=1)
        print "用户mid为：%s" % mid

        self.start_step("获取用户银币信息")
        dict = PHPInterface.get_user_info(mid)
        coin = eval(dict).get('result', {'coin': None}).get('coin')
        print "用户银币数为：%s" % coin
        if (coin < 53000):
            PHPInterface.add_money(mid, (53000 - coin))
            self.common.closeactivityprepublish(self.luadriver)
            time.sleep(10)

    def run_test(self):
        '''
        测试用例
        '''
        self.start_step("等待页面加载完成")
        self.hall_page.wait_element("同步标志")
        time.sleep(5)
        self.start_step("点击比赛场按钮")
        self.hall_page.wait_element("比赛场").click()
        time.sleep(5)
        self.start_step("点击邀请赛")
        self.match_page.wait_element("比赛场-邀请赛").click()
        time.sleep(5)
        self.start_step("查看我报名的邀请赛")
        self.match_page.wait_element("我报名的邀请赛").click()
        time.sleep(3)
        self.match_page.screenshot("1.png")
        if(self.match_page.is_exist("已报名比赛1")==True):
            self.match_page.wait_element("已报名比赛1").click()
            time.sleep(3)
            self.match_page.screenshot("2.png")
            time.sleep(3)
            self.match_page.wait_element("退赛").click()
            time.sleep(3)
            self.match_page.screenshot("3.png")
            time.sleep(2)
            self.luadriver.keyevent(4)
            time.sleep(3)

        else:
            print ("没有已报名的邀请赛")
            self.luadriver.keyevent(4)
            time.sleep(3)
            self.start_step("创建邀请赛")
            self.match_page.wait_element("创建邀请赛").click()
            time.sleep(3)
            self.match_page.wait_element("完成创建").click()
            time.sleep(3)
            self.match_page.wait_element("确定").click()
            time.sleep(3)
            self.match_page.screenshot("4.png")
            time.sleep(3)
            self.match_page.wait_element("马上报名").click()
            time.sleep(3)
            if(self.game_page.is_exist("资源下载-确定")==True):
                self.game_page.wait_element("资源下载-确定").click()
                time.sleep(10)
            else:
                self.match_page.screenshot("5.png")
                time.sleep(3)
                self.match_page.wait_element("知道了/现在进入").click()
                time.sleep(3)
                print ("邀请赛报名成功")
                self.match_page.wait_element("箭头返回").click()
                time.sleep(3)
                self.start_step("查看我报名的邀请赛")
                self.match_page.wait_element("我报名的邀请赛").click()
                time.sleep(3)
                self.match_page.screenshot("6.png")
                self.match_page.wait_element("已报名比赛1").click()
                time.sleep(3)
                self.match_page.screenshot("7.png")
                time.sleep(3)
                self.match_page.wait_element("退赛").click()
                time.sleep(3)
                self.match_page.screenshot("8.png")
                time.sleep(2)
                self.luadriver.keyevent(4)
                time.sleep(3)

        self.match_page.wait_element("箭头返回").click()
        time.sleep(3)
        self.match_page.wait_element("返回").click()
        time.sleep(3)
        self.hall_page.wait_element("同步标志")

    def post_test(self):
        '''
        测试用例执行完后，清理测试环境
        '''
        try:
            self.common.deletefile(self.luadriver)
            self.common.closedriver()
        except:
            self.log_info("close driver fail")
        finally:
            self.common.release_user(user_info['mid'])


__qtaf_seq_tests__ = [C31264_DFQP_Match_MyMatch]
if __name__ == "__main__":
    debug_run_all()