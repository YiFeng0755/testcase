# coding: utf-8

import urllib2
import urllib
import json

# 当前测试环境，默认是预发布
AUTO_TEST_URL = "http://pcususus01.ifere.com/ddfqp/?action=autotest.api"

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
