#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#Author: Lucyliu
'''
地方棋牌大厅页面
'''
import time
from appiumcenter.element import Element

from common import Interface


class Game_Page(Element):
    def get_game_list(self):
        '''
        获取当前界面子游戏列表名
        :return: 游戏列表名
        '''
        self.game_page = Game_Page()
        elements = self.game_page.get_elements("子游戏列表")
        # print len(elements)
        #去重,同时去除game0（约牌，比赛场）和game-1(更多游戏）
        elementsblack = ["game0","game-1"]
        game_list = []
        for i in range(len(elements)):
            name =elements[i].get_attribute("name")
            if name not in elementsblack:
                elementsblack.append(name)
                print name
                game_list.append(elements[i])
        # print len(game_list)
        return game_list

    def game_is_download(self):
        '''
        判断子游戏是否已下载
        '''
        self.game_page = Game_Page()
        if(self.game_page.element_is_exist("资源下载-确定") == True):
            self.game_page.wait_element("资源下载-确定").click()
            time.sleep(40)
        else:
            print ("游戏已下载")

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