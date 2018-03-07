# coding: utf-8

import util

# 内网环境
TEST_ENV = "http://192.168.97.3:58004/?"

def set_env(env=TEST_ENV):
    util.AUTO_TEST_URL = env

def add_robot(platid, mid, num):
    '''
    @brief 添加机器人
    @platid: 平台ID
    @followuid: 用户MID
    @svidtype
    @num：机器人数量
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "platid":platid,
        "followuid": mid,
        "svidtype":0,
        "num": num,
    }
    # print url
    # print postdata
    result = util.get(url, postdata)
    # print result
    return util.check_response(result)

# add_robot(510, 5306, 1)
def add_Money(mid, money):
    '''
    @brief 添加金币
    @platid: 平台ID
    @num：添加金币
    '''
    url = "http://texas-demo-510.boyaa.com/texas/demo/alibaba/money.php?"
    postdata = {
        "mid":mid,
        "money": money,
    }
    # print url
    # print postdata
    result = util.post(url, postdata)
    print result
    return util.check_response(result)

# add_Money(5306,1)