# coding: utf-8

import util
import uuid
import json
import base64
import hashlib
from collections import OrderedDict
import time
import traceback

# 测试环境
TEST_ENV = "http://192.168.200.21/dfqp/?action=autotest.api"
    
# 预发布
PRE_REPUBLISH_ENV = "http://pcususus01.ifere.com/ddfqp/?action=autotest.api"
    
# 正式
FORMAL_ENV = ""

def set_env(env=TEST_ENV):
    util.AUTO_TEST_URL = env

def shutdown_user(mid, type):
    '''
    @brief 封号/解封
    @param mid: 用户mid
    @param type: 1:封号; 0:解封
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": 'fenhao',
        "mids": [mid],
        "type": type
    }
    result = util.post(url, postdata)
    return util.check_response(result)


def set_sign_card(mid, type, count):
    '''
    @brief 增加/删除补签卡
    @param mid: 用户mid
    @param type: 1:添加; -1:删除
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": 'sign',
        "mid": mid,
        "type": type,
        "count": count
    }
    result = util.post(url, postdata)
    return util.check_response(result)


def set_vip(mid, type):
    '''
    @brief 设置vip
    @param mid: 用户mid
    @param type: -1:设置过期; 4:添加体验卡; 5:添加周卡; 6:添加月卡
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": 'vip',
        "mid": mid,
        "type": type
    }
    result = util.post(url, postdata)
    print result.decode('unicode_escape')
    return util.check_response(result)


def add_crystal(mid, crystal):
    '''
    @brief 添加金条
    @param mid: 用户mid
    @param crystal: 金条数量
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": 'crystal',
        "mid": mid,
        "crystal": crystal
    }
    result = util.post(url, postdata)
    return util.check_response(result)


def add_money(mid, money):
    '''
    @brief 添加银币
    @param mid: 用户mid
    @param money: 银币数量
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": 'money',
        "mid": mid,
        "money": money
    }
    result = util.post(url, postdata)
    return util.check_response(result)


def add_diamond(mid, diamond):
    '''
    @brief 添加钻石
    @param mid: 用户mid
    @param diamond: 钻石数量
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": 'diamond',
        "mid": mid,
        "diamond": diamond
    }
    result = util.post(url, postdata)
    return util.check_response(result)


def set_level(mid, level):
    '''
    @brief 设置玩家等级
    @param mid: 用户mid
    @param level: 等级
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": 'level',
        "mid": mid,
        "level": level
    }
    result = util.post(url, postdata)
    return util.check_response(result)


def set_notice(title, content, id=1, region=1, weight=1, start_time=int(time.time()),
               end_time=int(time.time() + 60 * 10), is_html=1, status=1,
               conditions={"min_version": "0", "max_version": "0", "stime": "08:4:38", "etime": "20:4:40", "week":[0,1,2,3,4,5,6]}):
    '''
    @brief 公告设置
    @param title: 标题
    @param content: 内容
    @param id: 应用id
    @param region: 区域id
    @param weight: 排序权重
    @param start_time: 开始时间:从1970开始的秒数(默认从当前时间开始)
    @param end_time: 结束时间:从1970开始的秒数(默认从当前开始时间+10分钟)
    @param is_html: 0:文本公告 ; 1:富文本公告 ; 2:图片公告
    @param status: 状态 0：关闭 1：正常
    @param conditions: 附加条件
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": 'notice',
        "app_id": id,
        "title": title,
        "content": json.dumps(content) if is_html ==2 else content,
        "weight": weight,
        "region": region,
        "start_time": time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start_time)),
        "end_time": time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(end_time)),
        "is_html": is_html,
        "status": status,
        "conditions": json.dumps(conditions)
    }
    result = util.post(url, postdata)
    return util.check_response(result)

     # print set_notice('777777',"公告自动化测试222",id=103000, end_time=int(time.time() + 60 * 4), is_html=0)
    # print set_notice('666666', content={"htmlpic":"https://dfqppic.266.com/dfqp/pic/task/khlvh7rg.png", "cmd": 1003, "gameid": 203, "level": 12, "matchconfigid": 12323232}, id=103000, end_time=int(time.time() + 60 * 4), is_html=2)
    

