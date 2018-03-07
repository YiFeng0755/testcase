#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#Author: Lucyliu
'''
斗地主游戏页面
'''
from appiumcenter.element import Element
from uilib.hall_page import Hall_Page

class Game_Page(Element):

   def to_hall_page(self,element):
      self.hall_page = Hall_Page()
      self.game_page = Game_Page()
      if not self.hall_page.element_is_exist(element, 2):
         try:
            self.game_page.wait_element("返回").click()
            self.game_page.wait_element("离开").click()
            while self.game_page.element_is_exist("确定1", 2):
               self.game_page.wait_element("确定1").click()
            while self.game_page.element_is_exist("返回大厅", 2):
               self.game_page.wait_element("返回大厅").click()
         except:
            print "未出现此元素"
