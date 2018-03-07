#!/usr/bin/env python
#-*-coding=utf-8-*-
import json
class GlobalVars:
    # 拼装成字典构造全局变量  借鉴map  包含变量的增删改查
    '''
    各参数说明
    luaDriver：公共drvier，初始化时创建的driver
    '''
    map = {}


    def set_map(self, key, value):
        '''
        设置单一变量值
        :param key:变量名
        :param value:变量值
        :return:
        '''
        if (isinstance(value, dict)):
            value = json.dumps(value)
        self.map[key] = value

    def set(self, **keys):
        '''
        设置多个变量   key-value
        :param keys:
        :return:
        '''
        try:
            for key_, value_ in keys.items():
                self.map[key_] = str(value_)
                print (key_ + ":" + str(value_))
        except BaseException as msg:
            print(msg)
            raise msg

    def del_map(self, key):
        '''
        删除key对应值
        :param key:
        :return:
        '''
        try:
            del self.map[key]
            return self.map
        except KeyError:
            print("key:'" + str(key) + "'  不存在")


    def get(self, *args):
        '''
        获取值
        :param args: key,key,key...   or "all",则直接返回整个map
        :return:
        '''
        try:
            dic = {}
            for key in args:
                if len(args) == 1:
                    dic = self.map[key]
                elif len(args) == 1 and args[0] == 'all':
                    dic = self.map
                else:
                    dic[key] = self.map[key]
            return dic
        except KeyError:
            print("key:'" + str(key) + "'  不存在")
            return None

singleGlobalVar = GlobalVars()