def send_message(mid, title, bodys, tool_id=None, num=3, havegot=0):
    '''
    @brief 发送私信
    @param mid: 用户mid
    @param title: 标题
    @param bodys: 内容
    @param tool_id: 道具id或者id数组
    @param num: 数量
    @param havegot:
    @return: 1:成功 ; 0:失败
    '''
    url = util.AUTO_TEST_URL
    
    if tool_id:
        if type(tool_id) == type(0):
            tool_id = [tool_id]
        assert type(tool_id) == type([])
    else:
        tool_id = []
    tool_id = tool_id if tool_id else [22]
    
    postdata = {
        "ops": "message",
        "title": title,
        "bodys": bodys,
        "mids": [mid],
        "rewards": json.dumps([{'type': tid, 'num': num, 'havegot': havegot} for tid in tool_id])
    }
    result = util.post(url, postdata)
    return util.check_response(result, only_check_code=True)


def set_splash(region, start_time=int(time.time()), end_time=int(time.time() * 60 * 10),
               background="https://dfqppic.266.com/dfqp/pic/flashscreen/4e05xkrv.jpg",
               splashscreen="https://dfqppic.266.com/dfqp/pic/flashscreen/4e05xkrv.jpg"):
    '''
    @brief 设置闪屏图片
    @param start_time: 开始时间:从1970开始的秒数(默认从当前时间开始)
    @param end_time: 结束时间:从1970开始的秒数(默认从当前开始时间+10分钟)
    @param backgroun: 背景图片url
    @param splashscreen: 闪屏图片url
    @return: 1:成功 ; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": 'bg',
        "region": region,
        "stime": start_time,
        "etime": end_time,
        "background": background,
        "splashScreen": splashscreen
    }
    result = util.post(url, postdata)
    return util.check_response(result)


def add_proxy(mid, pno, name, invitepno, region=1, isstore=1, sjname='test', sjarea=1, partner=1):
    '''
    @brief 添加代理商
    @param mid: 用户mid
    @param pno: 用户手机号
    @param name: 用户姓名
    @param invitepno: 上级代理商id
    @param region: 地区id
    @param isstore: 是否商家摊位  0:否 ; 1:是
    @param sjname: 商家名称
    @param sjarea: 商家区域 1:延吉市; 2:图们市; 3:敦化市; 4:龙井市 ; 5:珲春市; 6:和龙市 ; 7:汪清县; 8:安图县
    @param partner:  是否推广员 0:否; 1:是
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": 'agent',
        "mid": mid,
        "pno": pno,
        "name": name,
        "isstore": isstore,
        "region": region,
        "invitepno": invitepno,  # 2031899,
        "sjname": sjname,
        "sjarea": sjarea,
        "partner": partner
    }
    result = util.post(url, postdata)
    return util.check_response(result)


def reward_recrod(mid):
    '''
    @breif 获取兑奖记录
    @param mid: 用户mid
    @return: 兑奖记录json
    '''
    # 测试可用mid: 2008788
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": 'record',
        "mid": mid  # 2008788
    }
    result = util.post(url, postdata)
    return json.loads(result)

def get_user_info(mid):
    '''
    @brief 获取用户信息
    @param mid: 用户mid
    @return: 用户信息json
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": 'info',
        "mid": mid
    }
    result = util.post(url, postdata)
    return result

def set_user_bankrupt(mid):
    '''
    @breif 设置用户破产
    @param mid: 用户mid
    @return: 1:成功; 0:失败
    '''
    # 没有直接设置破产的接口，只能先获取银币数量，再减去相应的银币
    result = get_user_info(mid)
    try:
        user_info = json.loads(result)
        coin = user_info.get('result', {'coin': None}).get('coin')
        if coin <= 0:
            return 1
        else:
            return add_money(mid, -coin)
    except:
        return 0


def broadcast(mid, content='test', type=1):
    '''
    @breif 广播
    @param mid: 用户mid
    @param content: 发送内容
    @param type: 1:大厅; 2:积分房
    @return: 1:成功; 0:失败
    '''
    # 测试可用mid: 2008788
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": "broadcast",
        "mid": mid,
        "content": content,
        "type": type
    }
    result = util.post(url, postdata)
    return util.check_response(result)


def has_signed(mid, day_of_time=int(time.time())):
    '''
    @brief 查询某天是否签到
    @param day_of_time:  时间:从1970开始的秒数(默认从当前时间开始)
    @return: 1:已签到; 0:未签到
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": "signstat",
        "mid": mid,
        "day": day_of_time
    }
    result = util.post(url, postdata)
    try:
        result = json.loads(result)
        return result.get('result', {'status': '0'}).get('status')
    except:
        raise TypeError('cannot convert to josn')


