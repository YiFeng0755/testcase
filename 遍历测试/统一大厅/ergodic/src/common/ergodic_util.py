#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re,os,time,json,copy
from utils.confighelper import ConfigHelper
from uilib.hall_page import Hall_Page
from appiumcenter.element import Element
import utils.constant as constant
import base64

cfg_path = constant.cfg_path
serial = cfg_path.split('/')[-3]
print 'serial:%s' % serial
current_path = os.getcwd()
print 'current path:%s'%current_path

def open_json(filepath):
    with open(filepath) as json_file:
        data = json_file.read()
        return data

def dumpfile(path,driver):
    if not os.path.exists(path):
        os.makedirs(path)
    name = path.split('/')[-2]
    dumpcmd = "shell am startservice --user 0 com.boyaa.luaviewer_helper/.ViewerHelper"
    pullcmd = 'pull /mnt/sdcard/lua_uidump.json ' + path + name+'.json'
    cmdstop = 'shell am force-stop com.boyaa.luaviewer_helper'
    cmdrm = 'shell rm /mnt/sdcard/lua_uidump.json'

    driver.adb(dumpcmd)
    print "dump file"
    time.sleep(10)
    string_pulled = driver.pull_file('/mnt/sdcard/lua_uidump.json')
    print type (string_pulled)
    output_file = path + name + '.json'
    string_decoded = base64.decodestring(string_pulled)
    f = open(output_file,'w')
    f.write(string_decoded)
    time.sleep(10)
    if os.path.isfile(path + name+'.json'):
        print 'dump file success'
        return True
    else:
        return False

def get_btn_list_json(path):
    name = path.split('/')[-2]
    filepath = path+name+'.json'
    json_data = open_json(filepath)
    p = re.compile(r'\"type\"\:\"Button\"\,\"name\"\:\"[a-zA-Z\_\d]*\"\,')
    btn_list = []
    a = p.findall(json_data)
    for j in a:
        k = j.replace('"type":"Button","name":', '')
        l = k.replace(',', '')
        m = l.replace('"', '')
        btn_list.append(m)
    return btn_list

def save_btn_list(path,btn_list):
    if not os.path.exists('./%s/cfg/btn.ini'%serial):
        f = open('./%s/cfg/btn.ini'%serial,'w')
        f.close()
    Btn_list = json.dumps(btn_list)
    config = ConfigHelper('./%s/cfg/btn.ini'%serial)
    if not config.getConfig(path):
        config.addSection(path,'btn_list','')
    config.modifConfig(path,'btn_list',Btn_list)

def get_btn_list_ini(path):
    config = ConfigHelper('./%s/cfg/btn.ini'%serial)
    lst = config.getValue(path, 'btn_list')
    btn_list = json.loads(lst)
    return btn_list

def add_to_NoNeedBackPath(path):
    if not os.path.exists('./%s/cfg/NoNeedBackPath.json'%serial):
        f = open('./%s/cfg/NoNeedBackPath.json'%serial, 'w')
        path_list =[]
    else:
        f = open('./%s/cfg/NoNeedBackPath.json'%serial, 'r+')
        path_list = json.load(f)
    path_list.append(path)
    f.seek(0)
    json.dump(path_list,f)
    f.close()

def calc_add_btn(btn_list,Btn_list):
    a = copy.deepcopy(btn_list)
    b = copy.deepcopy(Btn_list)
    for item in a:
        try:
            b.remove(item)
        except:
            pass
    add_btn = b
    return add_btn

def calc_reduce_btn(btn_list,Btn_list):
    a = copy.deepcopy(btn_list)
    b = copy.deepcopy(Btn_list)
    for item in b:
        try:
            a.remove(item)
        except:
            pass
    reduce_btn = a
    return reduce_btn

def add_to_btn_black(btn):
    if not os.path.exists('./%s/cfg/btn_black.json'%serial):
        f = open('./%s/cfg/btn_black.json'%serial, 'w')
        btn_black_list =[]
    else:
        f = open('./%s/cfg/btn_black.json'%serial, 'r+')
        btn_black_list = json.load(f)
    if isinstance(btn,str):
        if btn not in btn_black_list:
            btn_black_list.append(btn)
    if isinstance(btn,list):
        l = [item for item in btn if item not in btn_black_list]
        btn_black_list.extend(l)
    f.seek(0)
    json.dump(btn_black_list,f)
    f.close()

def write_to_clicked_list(btn):
    if not os.path.exists('./%s/cfg/btn_clicked.json'%serial):
        f = open('./%s/cfg/btn_clicked.json'%serial, 'w')
        clicked_list =[]
    else:
        f = open('./%s/cfg/btn_clicked.json'%serial, 'r+')
        clicked_list = json.load(f)
    if btn not in clicked_list:
        clicked_list.append(btn)
    f.seek(0)
    json.dump(clicked_list, f)
    f.close()

def back_to_hall(driver):
    print '开始返回'
    for i in range(0,5):
        driver.keyevent(4)
        time.sleep(2)
    Flag = True
    while Flag:
        dumpfile('./%s/temp/'%serial,driver)
        current_list = get_btn_list_json('./%s/temp/'%serial)
        hall_list =get_btn_list_json('./%s/hall/'%serial)
        if current_list == hall_list:
            Flag = False
            print '已返回到大厅'
        elif current_list == get_btn_list_json('./%s/hall/backwards/'%serial):
            driver.keyevent(4)
            Flag = False
            print '已返回到大厅'
        else:
            print '继续返回'

