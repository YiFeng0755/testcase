#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#Author: Lucyliu
'''
地方棋牌大厅页面
'''
import time
from operator import itemgetter

from appiumcenter.element import Element
from appiumcenter.luadriver import LuaDriver
from utils import constant
from utils.confighelper import ConfigHelper

from common import Interface
from uilib.hall_page import Hall_Page
from common.common import Common
from uilib.sign_page import Sign_Page


class Game_Page(Element):
    def get_game_list(self):
        '''
        获取当前界面子游戏列表名
        :return: 游戏列表名
        '''
        self.game_page = Game_Page()
        self.common = Common()
        luaobj = LuaDriver()
        luadriver = luaobj.getLuaDriver()
        game_id = self.common.get_config_value("casecfg", "game_id")
        game_id = game_id.rstrip("|")
        # print game_id
        gamelist = game_id.split("|")
        print gamelist
        game_list = []
        # print game_id
        if game_id == 'undefined':
            elements = self.game_page.get_elements("子游戏列表")
            # print len(elements)
            #去重,同时去除game0（约牌，比赛场）和game-1(更多游戏）
            elementsblack = ["game0","game-1"]
            for i in range(len(elements)):
                name =elements[i].get_attribute("name")
                if name not in elementsblack:
                    elementsblack.append(name)
                    print name
                    game_list.append(elements[i])
            # print len(game_list)
        else:
            #gameid，添加"game"
            # print len(gamelist)
            for i in range(len(gamelist)):
                print "game"+gamelist[i]
                gameid = "game"+gamelist[i]
                try:
                    time.sleep(1)
                    elements1 = luadriver.find_lua_element_by_name(gameid)
                    print elements1.get_attribute("name")
                    game_list.append(elements1)
                except:
                    print "找不到元素 %s" % gamelist[i]
        print game_list
        return game_list

    def game_is_download(self):
        '''
        判断子游戏是否已下载
        '''
        self.game_page = Game_Page()
        self.sign_page = Sign_Page()
        if(self.game_page.element_is_exist("快速开始",6)==True):
            print ("游戏已下载")
            return True
        elif(self.game_page.element_is_exist("重新加载",1) == True):
            self.game_page.wait_element("重新加载").click()
            self.game_page.wait_element("快速开始",20)
            return True
        elif(self.game_page.element_is_exist("资源下载-确定",1) == True):
            self.game_page.wait_element("资源下载-确定").click()
            self.game_page.wait_element("快速开始",60)
            return True
        elif(self.game_page.element_is_exist("重新获取1",3)):
            # try:
            #     self.game_page.element_is_exist("重新获取1", 6).get_attribute('text') == "重新获取"
            # except:
            #     self.game_page.screenshot("download_fail.png")
            # while (self.sign_page.element_is_exist("关闭1")==True):
            #     self.sign_page.wait_element("关闭1").click()
            return False
        else:
            print "当前游戏下载出现问题"
            return False

    def game_play_way(self):
        '''
        选择玩法，调用方法
        elements = self.game_page.game_play_way()
        for i in range(len(elements)):
            elements[i][1].click()
        '''
        self.game_page = Game_Page()
        self.hall_page = Hall_Page()
        play_list = []
        no_select = self.game_page.get_elements("未选中的场次")
        select = self.game_page.get_elements("选中的场次")
        for i in range(len(no_select)):
            # dict[no_select[i]] = no_select[i].location['x']
            play_list.append((int(no_select[i].location['x']),no_select[i]))
        for i in range(len(select)):
            # dict[select[i]] = select[i].location['x']
            play_list.append((int(select[i].location['x']),select[i]))
        # dict1 = sorted(dict.iteritems(),key=lambda a:a[1])
        #根据X坐标来排序
        new_list = sorted(play_list, key=lambda item: item[0])
        return new_list

    def click_game_play(self,index=0):
        try:
            elements = self.game_play_way()
            elements[index][1].click()
        except:
            print "当前子游戏初级场"



    def set_robot(self,gameid,level=12,robotflag=0):
        '''
        设置机器人开关
        '''
        gamecfg = Interface.get_levelconfig(gameid, 0, 0, level)
        robotflag1 = gamecfg.get('values', {'ADDROBOTFLAG': None}).get('ADDROBOTFLAG')
        if (robotflag1 != robotflag):
            result = Interface.set_robot_flag(gameid, 0, 0, level, robotflag=robotflag)
            print result
        return True

    def game_is_exist(self,luadriver,gamename):
        '''
        判断子游戏是否存在，存在返回True，不存在返回False
        :param gamename: 子游戏元素名，不查找“更多游戏”
        '''
        self.game_page = Game_Page()
        time.sleep(1)
        if (luadriver.find_lua_element_by_name(gamename) != None):
            return True
        else:
            try:
                self.game_page.wait_element("右三角标").click()
                time.sleep(1)
                if (luadriver.find_lua_element_by_name(gamename) != None):
                    return True
            except:
                print "无此按钮"
            if(self.game_page.element_is_exist("更多游戏") == True):
                try:
                    self.game_page.wait_element("左三角标").click()
                    time.sleep(1)
                    if (luadriver.find_lua_element_by_name(gamename) != None):
                        return True
                except:
                    print "无此按钮"
            return False

    def room_set_cheat(self, game_list, switch=1):
        for i in range(len(game_list)):
            gameId = filter(lambda ch: ch in '0123456789', game_list[i].get_attribute("name"))
            if switch == 1:
                print "设置子游戏:%s 标准场为作弊场" % gameId
            else:
                print "设置子游戏:%s 标准场为非作弊场" % gameId
            for i in range(4):
                Interface.set_cheat(gameid=gameId, playmode=i, switch=switch)