def set_user_rank(mid, api, type, value):
    '''
    @brief 获取或设置排行榜内     set_user_rank(2193478, 103000, 'exp', 1)
    @param mid: 用户mid
    @param api: 应用id
    @param type: 类型
    @param value: 值
    @return: 1:成功; 0:失败
    '''

    url = "http://192.168.200.21/dfqp/index.php?action=externals.autoTest"
    guid = uuid.uuid1()
    inner = OrderedDict(
        [("tab", OrderedDict([("type", type), ("value", value)]))]
    )
    millions = str(int(time.time()))
    code = OrderedDict(
        [("mid", mid),
         ("api", api),
         ("guid", str(guid)),
         ("cmds", inner)]
    )
    codestr = json.dumps(code, encoding="UTF-8", separators=(',', ':'))
    base64_codesrc = base64.b64encode(codestr)
    src = base64_codesrc + millions + "terfv%^&4826oo"
    md5 = hashlib.md5()
    md5.update(src)
    key = md5.hexdigest()

    postdata = {
        "action": 'externals.autoTest',
        "key": key,
        "time": millions,
        "code": base64_codesrc
    }
    postdata = json.dumps(postdata)
    result = util.post(url, postdata)
    return check_result(result)


## 二期接口
# ok1
def add_mission(name='test', desc='test', region=1, sort_order=1,
                icon='https://dfqppic.266.com/dfqp/pic/task/khlvh7rg.png', reward_type=0, reward=1, 
                circle_type=0, jump_code=1007, gameid=103000,
                level=12, status=0, supported={"5203000": "1", "5201000": "1"},
                maxsupported={"5203000": "1", "5201000": "2"}, 
                conditions={
                    "totalPlayTimes": {
                        "games": "203",
                        "levels": ["12"],
                        "basechiptypes": ["0"],
                        "playmodes": ["0"],
                        "num": "6"
                    }
                }
                ):
    '''
    @brief 添加每日任务
    @param region: 区域id
    @param name: 任务名称
    @param desc: 任务描述
    @param sort_order: 排序
    @param icon: 任务图标
    @param reward_type: 任务奖励
    @param reward: 奖励数量
    @param circle_type: 任务周期类型 (0:每日任务  ; 1:生涯任务)
    @param jump_code: 任务跳转代码 
    @param gameid: 游戏id,("jump_code":为1007 存在)
    @param level: 场次id
    @param supported: 客户端版本限制,大于版本
    @param maxsupported: 客户端版本限制,小于版本
    @param conditions: 奖励条件相应配置
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": "addmission",
        "region": region,
        "name": name,
        "desc": desc,
        "sort_order": sort_order,
        "icon": icon,
        "reward_type": reward_type,
        "reward": reward,
        "circle_type": circle_type,
        "jump_code": jump_code,
        "gameid": gameid,
        "level": level,
        "status": status,
        "supported": json.dumps(supported),
        "maxsupported": json.dumps(maxsupported),
        "conditions": json.dumps(conditions)
    }
    #===========================================================================
    # postdata = {
    #     "ops": "addmission",
    #     "region": "1",
    #     "name": "测试",
    #     "desc": "测试",
    #     "sort_order": "1",
    #     "icon": "https://dfqppic.266.com/dfqp/pic/task/khlvh7rg.png",
    #     "reward_type": "0",
    #     "reward": "1",
    #     "circle_type": "0",
    #     "jump_code": "1007",
    #     "gameid": "103000",
    #     "level": "12",
    #     "status": "0",
    #     "supported": json.dumps({
    #         "5203000": "1",
    #         "5201000": "1"
    #     }),
    #     "maxsupported": json.dumps({
    #         "5203000": "1",
    #         "5201000": "2"
    #     }),
    #     "conditions": json.dumps({
    #         "totalPlayTimes": {
    #             "games": "203",
    #             "levels": [
    #                 "12"
    #             ],
    #             "basechiptypes": [
    #                 "0"
    #             ],
    #             "playmodes": [
    #                 "0"
    #             ],
    #             "num": "6"
    #         }
    #     })
    # }
    #===========================================================================
    url = util.AUTO_TEST_URL
    result = util.post(url, postdata)
    return util.check_response(result)


# ok2
def reset_img(mid):
    '''
    @brief 重置头像
    @param mid: mid
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata= {
        "ops": "reseticon",
        "mid": mid
    }
    result = util.post(url, postdata)
    return util.check_response(result)

