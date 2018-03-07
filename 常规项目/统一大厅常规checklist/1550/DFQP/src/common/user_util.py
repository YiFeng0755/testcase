#coding: utf8

from filelock import FileLock
#from time import sleep
import os
import utils.util as util
from utils.confighelper import ConfigHelper

cfg_path = os.sep.join([util.getrootpath(), 'cfg', 'user_account.ini'])
USER_DATA_PATH = cfg_path

def gimme_afree_account():
    
    free_user = None
    
    # 获取锁
    with FileLock(USER_DATA_PATH) as fl:
    # work with the file as it is now locked
    
        print("Lock acquired.")
    
        #sleep(10)
        import configparser
        config = configparser.ConfigParser()
        
        # 读配制
        config.read(fl.file_name)

        user_data = config['user']['data']
        # config = ConfigHelper(fl.file_name)
        # user_data = config['user']['data']

        import json
        user_account_array = json.loads(user_data)
        for user_info in user_account_array:
            if user_info['status'] == 'unuse':
                free_user = user_info.copy()
                user_info['status'] = 'use'
                break
        if free_user:
            config.set("user", "data", json.dumps(user_account_array))
            config.write(open(fl.file_name, "w"))
    #print free_user
    return free_user


def release_account(mid):
    mid = str(mid)
    # cfg_path = os.sep.join([util.getrootpath(), 'cfg', 'user_account1.ini'])
    # USER_DATA_PATH = cfg_path

    with FileLock(USER_DATA_PATH) as fl:
        print("Lock acquired for release account")
        has_found = False
        import configparser
        config = configparser.ConfigParser()

        # 读配制
        config.read(fl.file_name)

        user_data = config['user']['data']

        import json
        user_account_array = json.loads(user_data)
        for user_info in user_account_array:
            if user_info['mid'] == mid:
                user_info['status'] = 'unuse'
                has_found = True
        if has_found:
            config.set("user", "data", json.dumps(user_account_array))
            config.write(open(fl.file_name, "w"))
    return True