#coding: utf8

from filelock import FileLock
from collections import OrderedDict
import json,os
import utils.constant as constant
from utils import util

cfg_path = constant.user_cfg
USER_DATA_PATH = cfg_path
print USER_DATA_PATH

def gimme_afree_account():
    
    free_user = None
    
    # 获取锁
    with FileLock(USER_DATA_PATH) as fl:
    # work with the file as it is now locked
    
        print("Lock acquired.")
        fipath = unicode(fl.file_name)
        # fd = open(fl.file_name)
        fd = open(fipath)
        user_data = fd.read()
        fd.close()

        
        user_account_array = json.loads(user_data, object_pairs_hook=OrderedDict)
        users = user_account_array['data']
        for u in users:
            if u['status'] == 'unuse':
                free_user = u.copy()
                u['status'] = 'use'
                break
        if free_user:
            with open(USER_DATA_PATH, 'w') as f:
                f.write(json.dumps(user_account_array, indent=2))
        
        #=======================================================================
        # for user_info in user_account_array:
        #     if user_info['status'] == 'unuse':
        #         free_user = user_info.copy()
        #         user_info['status'] = 'use'
        #         break
        # if free_user:
        #     config.set("user", "data", json.dumps(user_account_array))
        #     config.write(open(fl.file_name, "w"))
        #=======================================================================
    return free_user

#print gimme_afree_account()

def release_account(mid):
    mid = str(mid)
    result = False
    
    with FileLock(USER_DATA_PATH) as fl:
        print("Lock acquired for release account")
        has_found = False
        
        fd = open(fl.file_name)
        user_data = fd.read()
        fd.close()

        user_account_array = json.loads(user_data, object_pairs_hook=OrderedDict)
        users = user_account_array['data']
        
        for user_info in users:
            if user_info['mid'] == mid:
                user_info['status'] = 'unuse'
                has_found = True
        if has_found:
            result = True
            with open(USER_DATA_PATH, 'w') as f:
                f.write(json.dumps(user_account_array, indent=2))
    return result
#