def back_to_PathBeforeWrong(driver,path):
    back_to_hall(driver)
    btnlist = path.split('/')
    btnlist.remove('')
    btnlist.remove('.')
    btnlist.remove('hall')
    btnlist.remove(serial)
    for btn in btnlist:
        driver.find_lua_element_by_name(btn).click()
        time.sleep(2)
        print '点了'+btn
    print '返回到了'+path+'路径'

def filter_BtnBlackClicked(add_btn):
    with open('./%s/cfg/btn_black.json'%serial, 'r') as f :
        btn_black_list = json.load(f)
        m =[item for item in add_btn if item not in btn_black_list]
    if os.path.exists('./%s/cfg/btn_clicked.json'%serial):
        with open('./%s/cfg/btn_clicked.json'%serial,'r') as file:
            btn_clicked_list = json.load(file)
            n = [item for item in m if item not in btn_clicked_list]
            return n
    else:
        return m

def is_imageBack_exists(path):
    name = path.split('/')[-2]
    filepath = path+name+'.json'
    json_data = open_json(filepath)
    p = re.findall(r'\"type\"\:\"Image\"\,\"name\"\:\"ImageBack\"\,',json_data)
    if p == ['"type":"Image","name":"ImageBack",']:
        return True
    elif p == []:
        return False

def click_btn(driver,path,btn):
    btn_list = get_btn_list_json(path)
    print 'btn_list=%s'%btn_list
    print '点了' + btn
    write_to_clicked_list(btn)
    try:
        driver.find_lua_element_by_name(btn).click()
    except:
        print '点击按钮出错，返回到出错前的路径'
        back_to_PathBeforeWrong(driver, path)
        clickable_btn = filter_BtnBlackClicked(get_btn_list_ini(path))
        print 'clickable_btn =%s' % clickable_btn
        if clickable_btn == [] and path == './%s/hall/'%serial:
            print '已遍历完'
        elif clickable_btn == []:
            back_pre_level(driver, path)
        else:
            button = clickable_btn[0]
            click_btn(driver, path, button)
        return
    time.sleep(2)
    android_eles = driver.find_elements_by_android_uiautomator('new UiSelector().clickable(true)')
    #write_to_clicked_list(btn)
    print 'android_eles=%s'%android_eles
    element = Element()
    screenpath = element.screenshotpath()
    driver.get_screenshot_as_file(screenpath+btn+'.png')
    Path =path+btn+'/'
    print '当前路径：'+Path
    dumpfile(Path,driver)
    Btn_list = get_btn_list_json(Path)
    print 'Btn_list=%s' % Btn_list
    add_btn = calc_add_btn(btn_list,Btn_list)
    print 'add_btn:%s' % add_btn
    for i in add_btn:
        if 'tab' in i or 'modeItem'== i:
            add_to_btn_black(i)
    reduce_btn = calc_reduce_btn(btn_list,Btn_list)
    print 'reduce_btn:%s'%reduce_btn
    back_list = ['Button_return', 'returnBtn', 'close', 'closeBtn', 'backBtn', 'back', 'Button_close']
    intersection = [item for item in back_list if item in add_btn]
    clickable_btn = list(set(filter_BtnBlackClicked(add_btn)))
    if Btn_list == btn_list and android_eles == []:
        print '界面无变化'
        add_to_NoNeedBackPath(Path)
    elif reduce_btn != [] and reduce_btn != btn_list and android_eles == []:
        add_to_btn_black(btn)
        with open('./%s/cfg/btn_black.json'%serial, 'r') as f:
            btn_black_list = json.load(f)
        print 'btn_black_list=%s'%btn_black_list
        print '界面出错，返回到出错前的路径'
        back_to_PathBeforeWrong(driver,path)
        clickable_btn = filter_BtnBlackClicked(get_btn_list_ini(path))
        print 'clickable_btn =%s'%clickable_btn
        Path = path
        print '当前路径：%s'%Path
    elif intersection == [] and is_imageBack_exists(Path)== False and android_eles == []:
        add_to_NoNeedBackPath(Path)
    elif intersection == [] and is_imageBack_exists(path) == True and android_eles == []:
        add_to_NoNeedBackPath(Path)
    print '当前路径下的可点击按钮clickable_btn =%s'%clickable_btn
    save_btn_list(Path,clickable_btn)
    if clickable_btn == [] and Path == './%s/hall/'%serial:
        print '已遍历完'
        return
    elif clickable_btn == []:
        back_pre_level(driver,Path)
    else:
        button = clickable_btn[0]
        click_btn(driver,Path,button)

def get_NoNeedBackPath():
    with open('./%s/cfg/NoNeedBackPath.json'%serial,'r') as f:
        path_list = json.load(f)
    return path_list

def back_pre_level(driver,path):
    if os.path.exists('./%s/cfg/NoNeedBackPath.json'%serial):
        no_back_list = get_NoNeedBackPath()
    else:
        no_back_list = []
    if not path in no_back_list:
        driver.keyevent(4)
    name = path.split('/')[-2]  # 进入当前目录所按下的btn的name名
    path = path.replace(name + '/', '')  # 返回到的路径
    Lst = get_btn_list_ini(path)
    time.sleep(3)
    print '返回到上一级'
    print '当前路径：'+path
    Lst.remove(name)  # 在上级目录的btn_list中删除名为name的btn
    print '当前路径下的可点击btn=%s'%Lst
    save_btn_list(path,Lst)
    if path == './%s/hall/'%serial and Lst ==[]:
        print '已遍历完'
        return
    elif Lst == []:
        back_pre_level(driver,path)
    else:
        btn = Lst[0]
        click_btn(driver,path,btn)

