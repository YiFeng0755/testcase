#!/bin/bash/python
# -*- coding:utf-8 -*-
import time
import re
import os
import json
from make_action_file import BlackFilter
from make_action_file import ActionClickBack,ActionIncrement,Is_Tab_Btn,Is_Back_Btn,diferenceList,make_path
from DumpElement import open_json,dumpfile,get_button_info
from uiautomator import Device

import os

#
# def dirlist(path, allfile):
#     filelist = os.listdir(path)
#
#     for filename in filelist:
#         filepath = os.path.join(path, filename)
#         if os.path.isdir(filepath):
#             dirlist(filepath, allfile)
#         else:
#             allfile.append(filepath)
#     return allfile
#
#
# print dirlist("D:\\Notepad++", [])


#
# btn_black = [u'Button_match', u'test', u'prepublish', u'online', u'hall', u'activity', u'service', u'returnBtn',
#                  u'closeBtn']
# action = "Normal"
# pre_path="../tmp/"

# def bianli(pre_path,pre_action):
#     for pre in pre_action:
#         if pre=="login":
#             print "login_fun"
#         else:
#             print "self.find_element(pre).click()"
#     #print "开始遍历"
#     rootjson="dumproot.json"
#     dumproot=pre_path+"dumproot.json"
#     if dumpfile(rootjson):
#         print "遍历第一层"
#         time.sleep(5)
#         json_root = open_json(dumproot).get('children')
#         get_button_info(json_root,btn_root)
#         ##黑名单
#         btn_root_filter=BlackFilter(btn_root,btn_black)
#         print "btn_root",btn_root
#         print "btn_root_filter",btn_root_filter
#         return btn_root,btn_root_filter
#         Ispath,PathList=make_path(pre_path, btn_root_filter)
#         print Ispath,PathList
#         self.click_btn(btn_root, btn_root_filter, action, pre_btn, after_btn)


class Stack:
    """模拟栈"""
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items)==0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        if not self.isEmpty():
            return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

if __name__ == '__main__':
    lista=[]
    listb=[u'silverBtn', u'saveBtn', u'takeBtn', u'goldBarBtn']
    lista
    print lista


    #print listb

    #print type(lista)
    # pre_path="../tmp/"
    # btn_black = [u'Button_match', u'test', u'prepublish', u'online', u'hall', u'activity', u'service', u'returnBtn',u'closeBtn']
    # action="Normal"
    # dumproot=""
    # btn_root=[]
    # btn_root_filter=[]
    # root = Catalog("root")
    # for btn in btn_black:
    #     subCatalog=Catalog(btn)
    #     root.add(subCatalog)
    #
    # root.display(0)
    # SubCatalog1 = Catalog("SubCatalog1")
    # SubCatalog2 = Catalog("SubCatalog2")
    # SubCatalog3 = Catalog("SubCatalog3")
    # leaf1 = Leaves("leaf1", "1")
    # leaf2 = Leaves("leaf2", "2")
    # leaf3 = Leaves("leaf3", "3")
    # leaf4 = Leaves("leaf4", "4")
    # root.add(SubCatalog1)
    # root.add(SubCatalog2)
    # SubCatalog1.add(SubCatalog3)
    # root.add(leaf1)
    #
    # SubCatalog1.add(leaf2)
    # SubCatalog1.add(leaf3)
    # SubCatalog2.add(leaf4)
    # root.display(0)
    # s="Androidbtn"
    # exec(s+"='btn'")
    # print Androidbtn













    ##loginfun() 登录方式
    ##以下是大厅的登录方式

    #self.luadriver.keyevent(4)
    # time.sleep(5)
    # Btimes=5
    #
    # dumpfile("")