# ok3
def get_mid(cid, region=1):
    '''
    @brief 通过cid获取mid
    @param cid: cid
    @param region: 地区
    @return: 用户mid
    '''
    # cid: 2183786
    # region: 1
    url = util.AUTO_TEST_URL
    postdata= {
        "ops": "getmidbycid",
        "cid": cid,
        "region": region
    }
    result = util.post(url, postdata)
    try:
        result_json = json.loads(result)
        return result_json['result']
    except:
        return None


# ok4
def set_mission_to_complete(mid, appid, missionid, type=1):
    '''
    @brief 设置任务为完成
    @param mid: mid
    @param appid: appid
    @param missionid: 任务id
    @param type: 1为设置任务完成，-1为设置任务取消
    @return: 1:成功; 0:失败
    '''
    # mid:2193478 appid:103000  missionid:530 type: 1
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": "mission",
        "mid": mid,
        "appid": appid,
        "type": type,
        "missionid": missionid
    }
    result = util.post(url, postdata)
    return util.check_response(result)

# ok 参数的意义5
def get_levelconfig(gameid, basechiptype=0, playmode=1, roomlevel=1):
    '''
    @brief 获取场次配置信息
    @param gameid: 游戏id
    @param basechiptype: 底注类型
    @param playmode: 玩法类型
    @param roomlevel: 房间ID
    @return: dict类型
    '''
    # game: 208
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": "getlevelconfig",
        "game": gameid,
        "basechiptype": basechiptype,
        "playmode": playmode,
        "roomlevel": roomlevel
    }
    try:
        result = util.post(url, postdata)
        return json.loads(result)['result']['result']
    except:
        return None

# ok6
def get_safebox(mid):
    '''
    @brief 获取保险箱信息
    @param mid: mid
    @return: dict类型
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": "safebox",
        "mid":mid
    }
    try:
        result = util.post(url, postdata)
        return json.loads(result)['result']
    except:
        return None


def check_result(response):
    result = 0
    try:
        json_result = json.loads(response, encoding="UTF-8")
        if json_result.get('code', '0') and json_result.get('ret', None) and json_result['ret'].get('status', '0'):
            result = 1
    except:
        result = 0
    return result



def set_cheat(gameid, basechiptype, playmode, roomlevel, switch, duration=[[{"s":"06:24","e":"18:24"},{"s":"19:24","e":"23:24"}]]):
    '''
    @brief 设置防作弊配置
    @param gameid: 游戏id
    @param basechiptype: 底注
    @param playmode: 玩法
    @param roomlevel: 场次
    @param switch: 1:24小时开启     2:分段开启      0:关闭
    @param duration: 开户时间段（switch为2时有效)
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": "cheatingset",
        "completeEquip": json.dumps([
            {
                "value": 
                    {
                        "zlyc": 
                            {
                                "switch":switch,
                                "date": duration
                            },
                        "zdhz":""
                    },
                "gameid": gameid,
                "basechiptype": basechiptype,
                "playmode": playmode,
                "roomlevel": roomlevel
            }
        ])
    }
    result = util.post(url, postdata)
    try:
        json_result = json.loads(result)
        return 1 if json_result['code'] == 200 and json_result['result'] == [1] else 0
    except Exception, e:
        traceback.print_exc()
        return 0


def set_robot_flag(gameid, basechiptype=0, playmode=1, roomlevel=1, robotflag=0):
    '''
    @brief 设置场次配置机器人状态
    @param gameid: 游戏id
    @param basechiptype: 底注
    @param playmode: 玩法
    @param roomlevel: 场次
    @param robotflag: 机器人状态 0 关闭 1 开启 2 开启等待时间  
    @return: 1:成功; 0:失败
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": "setrobotflag",
        "game": gameid,
        "basechiptype": basechiptype,
        "playmode": playmode,
        "roomlevel": roomlevel,
        "robotflag": robotflag
    }
    result = util.post(url, postdata)
    return util.check_response(result)


def get_app_games(appid, hall=None, display=None):
    '''
    @brief 获取应用游戏列表
    @param appid: 应用id
    @param hall: 底注
    @param display: 玩法
    @return: dic类型
    '''
    url = util.AUTO_TEST_URL
    postdata = {
        "ops": "getappgames",
        "appid": appid,
        "hall": hall,
        "display": display
    }
    if hall == None:
        postdata.pop("hall")
    if display == None:
        postdata.pop("display")
    try:
        result = util.post(url, postdata)
        return json.loads(result)['result']
    except:
        return None
