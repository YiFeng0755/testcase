# coding: utf-8

import util
import uuid
import json
import base64
import hashlib
from collections import OrderedDict
import time
import traceback

# 内网环境
TEST_ENV = "http://192.168.201.75/xx-landlord/application/api.alltest.php?"
    
# 外网测试环境
PRE_REPUBLISH_ENV = "http://192.168.201.75/xx-landlord/application/api.alltest.php?"
    
# 正式
FORMAL_ENV = ""

def set_env(env=TEST_ENV):
    util.AUTO_TEST_URL = env

def add_money(mid, money,flag=0):
    '''
    @brief 添加银币
    @param mid: 用户mid
    @param money: 金币数量
    @param flag:0:加,1:减
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "m":'sblack',
        "p": 'addmoney',
        "mid": mid,
        "flag":flag,
        "money": money
    }
    result = util.post(url, postdata)
    return util.check_response(result)

def get_money(mid):
    '''
    @brief 获取金币
    @param mid: 用户mid
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "m":'sblack',
        "p": 'getusermoney',
        "mid": mid,
    }
    result = util.post(url, postdata)
    print result
    return result

# print add_money(6837,600,0)
# print get_money(6837)
#
# print add_money(6837,3000,1)
# print add_money(6859,280000,1)
# print add_money(6860,100000,1)
# print add_money(6905,100000,1)