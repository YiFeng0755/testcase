# coding: utf-8

import urllib2
import urllib
import json

# 默认是预发布
from utils import constant
from utils.confighelper import ConfigHelper

def getcfg():
    config = ConfigHelper(constant.cfg_path)
    env = config.getValue('casecfg', 'env')
    if env =='1':
        AUTO_TEST_URL = "http://192.168.200.21/dfqp/?action=autotest.api"
    elif env =='2':
        AUTO_TEST_URL = "http://pcususus01.ifere.com/ddfqp/?action=autotest.api"
    else:
        print "只支持测试和预发布环境进行接口测试"
    return AUTO_TEST_URL
AUTO_TEST_URL = getcfg()

def post(url, data, urlencode=True):
    print 'post to:%s' % url
    if urlencode:
        data = urllib.urlencode(data)
    else:
        data = json.dumps(data)
    request = urllib2.Request(url,data)
    response=urllib2.urlopen(request)
    return response.read()

def check_response(response, only_check_code=False):
    # {"code":200,"error":"","result":{"status":1,"msg":"\u64cd\u4f5c\u6210\u529f"}}
    flag = 0
    try:
        result = json.loads(response)
        if only_check_code:
            if result.get('code', 0) == 200:
                flag = 1
        else:
            msg = result.get('result', {'msg': 'fail'}).get('msg')
            if result.get('code', 0) == 200 and  (msg == u'操作成功' or msg == u'该代理已存在，请勿重复添加!'):
                flag = 1
    except:
        flag = 0
    return flag
